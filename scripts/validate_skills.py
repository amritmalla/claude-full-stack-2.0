#!/usr/bin/env python3
"""Validate repository skill structure and plugin metadata."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOTS = ("skills/architecture", "skills/implementations")
WORKFLOW_ROOT = "workflows"
SKILLS_REF_RE = re.compile(r"\(\s*skills:\s*([^)]*)\)")
BACKTICK_RE = re.compile(r"`([^`]+)`")
REQUIRED_SECTIONS = (
    "When to use",
    "Inputs",
    "Process",
    "Outputs",
    "Quality checks",
    "References",
)
OPTIONAL_RESOURCE_DIRS = ("references", "assets", "checklists")
FRONTMATTER_RE = re.compile(r"\A---\r?\n(?P<body>.*?)\r?\n---\r?\n", re.DOTALL)
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LOCAL_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
PLUGIN_REQUIRED = {
    "name",
    "version",
    "description",
    "author",
    "homepage",
    "repository",
    "license",
    "skills",
}


@dataclass(frozen=True)
class Finding:
    path: str
    message: str


def rel(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def parse_frontmatter(text: str) -> tuple[dict[str, str], str] | tuple[None, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None, text
    data: dict[str, str] = {}
    for raw_line in match.group("body").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data, text[match.end() :]


def find_skill_files() -> list[Path]:
    files: list[Path] = []
    for root_name in SKILL_ROOTS:
        root = REPO_ROOT / root_name
        if root.exists():
            files.extend(sorted(root.rglob("SKILL.md")))
    return files


def validate_local_links(skill_file: Path, body: str) -> list[Finding]:
    findings: list[Finding] = []
    for target in LOCAL_LINK_RE.findall(body):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        path_part = target.split("#", 1)[0].strip()
        if not path_part:
            continue
        if path_part.startswith("<") and path_part.endswith(">"):
            path_part = path_part[1:-1]
        resolved = (skill_file.parent / path_part).resolve()
        if not resolved.exists():
            findings.append(Finding(rel(skill_file), f"broken local link: {target}"))
    return findings


def validate_skill(skill_file: Path) -> list[Finding]:
    findings: list[Finding] = []
    text = skill_file.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(text)

    if frontmatter is None:
        return [Finding(rel(skill_file), "missing YAML frontmatter")]

    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    expected_name = skill_file.parent.name

    if set(frontmatter) != {"name", "description"}:
        findings.append(
            Finding(
                rel(skill_file),
                "frontmatter must contain exactly name and description",
            )
        )
    if name != expected_name:
        findings.append(Finding(rel(skill_file), f"name '{name}' != directory '{expected_name}'"))
    if not NAME_RE.match(name):
        findings.append(Finding(rel(skill_file), f"name is not kebab-case: {name!r}"))
    if not description:
        findings.append(Finding(rel(skill_file), "missing description"))
    elif not description.startswith("Use when"):
        findings.append(Finding(rel(skill_file), "description must start with 'Use when'"))
    if len(description) > 1024:
        findings.append(Finding(rel(skill_file), f"description > 1024 chars ({len(description)})"))
    if len(text.splitlines()) > 400:
        findings.append(Finding(rel(skill_file), "SKILL.md exceeds 400 lines"))
    if not re.search(r"^# .+", body, re.MULTILINE):
        findings.append(Finding(rel(skill_file), "missing H1 heading"))

    for section in REQUIRED_SECTIONS:
        pattern = rf"^## {re.escape(section)}\s*$"
        if not re.search(pattern, body, re.MULTILINE | re.IGNORECASE):
            findings.append(Finding(rel(skill_file), f"missing required section: {section}"))

    for dirname in OPTIONAL_RESOURCE_DIRS:
        resource_dir = skill_file.parent / dirname
        if resource_dir.exists() and not any(resource_dir.iterdir()):
            findings.append(Finding(rel(resource_dir), "directory exists but is empty"))

    findings.extend(validate_local_links(skill_file, body))
    return findings


def collect_skill_names() -> set[str]:
    return {skill_file.parent.name for skill_file in find_skill_files()}


def find_workflow_files() -> list[Path]:
    root = REPO_ROOT / WORKFLOW_ROOT
    return sorted(root.rglob("WORKFLOW.md")) if root.exists() else []


def validate_workflow(workflow_file: Path, valid_skills: set[str]) -> list[Finding]:
    findings: list[Finding] = []
    text = workflow_file.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(text)

    if frontmatter is None:
        return [Finding(rel(workflow_file), "missing YAML frontmatter")]

    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    expected_name = workflow_file.parent.name
    if name != expected_name:
        findings.append(
            Finding(rel(workflow_file), f"name '{name}' != directory '{expected_name}'")
        )
    if not description.startswith("Use when"):
        findings.append(
            Finding(rel(workflow_file), "description must start with 'Use when'")
        )

    referenced = False
    for group in SKILLS_REF_RE.findall(body):
        for skill_name in BACKTICK_RE.findall(group):
            referenced = True
            if skill_name not in valid_skills:
                findings.append(
                    Finding(
                        rel(workflow_file),
                        f"references unknown skill: {skill_name!r}",
                    )
                )
    if not referenced:
        findings.append(
            Finding(rel(workflow_file), "no skill references found in any phase")
        )

    findings.extend(validate_local_links(workflow_file, body))
    return findings


def validate_plugin(path: Path) -> list[Finding]:
    if not path.exists():
        return [Finding(rel(path), "missing plugin metadata")]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [Finding(rel(path), f"invalid JSON: {exc}")]

    findings: list[Finding] = []
    missing = PLUGIN_REQUIRED - set(data)
    if missing:
        findings.append(Finding(rel(path), f"missing fields: {sorted(missing)}"))
    author = data.get("author")
    if not isinstance(author, dict) or not author.get("name"):
        findings.append(Finding(rel(path), "author must be an object with name"))
    skills = data.get("skills")
    if not isinstance(skills, list) or not skills:
        findings.append(Finding(rel(path), "skills must be a non-empty array of explicit paths"))
    elif "./" in skills:
        findings.append(Finding(rel(path), "skills must not point at repository root"))
    else:
        for skill_root in skills:
            if not isinstance(skill_root, str):
                findings.append(Finding(rel(path), f"skills entry must be a string: {skill_root!r}"))
                continue
            if not (path.parent.parent / skill_root).resolve().exists():
                findings.append(Finding(rel(path), f"skills path does not exist: {skill_root}"))
    return findings


def validate_repository() -> list[Finding]:
    findings: list[Finding] = []
    skills = find_skill_files()
    if not skills:
        findings.append(Finding(".", "no SKILL.md files found under architecture/ or implementations/"))
    for skill_file in skills:
        findings.extend(validate_skill(skill_file))
    valid_skills = collect_skill_names()
    for workflow_file in find_workflow_files():
        findings.extend(validate_workflow(workflow_file, valid_skills))
    findings.extend(validate_plugin(REPO_ROOT / ".claude-plugin" / "plugin.json"))
    findings.extend(validate_plugin(REPO_ROOT / ".codex-plugin" / "plugin.json"))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Output findings as JSON")
    args = parser.parse_args()

    findings = validate_repository()
    if args.json:
        print(json.dumps([finding.__dict__ for finding in findings], indent=2))
    elif findings:
        for finding in findings:
            print(f"FAIL {finding.path}: {finding.message}")
    else:
        print("All skills and plugin metadata valid.")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())

