# ADR Guide

Use this guide to decide which architecture choices need ADRs and to write them consistently.

## When to write an ADR

Write an ADR for non-obvious decisions with meaningful tradeoffs, such as:

- choosing modular monolith over microservices,
- choosing Postgres over a document database,
- adding async job processing,
- accepting eventual consistency,
- rejecting vector search,
- choosing third-party auth,
- introducing a queue,
- selecting tenant isolation strategy,
- deciding retention or deletion behavior.

Do not write ADRs for trivial choices, defaults already mandated by the stack, or implementation details with no durable architectural consequence.

## ADR structure

Each ADR must include:

- Status: Proposed, Accepted, Deprecated, or Superseded.
- Context: the problem and constraints that forced a decision.
- Decision: the specific choice made.
- Consequences: benefits, downsides, operational tradeoffs, and future limitations.

Consequences must include downsides. A one-sided ADR is incomplete.

## Filename and numbering

Create ADRs under `adrs/`.

Filename format:

```text
0001-choose-modular-monolith.md
0002-use-postgres-for-transactional-state.md
```

Use sequential numbering. Slugs should be lowercase, hyphen-separated, and decision-oriented.

## Quality bar

Each ADR should answer:

- What alternatives were considered?
- Why is this decision appropriate for the PRD?
- What operational burden does this add?
- What future change may force revisiting the decision?
- What downside is the team accepting?
