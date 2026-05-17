from pathlib import Path

from scripts import validate_skills


REPO_ROOT = Path(__file__).resolve().parents[1]


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

