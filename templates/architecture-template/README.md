# architecture-template

Starter for a new technology-agnostic architecture domain at `skills/architecture/<domain>/SKILL.md`. Conforms to [`SKILL_SPEC.md`](../../SKILL_SPEC.md). The `name` matches the domain directory exactly. Copy the skeleton below into `skills/architecture/<domain>/SKILL.md`, fill every section, and delete this paragraph.

---

```markdown
---
name: <domain>
description: Use when <trigger condition>. <One-sentence outcome and primary artifact.>
---

# <Title Case Domain>

## When to use
Trigger conditions and signals that this domain skill should be invoked. State what must already exist upstream.

## Inputs
What the user or upstream skill must supply (approved artifacts, decisions, constraints).

## Process
Numbered, imperative steps. Each step is a concrete action with a verifiable output. No narrative.

## Outputs
The concrete decision-oriented artifact(s) this skill produces and where they are written.

## Quality checks
Binary-verifiable conditions the output must satisfy (pass/fail, no "ensure it's good").

## References
Links to `references/*.md` deep dives and the `standards/` documents the output conforms to.
```

Optional resource directories: `references/`, `assets/`, `checklists/` — include only if `SKILL.md` references them.
