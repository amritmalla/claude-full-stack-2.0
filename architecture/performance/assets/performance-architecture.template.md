---
product: <kebab-case slug>          # matches the system-design / PRD slug
status: draft                       # draft | review | approved | superseded
owner: <name or role>
system_design: <relative path to source system-design.md>
prd: <relative path to source PRD, or null>
version: 0.1.0                      # semver
last_reviewed: YYYY-MM-DD
---

# Performance Architecture: [Product or System Name]

## Overview

[One paragraph: the performance scope, the user-visible paths that matter, what this architecture optimizes for, and what it intentionally does not cover.]

## Workload Shape

| Workload | Class | Steady RPS | Peak RPS | Concurrency | Burst Shape | Growth Horizon | Worst Plausible Spike |
|---|---|---|---|---|---|---|---|
| [workload] | [interactive / streaming / background / batch / event-driven] | [rps] | [rps] | [concurrency] | [shape] | [horizon] | [spike] |

## Performance Budgets

| Path | p50 | p95 | p99 | Throughput | Concurrency | Timeout | Cost / Unit | Measurement Point | Owner |
|---|---|---|---|---|---|---|---|---|---|
| [user-visible path] | [ms] | [ms] | [ms] | [rps] | [n] | [posture] | [cost/request|user|job] | [client/edge/server] | [owner] |

## Critical & Hot Paths

| Journey | Critical Path (latency) | Hot Path (cost) | Fan-out / Serialization Points |
|---|---|---|---|
| [journey] | [synchronous components] | [most-invoked components] | [fan-out, serialization] |

## Capacity Model

| Workload | CPU | Memory | IOPS | Network | Connections | Queue Depth | Cache Memory | Headroom Factor | Exhaustion Threshold |
|---|---|---|---|---|---|---|---|---|---|
| [workload] | [peak / spike] | [peak / spike] | [peak / spike] | [peak / spike] | [count] | [depth] | [memory] | [×factor] | [threshold] |

## Scaling Posture

| Workload | Scaling Shape | Trigger | Scaling Lag | Concurrency Limit | Saturation Ceiling | Ceiling Behavior |
|---|---|---|---|---|---|---|
| [workload] | [vertical / horizontal / autoscaled / queue-buffered / partitioned] | [trigger] | [lag] | [limit] | [ceiling] | [queue / degrade / shed / fail-closed / fail-open] |

## Caching & Precomputation

*Conditional — include only when cache/read-model/precomputation layers exist; otherwise list under Omitted sections.*

| Layer | Source of Truth | Cached Entity | Invalidation Trigger | TTL / Staleness Budget | Warm-up | Stampede Protection | Consistency Tradeoff | Budget Delta |
|---|---|---|---|---|---|---|---|---|
| [CDN / edge / distributed / in-process / read model / precomputed agg] | [source] | [entity] | [trigger] | [budget] | [strategy] | [protection] | [tradeoff] | [latency/throughput delta] |

## Backpressure & Load Shedding

| Component | Queue Posture | Retry / Timeout | Concurrency Cap | Circuit Breaker | Shed Behavior | User-Visible Symptom | Recovery Condition |
|---|---|---|---|---|---|---|---|
| [component] | [bounded queue] | [retry/timeout] | [cap] | [behavior] | [shed rule] | [symptom] | [recovery] |

## Performance Testing

| Test | Workload Simulated | Production Likeness | Budgets Validated | Pass/Fail Criteria | Environment Parity |
|---|---|---|---|---|---|
| [load / stress / soak / spike / failover-perf] | [workload] | [likeness] | [budgets] | [criteria] | [parity] |

## Regression Gating

| Metric | Gate Type | Threshold | Action |
|---|---|---|---|
| [metric] | [release-blocking / alert / informational] | [threshold] | [block / page / track] |

Measurement source of truth: [system]. Regression owner: [owner].

## Cost-Performance Tradeoffs

| Concern | Decision |
|---|---|
| Hard limits | [non-negotiable budgets] |
| Negotiable budgets | [movable under cost pressure] |
| Elasticity posture | [posture] |
| Cost-escalation triggers | [triggers] |
| Paths justifying higher spend | [paths] |
| Workloads degradable under cost pressure | [workloads] |

## Geographic Distribution

*Conditional — include only when users/workloads span regions and latency/correctness is region-sensitive; otherwise list under Omitted sections.*

| Concern | Decision |
|---|---|
| Region topology | [topology] |
| Synchronous cross-region cost | [cost] |
| Governing ADR | [ADR ref] |

## Implementation Handoffs

### backend-architecture

- [Latency budgets, concurrency posture, timeout expectations, async boundaries, degradation posture]

### frontend-architecture

- [Rendering latency budgets, asset-loading budgets, hydration constraints, interaction-latency targets]

### data-architecture

- [Query latency budgets, indexing expectations, cache ownership, partitioning pressure, read/write amplification]

### infrastructure-platform

- [Autoscaling posture, capacity assumptions, queueing posture, network throughput expectations]

### reliability / operations

- [Degradation posture, saturation behavior, failover-perf expectations, regression gates, SLI measurement]

## ADR Index

| ADR | Title | Status | Summary |
|---|---|---|---|
| NNNN | [title] | [proposed/accepted/...] | [summary] — links to `adrs/NNNN-<slug>.md` |

## Omitted sections

- [Conditional section name]: [one-line rationale for omission].

## Deferred Decisions

- [Decision, owner, deadline].
