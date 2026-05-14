---
product: <kebab-case-slug>
status: draft
owner: <name or role>
version: 0.1.0
last_reviewed: YYYY-MM-DD
---

# PRD — <Product Name>

> Conforms to [standards/prd-schema](../../../../standards/prd-schema/README.md).
>
> **Required sections:** Problem, Users, JTBD, Scope, Non-goals, Constraints, Assumptions, Success Metrics, Open Questions.
>
> **Conditional sections:** Why Now, Current Alternatives, Risks, Distribution and Adoption, Out of scope (future). Include if material; otherwise omit and add a one-line rationale under `## Omitted sections` at the bottom (e.g., "Why Now omitted: foundational build with no external urgency trigger").

## Problem

[Name the specific primary user and painful workflow. Do not include solutioning, features, or technology choices.]

## Why Now

[Explain current urgency. Omit if this is a foundational build, internal tool, or system component with no external trigger — and note the omission.]

## Users

[Primary persona, context, and optional secondary persona if explicitly accepted.]

## JTBD

[The job-to-be-done in the user's language.]

## Current Alternatives

[Current workaround or competing behavior. Omit if there is no prior workaround — e.g., this is a new internal capability with no incumbent.]

## Scope

[3-5 v1 outcomes. Avoid feature catalogs.]

## Non-goals

[At least three explicit exclusions with rationale.]

## Constraints

[Known limits that shape the PRD.]

## Assumptions

[Testable beliefs that must be true for success.]

## Risks

[Major risks with why each matters and mitigation or narrowing recommendation. Omit if no material risks remain after scope narrowing — and note the omission.]

## Distribution and Adoption

[For external products: how the first 100 users discover, adopt, or are required to use the workflow.
For internal tools / reference workloads / system components: which upstream and downstream consumers integrate, and how cutover is staged.
Omit only if neither applies.]

## Success Metrics

[2-4 metrics. Each must include unit, target, and timeframe.]

## Open Questions

[Only decisions the user explicitly deferred. Each: question, owner, decision deadline.]

## Out of scope (future)

[Backlog signals worth preserving but explicitly deferred past v1. Omit if no such signals exist.]

## Omitted sections

[List each conditional section omitted, with a one-line rationale. Remove this heading if all conditional sections are present.]
