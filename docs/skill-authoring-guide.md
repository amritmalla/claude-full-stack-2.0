# Skill Authoring Guide

A practical walkthrough for authoring a new skill. For the formal contract, see [`SKILL_SPEC.md`](../SKILL_SPEC.md).

## 1. Pick a domain and name

Skills live under `skills/<domain>/<name>/`. Domains in v0.1: `product`, `architecture`, `backend`, `data`, `testing`, `containers`, `cicd`, `deploy`, `observability`, `operations`.

Name is kebab-case, descriptive of the *job*, not the technology. Prefer `safe-migration-plan` over `flyway-migration-generator`.

## 2. Create the directory and SKILL.md

```
skills/<domain>/<name>/
└── SKILL.md
```

Start from this template:

```markdown
---
name: <name>
description: Use when <trigger>. <One-sentence outcome.>
---

# <Title Case Name>

## When to use
## Inputs
## Process
## Outputs
## Quality checks
## References
```

Fill each section. Process steps are imperative ("Identify X", "Emit Y") — not narrative.

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
./scripts/validate-skills.sh
```

Fix any failures. The validator enforces: frontmatter present, `name` matches directory, `description` starts with "Use when" and is ≤ 1024 chars.

## 6. Execute the skill against `orders-api`

Open Claude Code in this repository. Trigger the skill with a realistic prompt. Commit the output it produces under `examples/spring-boot/orders-api/.skill-outputs/<name>/`.

If the skill produces something that does not match its declared Outputs section, fix the skill until it does.

## 7. Write 5 trigger prompts

For your PR description, include:

- 3 prompts that *should* match this skill (and confirm Claude invokes it).
- 2 prompts that should *not* match (and confirm Claude does not invoke it).

This is a manual check, not automated. It catches descriptions that are too narrow (skill is never invoked) or too broad (skill is invoked for unrelated tasks).

## 8. Open the PR

Per [`CONTRIBUTING.md`](../CONTRIBUTING.md). Include the trigger prompts, the example output, and an updated `skills/<domain>/README.md` index.
