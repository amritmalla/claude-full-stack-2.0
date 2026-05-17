---
name: reliability
description: Use when an approved system design exists and the team needs production-grade reliability architecture before implementation and platform hardening. Produces service-level objectives and error-budget policy, dependency criticality analysis, failure-mode architecture, graceful-degradation behavior, blast-radius isolation, redundancy and failover posture, disaster-recovery strategy with RTO/RPO, chaos-validation planning, release-safety mechanisms, and implementation handoff guidance. Do not use for telemetry instrumentation, runbook authoring, oncall rotation design, performance budgets, or security threat modeling; use operations, performance, or security instead.
---

# Reliability

## When to use

Invoke after `system-design` has approved a design and before implementation and platform work hardens the runtime. Use it whenever a system has externally meaningful availability commitments, multi-component failure interactions, or stateful dependencies whose loss requires a recovery plan.

Do not use for telemetry pipelines or oncall workflow design (use `operations`), latency and throughput budgeting (use `performance`), security threat modeling (use `security`), or post-incident retrospectives on already-shipped systems.

## Inputs

Required:

- Approved `system-design.md` and its relevant ADRs.
- The reliability scope in question: the user-facing journeys, APIs, and background workflows whose availability must be defined.
- Dependency inventory: upstream services, datastores, third-party APIs, and platform substrates the system relies on.

Optional:

- PRD sections covering SLA commitments, compliance regime, and tolerance for degraded behavior.
- Existing SLOs, incident history, postmortems, and known failure patterns.
- Performance budgets from `performance` (latency and error budget interact).
- Platform topology from `infrastructure-platform` (regions, accounts, network zones).
- Cost envelope for redundancy and DR.

## Operating rules

- Reliability is user-visible. SLOs map to user journeys and externally observable workflows, not CPU uptime or infrastructure vanity metrics.
- SLOs are contractual and numerical: every SLO names the journey or endpoint, the indicator, the measurement point, the target, the time window, and the owner.
- An error budget is operational policy, not a dashboard. Define burn-rate thresholds, alert posture, and the response: deploy freeze, feature freeze, rollback-only posture, focus shift, escalation.
- Every dependency has a criticality class — critical, degradable, or optional — with a stated failure impact, fallback behavior, and detection signal. Reject hidden hard dependencies.
- Failure modes are specific to this design: which component fails, the failure shape (down, slow, wrong, intermittent, stale, partitioned, overloaded, partially degraded), what detects it, the blast radius, and recovery. Reject generic "service unavailable" reasoning.
- Graceful degradation is mandatory for critical journeys: define degraded behavior, the user-visible signal, the fallback mechanism, and the recovery path. Reject binary works-or-fails architectures.
- Redundancy must justify itself: name the failure it mitigates, the failover trigger, the failover time, and the operational tradeoff. Reject multi-region without a failure driver.
- Disaster recovery is only real if rehearsed: every DR claim names RTO, RPO, rehearsal cadence, validation ownership, and the last successful exercise. Reject backups without restore validation.
- Blast-radius isolation is architectural: name the containment unit, saturation boundaries, trip/recovery thresholds, and recovery behavior. Reject flat architectures where one dependency failure impacts all tenants.
- Surface reliability tradeoffs with performance, security, and cost directly and operationally. When a tradeoff changes behavior or cost materially, raise an ADR candidate against `system-design` and ask for confirmation with a recommended default: "I recommend X because Y. Confirm or redirect."
- Preserve the system design. Do not redefine bounded contexts, components, or data flow; consume them. A reliability concern that reveals a system-design gap is an ADR candidate or open decision.

## Output contract

`reliability-architecture.md` MUST conform to [standards/architecture-schema](../../../standards/architecture-schema/README.md), which is authoritative for its frontmatter, required and conditional sections, conditional-section omission rules, ADR numbering, and linkage back to `system-design.md` and its ADRs.

SLO, release-safety, and operational content additionally conforms to [observability-standards](../../../standards/observability-standards/README.md) (alerts map to user-impacting symptoms) and [deployment-standards](../../../standards/deployment-standards/README.md) (release gating and rollback align with the promotion flow); security-sensitive failover and DR decisions conform to [security-standards](../../../standards/security-standards/README.md). Skill structure conforms to [documentation-standards](../../../standards/documentation-standards/README.md).

Use `assets/reliability-architecture.template.md` as the scaffold; it implements the schema. No telemetry-pipeline configuration, runbook prose, or vendor failover SDK code appears in the architecture unless it materially changes reliability behavior.

## Progressive references

- Read `references/reliability-architecture-playbook.md` when defining SLIs/SLOs, error-budget policy, dependency criticality, failure-mode analysis, graceful degradation, redundancy posture, isolation boundaries, disaster recovery, chaos/game-day validation, incident posture, or release safety, and to check the anti-pattern list.
- Read `references/reliability-architecture-quality-rubric.md` before finalizing and use it as the validation checklist.
- Use `assets/reliability-architecture.template.md` for `reliability-architecture.md`.

## Process

Progress:

ADR candidates are drafted inline as decisions are made (steps 3, 7, 8, 9). Step 13 only consolidates them; it does not retrofit ADRs from prose.

- [ ] Step 1: Load `system-design.md`, relevant ADRs, recent incident history if available, and any existing SLOs. Identify user-facing journeys and externally observable workflows whose availability matters. Reject reliability discussion disconnected from user impact.
- [ ] Step 2: Define SLIs and SLOs per journey or endpoint: indicator, measurement point, target, time window, and owner. Reference `performance` for latency targets and latency-as-error-budget semantics.
- [ ] Step 3: Define the error-budget policy per SLO: budget, burn-rate thresholds, alert posture, and the operational action on burn (deploy freeze, focus shift, escalation). Draft an ADR candidate where the policy gates releases.
- [ ] Step 4: Inventory dependencies — every upstream service, datastore, queue, third-party API, identity provider, DNS, and platform substrate. Assign a criticality class and record outage impact, fallback posture, and detection signal.
- [ ] Step 5: Map failure modes per component and dependency: failure shape, trigger, blast radius, detection signal, mitigation, and recovery expectation. Reject generic failure-mode catalogs disconnected from this architecture.
- [ ] Step 6: Define graceful-degradation behavior per critical journey: degraded-mode behavior, user-visible impact, fallback mechanism, recovery path, and the acceptable degradation window.
- [ ] Step 7: Define redundancy and high-availability posture per component: strategy, placement topology, failover trigger, failover time, the failure mode addressed, and the consistency tradeoff. Draft an ADR candidate for each redundancy/topology decision. Reject redundancy without a named driver.
- [ ] Step 8: Define blast-radius isolation: containment unit, saturation controls (bulkheads, cells, tenant partitions, circuit breakers, concurrency caps, rate limits), and trip/recovery thresholds. Draft an ADR candidate for the isolation model.
- [ ] Step 9: Define disaster recovery per critical datastore and workflow: backup strategy, restore tooling, failover topology, RTO, RPO per data class, rehearsal cadence, and last validated date. Draft an ADR candidate for the DR topology.
- [ ] Step 10: Define chaos and game-day validation (conditional): exercises, cadence, success criterion, rollback posture, and operational ownership. Omit with rationale when no failover/degradation/restore path warrants rehearsal.
- [ ] Step 11: Define incident-posture inputs (conditional) that `operations` will refine: severity model, page-worthy symptom set, customer-impact threshold. Omit with rationale when `operations` fully owns the incident model.
- [ ] Step 12: Define release-safety mechanisms: deploy gating signals, rollback path, progressive-delivery posture, feature-flag fallbacks, and automatic-rollback triggers, aligned to the promotion flow.
- [ ] Step 13: Generate `reliability-architecture.md` from `assets/reliability-architecture.template.md` with explicit handoffs to `operations`, `infrastructure-platform`, `performance`, `security`, `backend-architecture`, and `data-architecture`. Consolidate ADR candidates and validate against [standards/architecture-schema](../../../standards/architecture-schema/README.md) and `references/reliability-architecture-quality-rubric.md`; revise until both pass or explicitly note any unresolved gap.

## Outputs

Required:

- `reliability-architecture.md` at `docs/architecture/<product-slug>/reliability-architecture.md`, with frontmatter and sections per [standards/architecture-schema](../../../standards/architecture-schema/README.md).

Optional, when applicable:

- SLO table keyed by user journey; dependency criticality matrix.
- Failure-mode catalog; DR topology or isolation-boundary diagram.
- Chaos-exercise catalog.
- ADR drafts for redundancy, region topology, isolation, or DR decisions.

Output rules:

- Keep the architecture decision-oriented and operationally concrete, not aspirational uptime marketing.
- Every redundancy and DR decision names the failure mode it addresses and the rejected alternative.
- Failure modes and degradation behavior name real components and journeys in this design.
- Treat recovery validation and rehearsal as part of the design, not a later implementation detail.
- No telemetry-pipeline configuration, runbook prose, or vendor SDK code appears in the architecture.

## Quality checks

- [ ] `references/reliability-architecture-quality-rubric.md` was loaded before finalizing.
- [ ] `reliability-architecture.md` validates against [standards/architecture-schema](../../../standards/architecture-schema/README.md): frontmatter complete; required sections present; conditional sections present with content or listed under `## Omitted sections` with rationale.
- [ ] Every user-facing journey or externally observable workflow names an SLI, SLO target, time window, and owner.
- [ ] Error-budget policy states burn-rate thresholds and the operational action on burn.
- [ ] Every dependency in scope has a criticality class with outage impact and fallback.
- [ ] Failure modes are specific to named components; no generic placeholders survive.
- [ ] Every critical journey defines graceful-degradation behavior for each degradable dependency.
- [ ] Redundancy decisions name the failure mode addressed and the failover trigger and time.
- [ ] Isolation strategy names the containment unit and trip/recovery thresholds where applicable.
- [ ] DR plan states RTO and RPO per data class, rehearsal cadence, and last validated date.
- [ ] Release safety names the rollback path and deploy-gating signals, aligned to [deployment-standards](../../../standards/deployment-standards/README.md).
- [ ] Reliability tradeoffs with security, cost, or performance are surfaced explicitly.
- [ ] No telemetry pipeline details, runbook prose, or vendor SDK code appear in the architecture.

## References

- Output schema: [`standards/architecture-schema`](../../../standards/architecture-schema/README.md).
- `assets/reliability-architecture.template.md`
- `references/reliability-architecture-playbook.md`
- `references/reliability-architecture-quality-rubric.md`
- Upstream: [`architecture/system-design`](../system-design/SKILL.md).
- Related architecture skills: [`operations`](../operations/SKILL.md), [`performance`](../performance/SKILL.md), [`security`](../security/SKILL.md), [`infrastructure-platform`](../infrastructure-platform/SKILL.md), [`backend-architecture`](../backend-architecture/SKILL.md), [`data-architecture`](../data-architecture/SKILL.md).
- Downstream: reliability-relevant work in [`implementations/infrastructure/*`](../../implementations/infrastructure/) and [`implementations/data/*`](../../implementations/data/).
