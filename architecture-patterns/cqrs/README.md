# cqrs

## Summary

CQRS (Command Query Responsibility Segregation) separates the write model (commands that change state) from one or more read models (queries optimized for specific views). The two sides evolve and scale independently.

## Problem & forces

A single model forced to serve both complex writes and high-volume diverse reads becomes a compromise that does neither well. The forces — divergent read/write scaling, query shapes that fight the write schema, and read-side denormalization — justify splitting responsibility.

## When to use / When not to use

**Use when**

- Read and write workloads scale very differently or have conflicting shapes.
- Many distinct read projections are needed from the same write data.
- The write side has rich invariants while reads are simple lookups.

**Avoid when**

- CRUD with simple queries — CQRS adds machinery for no gain.
- The team cannot tolerate read-model staleness (when fed asynchronously).
- It is adopted reflexively alongside event sourcing without a real read/write split need.

## Structure

Commands mutate the write store; changes propagate (often via [`event-driven`](../event-driven/README.md)) to denormalized read stores serving queries.

```text
command → write model → write DB
                          │ change events
                          ▼
                     projector → read DB → query API
```

## Key tradeoffs

Gain: independently optimized/scaled reads, simpler write invariants, multiple tailored projections. Pay: eventual consistency between write and read, projection code and rebuild tooling, more moving parts and operational surface.

## Failure modes & mitigations

- **Stale read models** — users expect read-after-write. Provide read-your-writes on critical paths or surface staleness explicitly.
- **Projection drift/bugs** — read model diverges from truth. Make projections deterministic and rebuildable from the source of truth.
- **Over-application** — CQRS everywhere. Apply only to the bounded contexts that need it.

## Related skills & patterns

- Skills: [`backend-architecture`](../../architecture/backend-architecture/SKILL.md), [`data-architecture`](../../architecture/data-architecture/SKILL.md), [`performance`](../../architecture/performance/SKILL.md)
- Patterns: [`event-driven`](../event-driven/README.md) (the usual propagation mechanism), [`domain-driven-design`](../domain-driven-design/README.md), [`microservices`](../microservices/README.md)
