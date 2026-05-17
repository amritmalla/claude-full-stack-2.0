# MongoDB Indexing and Query Optimization Playbook

Load this when auditing any owned area of `mongodb-indexing-and-query-optimization` or checking the anti-pattern list. It expands the operating rules and process steps in `SKILL.md` with the detail needed to produce evidence-driven query and index optimization.

## Why this workflow exists

Query and index defects are invisible until scale. A missing index is a `COLLSCAN` that is instant on 10k documents and a 30-second outage on 10M. An extra index nobody queries is a silent write tax and RAM pressure that evicts the working set. A compound index in the wrong field order serves none of the queries it looks like it should. A blocking in-memory sort works in the demo and OOMs the node under real fan-out. A scatter-gather shard key turns every query into an all-shard query. None of this fails a functional test — the data comes back, just slowly and expensively, until it doesn't come back at all.

The goal is optimization driven by `explain()` and the profiler, against the existing model, with every index justified and every hot query measured before and after — consuming the performance SLOs instead of inventing them.

## Behavioral rules in depth

### 1. Evidence first — `explain` is the unit of proof

No index is added or dropped without `explain("executionStats")` (or `allPlansExecution`) on a representative dataset, captured before and after. "This should be faster" is not evidence. The numbers that matter: `executionTimeMillis`, `totalKeysExamined`, `totalDocsExamined`, `nReturned`, `stage` (IXSCAN vs COLLSCAN vs FETCH), and whether a SORT stage is in-memory.

### 2. Consume performance and data-architecture; do not invent it

The query SLOs come from `performance`; the consistency and sharding posture from `data-architecture.md`. Optimization targets *those* numbers. If a needed decision is missing, raise an ADR candidate.

### 3. Tune the engine — do not redesign the model

Document shape, validators, and the shard-key *choice* belong to `mongodb-data-model-and-migration`. When the real fix is a model change (an unbounded array, a wrong shard key, a missing denormalization), that is a **finding handed back**, not a change made here. Crossing that line forks ownership of the schema.

### 4. Every index earns its keep

| Index state | Action |
|---|---|
| Maps to a named, frequent query | Keep; record the pattern |
| Prefix of another compound index | Drop (redundant) |
| Zero profiler hits over the window | Flag for drop with write/RAM cost |
| "Might need it later" | Drop — add it when the query exists |

Every index is a write amplifier and consumes RAM in the working set. Bloat is not free.

### 5. ESR — equality, sort, range

Compound index field order is Equality fields, then the Sort field, then Range fields. A `{status, createdAt}` index serves `find(status=X).sort(createdAt)`; `{createdAt, status}` does not. A compound index that violates ESR for its target query is a defect unless explicitly justified (e.g. a covering-index trade-off).

### 6. COLLSCAN on a real collection is a finding

Every collection scan on a non-trivial collection gets: an index, a query rewrite, or a written acceptance with a hard size bound and rationale. It is never left silent. A small lookup table scanned fully is fine *if stated*.

### 7. Cover the hot paths

For the highest-frequency reads, prefer an index that includes every projected field so the query is served entirely from the index (`totalDocsExamined: 0`, `FETCH` absent). Flag queries that fetch documents only to discard most fields.

### 8. Aggregation pipelines are cost-reviewed stage by stage

`$match` and `$project` as early as possible (reduce the stream before work). `$sort` index-backed or bounded by a preceding `$limit`. `$lookup` with a bounded foreign cardinality and an index on the foreign field. `$unwind` explosion (1 doc → N) noted and bounded. A blocking sort or an unbounded `$lookup` on a hot path is a finding.

### 9. Collation and projection are explicit on text/locale paths

A query whose collation does not match the index's collation silently does not use that index — `explain` shows the COLLSCAN even though the index "exists". Locale-sensitive sorts/matches must align query and index collation; call out every mismatch.

### 10. Shard-key effectiveness is measured, not assumed

Using the profiler/explain, quantify the share of queries that are single-shard (targeted) vs scatter-gather (broadcast). A low-cardinality, monotonically increasing, or non-query-aligned shard key produces hotspotting or all-shard fan-out. That is reported to `mongodb-data-model-and-migration` (resharding is its ownership), with the routing evidence.

### 11. Hot collections come from the profiler

Enable the profiler at a sensible `slowms` (or read the slow-query log) over a representative window. Rank by total time (frequency × latency), not just worst single query. Remediate the top contributors and re-measure.

### 12. An unmeasured optimization is unverified

Before/after `explain` for every changed query; profiler delta for hot paths. Without both, the work is unverified.

## Step detail

**Step 1 — Gather context.** Load `performance` (SLOs) and `data-architecture.md` (consistency, sharding). Pull the model/validators/access patterns from `mongodb-data-model-and-migration`. Raise an ADR candidate for any missing decision.

**Step 2 — Evidence collection.** Profiler at appropriate `slowms` (or slow-query log) on a representative dataset; capture top shapes by total time and frequency.

**Step 3 — Index audit.** Enumerate indexes; map to query patterns; flag unused/redundant/unjustified with write+RAM cost.

**Step 4 — Hot-query explain.** `explain("executionStats")`: find COLLSCAN, high `totalDocsExamined:nReturned`, in-memory SORT, uncovered hot reads; propose index/rewrite/bounded-acceptance.

**Step 5 — ESR check.** Verify compound order vs target query; correct violations.

**Step 6 — Pipeline cost review.** Early `$match`/`$project`; index-backed/bounded `$sort`; bounded `$lookup`; noted `$unwind`; rewrite blocking stages.

**Step 7 — Collation/projection.** Align query/index collation on text/locale paths; flag silent-disable mismatches.

**Step 8 — Shard-key effectiveness.** Quantify single-shard vs scatter-gather; report a wrong key to modeling with evidence.

**Step 9 — Validate.** Re-run `explain` per changed query (before/after); profiler delta for hot paths; SLO met or residual gap documented.

**Step 10 — Emit & validate.** `query-optimization.md` (ranked profiler findings, index-audit table, per-query before/after, pipeline rewrites, shard-key finding), handoff list. Validate against observability-, naming-, security-, deployment-standards, architecture-schema.

## Anti-patterns to detect

Call these out explicitly when found:

- An index added/dropped with no before/after `explain`
- Model/validator/shard-key *redesign* done here instead of handed to `mongodb-data-model-and-migration`
- Unused, redundant (prefix), or "just in case" indexes left in place
- Compound index violating ESR for its target query
- Silent `COLLSCAN` on a non-trivial collection
- Hot read path not covered, fetching then discarding most fields
- Aggregation with late `$match`, blocking in-memory `$sort`, or unbounded `$lookup`/`$unwind` on a hot path
- Query/index collation mismatch silently disabling the index
- Shard-key effectiveness asserted without single-shard-vs-scatter measurement
- Hot collections guessed instead of profiler-ranked
- PII/secrets in captured profiler/explain samples
- Live index build with no rollout-safe (rolling/background) path
