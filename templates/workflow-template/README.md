# workflow-template

Starter for a new workflow at `workflows/<workflow-name>/WORKFLOW.md`. Conforms to [`WORKFLOW_SPEC.md`](../../WORKFLOW_SPEC.md). A workflow only sequences existing skills — it never duplicates skill procedural content. The `name` matches the directory; every skill in `(skills: …)` must resolve to a real skill (CI-enforced by `scripts/validate_skills.py`). Copy the skeleton below, fill every phase, and delete this paragraph.

---

```markdown
---
name: <workflow-name>
description: Use when <trigger>. Sequences <N> skills covering <stages>.
---

# <Title>

<One-line statement of what lifecycle path this workflow chains.> Each phase has an explicit Entry artifact, Exit artifact, and Gate. Do not advance to the next phase until the Gate is satisfied.

## Phases

### Phase 1 — <Name> (skills: `<skill-a>`, `<skill-b>`)

**Entry:** <required input artifacts>
**Exit:** <produced artifacts>
**Gate:** <human or automated checkpoint required before the next phase>

### Phase 2 — <Name> (skills: `<skill-c>`)

**Entry:** Phase 1 exit met.
**Exit:** <produced artifacts>
**Gate:** <checkpoint>

## Rules

- Workflows sequence; they do not duplicate skill logic. Procedural detail lives in the linked skills.
- A phase is not complete until its Gate is satisfied.
- If a skill's Quality Checks fail, return to that skill before advancing.
```

A workflow has 2–6 phases. Skill names must match their directory names exactly.
