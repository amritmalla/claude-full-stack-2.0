# Reliability Architecture Playbook

Load this when defining SLOs, error budgets, dependency criticality, failure modes, degradation, redundancy, isolation, disaster recovery, chaos validation, or release safety. It expands the operating rules and process steps in `SKILL.md` with the detail needed to produce a production-grade `reliability-architecture.md`.

## Why this workflow exists

Reliability architecture ensures systems continue delivering acceptable user outcomes under failure, degradation, operational mistakes, dependency loss, traffic spikes, and disaster scenarios. It is not about maximizing uptime claims. It is about explicitly defining availability expectations, engineering bounded failure behavior, limiting blast radius, validating recovery capability, and ensuring the system fails predictably instead of catastrophically.

The goal is controlled degradation, measurable reliability, operational resilience, and recoverability under stress — not aspirational "five nines" marketing, untested failover assumptions, or redundant infrastructure without a failure model.

## Behavioral rules in depth

### 1. Reliability is user-visible

Reliability is defined by user journeys, externally observable workflows, and measurable outcomes. SLOs MUST map to user experience, not infrastructure vanity metrics. Reject CPU uptime as a primary reliability target.

### 2. SLOs are contractual and numerical

Every SLO MUST define the user journey or workflow, the measurement, the target, the time window, and the owner. Examples: API availability, successful checkout completion, event-processing completion, background-job freshness, stream-delivery continuity. Reject undefined reliability expectations.

### 3. Error budgets are operational policy

Error budgets are not dashboards. They define deployment posture, escalation rules, engineering prioritization, and release constraints. Every error budget MUST define burn thresholds, alert posture, and organizational response. Reject SLOs without operational consequences.

### 4. Every dependency has a criticality class

Every dependency MUST classify as critical, degradable, or optional. For each, define failure impact, fallback behavior, and acceptable degradation. Reject hidden hard dependencies.

### 5. Reliability must model real failure shapes

Failure modes MUST describe which component fails, how it fails, what detects it, what breaks, and what contains the blast radius. Failure shapes: down, slow, wrong, intermittent, stale, partitioned, overloaded, partially degraded. Reject generic "service unavailable" reasoning.

### 6. Graceful degradation is mandatory

Critical user journeys MUST define degraded behavior, fallback behavior, and user-visible expectations during dependency loss. Examples: stale cache fallback, read-only mode, reduced personalization, async reconciliation, queue buffering, feature disabling. Reject binary "works or completely fails" architectures.

### 7. Redundancy must justify itself

Redundancy MUST define which failure it mitigates, the failover trigger, the failover time, and the operational tradeoff. Strategies: replicas, multi-AZ, multi-region, active-passive, active-active, pilot-light. Reject multi-region deployment without a failure driver.

### 8. Disaster recovery is only real if rehearsed

Every DR claim MUST define RTO, RPO, rehearsal cadence, validation ownership, and the last successful exercise. Reject DR plans that have never been exercised.

### 9. Blast-radius isolation is architectural

Isolation boundaries MUST define the containment unit, saturation boundaries, and recovery behavior. Strategies: bulkheads, cells, queue partitioning, tenant isolation, rate limits, circuit breakers. Reject flat architectures where one dependency failure impacts all tenants or workflows.

### 10. Reliability tradeoffs must be surfaced directly

Call out over-coupled workflows, hidden synchronous dependencies, unbounded retries, weak failover assumptions, replica-lag risks, untested recovery posture, and operationally fragile architectures. Be direct, operational, and failure-oriented. Examples:

- "This workflow cannot degrade gracefully because the personalization service is a hard dependency."
- "Your failover assumption currently depends on DNS propagation timing."
- "This retry posture can amplify outages under dependency saturation."
- "Your active-active proposal introduces consistency tradeoffs not yet addressed."
- "This queue currently has no isolation boundary between tenants."

## Step detail

**Scope inventory (step 1).** Load the approved system design, dependency inventory, incident history, platform topology, and operational constraints. Identify critical user journeys, externally visible workflows, stateful systems, and business-critical operations. Reject reliability discussion disconnected from user impact.

**SLIs and SLOs (step 2).** For every critical journey define the service-level indicator, measurement point, target, time window, and owner. Examples: request success rate, checkout completion, stream continuity, background-sync freshness, queue-processing delay. Clarify latency-as-failure semantics and partial-degradation thresholds. Reject aspirational SLOs without operational capability.

**Error-budget policy (step 3).** For every SLO define the allowable failure budget, burn-rate thresholds, paging posture, release gating, and escalation actions: deploy freeze, feature freeze, rollback-only posture, incident escalation, engineering focus shift. Reject error budgets tracked but ignored operationally.

**Dependency criticality (step 4).** Inventory upstream services, datastores, queues, caches, external APIs, DNS, identity providers, and infrastructure substrates. Assign criticality (critical / degradable / optional). For each, define outage impact, fallback posture, and detection signals. Reject undeclared hard dependencies.

**Failure-mode analysis (step 5).** For each component and dependency define failure shape, trigger condition, blast radius, detection signal, mitigation path, and recovery expectation. Shapes: outage, high latency, stale data, partial partition, overload, inconsistent responses, corruption, throttling. Reject generic failure-mode catalogs disconnected from architecture.

**Graceful degradation (step 6).** For every critical workflow define degraded-mode behavior, user-visible impact, fallback mechanism, and recovery path: stale reads, async completion, read-only mode, cached recommendations, delayed notifications, disabled secondary features. Clarify acceptable degradation windows. Reject workflows that catastrophically fail from optional dependency loss.

**Redundancy and HA (step 7).** Define replica strategy, placement topology, failover trigger, failover mechanism, recovery time, and consistency tradeoffs: N+1 replicas, multi-AZ, active-passive, active-active, quorum systems, standby replicas. Clarify operational ownership and split-brain handling. Reject redundancy added without operational recovery modeling.

**Isolation and blast radius (step 8).** Define the isolation unit, containment boundaries, and saturation controls: bulkheads, cell architecture, tenant isolation, queues, circuit breakers, concurrency caps, rate limits. Specify trip thresholds, recovery thresholds, and escalation behavior. Reject shared dependency saturation across all tenants or workloads.

**Disaster recovery (step 9).** For every critical datastore and workflow define backup strategy, restore tooling, replication posture, failover topology, RTO, RPO, and rehearsal cadence. Topologies: active-active, active-passive, pilot light, warm standby, backup-and-restore. Clarify data-class-specific recovery expectations. Reject backup strategies without restore validation.

**Chaos and game-day (step 10, conditional).** Define failure exercises, rehearsal cadence, success criteria, rollback posture, and operational ownership: instance loss, AZ failure, region failover, dependency throttling, queue saturation, restore drills, DNS failure, cache loss. Reject failover paths never exercised operationally.

**Incident posture (step 11, conditional).** Define the severity model, paging posture, customer-impact thresholds, escalation triggers, and operational communication expectations that `operations` will refine. Clarify which symptoms are page-worthy. Reject alerting on infrastructure noise without user impact.

**Release safety (step 12).** Define deployment gating, rollback strategy, progressive delivery, feature-flag posture, and release health checks: canary, rolling, blue-green, staged rollout. Clarify automatic-rollback triggers and dependency-health gating. Reject production releases without rollback posture.

**Generate and validate (step 13).** Emit `reliability-architecture.md` from the template with explicit handoffs to operations, infrastructure-platform, backend architecture, data architecture, performance, and security. Consolidate ADR candidates. Validate against the architecture-schema and the quality rubric.

## Standards alignment

- Alerts map to user-impacting symptoms, not infrastructure noise ([observability-standards](../../../../standards/observability-standards/README.md)).
- Release gating and rollback align with the `dev → staging → production` promotion flow ([deployment-standards](../../../../standards/deployment-standards/README.md)).
- Security-sensitive failover and DR decisions conform to [security-standards](../../../../standards/security-standards/README.md).
- The artifact conforms to [architecture-schema](../../../../standards/architecture-schema/README.md) for layout, frontmatter, sections, ADR numbering, and linkage.

## Anti-patterns to detect

Call these out explicitly when detected:

- SLOs without operational consequences
- Hidden hard dependencies
- Retry storms under saturation
- Unbounded queues
- No graceful degradation
- Single-region dependency for critical workflows
- Untested failover assumptions
- Backups without restore validation
- Shared infrastructure blast radius across tenants
- Infinite retries
- Missing circuit breakers
- Replica lag ignored in read behavior
- Active-active without consistency strategy
- DR plans never rehearsed
- Alerting disconnected from user impact
- Releases without rollback posture
- Dependency saturation without isolation
- Stateful workloads without recovery modeling
- Queue consumers without dead-letter handling
- No failure testing for critical workflows
- Multi-region complexity without business justification

## Writing style

Operational, failure-oriented, architecture-focused, and explicit about recovery behavior. Avoid vague availability claims, vendor marketing language, aspirational uptime statements, and implementation-level infrastructure details. The objective is resilient systems with predictable failure behavior, bounded blast radius, and validated recovery capability.
