# domain-driven-design

## Summary

Domain-driven design (DDD) aligns the software model with the business domain through a shared *ubiquitous language*, and partitions the system into *bounded contexts* — each with its own model and explicit relationships to others.

## Problem & forces

In a complex domain, a single shared model collapses under conflicting meanings of the same term across teams. The forces — language clarity, autonomous team models, and explicit integration contracts — justify the modeling discipline DDD imposes.

## When to use / When not to use

**Use when**

- The domain is complex and central to competitive advantage.
- Multiple teams/subdomains use the same words to mean different things.
- You need principled seams for [`modular-monolith`](../modular-monolith/README.md) modules or [`microservices`](../microservices/README.md).

**Avoid when**

- The domain is simple/generic (CRUD, well-known utility) — modeling overhead exceeds value.
- The team will perform tactical patterns (entities, aggregates) without the strategic context mapping that gives them meaning.

## Structure

Strategic design splits the domain into bounded contexts with a context map; tactical patterns (aggregates, entities, value objects, domain events) model each context internally.

```text
[Context A: model A] ──contract──▶ [Context B: model B]
        │ aggregates, entities, domain events (per context)
```

## Key tradeoffs

Gain: shared language reduces miscommunication, clear context boundaries enable autonomy, models stay aligned to business change. Pay: significant modeling and collaboration effort, requires domain-expert access, easy to misapply tactically without strategy.

## Failure modes & mitigations

- **Tactical-only DDD** — aggregates without bounded contexts. Start with strategic context mapping.
- **One model to rule all** — ignoring context boundaries. Allow the same term to differ per context; integrate via explicit contracts.
- **Anemic domain model** — logic in services, data in dumb objects. Put invariants inside aggregates.

## Related skills & patterns

- Skills: [`system-design`](../../skills/architecture/system-design/SKILL.md), [`backend-architecture`](../../skills/architecture/backend-architecture/SKILL.md)
- Patterns: [`microservices`](../microservices/README.md) and [`modular-monolith`](../modular-monolith/README.md) (boundaries derive from contexts), [`hexagonal-architecture`](../hexagonal-architecture/README.md), [`event-driven`](../event-driven/README.md) (domain events)
