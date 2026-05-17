# MongoDB Indexing and Query Optimization — Layout Reference

Use this as the canonical explain / index-audit / pipeline-review pattern reference. Placeholder tokens use `<camelCase>` / `<collection>`. This skill tunes the engine against the existing model; modeling/shard-key choice is handed to `mongodb-data-model-and-migration`.

## Deliverable layout

```
query-optimization.md          # ranked profiler findings + index-audit table +
                                #   per-query before/after explain + pipeline rewrites
                                #   + shard-key effectiveness finding
samples/
├── explain-<query>-before.json
├── explain-<query>-after.json
└── profiler-top-<window>.json  # PII/secret-free
```

## Evidence collection (profiler)

```js
db.setProfilingLevel(1, { slowms: <slo-threshold-ms> })   // representative dataset
// ... run representative load / wait for the window ...
db.system.profile.aggregate([
  { $group: { _id: "$ns", totalMs: { $sum: "$millis" }, n: { $sum: 1 } } },
  { $sort: { totalMs: -1 } }, { $limit: 20 }               // rank by TOTAL time
])
```

## Hot-query explain — what to read

```js
db.<collection>.find({ <query> }).sort({ <sortField>: 1 })
  .explain("executionStats")
// Inspect:
//   stage            IXSCAN good | COLLSCAN finding | SORT (in-memory) finding
//   totalKeysExamined / totalDocsExamined vs nReturned   (ratio ~1 is ideal)
//   executionTimeMillis vs the performance SLO
//   FETCH absent + totalDocsExamined:0  => covered query
```

## Index audit table (in query-optimization.md)

```
| index | maps to query pattern | keep/drop/add | write+RAM cost | evidence |
|-------|-----------------------|---------------|----------------|----------|
| {status:1,createdAt:1} | find(status).sort(createdAt) | keep (ESR ok) | low | explain-A |
| {createdAt:1} | (prefix of above) | DROP redundant | -1 write idx | — |
| {email:1} | 0 profiler hits / window | DROP unused | -1 write idx | profiler |
| {tenantId:1,_id:1} | covering hot read | ADD | +1 write idx | explain-B |
```

## ESR — compound index order

```
query: find({ status: "ACTIVE", score: { $gt: 10 } }).sort({ createdAt: -1 })
ESR  : Equality(status) -> Sort(createdAt) -> Range(score)
index: { status: 1, createdAt: -1, score: 1 }      // serves the query
WRONG: { score: 1, status: 1, createdAt: -1 }      // range first => poor
```

## Aggregation pipeline cost review

```js
[
  { $match: { tenantId: <id>, status: "OPEN" } },  // EARLY (indexed) — reduce stream
  { $project: { _id: 1, amount: 1, createdAt: 1 } },// EARLY — shrink docs
  { $sort:  { createdAt: -1 } },                     // index-backed OR after $limit
  { $limit: 100 },                                   // bound before $lookup
  { $lookup: { from: "<small/indexed>", /* bounded cardinality */ } }
]
// Findings: late $match | blocking $sort | unbounded $lookup/$unwind on hot path
```

## Collation mismatch (silent index disable)

```js
// Index built with a locale collation:
db.<c>.createIndex({ name: 1 }, { collation: { locale: "en", strength: 2 } })
// Query WITHOUT the matching collation => COLLSCAN even though the index exists:
db.<c>.find({ name: "abc" })                              // <-- finding
db.<c>.find({ name: "abc" }).collation({ locale: "en", strength: 2 })  // uses it
```

## Shard-key effectiveness (finding handed to modeling)

```
single-shard (targeted) query share : <measured %>
scatter-gather (broadcast) share    : <measured %>
verdict: <effective | hotspotting | scatter-prone>
-> if not effective: FINDING to mongodb-data-model-and-migration (owns resharding)
```

## Handoffs this skill names (does not implement)

| Concern | Owner |
|---|---|
| Document modeling, `$jsonSchema`, shard-key choice, migrations | `mongodb-data-model-and-migration` |
| Replica-set topology, read-preference routing, write concern | `mongodb-replication-and-ha-readiness` |
| Backup/restore, PITR, oplog-window observability | `mongodb-backup-and-operational-readiness` |
| Auth, RBAC, CSFLE, TLS, audit log | `mongodb-security-and-data-access-hardening` |
| ODM/repository query code (Spring Data, Mongoose, etc.) | backend implementation skill |
