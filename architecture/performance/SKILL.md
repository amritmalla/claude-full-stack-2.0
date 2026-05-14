---
name: performance
description: Use when an approved system design exists and the team needs performance architecture before implementation or scale events. Produces latency, throughput, and cost budgets per user-visible path, capacity model and headroom posture, scaling strategy, hot-path and critical-path identification, caching and precomputation strategy, load and stress testing plan, perf regression-gating posture, and implementation handoff notes. Do not use for availability SLOs and failure modes (reliability), telemetry instrumentation (operations), single-query optimization, or ad-hoc profiling of an existing bottleneck.
---

# Performance

## Description

This skill turns an approved system design into a performance architecture: explicit budgets per user-visible path, a capacity model that maps load to resources, a scaling strategy, identification of hot and critical paths, caching and precomputation posture, and a load and stress testing plan that gates regressions before release.

## When to use

Invoke after `system-design` has approved a design and before `backend-architecture`, `frontend-architecture`, or `data-architecture` finalize interface, rendering, or storage decisions whose performance characteristics need a budget envelope.

Do not use for: availability targets and failure-mode design (use `reliability`), telemetry pipeline design (use `operations`), one-off query tuning or profiling an already-shipped bottleneck (treat as engineering work, not architecture), or pure cost optimization on a steady-state system without a perf concern.

## Inputs

Required:

- Approved `system-design.md`.
- The performance scope in question: the user-visible journeys, batch jobs, or background workflows whose performance must be defined.
- Expected load shape: traffic profile, peak vs steady, growth horizon.

Optional:

- PRD sections covering perceived-performance commitments, SLAs, and competitive benchmarks.
- Existing latency, throughput, and resource telemetry.
- Cost envelope and unit-economics targets.
- Hardware, region, or vendor constraints.
- Reliability SLO targets from `reliability` (availability and error budget interact with latency posture).

## Operating rules

- Budgets are stated in numbers and on user-visible paths. "Fast" is not a budget. p50, p95, p99 latency, requests per second, and cost per request are.
- Every budget names the path it applies to (user journey, endpoint, job) and the measurement point (client, edge, server boundary).
- Capacity modeling beats benchmarking. Start from the load shape and derive expected resource demand; use benchmarks to validate, not to discover requirements.
- Choose scaling shape per workload: vertical, horizontal, autoscaled, queue-buffered, or partitioned. State the trigger, the lag, and the limit.
- Identify the critical path and the hot path. The critical path determines user-visible latency; the hot path determines cost. They may diverge.
- Caching, precomputation, and read-model strategy are perf decisions with consistency and invalidation costs. Decide them here in budget terms, then hand off implementation to `data-architecture` and `backend-architecture`.
- Load and stress tests are part of the architecture, not an afterthought. Define what is tested, against which budget, with what gating behavior.
- Cost is a perf budget. Define cost per request, per user, or per job alongside latency and throughput budgets.
- When performance posture conflicts with reliability or security (e.g., dropping retries to hit latency, weakening tenant isolation for cache reuse), raise an ADR candidate.

## Process

1. Load `system-design.md`. List user-visible paths, externally observable workflows, and any batch or background jobs whose timing is contractually or operationally meaningful.
2. Define load shape: peak RPS, steady RPS, diurnal and seasonal pattern, growth horizon, and the worst plausible spike. Tie each to a workload class.
3. Set budgets per path: latency (p50, p95, p99 with measurement point), throughput, error budget interaction, and cost per request/user/job. Reject vague targets.
4. Identify the critical path per user journey: the synchronous components and dependencies whose latency adds up. Identify the hot path: the components most-invoked per unit of business value.
5. Build a capacity model per workload: expected resource demand (CPU, memory, IOPS, connections, tokens, payload size) at peak and at the worst plausible spike. State the headroom factor.
6. Define the scaling strategy per workload: scaling shape, trigger, response time, and ceiling. State what happens at the ceiling (queue, shed, degrade, fail).
7. Define caching, precomputation, and read-model posture: where caches sit, what they cache, staleness budget, invalidation triggers, stampede protection, and the budget delta they buy.
8. Define backpressure, queuing, and load-shedding posture: which paths queue, which shed, the SLO impact of shedding, and the user-visible behavior under saturation.
9. Define the perf testing plan: load tests per critical path against stated budgets, stress tests to find ceilings, soak tests for leak detection, and the gating rule between non-prod and prod.
10. Define regression-gating posture: which perf signals block release, which alert, which are tracked only, and the source-of-truth for measurement.
11. Define cost-perf trade-off levers: which budgets can move under cost pressure, which are hard limits, and the decision owner.
12. Produce `performance-architecture.md` with explicit handoffs to `backend-architecture`, `frontend-architecture`, `data-architecture`, `infrastructure-platform`, `reliability`, and `operations`.

## Outputs

Required:

- `performance-architecture.md` covering load shape, per-path budgets, critical and hot paths, capacity model, scaling strategy, caching and precomputation posture, backpressure and shedding, perf testing plan, regression-gating posture, and cost-perf trade-offs.

Optional, when applicable:

- Budget table keyed by user journey or endpoint.
- Capacity worksheet (load → resources).
- Scaling decision table per workload.
- Cache topology summary referencing `data-architecture`.
- ADR drafts for budget choices that constrain implementation.

## Quality checks

- [ ] Every user-visible path names a p50, p95, and p99 latency budget with a measurement point.
- [ ] Every workload class names a throughput budget tied to the stated load shape.
- [ ] Cost budget is stated per request, user, or job for every workload class.
- [ ] Critical path and hot path are explicitly identified per user journey.
- [ ] Capacity model maps peak load and worst-plausible spike to resource demand with a stated headroom factor.
- [ ] Scaling strategy per workload names the shape, trigger, response time, ceiling, and ceiling behavior.
- [ ] Every cache or precomputation layer names what it buys (latency or throughput delta) against which budget.
- [ ] Backpressure or shedding behavior is defined for every path that can saturate.
- [ ] Load, stress, and soak tests are defined with budgets they gate against and a regression-gating rule.
- [ ] No code-level micro-optimizations, profiler outputs, or vendor-specific tuning flags appear in the architecture.

## References

- Upstream: [`architecture/system-design`](../system-design/SKILL.md).
- Related architecture skills: [`backend-architecture`](../backend-architecture/SKILL.md), `frontend-architecture`, `data-architecture`, `infrastructure-platform`, `reliability`, `operations`.
- Downstream: perf-related work in `implementations/backend/*`, `implementations/frontend/*`, `implementations/data/*`, and `implementations/infrastructure/*`.
