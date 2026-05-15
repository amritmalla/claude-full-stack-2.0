# reliability

> Status: draft

## Purpose

Turns an approved system design into production-grade reliability architecture before implementation and platform hardening: service-level objectives and error-budget policy, dependency criticality, failure-mode architecture, graceful degradation, blast-radius isolation, redundancy and failover posture, disaster recovery with RTO/RPO, chaos validation, and release safety.

Technology-agnostic and failure-oriented. Owns *what* reliability the system commits to and *how* it fails, degrades, and recovers — not the vendor failover tooling or telemetry pipeline that implements it. Vendor-specific failover, backup, and rollout mechanics live under [implementations/infrastructure](../../implementations/infrastructure/) and [implementations/data](../../implementations/data/).

## Owns

- Service-level objectives mapped to user journeys
- Error-budget policy and release/escalation consequences
- Dependency criticality classification
- Failure-mode architecture and blast-radius containment
- Graceful-degradation behavior per critical journey
- Redundancy and high-availability posture
- Disaster-recovery strategy with RTO/RPO and rehearsal
- Release-safety mechanisms and rollback posture

## Produces

| Artifact | Conforms to |
|---|---|
| `reliability-architecture.md` | [architecture-schema](../../standards/architecture-schema/README.md), [documentation-standards](../../standards/documentation-standards/README.md) |
| ADR drafts (redundancy, region topology, isolation, DR) | [architecture-schema](../../standards/architecture-schema/README.md) |

## Skills

- [reliability](SKILL.md) - turns an approved system design into reliability architecture: SLOs, error budgets, dependency criticality, failure modes, degradation, redundancy, isolation, disaster recovery, chaos validation, release safety, and implementation handoffs.

## Standards this architecture domain conforms to

- [architecture-schema](../../standards/architecture-schema/README.md) - `reliability-architecture.md` artifact structure and system-design traceability.
- [observability-standards](../../standards/observability-standards/README.md) - alerts map to user-impacting symptoms.
- [deployment-standards](../../standards/deployment-standards/README.md) - release gating and rollback align with the promotion flow.
- [security-standards](../../standards/security-standards/README.md) - failover and DR decisions crossing trust/tenant boundaries.
- [documentation-standards](../../standards/documentation-standards/README.md) - skill structure.

## Upstream inputs

Requires an approved `system-design.md` per [architecture-schema](../../standards/architecture-schema/README.md) whose design has externally meaningful availability commitments, multi-component failure interactions, or stateful dependencies requiring a recovery plan. Component boundaries, data ownership, and ADRs in the system design shape the reliability architecture produced here; they are consumed, not redefined.

## Downstream consumers

Reliability architecture produced here is the source of truth for:

- [implementations/infrastructure/*](../../implementations/infrastructure/) - redundancy placement, failover mechanics, region topology, and rollout safety.
- [implementations/data/*](../../implementations/data/) - backup/restore, replication failover, and RTO/RPO expectations.
- [architecture/operations](../operations/README.md) - severity inputs, page-worthy symptoms, and runbook hooks.
- [architecture/performance](../performance/SKILL.md) - latency-as-error-budget interaction and saturation thresholds.
