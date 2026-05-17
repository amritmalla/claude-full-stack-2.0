# Repository Conventions

Mandatory conventions for `claude-full-stack-2.0`. These rules apply to human and AI contributors.

## Skill Layout

Technology-agnostic skills live at:

```text
architecture/<domain>/SKILL.md
```

Technology-specific execution skills live at:

```text
implementations/<category>/<ecosystem>/<skill-name>/SKILL.md
```

Each skill directory may include:

```text
SKILL.md       # required
references/   # optional deep dives loaded on demand
assets/       # optional templates or starter files
checklists/   # optional quality gates
```

`architecture-patterns/`, `standards/`, `workflows/`, and `templates/` support the skill system but do not define invocable skills unless they contain their own explicit spec. Each `architecture-patterns/<name>/README.md` conforms to [`standards/architecture-pattern-schema`](standards/architecture-pattern-schema/README.md).

## SKILL.md Rules

- Frontmatter has exactly the fields needed by Claude Code: `name` and `description`.
- `name` matches the skill directory exactly.
- `description` starts with `Use when`, stays under 1024 characters, and names real trigger conditions.
- The skill body includes `When to use`, `Inputs`, `Process`, `Outputs`, `Quality checks`, and `References`.
- `SKILL.md` stays under 400 lines. Move details into `references/`.
- Instructions are imperative and executable. Avoid essay-style background unless it changes an action.
- Quality checks are binary-verifiable.
- Output contracts link to the relevant `standards/` documents.

## References And Assets

- Files in `references/`, `assets/`, and `checklists/` must be intentionally referenced by `SKILL.md` or the parent README when practical.
- Markdown links to local files must stay valid.
- Templates must be usable as starting points, not placeholders full of TODOs.

## Examples

Every new skill should be exercised against the reference project under:

```text
examples/spring-boot/orders-api/.skill-outputs/<skill-name>/
```

The output should prove the skill can run end-to-end without inventing missing upstream decisions.

## Scripts

- Prefer standard-library Python for repository validation and deterministic helper tools.
- Scripts must support `--help`.
- Machine-readable scripts should support `--json` when useful.
- Do not hardcode secrets or call LLM APIs from repository validation scripts.
- Keep shell wrappers thin; core validation should be cross-platform.

## Plugin Metadata

- Keep `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` aligned on name, version, description, repository, license, and skill paths.
- `author` is an object.
- `skills` points at explicit skill roots, not the repository root.

## Git And PRs

- Use Conventional Commit style where practical: `feat:`, `fix:`, `docs:`, `test:`, `chore:`.
- One concern per PR.
- Skill PRs include three should-match and two should-not-match trigger prompts.
- CI must pass `python scripts/validate_skills.py`, `python -m pytest`, and markdown lint.

