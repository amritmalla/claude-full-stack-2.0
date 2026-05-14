---
name: data-architecture
description: Use when an approved system design exists and the team needs operational data layer architecture before schema implementation. Produces database engine selection, data ownership boundaries, consistency model, schema and indexing strategy, partitioning and sharding posture, replication and high-availability topology, cache strategy, retention and deletion rules, migration approach, and implementation handoff notes. Do not use for analytics pipelines, warehouse modeling, stream processing, single-table tweaks, or engine-specific DDL; use the relevant implementations/data/<engine> skill for DDL.
---

# Data Architecture

## When to use

Invoke after `system-design` has identified bounded contexts and data ownership, and before `implementations/data/<engine>` skills generate concrete DDL, migrations, or index definitions.

Do not use for analytics pipelines, warehouse or lakehouse modeling, stream processing topology (out of scope for this repo today), single-table schema tweaks inside an already-defined data model (go directly to the engine-specific implementation skill), or persistence-framework code (use the relevant backend implementation skill).

## Inputs

Required:

- Approved `system-design.md` with bounded contexts and data ownership declared.
- The data scope in question: a service's primary store, a shared store, a cross-context read model, or a cache tier.
- Primary access patterns: read shape, write shape, hot keys, and transactional groupings.

Optional:

- PRD or system-design sections on volume, growth, SLOs, residency, retention, and compliance regime.
- Existing schemas, ER diagrams, or query logs.
- Vendor or hosting constraints (managed RDS, cloud SQL, self-hosted, on-prem).
- Budget envelope for storage, IOPS, and replication.
- Cross-context consistency expectations from `backend-architecture`.

## Operating rules

- Data ownership is per bounded context. Each table or collection is owned by exactly one component; cross-context access is via API or replicated read model, not direct queries.
- Choose the engine for the access pattern, not the org's preference. Relational, document, key-value, search, and analytical engines have non-overlapping sweet spots.
- Decide the consistency model explicitly per write path: strong, read-your-writes, eventual, or causally consistent. Name the mechanism that enforces it.
- Index for stated access patterns only. Every index has a query it serves, a write cost, and a maintenance owner.
- Partition or shard only when a measured constraint (size, throughput, blast radius, tenancy) demands it. Document the partition key, rebalancing strategy, and cross-partition query behavior.
- Replication topology serves availability and read scaling; it is not a backup. State failover behavior, replica lag tolerance, and read-after-write rules per consumer.
- Caching is a contract, not a hack. Each cache layer names its source of truth, invalidation rule, staleness budget, and what breaks if it goes cold.
- Retention and deletion are first-class. Every dataset states a retention period, a deletion mechanism, and any legal hold or audit constraint.
- Migrations are expand / migrate / contract by default. Do not propose destructive migrations behind a single deploy.
- When a data decision crosses a trust, tenancy, residency, or regulatory boundary, raise an ADR candidate against `system-design`.

## Process

1. Load `system-design.md` and list every component that owns or reads persistent state. Record the bounded context, the data it owns, and the systems it reads from.
2. Inventory access patterns per owned dataset: read shapes (point lookups, range scans, joins, full-text, vector), write shapes (single-row, batch, append-only), transactional groupings, and hot-key risks.
3. Choose the engine per dataset. Justify against access patterns, consistency needs, volume, and operational maturity. Reject engines whose sweet spot does not match.
4. Define data ownership boundaries: per dataset, name the owning component, the allowed write path, and the consumption mechanism for other contexts (API, event, replicated read model).
5. Define the consistency and concurrency model per write path: isolation level, locking or MVCC behavior, optimistic vs pessimistic concurrency, and how lost-update and write-skew are prevented.
6. Define the schema strategy: normalization posture, key design (natural vs surrogate), referential integrity rules, soft-delete vs hard-delete policy, and tenant isolation pattern if multi-tenant.
7. Define indexing strategy: per access pattern, name the index that serves it, its write cost, and any covered-query expectations. Flag indexes whose only justification is "just in case."
8. Define partitioning and sharding posture per dataset: partition key, rebalancing approach, cross-partition query and transaction rules, and the throughput or size signal that triggered it.
9. Define replication and high-availability topology per engine: primary-replica layout, failover RTO/RPO, replica lag tolerance, and which reads are allowed against replicas.
10. Define cache strategy: which layers cache what (in-process, distributed, CDN, materialized read model), source of truth, invalidation trigger, staleness budget, and stampede protection.
11. Define retention and deletion: per dataset, retention period, deletion mechanism (TTL, scheduled job, tombstone), audit and legal-hold behavior, and PII-specific handling.
12. Define migration approach: tooling, expand-migrate-contract phasing rules, online-migration constraints, backfill strategy, and rollback plan.
13. Define operational concerns: backup cadence and restore drills, monitoring signals (replication lag, query latency, lock waits, cache hit ratio), and runbook hooks.
14. Produce `data-architecture.md` with explicit handoffs to `implementations/data/<engine>`, `backend-architecture`, `security`, `reliability`, and `operations`.

## Outputs

Required:

- `data-architecture.md` covering engine selection, ownership boundaries, consistency model, schema strategy, indexing strategy, partitioning posture, replication topology, cache strategy, retention rules, migration approach, and handoff notes.

Optional, when applicable:

- ER diagram or dataset inventory.
- Access-pattern catalog mapped to indexes.
- Partition or sharding plan.
- Replication topology diagram.
- Cache topology and invalidation rules.
- ADR drafts for engine, consistency, partitioning, or replication decisions.

## Quality checks

- [ ] Every owned dataset names its owning component, engine, and primary access patterns.
- [ ] Each engine choice is justified against access patterns and consistency needs, not preference.
- [ ] The consistency model is explicit for every write path, with the enforcing mechanism named.
- [ ] Every index maps to a stated access pattern; no "just in case" indexes survive.
- [ ] Partitioning or sharding, if proposed, names the partition key, rebalancing rule, and the measured constraint that triggered it.
- [ ] Replication topology states failover RTO/RPO, replica lag tolerance, and read-after-write rules.
- [ ] Every cache layer names its source of truth, invalidation rule, and staleness budget.
- [ ] Every dataset states retention, deletion mechanism, and PII or legal-hold treatment.
- [ ] Migration approach is expand-migrate-contract or has an ADR justifying an alternative.
- [ ] No engine-specific DDL, ORM classes, or vendor SDK calls appear in the architecture.

## References

- Upstream: [`architecture/system-design`](../system-design/SKILL.md).
- Downstream implementation skills: `implementations/data/postgres`, `implementations/data/mongodb`, `implementations/data/redis`, `implementations/data/elasticsearch`, `implementations/data/clickhouse`.
- Related architecture skills: [`backend-architecture`](../backend-architecture/SKILL.md), `ai-native-engineering` (for retrieval corpora ownership), `security`, `reliability`, `operations`.
