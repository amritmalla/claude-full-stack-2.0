# prd-schema

Canonical structure for Product Requirement Documents produced by any `architecture/product-planning` skill. Downstream skills (`system-design`, `backend-systems`, `frontend-architecture`, `testing-quality`) consume PRDs against this schema.

## File location

`docs/product/<slug>/PRD.md` — one folder per product or major feature.

## Frontmatter (required)

```yaml
---
product: <kebab-case slug>
status: draft | review | approved | shipped
owner: <name or role>
version: <semver, starts at 0.1.0>
last_reviewed: YYYY-MM-DD
---
```

## Sections

### Required

| Section | Purpose | Gate |
|---|---|---|
| `## Problem` | The painful workflow and primary user. No solutioning, features, or technology. | Names a specific user and a specific pain |
| `## Users` | Primary persona, context. Secondary only if explicitly accepted. | One primary persona |
| `## JTBD` | Job-to-be-done in the user's language | At least one "when... I want... so I can..." |
| `## Scope` | 3-5 v1 outcomes (not feature catalogs) | Outcomes, ranked |
| `## Non-goals` | Explicit exclusions with rationale | At least 3 entries |
| `## Constraints` | Known limits that shape the PRD | Budget, regulatory, technical, timeline |
| `## Assumptions` | Testable beliefs that must be true for success | Each tagged `validated` / `unvalidated` |
| `## Success Metrics` | How "shipped" becomes "working" | 2-4 metrics: name, unit, target, timeframe, measurement source |
| `## Open Questions` | Intentionally deferred decisions | Each with owner and decision deadline |

### Conditional

Include if material; otherwise omit and add a one-line rationale under a final `## Omitted sections` heading.

| Section | When to include |
|---|---|
| `## Why Now` | Whenever there is external urgency. Omit for foundational builds, internal tools, or system components with no external trigger. |
| `## Current Alternatives` | Whenever a workaround or competitor exists. Omit when there is no incumbent. |
| `## Risks` | Whenever material risks remain after scope narrowing. Each: severity (`high`/`med`/`low`), why it matters, mitigation. |
| `## Distribution and Adoption` | External products: how the first 100 users discover or adopt. Internal tools / system components: integration consumers and cutover staging. Omit only if neither applies. |
| `## Out of scope (future)` | Backlog signals worth preserving but explicitly deferred past v1. |

## Versioning

- Bump **patch** for typo / clarification edits.
- Bump **minor** for added non-goals, metrics, or risks.
- Bump **major** when Scope changes — requires re-approval.

## Linkage contract

A PRD with `status: approved` is the sole upstream input to:

- [architecture/system-design](../../architecture/system-design/README.md) — consumes Problem, Scope, Non-goals, Success Metrics.
- [architecture/backend-systems](../../architecture/backend-systems/README.md) and [architecture/frontend-architecture](../../architecture/frontend-architecture/README.md) — consume Scope, JTBD.
- [architecture/testing-quality](../../architecture/testing-quality/README.md) — consumes Success Metrics → acceptance criteria.

Downstream skills MUST NOT proceed if the PRD is `draft` or `review`.

## Anti-patterns

- Multi-persona v1 PRDs. Split into two products instead.
- Success metrics without a measurement source. "Users will be happy" is not a metric.
- "TBD" left in approved PRDs — convert to an Open Question with an owner and deadline.
- Scope written as a feature catalog instead of user-visible outcomes.
- Conditional sections kept around as empty headings instead of being omitted with rationale.
