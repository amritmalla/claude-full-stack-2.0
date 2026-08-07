"""MCP stdio server exposing claude-full-stack-2.0 skills and workflows as tools.

Each SKILL.md / WORKFLOW.md becomes one MCP tool whose description is the
frontmatter `description` (already written as "Use when …"). Claude's tool
routing picks the right one based on the user's request.

Bonus tools:
- `list_skills` — discoverable browse (filter by kind / domain / ecosystem).
- `get_skill_reference` — fetch a named reference file from a skill's
  `references/` directory without bloating the primary tool result.
"""
from __future__ import annotations

import asyncio
import json
from typing import Any

from mcp.server import Server
from mcp.types import Tool, TextContent

from .loader import SkillEntry, load_entries, reference_files


SERVER_INSTRUCTIONS = """\
claude-full-stack-skills exposes 88 reusable engineering skills + workflows
from the claude-full-stack-2.0 project as MCP tools.

Each tool is a self-contained recipe — architecture domains (system-design,
backend-architecture, ai-native-engineering, …), ecosystem implementations
(spring-boot, fastapi, postgres, kubernetes, react, flutter, anthropic, …),
and lifecycle workflows (idea-to-production-full-stack, production-readiness-
review, …).

Tools follow the Anthropic Skills format: a frontmatter `description` that
starts with "Use when …" tells you when to invoke. Call the tool to receive
the full SKILL.md or WORKFLOW.md body — a step-by-step recipe with inputs,
outputs, quality checks, and references.

For deep-dive references, call `get_skill_reference(skill, reference)`.
To browse the catalog, call `list_skills`.
"""


def _entry_to_tool(e: SkillEntry) -> Tool:
    return Tool(
        name=e.name,
        description=e.description,
        inputSchema={
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    )


def _list_skills_tool() -> Tool:
    return Tool(
        name="list_skills",
        description=(
            "List available skills and workflows. Use to browse the catalog "
            "when no single skill description matches the user's request. "
            "Returns names + descriptions grouped by kind."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "kind": {
                    "type": "string",
                    "enum": ["skill", "workflow"],
                    "description": "Filter to only skills or only workflows.",
                },
                "contains": {
                    "type": "string",
                    "description": "Case-insensitive substring match against names + descriptions.",
                },
            },
            "additionalProperties": False,
        },
    )


def _get_reference_tool() -> Tool:
    return Tool(
        name="get_skill_reference",
        description=(
            "Fetch a named reference markdown file from a skill's references/ "
            "directory. Use when a skill body links to references/<name>.md and "
            "you need its full content."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "skill": {
                    "type": "string",
                    "description": "The skill or workflow name (kebab-case).",
                },
                "reference": {
                    "type": "string",
                    "description": "Reference filename, with or without .md suffix (e.g. 'setup' or 'setup.md').",
                },
            },
            "required": ["skill", "reference"],
            "additionalProperties": False,
        },
    )


def build_server() -> Server:
    """Construct the MCP server with all skill/workflow tools wired up."""
    entries = load_entries()
    by_name: dict[str, SkillEntry] = {e.name: e for e in entries}

    try:
        server = Server(name="claude-full-stack-skills", instructions=SERVER_INSTRUCTIONS)
    except TypeError:
        server = Server(name="claude-full-stack-skills")
        try:
            server.instructions = SERVER_INSTRUCTIONS
        except AttributeError:
            pass

    @server.list_tools()
    async def _list() -> list[Tool]:
        tools = [_entry_to_tool(e) for e in entries]
        tools.append(_list_skills_tool())
        tools.append(_get_reference_tool())
        return tools

    @server.call_tool()
    async def _call(name: str, arguments: dict[str, Any]) -> list[TextContent]:
        # Per-skill tool: return the body verbatim.
        if name in by_name:
            return [TextContent(type="text", text=by_name[name].body)]

        if name == "list_skills":
            return _do_list_skills(entries, arguments)

        if name == "get_skill_reference":
            return _do_get_reference(by_name, arguments)

        return [TextContent(
            type="text",
            text=json.dumps({"error": f"unknown tool: {name}"}),
        )]

    return server


def _do_list_skills(entries: list[SkillEntry], args: dict[str, Any]) -> list[TextContent]:
    kind = (args.get("kind") or "").strip().lower()
    contains = (args.get("contains") or "").strip().lower()
    out: dict[str, list[dict]] = {"skill": [], "workflow": []}
    for e in entries:
        if kind and e.kind != kind:
            continue
        if contains and contains not in e.name.lower() and contains not in e.description.lower():
            continue
        out[e.kind].append({"name": e.name, "description": e.description})
    payload = {
        "total": sum(len(v) for v in out.values()),
        "skills": out["skill"],
        "workflows": out["workflow"],
    }
    return [TextContent(type="text", text=json.dumps(payload, indent=2))]


def _do_get_reference(
    by_name: dict[str, SkillEntry],
    args: dict[str, Any],
) -> list[TextContent]:
    skill_name = args.get("skill", "").strip()
    ref = args.get("reference", "").strip()
    if not skill_name or not ref:
        return [TextContent(
            type="text",
            text=json.dumps({"error": "both 'skill' and 'reference' are required"}),
        )]
    entry = by_name.get(skill_name)
    if entry is None:
        return [TextContent(
            type="text",
            text=json.dumps({"error": f"unknown skill: {skill_name}"}),
        )]
    if not ref.endswith(".md"):
        ref = ref + ".md"
    for ref_path in reference_files(entry):
        if ref_path.name == ref:
            return [TextContent(type="text", text=ref_path.read_text(encoding="utf-8"))]
    available = [p.name for p in reference_files(entry)]
    return [TextContent(
        type="text",
        text=json.dumps({
            "error": f"reference {ref!r} not found in skill {skill_name!r}",
            "available": available,
        }),
    )]


async def serve_stdio() -> None:
    from mcp.server.stdio import stdio_server
    server = build_server()
    async with stdio_server() as (reader, writer):
        await server.run(reader, writer, server.create_initialization_options())


def run() -> None:
    """Console-script entry point: launches the stdio server."""
    asyncio.run(serve_stdio())
