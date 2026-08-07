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

from mcp.server import MCPServer
from mcp.types import TextContent

from . import __version__
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


LIST_SKILLS_DESCRIPTION = (
    "List available skills and workflows. Use to browse the catalog "
    "when no single skill description matches the user's request. "
    "Returns names + descriptions grouped by kind."
)

GET_REFERENCE_DESCRIPTION = (
    "Fetch a named reference markdown file from a skill's references/ "
    "directory. Use when a skill body links to references/<name>.md and "
    "you need its full content."
)


def _make_body_tool(entry: SkillEntry):
    """Build a zero-argument tool returning one skill/workflow body verbatim.

    A factory (rather than a closure written inline in the registration loop)
    binds `entry` per iteration and keeps the generated function free of
    parameters — `add_tool` derives each tool's schema from the signature and
    rejects parameter names starting with an underscore.
    """

    async def _tool() -> str:
        return entry.body

    return _tool


def build_server() -> MCPServer:
    """Construct the MCP server with all skill/workflow tools wired up."""
    entries = load_entries()
    by_name: dict[str, SkillEntry] = {e.name: e for e in entries}

    server = MCPServer(
        name="claude-full-stack-skills",
        version=__version__,
        instructions=SERVER_INSTRUCTIONS,
    )

    # One tool per SKILL.md / WORKFLOW.md, registered dynamically.
    # structured_output=False keeps the body in `content` only; leaving it on
    # would repeat every document verbatim in `structured_content`.
    for entry in entries:
        server.add_tool(
            _make_body_tool(entry),
            name=entry.name,
            description=entry.description,
            structured_output=False,
        )

    async def list_skills(kind: str | None = None, contains: str | None = None) -> str:
        return _do_list_skills(entries, {"kind": kind, "contains": contains})[0].text

    async def get_skill_reference(skill: str, reference: str) -> str:
        return _do_get_reference(by_name, {"skill": skill, "reference": reference})[0].text

    server.add_tool(
        list_skills,
        name="list_skills",
        description=LIST_SKILLS_DESCRIPTION,
        structured_output=False,
    )
    server.add_tool(
        get_skill_reference,
        name="get_skill_reference",
        description=GET_REFERENCE_DESCRIPTION,
        structured_output=False,
    )

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
    await build_server().run_stdio_async()


def run() -> None:
    """Console-script entry point: launches the stdio server."""
    asyncio.run(serve_stdio())
