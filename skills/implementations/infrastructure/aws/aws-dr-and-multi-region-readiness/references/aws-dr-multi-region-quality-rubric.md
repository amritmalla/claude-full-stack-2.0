# AWS DR and Multi-Region Readiness Quality Rubric

Load this before declaring the DR posture complete. Revise until each check passes or the unresolved gap is explicitly documented in `dr-multi-region-readiness.md`.

## Context & boundary

- [ ] RPO/RTO targets are sourced from `architecture/reliability`; failover ownership and drill cadence from `architecture/operations` (or an ADR candidate is raised).
- [ ] The workload tier from `architecture-schema` drove the multi-AZ-vs-multi-region and active-passive-vs-active-active decision.
- [ ] The single-region foundation and runtime are extended, not redesigned.

## Topology

- [ ] Multi-AZ is confirmed for tier-0/1 compute and data.
- [ ] The multi-region topology (backup-restore / pilot-light / warm-standby / active-active) matches the tier.
- [ ] The chosen topology names the RTO/RPO it satisfies and the cost trade-off.
- [ ] No under-provisioning (single-region tier-0/1) and no gold-plating (active-active for tier-2).

## Replication & failover

- [ ] Each data store has a defined cross-region replication path (RDS/Aurora, S3 CRR, DynamoDB Global Tables, EBS snapshot copy).
- [ ] Each replication path has a lag budget that satisfies the RPO.
- [ ] Route 53 health-check-based failover has a defined, tested trigger.
- [ ] A documented fail-back procedure exists (not a one-way failover).

## Backups

- [ ] AWS Backup has tier-driven retention.
- [ ] Backups are copied cross-region and (where ransomware/account-compromise resilience requires) cross-account.
- [ ] Backups are encrypted via the foundation CMK strategy.
- [ ] Immutability / Vault Lock is set where compliance requires.

## Drill & validation

- [ ] Failover health checks and DR alarms are wired via the observability skill's substrate.
- [ ] A failover drill has been executed (not just documented).
- [ ] The achieved RPO and RTO are recorded against the targets.
- [ ] A backup restore has actually been performed.
- [ ] The fail-back path has been exercised.
- [ ] Any achieved-vs-target gap is reported with an ADR candidate, not hidden.

## Standards conformance & handoffs

- [ ] [deployment-standards](../../../../../../standards/deployment-standards/README.md): failover/traffic-shift mechanics reproducible via IaC-ready definitions; fail-back defined.
- [ ] [observability-standards](../../../../../../standards/observability-standards/README.md): failover health checks and DR alarms wired; drill results recorded.
- [ ] [security-standards](../../../../../../standards/security-standards/README.md): cross-region replicas/backups encrypted via the foundation CMK strategy; least-privilege access.
- [ ] [naming-conventions](../../../../../../standards/naming-conventions/README.md): region, replica, backup-vault, failover-record naming.
- [ ] [architecture-schema](../../../../../../standards/architecture-schema/README.md): tier drove multi-AZ-vs-multi-region and active-passive-vs-active-active.
- [ ] Org topology, single-region foundation/runtime, observability/cost, and Terraform module/state mechanics are named handoffs — none implemented here.

## Failure handling

If a check fails:

1. Identify the under/over-sized topology, the lagging replication path, or the un-rehearsed step.
2. Ask the user for clarification if the decision cannot be inferred from `architecture/reliability` or `architecture/operations`.
3. Revise the design, re-run the failover drill and record the achieved RPO/RTO.
4. Keep any unresolved gap explicit in `dr-multi-region-readiness.md` — do not hide it as an assumption.
