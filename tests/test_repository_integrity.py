import json
from pathlib import Path

from scripts import validate_skills


REPO_ROOT = Path(__file__).resolve().parents[1]
CLAUDE_PLUGIN = REPO_ROOT / ".claude-plugin" / "plugin.json"


def test_repository_validation_passes():
    findings = validate_skills.validate_repository()
    assert findings == []


def test_expected_skill_count_floor():
    skills = validate_skills.find_skill_files()
    assert len(skills) >= 60


def test_no_duplicate_skill_names():
    names: dict[str, list[str]] = {}
    for skill_file in validate_skills.find_skill_files():
        names.setdefault(skill_file.parent.name, []).append(
            skill_file.parent.relative_to(REPO_ROOT).as_posix()
        )

    duplicates = {name: paths for name, paths in names.items() if len(paths) > 1}
    assert duplicates == {}


def test_every_skill_on_disk_is_listed_in_claude_plugin_manifest():
    findings = validate_skills.validate_plugin_coverage(
        CLAUDE_PLUGIN, validate_skills.find_skill_files()
    )
    assert findings == []


def test_plugin_coverage_detects_a_missing_skill(tmp_path):
    """The coverage check must fail when a skill on disk is absent from the manifest.

    Guards against the check silently degrading into a no-op, which is how
    rust-service-scaffold shipped unlisted in the first place.
    """
    data = json.loads(CLAUDE_PLUGIN.read_text(encoding="utf-8"))
    dropped = data["skills"].pop()

    manifest = tmp_path / ".claude-plugin" / "plugin.json"
    manifest.parent.mkdir(parents=True)
    manifest.write_text(json.dumps(data, indent=2), encoding="utf-8")

    findings = validate_skills.validate_plugin_coverage(
        manifest, validate_skills.find_skill_files()
    )
    assert [f for f in findings if dropped.removeprefix("./") in f.message]


def test_plugin_coverage_skips_manifests_listing_directory_roots():
    """The codex manifest lists roots, which cover their subtrees. It must not drift-fail."""
    findings = validate_skills.validate_plugin_coverage(
        REPO_ROOT / ".codex-plugin" / "plugin.json", validate_skills.find_skill_files()
    )
    assert findings == []

