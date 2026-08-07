# Skill Authoring Guide

A practical walkthrough for authoring a new skill. For the formal contract, see [`SKILL_SPEC.md`](../SKILL_SPEC.md).

## 1. Pick an architecture domain or implementation, and a name

Decide first whether the skill is **technology-agnostic** (the parent skill at `skills/architecture/<domain>/SKILL.md`) or **ecosystem-specific** (lives under `skills/implementations/<category>/<ecosystem>/<name>/`). See [`../docs/architecture/research.md`](../docs/architecture/research.md) for the distinction.

Existing architecture domains: `saas-idea-validation`, `idea-development`, `system-design`, `backend-architecture`, `frontend-architecture`, `data-architecture`, `infrastructure-platform`, `reliability`, `security`, `quality-engineering`, `performance`, `operations`, `ai-native-engineering`.

Existing implementation categories: `backend/`, `frontend/`, `infrastructure/`, `data/`, `ai/` — each with one or more ecosystems (e.g., `backend/spring-boot/`).

Name is kebab-case and descriptive of the job. For architecture domains, the skill name matches the domain folder, such as `quality-engineering` or `operations`. For implementation skills, prefer job names over tool names: `safe-migration-plan` is better than `flyway-migration-generator`.

## 2. Create the directory and SKILL.md

```
skills/architecture/<domain>/SKILL.md
# OR
skills/implementations/<category>/<ecosystem>/<name>/SKILL.md
```

Use the `SKILL.md` frontmatter and section structure defined in [`SKILL_SPEC.md`](../SKILL_SPEC.md) — that is the single source of truth for the format. Fill each section; Process steps are imperative ("Identify X", "Emit Y") — not narrative.

## 3. Write the description

The `description` is the *only* text Claude reads to decide whether to invoke. Get this right.

- Must start with "Use when".
- ≤ 1024 characters.
- Specific enough to match real triggers; generic enough to catch variants.
- Mention the output artifact and the typical input.

Bad: `Use when you need help with databases.`
Good: `Use when designing a Postgres schema for a new service or planning a schema change for an existing one. Produces an initial schema and a zero-downtime migration plan using the expand/migrate/contract pattern.`

## 4. Make Quality Checks binary

Every quality check is a checkbox a human or Claude can mark pass/fail without ambiguity.

Bad: `- [ ] Schema is well-designed.`
Good: `- [ ] Every FK column has an index.`

## 5. Run the validator

```bash
python scripts/validate_skills.py
```

Fix any failures. The validator enforces: frontmatter present, `name` matches directory, `description` starts with "Use when" and is ≤ 1024 chars.

## 6. Sanity-check the skill

Trigger the skill in Claude Code with a realistic prompt and confirm it runs end-to-end and the result matches its declared Outputs section. Fix the skill until it does. No artifact is committed — there is no reference-output gate.

## 7. Write 5 trigger prompts

For your PR description, include:

- 3 prompts that *should* match this skill (and confirm Claude invokes it).
- 2 prompts that should *not* match (and confirm Claude does not invoke it).

This is a manual check, not automated. It catches descriptions that are too narrow (skill is never invoked) or too broad (skill is invoked for unrelated tasks).

## 8. Open the PR

Per [`CONTRIBUTING.md`](../CONTRIBUTING.md). Include the trigger prompts and an updated entry in the parent architecture domain's or implementation's `README.md`. Also add an **Output contract** section in `SKILL.md` linking to any [`standards/`](../standards/) the skill conforms to.
