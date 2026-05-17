# implementation-template

Starter for a new ecosystem-specific execution skill at `implementations/<category>/<ecosystem>/<skill-name>/SKILL.md`. Conforms to [`SKILL_SPEC.md`](../../SKILL_SPEC.md). The `name` matches the leaf skill directory exactly and is a job name, not a tool name (`safe-migration-plan`, not `flyway-runner`). Copy the skeleton below, fill every section, and delete this paragraph.

---

```markdown
---
name: <skill-name>
description: Use when <trigger condition>. <One-sentence outcome and primary artifact.>
---

# <Title Case Skill Name>

## When to use
Trigger conditions. Name the upstream architecture decision this skill executes and what must already be approved.

## Inputs
Approved upstream artifacts (e.g. the relevant `*-architecture.md`), contracts, and constraints. State what the skill refuses to invent.

## Process
Numbered, imperative steps producing production-ready code/configuration. Each step has a concrete, verifiable output.

## Outputs
The concrete artifacts produced and where they are written.

## Quality checks
Binary-verifiable conditions (build passes, gate enforced, no secret committed, etc.).

## References
Links to `references/*.md` and the `standards/` documents this skill conforms to (Output contract).
```

Optional resource directories: `references/`, `assets/`, `checklists/` — include only if `SKILL.md` references them.
