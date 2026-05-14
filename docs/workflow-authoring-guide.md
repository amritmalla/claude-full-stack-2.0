# Workflow Authoring Guide

A practical walkthrough for authoring a new workflow. For the formal contract, see [`WORKFLOW_SPEC.md`](../WORKFLOW_SPEC.md).

## What a workflow is

A workflow sequences existing skills into a lifecycle path. It does *not* contain procedural detail — that belongs in the skills it references.

If your workflow has a step with its own inputs, process, and outputs, that step is a skill. Author the skill first, then reference it.

## 1. Create the directory

```
workflows/<workflow-name>/
└── WORKFLOW.md
```

The directory name matches the `name` field in frontmatter.

## 2. Identify the phases

A workflow has 2–6 phases. Each phase is a coherent stage of work that ends with an explicit checkpoint (PR review, smoke test, on-call handoff).

Phases for the v0.1 capstone workflow `idea-to-production-spring-boot`: Define → Build → Ship → Operate.

## 3. Fill the WORKFLOW.md template

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

For each phase, list:

- **Skills** invoked in this phase, by name (matching their directory names).
- **Entry** — what must exist before this phase starts (concrete artifacts).
- **Exit** — what this phase produces (concrete artifacts).
- **Gate** — the explicit checkpoint required before advancing.

## 4. Cross-check skill references

Every skill named in `(skills: …)` must exist under `architecture/` or `implementations/`. The CI does not enforce this in v0.1, but a maintainer will check it on review.

## 5. Open the PR

Include in the PR description: the lifecycle path the workflow covers, who you expect to invoke it, and the rationale for the phase boundaries.
