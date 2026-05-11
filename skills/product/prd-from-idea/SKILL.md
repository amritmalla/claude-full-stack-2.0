---
name: prd-from-idea
description: Use when a user has a rough product idea and needs a tight PRD before
  any architecture or coding work. Produces a one-page PRD with problem statement,
  users, scope, explicit non-goals, success metrics, and open questions.
---

# PRD from Idea

## When to use

Invoke when the user describes a new product, feature, or service in informal terms ("I want to build X", "we need a thing that does Y") and there is no written PRD yet. Do not invoke for changes to an existing PRD — those belong in a doc-edit flow.

## Inputs

- A 1–5 sentence informal description of the idea.
- (Optional) Target users or customer segment.
- (Optional) Known constraints: budget, deadline, stack, regulatory.

## Process

1. Restate the idea in one sentence. Confirm with the user before proceeding.
2. Identify the primary user persona and the job-to-be-done. Name the persona explicitly.
3. Draft a problem statement: what hurts today, for whom, and why now. Do not solution in this section.
4. Define scope as a bulleted list of in-scope outcomes (not features).
5. Define non-goals explicitly. List at least three things this product will NOT do.
6. Propose 2–4 success metrics. Each metric must have a unit and a target value.
7. List open questions blocking design.
8. Emit the final PRD as `PRD.md` with sections: Problem, Users, Scope, Non-goals, Success Metrics, Open Questions.

## Outputs

- `PRD.md` (one page, six sections).

## Quality checks

- [ ] Problem statement names a specific user and a specific pain.
- [ ] Non-goals section lists ≥ 3 items and contradicts at least one tempting scope creep.
- [ ] Every success metric has a unit and a target value.
- [ ] Problem section contains no solutioning ("we will build X").
- [ ] Open Questions section is non-empty.

## References

(None in v0.1. Deep-dive templates land in v0.2.)
