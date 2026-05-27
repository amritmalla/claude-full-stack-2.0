"""Walk the bundled (or external) skills/ and workflows/ trees and produce
SkillEntry records the server can expose as MCP tools.

Frontmatter format (per SKILL_SPEC.md / WORKFLOW_SPEC.md):

    ---
    name: kebab-case-id
    description: Use when ...
    ---

    <markdown body>

Each skill or workflow becomes one MCP tool whose:

- tool name      = the SKILL/WORKFLOW directory name (kebab-case)
- description    = the frontmatter `description` field
- input schema   = empty object (no inputs needed)
- tool result    = the full SKILL.md / WORKFLOW.md body
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

import yaml


_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)


@dataclass(frozen=True)
class SkillEntry:
    """One entry the MCP server can expose as a tool."""

    name: str           # kebab-case, unique across skills + workflows
    kind: str           # "skill" or "workflow"
    description: str    # frontmatter `description` — drives Claude's tool routing
    path: Path          # absolute path to the SKILL.md or WORKFLOW.md file
    body: str           # full file body (frontmatter included)


def resolve_root() -> Path:
    """Find the directory holding `skills/` and `workflows/`.

    Resolution order:
      1. `CLAUDE_FULL_STACK_SKILLS_ROOT` env var (if set + exists).
      2. The bundled copy under the installed package (`_bundled/`).
      3. The repo root reached by walking up from this file (dev mode).

    Raises FileNotFoundError if no plausible root is found.
    """
    env = os.environ.get("CLAUDE_FULL_STACK_SKILLS_ROOT")
    if env:
        p = Path(env).expanduser().resolve()
        if (p / "skills").is_dir():
            return p
        raise FileNotFoundError(
            f"CLAUDE_FULL_STACK_SKILLS_ROOT={env!r} does not contain a skills/ directory"
        )

    # Bundled copy shipped with the wheel.
    bundled = Path(__file__).parent / "_bundled"
    if (bundled / "skills").is_dir():
        return bundled

    # Dev mode: walk up looking for a skills/ sibling of pyproject.toml.
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "skills").is_dir() and (parent / "pyproject.toml").is_file():
            return parent

    raise FileNotFoundError(
        "Could not locate skills/ directory. Set CLAUDE_FULL_STACK_SKILLS_ROOT "
        "to the path of the claude-full-stack-2.0 repo (or reinstall the "
        "package so the bundled skills are present)."
    )


_KV_LINE_RE = re.compile(r"^(\w[\w-]*)\s*:\s*(.*)$")


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Return (frontmatter_dict, body). Body excludes the frontmatter block.

    Uses YAML first; falls back to a line-by-line `key: value` parser when YAML
    chokes (skill descriptions frequently contain unquoted colons, which YAML
    rejects as nested mappings).
    """
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    body = text[m.end():]
    raw = m.group(1)
    try:
        front = yaml.safe_load(raw) or {}
        if isinstance(front, dict):
            return front, body
    except yaml.YAMLError:
        pass
    # Fallback: parse top-level `key: rest-of-line` pairs, no nesting.
    front: dict = {}
    current_key: str | None = None
    for line in raw.splitlines():
        if not line.strip():
            continue
        kv = _KV_LINE_RE.match(line)
        if kv:
            current_key = kv.group(1)
            front[current_key] = kv.group(2).strip()
        elif current_key is not None and (line.startswith(" ") or line.startswith("\t")):
            # Continuation of the previous value (folded line).
            front[current_key] = (front[current_key] + " " + line.strip()).strip()
    return front, body


def load_entries(root: Optional[Path] = None) -> list[SkillEntry]:
    """Walk `root/skills/**/SKILL.md` and `root/workflows/**/WORKFLOW.md`.

    Skips any file whose frontmatter is missing `name` or `description`.
    """
    root = root or resolve_root()
    entries: list[SkillEntry] = []
    seen_names: set[str] = set()

    for kind, dir_name, filename in (
        ("skill", "skills", "SKILL.md"),
        ("workflow", "workflows", "WORKFLOW.md"),
    ):
        base = root / dir_name
        if not base.is_dir():
            continue
        for md in base.rglob(filename):
            text = md.read_text(encoding="utf-8")
            front, _ = parse_frontmatter(text)
            name = (front.get("name") or "").strip()
            desc = (front.get("description") or "").strip()
            if not name or not desc:
                continue
            if name in seen_names:
                # Disambiguate by prefixing with kind.
                name = f"{kind}-{name}"
                if name in seen_names:
                    continue
            seen_names.add(name)
            entries.append(SkillEntry(
                name=name,
                kind=kind,
                description=desc,
                path=md,
                body=text,
            ))

    # Stable order for predictable tool listings.
    entries.sort(key=lambda e: (e.kind, e.name))
    return entries


def reference_files(entry: SkillEntry) -> list[Path]:
    """Return any `references/*.md` files that live next to the SKILL.md.

    These can be exposed as a secondary tool that fetches a named reference
    on demand without bloating the primary tool result.
    """
    refs_dir = entry.path.parent / "references"
    if not refs_dir.is_dir():
        return []
    return sorted(p for p in refs_dir.glob("*.md") if p.is_file())
