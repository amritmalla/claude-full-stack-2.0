# MongoDB Backup and Operational Readiness Playbook

Load this when designing any owned area of `mongodb-backup-and-operational-readiness` or checking the anti-pattern list. It expands the operating rules and process steps in `SKILL.md` with the detail needed to produce a recovery posture that actually recovers.

## Why this workflow exists

Backup defects are discovered the one time they matter, and then it is too late. A backup job that has succeeded for a year but has never been restored is an untested assumption — the restore fails on a missing oplog slice, a corrupt snapshot, or a procedure nobody has run. A `mongodump` of a busy primary captures an inconsistent point. PITR "configured" with an oplog that does not chain back to the base backup recovers nothing. An RPO target written in a doc but never measured is a wish. None of this shows up until the disaster, when the measured data loss is hours and the runbook is a blank page.

The goal is a backup whose restore has actually been performed and measured against RPO/RTO, with the oplog chain that makes PITR real and runbook inputs the on-call can execute — consuming the reliability and operations posture instead of inventing it.

## Behavioral rules in depth

### 1. Backup and restore are paired — the restore is the deliverable

A backup job that succeeds is not the work. The work is a *restore that has been performed* and measured. This is a locked data-tier constraint, not a nice-to-have. If only the backup half exists, the skill is not done.

### 2. Consume reliability and operations; do not invent it

RPO/RTO come from `architecture/reliability`; backup ownership and drill cadence from `architecture/operations`. The mechanism is chosen *to meet* the RPO, not by preference. If a needed decision is missing, raise an ADR candidate.

### 3. Build on the topology — do not redesign it

The replica set, the member backups are taken from, and the oplog window are `mongodb-replication-and-ha-readiness`'s ownership. A backup that needs a topology change (a dedicated hidden member, a longer oplog) is a finding handed back, not a topology edit made here.

### 4. The mechanism matches the deployment and the RPO

| Mechanism | Fits | RPO/restore profile |
|---|---|---|
| `mongodump` | Small data, logical portability | Coarse RPO, slow large restore |
| Filesystem/volume snapshot | Large data, fast restore | Snapshot-interval RPO, fast restore |
| Cloud/Ops Manager | Self-managed at scale | Continuous oplog, point-in-time |
| Atlas continuous backup | Atlas-hosted | Continuous, managed PITR |

A mechanism whose achievable RPO exceeds the target is rejected — pick another or escalate.

### 5. Consistency respects the replica set

Back up from a secondary or hidden member, or take a journaled/filesystem-consistent snapshot. A naive `cp` of a live primary's data files captures a torn state. State explicitly how the consistent point is guaranteed.

### 6. PITR is only real if the oplog chains

Point-in-time recovery = base backup + a continuous oplog slice from the base time to the target time. If the oplog window does not cover the gap between backups, PITR cannot reach points in that gap. State the maximum recoverable point and any gap to the RPO — do not claim PITR without the chain.

### 7. RPO/RTO are measured, not asserted

Execute a restore. Measure: actual RPO (how much data, in time, was lost vs the last recoverable point) and actual RTO (wall-clock from decision to serving). Compare to targets. A gap is reported with an ADR candidate, never rounded away.

### 8. Drills recur — once is decay

Encode the `architecture/operations` drill cadence. A restore proven in January and never again is, by December, an assumption again. The cadence is part of the deliverable.

### 9. Backups are encrypted; the key model is security's

Production backups are encrypted at rest with least-privilege access. This skill *requires* it and names the encryption key and access model to `mongodb-security-and-data-access-hardening` (so there is one owner for key custody). An unencrypted production backup is rejected.

### 10. Observe what silently breaks recovery

Oplog window (shrinking below the recovery requirement), replication lag (a lagging backup source), backup job success/failure, last-successful-backup age (the silent killer), and balancer state on sharded clusters. Each has a threshold and an alert destination — a stale backup nobody is paged about is the classic post-incident finding.

### 11. Runbook inputs are concrete and executable

For primary loss, oplog rollover, and chunk-balancer issues: the firing signal, the exact confirming command, the first recovery step, and the escalation. Structured for the operations runbook. "Investigate the cluster" is not a runbook input.

### 12. An un-rehearsed backup posture is not done

The completion gate: a restore has been executed and RPO/RTO measured. Documentation alone does not satisfy it.

## Step detail

**Step 1 — Gather context.** Load `architecture/reliability` (RPO/RTO) and `architecture/operations` (ownership, cadence, runbook hook). Pull topology/backup-source/oplog-window from `mongodb-replication-and-ha-readiness`. Resolve tier from `architecture-schema`. Raise an ADR candidate for any missing decision.

**Step 2 — Mechanism.** Select per deployment model + RPO; justify against achievable RPO and restore speed.

**Step 3 — Consistency.** Backup-source member + consistent-point guarantee; never a naive live-primary copy.

**Step 4 — PITR.** Base + oplog chain covering the window; state max recoverable point and any RPO gap.

**Step 5 — Frequency/retention.** Per tier; compliance/legal-hold handling.

**Step 6 — Encryption/access.** Require encrypted, least-privilege artifacts; name the key/access model to the security skill.

**Step 7 — Observability.** Oplog window, lag, backup success, last-successful-age, balancer state — thresholds + destinations.

**Step 8 — Runbook inputs.** Primary loss, oplog rollover, balancer issues — signal → command → first step → escalation.

**Step 9 — Restore drill.** Restore to a target time; measure RPO/RTO vs targets; exercise PITR; record results; encode recurring cadence.

**Step 10 — Emit & validate.** `backup-operational-readiness.md` (mechanism+rationale, consistency, PITR chain, frequency/retention, observability thresholds, runbook inputs, drill results vs RPO/RTO), handoff list. Validate against observability-, deployment-, security-standards, architecture-schema, naming-conventions.

## Anti-patterns to detect

Call these out explicitly when found:

- A backup job with no executed, measured restore (the classic "backup that isn't")
- Mechanism whose achievable RPO exceeds the target, used anyway
- `mongodump`/file copy of a live primary with no consistent-point guarantee
- "PITR enabled" with an oplog window that does not chain to the base backup
- RPO/RTO asserted in a doc but never measured in a drill
- A one-off restore with no encoded recurring drill cadence
- Unencrypted production backup; key model not named to the security skill
- No last-successful-backup-age alert (stale backups fail silently)
- Runbook "inputs" as prose instead of signal → command → step → escalation
- Topology *redesign* done here instead of handed to `mongodb-replication-and-ha-readiness`
- Storage/volume/bucket provisioning authored here (infrastructure layer)
