# modular-monolith

## Summary

A modular monolith is a single deployable whose internals are split into strongly-bounded modules with explicit interfaces and no cross-module reach-through. It delivers most of the organizational clarity of microservices without the distributed-systems cost.

## Problem & forces

Teams want clean domain boundaries and parallel work, but a premature service split adds network failure modes, eventual consistency, and operational overhead before boundaries are even stable. The forces — boundary clarity, single-deploy simplicity, refactor freedom — favor keeping one process while enforcing internal seams.

## When to use / When not to use

**Use when**

- A small-to-medium team owns the system and ships on one cadence.
- Domain boundaries are still being discovered and need to stay cheap to move.
- You want microservices-ready seams without paying the distributed tax yet.

**Avoid when**

- Independent deploy cadence or per-capability scaling is a hard requirement ([`microservices`](../microservices/README.md)).
- Strict fault isolation between capabilities is mandatory.

## Structure

One process, one datastore, modules with public interfaces; cross-module access only through those interfaces (enforced by package boundaries or build rules).

```text
┌─ deployable ───────────────────────────┐
│ [module A] → ifc → [module B]          │
│      ↘ ifc → [module C]                │
│ shared DB (schema-per-module optional) │
└────────────────────────────────────────┘
```

## Key tradeoffs

Gain: one deploy/test/observability surface, in-process calls (no network), free refactoring of boundaries, transactional consistency. Pay: no independent scaling or deploy, one runtime/blast radius, discipline required to keep modules from leaking.

## Failure modes & mitigations

- **Boundary erosion** — modules reach into each other's internals. Mitigate with enforced package/build boundaries and architecture tests.
- **Shared-schema coupling** — modules entangle via the database. Use schema-per-module and forbid cross-schema joins.
- **Big ball of mud** — no real modules, just folders. Require explicit module interfaces, reviewed like APIs.

## Related skills & patterns

- Skills: [`system-design`](../../architecture/system-design/SKILL.md), [`backend-architecture`](../../architecture/backend-architecture/SKILL.md)
- Patterns: [`microservices`](../microservices/README.md) (the migration target when seams stabilize), [`domain-driven-design`](../domain-driven-design/README.md) (defines the module boundaries), [`hexagonal-architecture`](../hexagonal-architecture/README.md)
