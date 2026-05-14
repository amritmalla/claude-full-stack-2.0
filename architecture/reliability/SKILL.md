---
name: reliability
description: Use when an approved system design exists and the team needs reliability architecture before implementation. Produces service-level objectives and error budget policy, failure domain map, dependency criticality and graceful degradation modes, blast-radius isolation, redundancy and high-availability posture, disaster recovery and backup strategy with RTO/RPO, chaos and game-day plan, incident posture, and implementation handoff notes. Do not use for telemetry instrumentation, runbook authoring, oncall rotation design, performance budgets, or security threat modeling; use operations, performance, or security instead.
---

# Reliability

## When to use

Invoke after `system-design` has approved a design and before implementation and platform work hardens the runtime. Use it whenever a system has externally meaningful availability commitments, multi-component failure interactions, or stateful dependencies whose loss requires a recovery plan.

Do not use for telemetry pipelines or oncall workflow design (use `operations`), latency and throughput budgeting (use `performance`), security threat modeling (use `security`), or post-incident retrospectives on already-shipped systems.

## Inputs

Required:

- Approved `system-design.md`.
- The reliability scope in question: the user-facing journeys, APIs, and background workflows whose availability must be defined.
- Dependency inventory: upstream services, datastores, third-party APIs, and platform substrates the system relies on.

Optional:

- PRD sections covering SLA commitments, compliance regime, and tolerance for degraded behavior.
- Existing SLOs, incident history, postmortems, and known failure patterns.
- Performance budgets from `performance` (latency and error budget interact).
- Platform topology from `infrastructure-platform` (regions, accounts, network zones).
- Cost envelope for redundancy and DR.

## Operating rules

- SLOs are user-visible and numerical. They name the journey or endpoint, the measurement, the target, the time window, and the owner.
- An error budget is a policy, not a metric. Define what happens when it burns: feature freeze, deploy gating, focus shift.
- Every dependency has a criticality class. Loss of a critical dependency is a user-visible outage; loss of a degradable dependency triggers a defined fallback.
- Failure modes are specific to this design. List the components that can fail, the failure shape (slow, wrong, down, partial), the blast radius, and the detection signal.
- Redundancy is justified by a stated failure mode and recovery target, not by default. N+1, multi-AZ, multi-region each have cost and complexity that need a driver.
- Disaster recovery is tested or it does not exist. Every DR claim names the rehearsal cadence and the last validated date.
- Graceful degradation is a first-class behavior. For every critical user journey, define what the system does when a dependency is unavailable.
- Blast radius isolation (bulkheads, cells, tenant partitions, circuit breakers) is decided here, not in code. State the unit of isolation and what it contains.
- When reliability posture conflicts with performance, security, or cost (e.g., synchronous replication tax, multi-region cost), raise an ADR candidate.

## Process

1. Load `system-design.md`, recent incident history if available, and any existing SLOs. Identify user-facing journeys and externally observable workflows whose availability matters.
2. Define SLIs and SLOs per journey or endpoint: indicator definition, measurement point, target, time window, and owner. Use availability and latency-as-error-budget indicators; reference `performance` for latency targets.
3. Define the error budget policy: budget per SLO, burn-rate alerts, and the actions tied to burn (deploy freeze, focus shift, escalation).
4. Inventory dependencies: every upstream service, datastore, queue, third-party API, and platform substrate the system relies on. Assign a criticality class: critical, degradable, or optional.
5. Map failure modes per component and per dependency: failure shape (down, slow, wrong, partial, intermittent), trigger conditions, blast radius, detection signal, and mitigation. Reject generic failure-mode lists.
6. Define graceful degradation behavior per critical user journey: when a degradable dependency is unavailable, what the system returns, with what user-visible signal, and within what budget.
7. Define redundancy posture per component: replica count, placement (AZ, region, account), failover trigger, failover time, and the failure mode it addresses. Reject redundancy without a named driver.
8. Define isolation strategy: bulkheads, cells, tenant partitions, queues, circuit breakers, and rate limits. State the unit of isolation, what it contains, and the trip and recovery thresholds.
9. Define disaster recovery: backup strategy per datastore, restore tooling, region-failover topology (active-active, active-passive, pilot light, backup-and-restore), RTO and RPO per data class, and the rehearsal cadence.
10. Define chaos and game-day plan: what is exercised (instance loss, AZ loss, dependency degradation, region failover, restore), how often, and the success criterion per exercise.
11. Define incident posture inputs that `operations` will refine: severity definitions, the page-worthy symptom set, and the customer-communication threshold.
12. Define release safety mechanisms: deploy gating signals, rollback path, progressive-delivery posture, and feature-flag fallbacks for risky changes.
13. Produce `reliability-architecture.md` with explicit handoffs to `operations`, `infrastructure-platform`, `performance`, `security`, `backend-architecture`, and `data-architecture`.

## Outputs

Required:

- `reliability-architecture.md` covering SLOs and error budget policy, dependency criticality map, failure-mode catalog, graceful degradation behavior per journey, redundancy posture per component, isolation strategy, DR plan with RTO/RPO, chaos plan, incident posture inputs, and release safety mechanisms.

Optional, when applicable:

- SLO table keyed by user journey.
- Dependency criticality matrix.
- Failure-mode catalog.
- DR topology diagram.
- ADR drafts for redundancy, region topology, or isolation decisions.

## Quality checks

- [ ] Every user-facing journey or externally observable workflow names at least one SLI, an SLO target, a time window, and an owner.
- [ ] An error budget policy is stated with burn-rate thresholds and the action taken on burn.
- [ ] Every dependency in scope is assigned a criticality class.
- [ ] Failure modes are specific to named components in this design; no generic placeholders survive.
- [ ] Every critical user journey defines a graceful-degradation behavior for each degradable dependency.
- [ ] Redundancy decisions name the failure mode they address and the failover trigger and time.
- [ ] Isolation strategy names the unit of isolation, what it contains, and trip/recovery thresholds where applicable.
- [ ] DR plan states RTO and RPO per data class and names a rehearsal cadence.
- [ ] Chaos plan names the exercises, cadence, and success criterion.
- [ ] Release safety names the rollback path and the deploy-gating signals.
- [ ] No telemetry pipeline details, runbook prose, or vendor SDK code appear in the architecture.

## References

- Upstream: [`architecture/system-design`](../system-design/SKILL.md).
- Related architecture skills: `operations`, `performance`, `security`, `infrastructure-platform`, [`backend-architecture`](../backend-architecture/SKILL.md), `data-architecture`.
- Downstream: reliability-relevant work in `implementations/infrastructure/*` and `implementations/data/*`.
