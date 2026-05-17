# MongoDB Indexing and Query Optimization Quality Rubric

Load this before declaring the optimization complete. Revise until each check passes or the unresolved gap is explicitly documented in `query-optimization.md`.

## Context & boundary

- [ ] Query SLOs are sourced from `performance`; consistency/sharding posture from `data-architecture.md` (or an ADR candidate is raised).
- [ ] The existing model, validators, and declared access patterns from `mongodb-data-model-and-migration` are the audit baseline.
- [ ] No document-shape, validator, or shard-key *redesign* is done here — such needs are findings handed back to `mongodb-data-model-and-migration`.

## Evidence

- [ ] The profiler (or slow-query log) was enabled at an appropriate `slowms` on a representative dataset.
- [ ] Top query and aggregation shapes are ranked by total time and by frequency.
- [ ] Every changed query has a captured before/after `explain("executionStats")`.
- [ ] Hot paths have a captured profiler delta.

## Index audit

- [ ] Every index maps to a named query/aggregation pattern.
- [ ] Unused, redundant (prefix-of-another), and "just in case" indexes are flagged for removal with their write/RAM cost stated.
- [ ] Every compound index target follows ESR (equality, sort, range) or has a documented exception.
- [ ] Live index builds use a rollout-safe (rolling/background) path and are reproducible from source.

## Query & pipeline

- [ ] Every `COLLSCAN` on a non-trivial collection is a finding with an index, rewrite, or documented bounded acceptance.
- [ ] Hot read paths are covered (index + projection) or the gap is justified.
- [ ] Aggregation pipelines are stage-cost-reviewed; early `$match`/`$project`, index-backed/bounded `$sort`, bounded `$lookup`, noted `$unwind`.
- [ ] Blocking in-memory sorts and unbounded `$lookup`/`$unwind` on hot paths are remediated.
- [ ] Collation/projection mismatches that silently disable an index are called out.

## Sharding & SLO

- [ ] If sharded, shard-key effectiveness is quantified (single-shard vs scatter-gather share).
- [ ] A hot or scatter-prone shard key is reported as a finding to `mongodb-data-model-and-migration` with routing evidence.
- [ ] Each changed query meets its SLO, or the residual gap is documented.

## Standards conformance & handoffs

- [ ] [observability-standards](../../../../../../standards/observability-standards/README.md): slow-query/profiler signals and query-latency metrics exposed; profiler posture reproducible.
- [ ] [naming-conventions](../../../../../../standards/naming-conventions/README.md): named indexes describing purpose; no anonymous index keys.
- [ ] [security-standards](../../../../../../standards/security-standards/README.md): no PII/secrets in captured profiler/explain samples.
- [ ] [deployment-standards](../../../../../../standards/deployment-standards/README.md): live index builds rollout-safe and reproducible.
- [ ] [architecture-schema](../../../../../../standards/architecture-schema/README.md): indexes stay within the owning component's collections.
- [ ] Modeling, replication, backup, security, and ODM/repository code are named handoffs — none implemented here.

## Failure handling

If a check fails:

1. Identify the unjustified index, unmeasured query, or blocking pipeline stage.
2. Ask the user for clarification if the decision cannot be inferred from `performance` or `data-architecture.md`.
3. Revise the index/query/pipeline, re-capture the before/after `explain` and profiler delta.
4. Keep any unresolved gap explicit in `query-optimization.md` — do not hide it as an assumption.
