# Workflow Specification

A workflow sequences skills into a lifecycle path. Workflows never duplicate skill logic — they only order skills, define entry and exit artifacts, and set checkpoints between phases.

## File Layout

```
workflows/<workflow-name>/
└── WORKFLOW.md
```

The directory name is the workflow identifier and MUST match the `name` field in frontmatter.

## WORKFLOW.md Format

```markdown
---
name: <kebab-case>
description: Use when <trigger>. Sequences <N> skills covering <stages>.
---

# <Title>

## Phases

### Phase N — <Name> (skills: a, b, c)
**Entry:** <required input artifacts>
**Exit:** <produced artifacts>
**Gate:** <human or automated checkpoint required before next phase>
```

## Authoring Rules

1. **Workflows sequence, not duplicate.** A workflow may not contain procedural content that belongs in a skill. If a step has its own inputs/process/outputs, it is a skill.
2. **Every phase has Entry, Exit, and Gate.** Entry is what must exist before the phase starts. Exit is what the phase produces. Gate is the explicit checkpoint (review, test, sign-off) required before the next phase begins.
3. **Skills are referenced by name** in `(skills: a, b, c)`, matching their directory names exactly.
4. **`description`** follows the same rules as skills: starts with "Use when", ≤ 1024 chars.

## Quality Bar

- Frontmatter valid (`name` matches directory; `description` starts with "Use when").
- Every phase lists its skills, Entry, Exit, and Gate.
- Each referenced skill exists under `capabilities/` or `implementations/`.
- No procedural content duplicates a skill's body.
