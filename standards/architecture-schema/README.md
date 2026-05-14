# architecture-schema

Canonical structure for system architecture documents and Architecture Decision Records (ADRs). Produced by `architecture/system-design`; consumed by every downstream implementation domain.

## File layout

```
docs/architecture/<product-slug>/
├── system-design.md           # primary artifact, always present
├── adrs/
│   └── NNNN-<slug>.md         # one per non-obvious decision, monotonic numbering
└── components/                # OPTIONAL — only when escalated (see "Per-component breakout")
    └── <component>.md
```

## `system-design.md`

Primary artifact. One file per system.

### Frontmatter (required)

```yaml
---
product: <kebab-case slug>         # matches the PRD slug
status: draft | review | approved | superseded
owner: <name or role>
prd: <relative path to source PRD>
version: <semver, starts at 0.1.0>
last_reviewed: YYYY-MM-DD
---
```

### Required sections

| Section | Purpose |
|---|---|
| `## Overview` | One-paragraph system summary: core workflows, primary actors, what it optimizes for and intentionally does not. |
| `## Architecture Style` | Chosen style with PRD-based justification, simpler alternatives considered, operational tradeoffs accepted. |
| `## Bounded Contexts` | Table or list: Name, Responsibility, Owned Data, Dependencies, Upstream/Downstream Interactions. |
| `## Components` | One subsection per component: Responsibility, Interfaces, Dependencies, Inputs/Outputs, Persistence, Consistency, Scaling Expectations. |
| `## Data Flow` | Entry points, request paths, async boundaries, consistency model per entity, idempotency, retry behavior, reconciliation. |
| `## Failure Modes` | Table or list: Component, Failure Scenario, User Impact, Detection, Recovery, Degradation. Specific to *this* design — no generic checklists. |
| `## ADR Index` | Table: ADR number, Title, Status, Summary. Links to `adrs/NNNN-<slug>.md`. |

### Conditional sections

Include if material; otherwise omit and add a one-line rationale under `## Omitted sections`.

| Section | When to include |
|---|---|
| `## Persistence Strategy` | Multiple stores, or non-trivial caching / retention / migration concerns. Omit when a single store with an obvious mapping suffices — fold one paragraph into Components instead. |
| `## Security and Compliance` | Always for external products and any system handling user data. Conforms to [security-standards](../security-standards/README.md). May be omitted with one-line rationale for purely internal reference workloads. |
| `## Operational Considerations` | When the design introduces durable operational burden (observability vendor choice, feature flag system, backfill machinery). May fold into Failure Modes if the design has one runtime topology and no durable operational decisions. Conforms to [observability-standards](../observability-standards/README.md) and [deployment-standards](../deployment-standards/README.md). |

## Diagrams

Use Mermaid (`graph`, `flowchart`, `sequenceDiagram`) inline. PNG/SVG only when Mermaid is insufficient; place under `assets/diagrams/`.

## Per-component breakout (optional escalation)

For small systems, the inline `## Components` section is sufficient. Promote a component to its own file in `components/<name>.md` when ANY of the following hold:

- The component is `tier: 0` (see "Component tiers" below).
- Its interface surface exceeds ~5 endpoints or topics.
- It has independent ownership distinct from the system as a whole.
- It implements a distinct pattern (e.g. event-driven module inside an otherwise synchronous system).

Per-component files use this frontmatter:

```yaml
---
component: <kebab-case>
owner: <team or role>
tier: 0 | 1 | 2 | 3
implements: [<architecture-domain-ref>, ...]
implementation: <impl-ref>           # e.g. implementations/backend/spring-boot
patterns: [<pattern-ref>, ...]
---
```

Required sections in a component file: Responsibility, Public interface, Data ownership, Runtime, Observability hooks, SLOs.

## Component tiers

Declared in component frontmatter and used by other standards (deployment gates, security review depth, observability coverage):

| Tier | Meaning |
|---|---|
| 0 | Critical path — outage is incident-grade |
| 1 | Important — degraded experience without it |
| 2 | Standard — affects a subset of users |
| 3 | Experimental — failure is acceptable |

## ADRs

`adrs/NNNN-<slug>.md`:

```markdown
---
id: NNNN
title: <Decision title>
status: proposed | accepted | superseded | deprecated
date: YYYY-MM-DD
supersedes: <NNNN or null>
---

## Context
## Decision
## Consequences
## Alternatives considered
```

Rules:

- Numbering is monotonic across the system; never reused.
- Once an ADR is `accepted`, the body MUST NOT be edited. Changes require a new ADR that `supersedes` the old one.
- ADRs are drafted inline as decisions are made, not retroactively.
- `Consequences` MUST include downsides, not only benefits.
- `Alternatives considered` is non-optional — the value of an ADR is the rejected options.

## Linkage contract

- `system-design.md` MUST link to its source PRD in frontmatter.
- Every component (inline subsection or breakout file) MUST list the `architecture/` it implements.
- Every ADR MUST be referenced from `system-design.md`'s ADR Index.
- Once `system-design.md` is `approved`, it is the sole upstream input to `implementations/*` scaffolding skills.

## Versioning

- Bump **patch** for typo / clarification edits.
- Bump **minor** for added components, ADRs, or failure modes.
- Bump **major** when architecture style or bounded contexts change — requires re-approval and a superseding ADR.

## Anti-patterns

- ADRs without "Alternatives considered" — the value of an ADR is the rejected options.
- Components that write to another component's data (silent coupling).
- Hand-drawn architecture images instead of Mermaid (cannot be diffed).
- Generic failure-mode checklists ("queue backlog" listed when there is no queue).
- Persistence Strategy section padded with "we use Postgres" when one paragraph in Components would do.
- ADRs retrofitted from prose at the end of the design pass instead of drafted inline.
