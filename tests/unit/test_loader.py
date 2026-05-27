from pathlib import Path
import pytest

from claude_full_stack_skills.loader import (
    SkillEntry,
    load_entries,
    parse_frontmatter,
    reference_files,
    resolve_root,
)


def test_parse_frontmatter_extracts_name_and_description():
    text = (
        "---\n"
        "name: backend-architecture\n"
        "description: Use when you need backend boundaries.\n"
        "---\n\n"
        "# Backend Architecture\n\n"
        "Body content.\n"
    )
    front, body = parse_frontmatter(text)
    assert front["name"] == "backend-architecture"
    assert front["description"].startswith("Use when")
    assert "# Backend Architecture" in body
    assert "---" not in body.split("\n")[0]


def test_parse_frontmatter_handles_missing_frontmatter():
    text = "# No frontmatter here\n\nBody only.\n"
    front, body = parse_frontmatter(text)
    assert front == {}
    assert body == text


def test_resolve_root_finds_repo_in_dev_mode():
    root = resolve_root()
    assert (root / "skills").is_dir()
    assert (root / "workflows").is_dir()


def test_load_entries_finds_real_skills():
    entries = load_entries()
    # Repo ships 83 SKILL.md + 4 WORKFLOW.md.
    names = {e.name for e in entries}
    kinds = {e.kind for e in entries}
    assert kinds == {"skill", "workflow"}
    # Spot-check a few known entries.
    assert "system-design" in names
    assert "backend-architecture" in names
    assert "memory-management" in names
    # Workflow entries.
    assert any(e.kind == "workflow" for e in entries)


def test_load_entries_descriptions_start_with_use_when():
    """SKILL_SPEC mandates frontmatter `description` starts with 'Use when'."""
    entries = load_entries()
    bad = [e for e in entries if not e.description.lower().startswith("use when")]
    assert not bad, f"{len(bad)} entries have non-conforming descriptions: {[e.name for e in bad[:5]]}"


def test_load_entries_skill_count():
    entries = load_entries()
    skills = [e for e in entries if e.kind == "skill"]
    workflows = [e for e in entries if e.kind == "workflow"]
    assert len(skills) >= 80, f"expected ~83 skills, got {len(skills)}"
    assert len(workflows) >= 3, f"expected ~4 workflows, got {len(workflows)}"


def test_load_entries_unique_names():
    entries = load_entries()
    names = [e.name for e in entries]
    assert len(names) == len(set(names)), "duplicate tool names would clash in MCP"


def test_reference_files_for_known_skill(tmp_path: Path):
    """memory-management ships with two reference files."""
    entries = {e.name: e for e in load_entries()}
    if "memory-management" not in entries:
        pytest.skip("memory-management skill not present in this checkout")
    refs = reference_files(entries["memory-management"])
    names = {p.name for p in refs}
    assert "setup.md" in names
    assert "usage-by-phase.md" in names


def test_env_var_override(tmp_path: Path, monkeypatch):
    """CLAUDE_FULL_STACK_SKILLS_ROOT redirects discovery to a custom tree."""
    (tmp_path / "skills" / "x").mkdir(parents=True)
    (tmp_path / "skills" / "x" / "SKILL.md").write_text(
        "---\nname: x\ndescription: Use when X.\n---\n\nbody\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("CLAUDE_FULL_STACK_SKILLS_ROOT", str(tmp_path))
    root = resolve_root()
    assert root == tmp_path.resolve()
    entries = load_entries()
    assert {e.name for e in entries} == {"x"}
