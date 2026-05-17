---
name: performance
description: Use when an approved system design exists and the team needs performance architecture before implementation or scale events. Produces explicit latency, throughput, concurrency, and cost budgets per user-visible path, a capacity and headroom model, scaling and backpressure posture, hot-path and critical-path analysis, caching and precomputation strategy, performance test and regression-gating policy, and implementation handoff notes. Do not use for availability and disaster-recovery design (use reliability), telemetry instrumentation (use operations), ad-hoc profiling, single-query tuning, or vendor-specific runtime tuning.
---

# Performance

## When to use

Invoke after `system-design` has approved bounded contexts, service interactions, major data flows, and user-visible journeys, and before backend implementation, frontend rendering decisions, persistence tuning, infrastructure provisioning, or a scale event. Use it whenever user-visible latency matters, workloads may saturate, growth projections exist, cost-per-request matters, or scale posture changes materially.

Do not use for availability and disaster-recovery architecture (use `reliability`), telemetry pipeline design (use `operations`), one-off profiling of a production bottleneck, database query or GC tuning, CDN/vendor optimization flags, implementation-level micro-optimizations, or incident retrospectives.

## Inputs

Required:

- Approved `system-design.md` and its relevant ADRs.
- The performance scope: user-visible journeys, externally observable workflows, and batch or background jobs whose timing is contractually or operationally meaningful.
- Expected load shape: peak and steady-state traffic, concurrency profile, and growth horizon.

Optional:

- PRD success metrics, perceived-performance commitments, SLAs, competitive benchmarks.
- Existing latency, throughput, and resource telemetry; historical scaling or incident events.
- Reliability SLOs from `reliability` (availability and error budget interact with latency posture).
- Cost envelope and unit-economics targets.
- Geographic distribution; hardware, region, or vendor constraints; existing caching posture.

## Operating rules

- Budgets are numerical and on user-visible paths. "Fast" is not a budget; p50/p95/p99 latency, RPS, concurrency, and cost-per-request are. Every budget names the path, the measurement point, the percentile, and the owner.
- Performance architecture is workload-specific, not framework-specific. Classify workloads (interactive, streaming, background, batch, event-driven) before sizing anything.
- Capacity modeling precedes benchmarking. Derive expected resource demand from the load shape; use benchmarks to validate, not to discover requirements.
- Critical paths and hot paths are separate concerns. The critical path drives user-visible latency; the hot path drives cost. State both per journey; they may diverge.
- Every cache, read model, or precomputation introduces consistency cost, invalidation complexity, and warm-up behavior. Decide it here in budget terms; hand mechanics to `data-architecture`/`backend-architecture`.
- Scaling posture defines trigger, lag, ceiling, and saturation behavior. Backpressure is mandatory for every saturable dependency; bounded queues over infinite retries; fast failure over cascading latency amplification.
- Graceful degradation of optional functionality is preferable to uncontrolled collapse of core workflows. Cost is a first-class performance budget, not an afterthought.
- Priority under conflict: correctness under load > predictable latency > graceful degradation > reliability preservation > cost efficiency > peak throughput > developer ergonomics.
- When performance posture conflicts with reliability, security, or cost (dropping retries to hit latency, weakening tenant isolation for cache reuse), raise an ADR candidate against `system-design` and ask for confirmation with a recommended default: "I recommend X because Y. Confirm or redirect."
- Preserve the system design. Do not redefine bounded contexts, components, or data flow; consume them.

## Output contract

`performance-architecture.md` MUST conform to [standards/architecture-schema](../../../standards/architecture-schema/README.md), which is authoritative for its frontmatter, required and conditional sections, conditional-section omission rules, ADR numbering, and linkage back to `system-design.md` and its ADRs.

Regression-gating and operational content additionally conforms to [deployment-standards](../../../standards/deployment-standards/README.md) (release/canary gates and rollback align with the promotion flow) and [observability-standards](../../../standards/observability-standards/README.md) (perf SLIs and saturation indicators map to user-impacting symptoms); cache-reuse decisions that cross tenant boundaries conform to [security-standards](../../../standards/security-standards/README.md). Skill structure conforms to [documentation-standards](../../../standards/documentation-standards/README.md).

Use `assets/performance-architecture.template.md` as the scaffold; it implements the schema. No profiler outputs, code-level micro-optimizations, or vendor-specific tuning flags appear in the architecture unless they materially change architecture behavior.

## Progressive references

- Read `references/performance-architecture-playbook.md` when defining workload shape, budgets, critical/hot paths, the capacity model, scaling posture, caching/precomputation, backpressure and load shedding, performance testing, regression gating, or cost-performance tradeoffs, and to check the decision framework and anti-pattern list.
- Read `references/performance-architecture-quality-rubric.md` before finalizing and use it as the validation checklist.
- Use `assets/performance-architecture.template.md` for `performance-architecture.md`.

## Process

Progress:

ADR candidates are drafted inline as decisions are made (steps 5, 6, 7, 9). Step 12 only consolidates them; it does not retrofit ADRs from prose.

- [ ] Step 1: Load `system-design.md` and relevant ADRs. List user-visible paths, externally observable workflows, async flows, background jobs, and the dependency graph. Identify critical paths, hot paths, fan-out, and high-cost operations.
- [ ] Step 2: Define workload shape per workload: class, steady-state and peak RPS, concurrency, burst shape, geographic distribution, seasonal pattern, growth horizon, and worst plausible spike.
- [ ] Step 3: Define performance budgets per user-visible path: p50/p95/p99 latency, throughput, concurrency, timeout posture, error-budget interaction, and cost-per-request/user/job, each with a measurement point and owner. Reject vague targets.
- [ ] Step 4: Identify the critical path (synchronous latency contributors), the hot path (most-invoked per unit of business value), serialization points, and cost-amplifying operations per journey.
- [ ] Step 5: Build the capacity model per workload: CPU, memory, IOPS, network, connections, queue depth, payload size, cache memory at peak and worst plausible spike; state headroom factor, exhaustion threshold, and recovery expectation. Draft an ADR candidate where capacity assumptions constrain topology.
- [ ] Step 6: Define scaling posture per workload: scaling shape, autoscaling trigger, scaling lag, partitioning posture, concurrency limits, saturation ceiling, and ceiling behavior (queue/degrade/shed/fail). Draft an ADR candidate for partitioning or scale-shape decisions.
- [ ] Step 7: Define caching and precomputation (conditional) per layer: location, source of truth, cached entity, invalidation trigger, TTL/staleness budget, warm-up, stampede protection, consistency tradeoff, and budget delta. Draft an ADR candidate where caching weakens correctness or crosses tenant boundaries. Omit the section with rationale when no cache layer exists.
- [ ] Step 8: Define backpressure and load shedding per saturable component: queue/retry/timeout posture, concurrency cap, circuit-breaker behavior, rate limits, shed behavior, user-visible symptom, and recovery condition.
- [ ] Step 9: Define performance testing: load, stress, soak, spike, and failover-perf tests — workload simulated, production likeness, budgets validated, pass/fail criteria, environment parity. Draft an ADR candidate where a test gates contractual workflows.
- [ ] Step 10: Define regression gating: which metrics block release, which alert, which are informational; CI/release/canary gates, rollback thresholds, measurement source of truth, and ownership.
- [ ] Step 11: Define cost-performance tradeoffs: hard limits vs negotiable budgets, elasticity posture, cost-escalation triggers, which paths justify higher spend, which workloads may degrade under cost pressure.
- [ ] Step 12: Generate `performance-architecture.md` from `assets/performance-architecture.template.md` with explicit handoffs to `backend-architecture`, `frontend-architecture`, `data-architecture`, `infrastructure-platform`, `reliability`, and `operations`. Consolidate ADR candidates and validate against [standards/architecture-schema](../../../standards/architecture-schema/README.md) and `references/performance-architecture-quality-rubric.md`; revise until both pass or explicitly note any unresolved gap.

## Outputs

Required:

- `performance-architecture.md` at `docs/architecture/<product-slug>/performance-architecture.md`, with frontmatter and sections per [standards/architecture-schema](../../../standards/architecture-schema/README.md).

Optional, when applicable:

- Budget table keyed by user journey or endpoint; capacity worksheet (load → resources).
- Scaling decision matrix per workload; critical-path or cache-topology diagram.
- ADR drafts for budget, scaling, partitioning, or caching decisions that constrain implementation.

Output rules:

- Keep the architecture decision-oriented and budget-driven, not benchmark-decorative.
- Every budget is numerical, user-visible, and names its measurement point and owner.
- Critical path and hot path are stated per journey even when they coincide.
- Every scaling and caching decision names the saturation driver or budget delta and the rejected alternative.
- No profiler outputs, code-level micro-optimizations, or vendor-specific tuning flags appear in the architecture.

## Quality checks

- [ ] `references/performance-architecture-quality-rubric.md` was loaded before finalizing.
- [ ] `performance-architecture.md` validates against [standards/architecture-schema](../../../standards/architecture-schema/README.md): frontmatter complete; required sections present; conditional sections present with content or listed under `## Omitted sections` with rationale.
- [ ] Every user-visible path defines p50, p95, and p99 latency budgets with a measurement point and owner.
- [ ] Every workload class defines throughput and concurrency expectations tied to the stated load shape.
- [ ] Critical paths and hot paths are explicitly identified per journey.
- [ ] Capacity model includes peak load and worst plausible spike with a stated headroom factor.
- [ ] Scaling posture defines the ceiling and ceiling behavior per workload.
- [ ] Every cache or precomputation layer names invalidation, staleness policy, and the budget delta it buys.
- [ ] Every saturable dependency defines backpressure or load-shedding behavior and recovery condition.
- [ ] Load, stress, spike, and soak testing are defined with the budgets they gate.
- [ ] Regression gates define release-blocking thresholds, aligned to [deployment-standards](../../../standards/deployment-standards/README.md).
- [ ] Cost posture is explicitly stated per workload class.
- [ ] No vendor-specific tuning flags, profiler outputs, or implementation-level optimizations appear.

## References

- Output schema: [`standards/architecture-schema`](../../../standards/architecture-schema/README.md).
- `assets/performance-architecture.template.md`
- `references/performance-architecture-playbook.md`
- `references/performance-architecture-quality-rubric.md`
- Upstream: [`architecture/system-design`](../system-design/SKILL.md).
- Related architecture skills: [`backend-architecture`](../backend-architecture/SKILL.md), [`frontend-architecture`](../frontend-architecture/SKILL.md), [`data-architecture`](../data-architecture/SKILL.md), [`reliability`](../reliability/SKILL.md), [`operations`](../operations/SKILL.md), [`security`](../security/SKILL.md), [`infrastructure-platform`](../infrastructure-platform/SKILL.md).
- Downstream: perf-relevant work in [`implementations/backend/*`](../../implementations/backend/), [`implementations/frontend/*`](../../implementations/frontend/), [`implementations/data/*`](../../implementations/data/), and [`implementations/infrastructure/*`](../../implementations/infrastructure/).
