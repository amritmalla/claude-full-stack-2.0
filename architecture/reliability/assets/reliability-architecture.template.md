---
product: <kebab-case slug>          # matches the system-design / PRD slug
status: draft                       # draft | review | approved | superseded
owner: <name or role>
system_design: <relative path to source system-design.md>
prd: <relative path to source PRD, or null>
version: 0.1.0                      # semver
last_reviewed: YYYY-MM-DD
---

# Reliability Architecture: [Product or System Name]

## Overview

[One paragraph: the reliability scope, the critical user journeys and externally observable workflows, what this architecture optimizes for, and what it intentionally does not cover.]

## Service-Level Objectives

| Journey / Workflow | SLI | Measurement Point | Target | Time Window | Owner |
|---|---|---|---|---|---|
| [journey] | [success rate / latency-as-error / freshness] | [where measured] | [target] | [rolling window] | [owner] |

## Error-Budget Policy

| SLO | Budget | Burn-Rate Thresholds | Alert Posture | Operational Response |
|---|---|---|---|---|
| [SLO] | [budget] | [fast/slow burn] | [page/ticket] | [deploy freeze / focus shift / escalation] |

## Dependency Criticality

| Dependency | Class | Outage Impact | Fallback Posture | Detection Signal |
|---|---|---|---|---|
| [dependency] | [critical / degradable / optional] | [user-visible impact] | [fallback or none] | [signal] |

## Failure Modes

| Component | Failure Shape | Trigger | Blast Radius | Detection | Mitigation | Recovery |
|---|---|---|---|---|---|---|
| [component] | [down / slow / wrong / intermittent / stale / partitioned / overloaded] | [trigger] | [contained scope] | [signal] | [mitigation] | [recovery expectation] |

## Graceful Degradation

| Critical Journey | Degraded Behavior | User-Visible Signal | Fallback Mechanism | Recovery Path | Degradation Window |
|---|---|---|---|---|---|
| [journey] | [behavior] | [what the user sees] | [stale cache / read-only / async / disabled feature] | [path] | [acceptable window] |

## Redundancy & High Availability

| Component | Strategy | Placement Topology | Failover Trigger | Failover Time | Failure Mode Addressed | Consistency Tradeoff |
|---|---|---|---|---|---|---|
| [component] | [N+1 / multi-AZ / active-passive / active-active / pilot-light] | [topology] | [trigger] | [RTO-ish] | [failure mode] | [tradeoff] |

## Blast-Radius Isolation

| Isolation Unit | Containment Boundary | Saturation Controls | Trip Threshold | Recovery Threshold |
|---|---|---|---|---|
| [bulkhead / cell / tenant partition / queue] | [what it contains] | [circuit breaker / concurrency cap / rate limit] | [trip] | [recovery] |

## Disaster Recovery

| Datastore / Workflow | Backup Strategy | Restore Tooling | Failover Topology | RTO | RPO | Rehearsal Cadence | Last Validated |
|---|---|---|---|---|---|---|---|
| [datastore] | [strategy] | [tooling] | [active-active / active-passive / pilot-light / warm-standby / backup-restore] | [RTO] | [RPO] | [cadence] | [date] |

## Release Safety

| Concern | Decision |
|---|---|
| Deploy gating signals | [signals] |
| Rollback path | [mechanism] |
| Progressive-delivery posture | [canary / rolling / blue-green / staged] |
| Feature-flag fallbacks | [flags] |
| Automatic-rollback triggers | [triggers] |

## Chaos & Game-Day Validation

*Conditional — include only when failover/degradation/restore paths must be exercised; otherwise list under Omitted sections.*

| Exercise | Cadence | Success Criterion | Rollback Posture | Owner |
|---|---|---|---|---|
| [instance loss / AZ loss / region failover / dependency throttling / restore drill] | [cadence] | [criterion] | [posture] | [owner] |

## Incident Posture

*Conditional — include only when reliability seeds severity/paging inputs that `operations` refines; otherwise list under Omitted sections.*

| Concern | Decision |
|---|---|
| Severity model | [definitions] |
| Page-worthy symptom set | [symptoms] |
| Customer-impact threshold | [threshold] |
| Escalation triggers | [triggers] |

## Multi-Region Strategy

*Conditional — include only when multi-region or active-active is opted in; otherwise list under Omitted sections.*

| Concern | Decision |
|---|---|
| Business driver | [driver] |
| Region topology | [topology] |
| Consistency tradeoff | [tradeoff] |
| Governing ADR | [ADR ref] |

## Implementation Handoffs

### operations

- [Severity inputs, page-worthy symptoms, runbook hooks consumed by operations]

### infrastructure-platform

- [Redundancy placement, failover mechanics, region topology handoff]

### performance

- [Latency-as-error-budget interaction, load/saturation thresholds]

### security

- [Failover and DR decisions crossing trust/tenant boundaries]

### backend-architecture / data-architecture

- [Degradation behavior, consistency tradeoffs, backup/restore expectations]

## ADR Index

| ADR | Title | Status | Summary |
|---|---|---|---|
| NNNN | [title] | [proposed/accepted/...] | [summary] — links to `adrs/NNNN-<slug>.md` |

## Omitted sections

- [Conditional section name]: [one-line rationale for omission].

## Deferred Decisions

- [Decision, owner, deadline].
