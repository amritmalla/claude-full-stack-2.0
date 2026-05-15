# Performance Architecture Playbook

Load this when defining workload shape, budgets, critical/hot paths, the capacity model, scaling posture, caching, backpressure, performance testing, regression gating, or cost-performance tradeoffs. It expands the operating rules and process steps in `SKILL.md` with the detail needed to produce a production-grade `performance-architecture.md`.

## Why this workflow exists

Performance architecture turns an approved system design into explicit, measurable budgets, scaling posture, capacity assumptions, and regression-gating rules before implementation begins. It defines what "fast enough" means, where performance matters, how load maps to resources, how the system behaves under saturation, and which tradeoffs are acceptable. It does not perform implementation-level optimization.

## Architectural priorities

Priority order, used to resolve conflicts:

1. Correctness under load
2. Predictable latency
3. Graceful degradation
4. Reliability preservation
5. Cost efficiency
6. Peak throughput
7. Developer ergonomics

Preserve correctness before latency, latency before throughput, and reliability before cost optimization.

## Operating principles in depth

- Budgets must be numerical and user-visible; every budget names the path, the measurement point, and the percentile.
- Performance architecture is workload-specific, not framework-specific.
- Capacity modeling precedes benchmarking.
- Critical paths and hot paths are separate concerns: critical drives user-visible latency, hot drives cost.
- Every cache introduces consistency cost, invalidation complexity, and warm-up behavior.
- Scaling posture must define trigger, lag, ceiling, and saturation behavior.
- Backpressure is mandatory for any saturable dependency.
- Graceful degradation is preferable to uncontrolled collapse.
- Cost is a first-class performance metric.

### Cross-skill invariants

- **Budget invariant.** Every user-visible path defines latency budget, throughput expectation, concurrency expectation, and cost posture.
- **Degradation invariant.** Every saturable dependency defines queue behavior, shed behavior, timeout posture, and user-visible fallback.
- **Measurement invariant.** Every metric defines measurement point, aggregation window, percentile, and owner.

## Decision framework

### Latency

- Prefer eliminating synchronous work before scaling infrastructure.
- Prefer bounded latency over maximum throughput.
- Prefer predictable p95 over exceptional p50.
- Prefer colocating dependent services before adding caches.

### Scaling

- Prefer vertical scaling while contention is low and coordination costs dominate.
- Prefer horizontal scaling when contention, concurrency, or fault isolation dominate.
- Prefer queue-buffered systems over burst amplification.
- Prefer partitioning only after a measurable saturation driver exists.

### Caching

- Prefer removing redundant computation before introducing caches.
- Every cache must justify expected hit ratio, invalidation strategy, staleness tolerance, warm-up behavior, memory cost, and operational ownership.
- Prefer explicit stale-data semantics over accidental inconsistency.

### Load shedding

- Prefer degrading optional functionality before rejecting core workflows.
- Prefer bounded queues over infinite retries.
- Prefer fast failure over cascading latency amplification.

### Cost

- Prefer stable unit economics over peak benchmark numbers.
- Prefer reducing hot-path amplification before scaling infrastructure.
- Prefer precomputation only when operational cost is justified by budget savings.

## Step detail

**Load system design (step 1).** Load user-visible journeys, externally observable workflows, synchronous flows, async workflows, background jobs, and the dependency graph. Identify critical paths, hot paths, fan-out patterns, and high-cost operations.

**Workload shape (step 2).** For each workload state steady-state RPS, peak RPS, concurrency, burst shape, geographic distribution, seasonal patterns, growth horizon, and the worst plausible spike. Classify each as interactive, streaming, background, batch, event-driven, or admin/internal.

**Performance budgets (step 3).** For every user-visible path define p50/p95/p99 latency, throughput target, concurrency expectation, timeout posture, error-budget interaction, and cost-per-request/user/job. Every budget includes a measurement point, an owner, and an enforcement expectation. Reject vague targets.

**Critical and hot paths (step 4).** Per journey define the synchronous critical path, fan-out dependencies, serialization points, network-sensitive operations, and cost-amplifying operations. Distinguish latency-critical, throughput-critical, and cost-critical paths.

**Capacity model (step 5).** Per workload estimate CPU, memory, IOPS, network bandwidth, connection counts, queue depth, payload sizes, storage growth, cache memory, and concurrency amplification. Model peak load, worst plausible spike, and failover scenarios. State headroom factor, exhaustion threshold, and recovery expectation.

**Scaling posture (step 6).** Per workload define vertical vs horizontal scaling, autoscaling triggers, scaling lag, queue-buffering posture, partitioning posture, concurrency limits, and saturation ceilings. State what happens at the ceiling: queue, degrade, shed, fail closed, or fail open.

**Caching and precomputation (step 7, conditional).** For each cache layer (CDN, edge, distributed, in-process, materialized read model, precomputed aggregation) define location, source of truth, cached entity, invalidation trigger, TTL, staleness budget, warm-up strategy, stampede protection, consistency tradeoff, and the latency/throughput improvement. Omit the section with rationale when no cache layer exists.

**Backpressure and load shedding (step 8).** For each saturable component define queue posture, retry posture, timeout posture, concurrency cap, circuit-breaker behavior, rate limits, load-shedding behavior, degradation behavior, and the user-visible symptom. State recovery conditions explicitly.

**Performance testing (step 9).** Define load, stress, soak, spike, failover-perf, and degradation tests. Per test define workload simulated, production likeness, budgets validated, pass/fail criteria, and environment parity expectations.

**Regression gating (step 10).** Define which metrics block release, which alert only, and which are informational. Include CI perf gates, release gates, canary gating, rollback thresholds, regression ownership, and the source of truth for measurements.

**Cost-performance tradeoffs (step 11).** Define hard limits, negotiable budgets, elasticity posture, and cost-escalation triggers. State which paths justify higher spend and which workloads may degrade under cost pressure.

**Produce artifact (step 12).** Emit `performance-architecture.md` from the template with explicit handoffs to backend, frontend, data, infrastructure-platform, reliability, and operations. Consolidate ADR candidates and validate against the architecture-schema and the quality rubric.

## ADR triggers

Raise an ADR when:

- multi-region latency changes user-visible correctness
- synchronous cross-region traffic is introduced
- eventual consistency affects UX guarantees
- a shared cache crosses tenant boundaries
- partitioning becomes mandatory
- aggressive caching weakens correctness guarantees
- cost constraints materially weaken latency posture
- load shedding affects contractual workflows
- queue buffering changes business semantics
- third-party APIs become critical-path dependencies

## Handoff contents

- **backend-architecture** — latency budgets, concurrency posture, timeout expectations, async boundaries, degradation posture.
- **frontend-architecture** — rendering latency budgets, asset-loading budgets, hydration constraints, interaction-latency targets.
- **data-architecture** — query latency budgets, indexing expectations, cache ownership, partitioning pressure, read/write amplification constraints.
- **infrastructure-platform** — autoscaling posture, capacity assumptions, queueing posture, network throughput expectations.
- **reliability** — degradation posture, saturation behavior, failover-perf expectations, load-shedding policy.
- **operations** — regression gates, perf alerts, SLI measurement expectations, saturation indicators.

## Standards alignment

- Release/canary gates and rollback thresholds align with the `dev → staging → production` promotion flow ([deployment-standards](../../../standards/deployment-standards/README.md)).
- Perf SLIs and saturation indicators map to user-impacting symptoms ([observability-standards](../../../standards/observability-standards/README.md)).
- Cache-reuse decisions that cross tenant boundaries conform to [security-standards](../../../standards/security-standards/README.md).
- The artifact conforms to [architecture-schema](../../../standards/architecture-schema/README.md) for layout, frontmatter, sections, ADR numbering, and linkage.

## Anti-patterns to detect

Call these out explicitly when detected:

- Defining "fast" without numerical budgets
- Scaling before identifying bottlenecks
- Infinite retries under saturation
- Offset pagination on high-scale hot paths
- Shared caches without ownership boundaries
- Cache invalidation without staleness policy
- Synchronous fan-out across many dependencies
- Unbounded concurrency pools
- Horizontal scaling without partition strategy
- Load tests without production-like datasets
- Benchmarking synthetic paths unrelated to user journeys
- Treating p50 latency as representative
- Queueing critical synchronous user paths indefinitely
- Ignoring cold-start behavior
- Ignoring tail-latency amplification across dependencies

## Writing style

Budget-driven, workload-specific, architecture-focused, and explicit about saturation behavior. Avoid vague speed claims, framework tutorials, profiler dumps, and vendor tuning flags. The objective is a measurable performance envelope with predictable behavior under load, bounded cost, and enforced regression gates.
