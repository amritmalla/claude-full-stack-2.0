# Performance Architecture Quality Rubric

Load this before emitting `performance-architecture.md`. Revise until each check passes or the unresolved gap is explicitly documented.

## Budgets and measurement

- [ ] Every user-visible path defines p50, p95, and p99 latency budgets.
- [ ] Every budget names a measurement point, percentile, and owner.
- [ ] Every workload class defines throughput and concurrency expectations tied to the stated load shape.
- [ ] Cost-per-request/user/job is stated for every workload class.
- [ ] No vague targets ("fast", "scalable") survive.

## Workload and paths

- [ ] Every workload is classified (interactive / streaming / background / batch / event-driven).
- [ ] Workload shape states steady-state, peak, burst, growth horizon, and worst plausible spike.
- [ ] Critical paths and hot paths are explicitly identified per journey, even when they coincide.
- [ ] Fan-out, serialization points, and cost-amplifying operations are named.

## Capacity and scaling

- [ ] Capacity model maps peak load and worst plausible spike to resource demand.
- [ ] Headroom factor, exhaustion threshold, and recovery expectation are stated.
- [ ] Scaling posture names shape, trigger, lag, ceiling, and ceiling behavior per workload.
- [ ] No horizontal scaling without a partition strategy where contention demands it.

## Caching and backpressure

- [ ] Every cache/precomputation layer names source of truth, invalidation trigger, staleness budget, warm-up, stampede protection, and the budget delta it buys, or the section is omitted with rationale.
- [ ] No shared cache crosses tenant boundaries without an ADR.
- [ ] Every saturable dependency defines queue/retry/timeout posture, shed behavior, and user-visible symptom.
- [ ] Recovery conditions are explicit; no infinite retries or unbounded queues.

## Testing and regression gating

- [ ] Load, stress, spike, and soak tests are defined with the budgets they gate and environment parity expectations.
- [ ] Regression gates define which metrics block release, which alert, which are informational.
- [ ] Release/canary gates and rollback thresholds align with the `dev → staging → production` promotion flow ([deployment-standards](../../../../standards/deployment-standards/README.md)).
- [ ] Measurement source of truth and regression ownership are named.

## Cost and tradeoffs

- [ ] Hard limits vs negotiable budgets and cost-escalation triggers are explicit.
- [ ] Which paths justify higher spend and which degrade under cost pressure is stated.
- [ ] Performance tradeoffs with reliability or security are surfaced, not buried.

## Linkage and decisions

- [ ] `performance-architecture.md` conforms to [architecture-schema](../../../../standards/architecture-schema/README.md): frontmatter complete, required sections present, conditional sections present or omitted with rationale under `## Omitted sections`.
- [ ] Frontmatter links the source `system-design.md`; bounded contexts, components, and data flow are consumed, not redefined.
- [ ] Every ADR candidate has Context, Decision, Consequences (including downsides), and Alternatives considered; ADRs share the system's monotonic numbering.
- [ ] No profiler outputs, code-level micro-optimizations, or vendor-specific tuning flags leaked into the architecture.
- [ ] At least one weak-performance risk was surfaced, or the design's intentional simplicity was explained.
- [ ] Any diagram present is prose-consistent: no node references an element absent from this document; if this domain's primary topology diagram (per its authoring skill's Outputs) is omitted, the omission is stated with a rationale.

## Failure handling

If a check fails:

1. Identify the missing or weak performance decision and the budget or saturation risk it leaves uncovered.
2. Ask the architecture or product owner for clarification if it cannot be inferred from `system-design.md` or the PRD.
3. Revise `performance-architecture.md` or the relevant ADR.
4. Keep unresolved questions explicit as open decisions with owners; do not hide them as assumptions or claim unvalidated capacity headroom.
