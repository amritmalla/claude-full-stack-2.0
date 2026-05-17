# MongoDB Backup and Operational Readiness Quality Rubric

Load this before declaring the backup posture complete. Revise until each check passes or the unresolved gap is explicitly documented in `backup-operational-readiness.md`.

## Context & boundary

- [ ] RPO/RTO are sourced from `architecture/reliability`; backup ownership and drill cadence from `architecture/operations` (or an ADR candidate is raised).
- [ ] The replica topology, backup-source member, and oplog window are consumed from `mongodb-replication-and-ha-readiness` — not redesigned here.
- [ ] No storage/volume/bucket provisioning is done here (infrastructure layer).

## Backup mechanism & consistency

- [ ] The backup mechanism matches the deployment model (self-hosted / Ops Manager / Atlas).
- [ ] Its achievable RPO is within the target; a shortfall is escalated, not accepted silently.
- [ ] Backup consistency is guaranteed (secondary/hidden member or journaled/filesystem-consistent snapshot).
- [ ] No naive copy of a live primary's data files.

## PITR & retention

- [ ] PITR has a base backup plus an oplog chain covering the recovery window.
- [ ] The maximum recoverable point and any gap to the RPO are stated.
- [ ] Backup frequency and retention match the tier.
- [ ] Compliance/legal-hold handling is defined.

## Encryption & observability

- [ ] Backups are encrypted at rest with least-privilege access.
- [ ] The encryption key and access model is named to `mongodb-security-and-data-access-hardening`.
- [ ] Oplog window, replication lag, backup job success/failure, and last-successful-backup age are exposed with thresholds.
- [ ] Sharded clusters expose balancer-state signal.

## Runbook & drill

- [ ] Concrete runbook input exists for primary loss (signal → command → first step → escalation).
- [ ] Concrete runbook input exists for oplog rollover.
- [ ] Concrete runbook input exists for chunk-balancer issues.
- [ ] A restore drill has been executed (not just documented).
- [ ] Measured RPO and RTO are recorded against the targets.
- [ ] PITR to a chosen point was exercised.
- [ ] The recurring drill cadence from `architecture/operations` is encoded.
- [ ] Any achieved-vs-target gap is reported with an ADR candidate, not hidden.

## Standards conformance & handoffs

- [ ] [observability-standards](../../../../../standards/observability-standards/README.md): oplog window, lag, backup success/age, balancer-state signals with thresholds.
- [ ] [deployment-standards](../../../../../standards/deployment-standards/README.md): backup and restore reproducible from configuration, not click-ops.
- [ ] [security-standards](../../../../../standards/security-standards/README.md): backups encrypted/access-controlled; no PII/secret leak in tooling logs; key model named to the security skill.
- [ ] [architecture-schema](../../../../../standards/architecture-schema/README.md): tier drove frequency, retention, PITR requirement.
- [ ] [naming-conventions](../../../../../standards/naming-conventions/README.md): backup-set, snapshot, vault naming.
- [ ] Modeling, query tuning, topology, the security key model, and storage provisioning are named handoffs — none implemented here.

## Failure handling

If a check fails:

1. Identify the un-restored backup, the broken PITR chain, or the missing observability signal.
2. Ask the user for clarification if the decision cannot be inferred from `architecture/reliability` or `architecture/operations`.
3. Revise the procedure, re-execute the restore drill and re-measure RPO/RTO.
4. Keep any unresolved gap explicit in `backup-operational-readiness.md` — do not hide it as an assumption.
