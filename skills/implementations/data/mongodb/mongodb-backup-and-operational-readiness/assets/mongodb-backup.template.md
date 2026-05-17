# MongoDB Backup and Operational Readiness — Layout Reference

Use this as the canonical backup / PITR / restore-drill / runbook pattern reference. Placeholder tokens use `<name>`. This skill designs the backup procedure; storage provisioning is the infrastructure layer's and the encryption key model is `mongodb-security-and-data-access-hardening`'s.

## Deliverable layout

```
backup-operational-readiness.md   # mechanism+rationale + consistency + PITR chain +
                                   #   frequency/retention + observability thresholds +
                                   #   runbook inputs + DRILL RESULTS vs RPO/RTO
runbooks/
├── primary-loss.md
├── oplog-rollover.md
└── balancer-issues.md
drill-log.md                       # executed; measured RPO/RTO recorded
```

## Mechanism selection (in backup-operational-readiness.md)

```
deployment: self-hosted | Ops/Cloud Manager | Atlas
RPO target (architecture/reliability): <e.g. 5 min>
chosen: <volume snapshot every 5m + continuous oplog>  because <achievable RPO <= target>
rejected: mongodump nightly  because <RPO 24h > target>
```

## Consistency — never a naive live-primary copy

```
backup source: hidden member  (no client traffic; consistent)
                — OR — journaled filesystem/volume snapshot
guarantee: fsyncLock / journaled snapshot / secondary read
# `cp` of a live primary's --dbpath = torn state = rejected
```

## PITR chain — must cover the window

```
base backup @ T0  ──oplog slice [T0 .. Tn]──►  restore to any T in [T0, Tn]
max recoverable point = Tn (latest archived oplog entry)
gap to RPO: target=5m, achievable=<measured> -> OK | RESIZE oplog (finding to repl skill)
```

## Restore drill (drill-log.md) — the completion gate

```markdown
# drill-log.md  (EXECUTED, not just written)
1. Provision a scratch target from the latest base backup
2. Replay oplog to target time  T_target
3. Measure RPO = (last durable write time) - T_target            -> <x> (target <y>)
4. Measure RTO = (decision time) -> (serving from restore)        -> <a> (target <b>)
5. Verify integrity (counts, checksums, a known record)
Recorded: achieved RPO=<x> (target <y>) | achieved RTO=<a> (target <b>)
Recurring cadence (architecture/operations): <e.g. quarterly>
Gap (if any): <reported with ADR candidate — never hidden>
```

## Observability — what silently breaks recovery

```
oplog_window_hours       < required        -> ALERT (PITR/resync at risk)
replication_lag_seconds  > threshold       -> ALERT (lagging backup source)
backup_job_status        = failed          -> ALERT
last_successful_backup_age > frequency*2   -> ALERT  (the silent killer)
sharded: balancer_state / chunk_imbalance  -> ALERT
```

## Runbook input — concrete, executable

```markdown
# runbooks/primary-loss.md
- Fires:   replica-set has no PRIMARY for > <N>s
- Confirm: rs.status()  (check members[].stateStr / electionId)
- First:   verify a majority of voters is reachable; let election complete;
           if no majority -> follow forced-reconfig procedure
- Escalate: <on-call path from architecture/operations>
```
(Repeat for **oplog-rollover.md** and **balancer-issues.md**.)

## Handoffs this skill names (does not implement)

| Concern | Owner |
|---|---|
| Document modeling, validators, shard-key, migrations | `mongodb-data-model-and-migration` |
| Query/index/pipeline tuning | `mongodb-indexing-and-query-optimization` |
| Replica topology, backup-source member, oplog-window sizing | `mongodb-replication-and-ha-readiness` |
| Backup-artifact encryption key + access model, RBAC, TLS, audit | `mongodb-security-and-data-access-hardening` |
| Storage/volume/bucket provisioning | infrastructure layer |
