# MongoDB Replication and HA Readiness — Layout Reference

Use this as the canonical topology / read-preference / write-concern / oplog pattern reference. Placeholder tokens use `<name>`. This skill designs the MongoDB topology; host/cluster provisioning is the infrastructure layer's, and per-operation concern declarations come from `mongodb-data-model-and-migration`.

## Deliverable layout

```
replication-ha.md             # member/priority/region map + concern-survivability
                              #   matrix + read-preference table + oplog sizing +
                              #   change-stream posture + rehearsed-failover results
config/
├── replicaset-config.js      # rs.initiate / reconfig (reproducible, not click-ops)
└── oplog-sizing.md           # worst recovery interval vs configured window
```

## Member topology — odd votes, failure-domain aware

```js
rs.initiate({
  _id: "<rs>",
  members: [
    { _id: 0, host: "<az-a>", priority: 2 },          // intended primary
    { _id: 1, host: "<az-b>", priority: 1 },
    { _id: 2, host: "<az-c>", priority: 1 },          // 3 data-bearing voters (odd)
    // tier-0: NO arbiter. hidden/delayed member only if reliability posture calls.
  ]
})
// One AZ loss must NOT remove the voting majority (per the tier's failure domain).
```

## Concern-survivability matrix (in replication-ha.md)

```
| operation class | declared w / readConcern | planned failure | still honored? |
|-----------------|--------------------------|-----------------|----------------|
| order write     | w:"majority", j:true     | lose 1 AZ       | YES (2/3 left) |
| audit append    | w:1 (loss window: 5s)    | lose 1 AZ       | YES (relaxed)  |
| balance read    | readConcern:"majority"   | lose 1 AZ       | YES            |
# A "NO" => finding to mongodb-data-model-and-migration OR raised ADR candidate.
```

## Read preference — explicit, staleness-bounded

```js
// read-after-write / consistency-sensitive:
db.<c>.find(<q>).readPref("primary")
// staleness explicitly acceptable — bound it:
db.<c>.find(<q>).readPref("secondaryPreferred", [], { maxStalenessSeconds: 90 })
```

## Write concern — sized to durability

```js
db.<c>.insertOne(<doc>, { writeConcern: { w: "majority", j: true } })  // mutation
// relaxed — name the data + accepted loss window in replication-ha.md:
db.metrics.insertOne(<doc>, { writeConcern: { w: 1 } })  // loss window: <=5s
```

## Oplog sizing (oplog-sizing.md)

```
worst recovery interval = max(secondary resync, maintenance window,
                              partition duration, backup-induced lag)
configured oplog window  = <measured hours>
requirement              = worst interval + safety margin
verdict                  = window > requirement ? OK : RESIZE
# Oplog rollover before a secondary catches up => full resync (outage-grade).
```

## Change-stream availability

```
- consumers persist resume tokens; handle ChangeStreamHistoryLost
- oplog window >= max consumer downtime
- failover behavior for in-flight streams: <specified>
```

## Handoffs this skill names (does not implement)

| Concern | Owner |
|---|---|
| Document modeling, validators, shard-key choice, per-op concern declaration | `mongodb-data-model-and-migration` |
| Query/index/pipeline tuning | `mongodb-indexing-and-query-optimization` |
| Backup, oplog-based PITR, restore drills | `mongodb-backup-and-operational-readiness` |
| Internal auth (keyfile/x.509), member TLS, RBAC, audit | `mongodb-security-and-data-access-hardening` |
| Host/VM/cluster provisioning | infrastructure layer |
| Read-preference wiring in application code | backend implementation skill |
