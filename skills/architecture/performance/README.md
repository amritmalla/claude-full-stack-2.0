# performance

> Status: draft

## Purpose

Turns an approved system design into performance architecture before implementation or scale events: explicit latency, throughput, concurrency, and cost budgets per user-visible path, a capacity and headroom model, scaling and backpressure posture, hot-path and critical-path analysis, caching and precomputation strategy, and performance-regression gating.

Technology-agnostic and budget-driven. Owns *what "fast enough" means*, *where performance matters*, and *how the system behaves under saturation* — not the framework, query plan, or runtime flags that implement it. Implementation-level optimization lives under [implementations/backend](../../implementations/backend/), [implementations/frontend](../../implementations/frontend/), [implementations/data](../../implementations/data/), and [implementations/infrastructure](../../implementations/infrastructure/).

## Owns

- Latency, throughput, concurrency, and cost budgets per user-visible path
- Workload classification and load-shape modeling
- Capacity and headroom model
- Critical-path and hot-path analysis
- Scaling, partitioning, and saturation-ceiling posture
- Caching and precomputation strategy in budget terms
- Backpressure and load-shedding posture
- Performance testing and regression-gating policy
- Cost-performance tradeoff levers

## Produces

| Artifact | Conforms to |
|---|---|
| `performance-architecture.md` | [architecture-schema](../../../standards/architecture-schema/README.md), [documentation-standards](../../../standards/documentation-standards/README.md) |
| ADR drafts (budget, scaling, partitioning, caching) | [architecture-schema](../../../standards/architecture-schema/README.md) |

## Skills

- [performance](SKILL.md) - turns an approved system design into performance architecture: workload shape, budgets, critical/hot paths, capacity model, scaling and backpressure posture, caching strategy, performance testing, regression gating, cost-performance tradeoffs, and implementation handoffs.

## Standards this architecture domain conforms to

- [architecture-schema](../../../standards/architecture-schema/README.md) - `performance-architecture.md` artifact structure and system-design traceability.
- [deployment-standards](../../../standards/deployment-standards/README.md) - release/canary gates and rollback align with the promotion flow.
- [observability-standards](../../../standards/observability-standards/README.md) - perf SLIs and saturation indicators map to user-impacting symptoms.
- [security-standards](../../../standards/security-standards/README.md) - cache-reuse decisions crossing tenant boundaries.
- [documentation-standards](../../../standards/documentation-standards/README.md) - skill structure.

## Upstream inputs

Requires an approved `system-design.md` per [architecture-schema](../../../standards/architecture-schema/README.md) whose design has user-visible paths constrained by latency, throughput, concurrency, or cost-per-request, or an anticipated scale event. Bounded contexts, service interactions, data flows, and ADRs in the system design shape the performance architecture produced here; they are consumed, not redefined.

## Downstream consumers

Performance architecture produced here is the source of truth for:

- [implementations/backend/*](../../implementations/backend/) - latency budgets, concurrency posture, timeout and async boundaries.
- [implementations/frontend/*](../../implementations/frontend/) - rendering, asset-loading, hydration, and interaction-latency budgets.
- [implementations/data/*](../../implementations/data/) - query latency budgets, cache ownership, partitioning pressure.
- [implementations/infrastructure/*](../../implementations/infrastructure/) - autoscaling, capacity assumptions, queueing posture.
- [architecture/reliability](../reliability/README.md) - degradation posture, saturation behavior, load-shedding policy.
- [architecture/operations](../operations/README.md) - regression gates, perf alerts, SLI measurement expectations.
