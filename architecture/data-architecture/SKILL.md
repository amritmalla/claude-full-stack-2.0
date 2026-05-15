---
name: data-architecture
description: Use when an approved system design exists and the team needs production-grade operational data architecture before engine-specific implementation. Produces data ownership boundaries, engine selection, consistency model, schema strategy, indexing posture, partitioning and sharding rules, replication topology, cache architecture, retention and deletion policy, migration strategy, and operational handoff guidance. Do not use for analytics pipelines, warehouse modeling, stream processing, single-table tweaks, ORM code, or engine-specific DDL; use the relevant implementations/data/<engine> skill instead.
---

# Data Architecture

## When to use

Invoke after `system-design` has identified bounded contexts and data ownership, and before `implementations/data/<engine>` skills generate concrete DDL, migrations, or index definitions.

Do not use for analytics pipelines, warehouse or lakehouse modeling, stream-processing topology, single-table schema tweaks inside an already-defined data model (go directly to the engine-specific implementation skill), persistence-framework or ORM code, or isolated migration scripts.

## Inputs

Required:

- Approved `system-design.md` with bounded contexts and data ownership declared, and the relevant ADRs.
- The data scope in question: a service's primary store, a shared store, a cross-context read model, or a cache tier.
- Primary access patterns: read shape, write shape, hot keys, and transactional groupings.

Optional:

- PRD or system-design sections on volume, growth, SLOs, residency, retention, and compliance regime.
- Existing schemas, ER diagrams, or query logs.
- Vendor or hosting constraints (managed RDS, cloud SQL, self-hosted, on-prem).
- Budget envelope for storage, IOPS, and replication.
- Cross-context consistency expectations from `backend-architecture`.

## Operating rules

- Data ownership is explicit and singular: every dataset has exactly one owning bounded context and one authoritative write path; cross-context access is via API, event, replicated read model, or projection, never ad hoc cross-service joins.
- Choose engines for access patterns, not preference. Justify each engine against query shape, write behavior, consistency need, operational maturity, scaling, and cost; reject organization-default thinking.
- Consistency is a business decision. Every write path declares its consistency guarantee, concurrency model, conflict resolution, and enforcement mechanism. Reject implied or "eventual somehow" consistency.
- Operational realities override theoretical purity. Account for replication lag, failover, hot partitions, backup restoration, migration windows, cache stampedes, and team staffing capacity; call out architecture too operationally expensive for the team.
- Partitioning and sharding are not defaults. Partition or shard only when a measured constraint (throughput, size, tenancy, blast radius, region) demands it; every proposal names the partition key, rebalance strategy, cross-partition behavior, and hotspot mitigation.
- Caching is a contract. Every cache layer names its source of truth, invalidation rule, staleness budget, warmup behavior, and cold-cache failure semantics.
- Retention and deletion are first-class. Every dataset states retention duration, deletion mechanism, archival behavior, legal-hold expectations, and PII handling.
- Migrations are expand / migrate / contract by default. Reject destructive one-step migrations and giant blocking rewrites.
- Challenge weak data architecture directly and concretely: shared databases, entity-service coupling, data-model-driven service boundaries, premature polyglot persistence, unbounded event retention, and transactional RPC chains.
- When a data decision crosses a trust, tenancy, residency, or regulatory boundary, raise an ADR candidate against `system-design`.

## Output contract

`data-architecture.md` MUST conform to [standards/architecture-schema](../../standards/architecture-schema/README.md), which is authoritative for its frontmatter, required and conditional sections, conditional-section omission rules, and linkage back to `system-design.md` and its ADRs.

Security, observability, and operational content additionally conforms to [security-standards](../../standards/security-standards/README.md), [observability-standards](../../standards/observability-standards/README.md), and [deployment-standards](../../standards/deployment-standards/README.md). Skill structure conforms to [documentation-standards](../../standards/documentation-standards/README.md).

Use `assets/data-architecture.template.md` as the scaffold; it implements the schema. No engine-specific DDL, ORM classes, or vendor SDK calls appear in the architecture unless they materially change architecture behavior.

## Progressive references

- Read `references/data-architecture-playbook.md` when inventorying access patterns, selecting engines, defining ownership and consumption boundaries, the consistency and concurrency model, schema strategy, indexing, partitioning posture, replication topology, cache architecture, retention, migration strategy, or operational readiness, and to check the anti-pattern list.
- Read `references/data-architecture-quality-rubric.md` before finalizing and use it as the validation checklist.
- Use `assets/data-architecture.template.md` for `data-architecture.md`.

## Process

Progress:

ADR candidates are drafted inline as decisions are made (steps 3, 5, 8, 9, 11). Step 13 only consolidates them; it does not retrofit ADRs from prose.

- [ ] Step 1: Load `system-design.md` and relevant ADRs. List every component that owns or reads persistent state; record bounded context, owned datasets, consumed datasets, write authority, and cross-context dependencies. Reject ambiguous or shared-write ownership.
- [ ] Step 2: Inventory access patterns per owned dataset: point lookups, range scans, joins, aggregations, search, vector similarity, append-only flows, reporting; plus hot keys, skew, read/write ratio, latency expectations, and transactional groupings. See `references/data-architecture-playbook.md`.
- [ ] Step 3: Choose the engine per dataset (relational, document, key-value, search, time-series, analytical, vector). Justify operational fit, consistency fit, and scaling; explain why alternatives were rejected. Draft an ADR candidate for each non-obvious engine choice.
- [ ] Step 4: Define ownership and consumption boundaries: owning component, authoritative write path, replication consumers, API consumers, projection/read-model strategy, who may mutate vs observe, and how synchronization occurs.
- [ ] Step 5: Define the consistency and concurrency model per write path: consistency expectation, isolation level, conflict handling, optimistic vs pessimistic concurrency, MVCC behavior, lock contention risk, and lost-update prevention. Draft ADR candidates for the consistency model and any async/eventing or saga decision.
- [ ] Step 6: Define schema and data-modeling strategy: normalization posture, aggregate boundaries, tenant isolation, key design (surrogate vs natural), soft-delete policy, referential integrity, and immutable/audit requirements. Reject giant shared aggregates, EAV, and JSON blobs replacing structure.
- [ ] Step 7: Define indexing strategy: per access pattern name the serving index, lookup behavior, write/maintenance cost, and cardinality assumptions. Reject speculative or ORM-sprawl indexes with no named query.
- [ ] Step 8: Determine partitioning and sharding posture. If proposed, define partition key, rebalance strategy, cross-partition query and transaction behavior, hotspot handling, operational tooling, and the measurable constraint that triggered it. Draft an ADR candidate for any sharding decision.
- [ ] Step 9: Define replication and high-availability topology per engine: primary/replica layout, failover model, RTO/RPO, replica lag tolerance, read routing, read-after-write guarantees, and backup strategy (replicas are not backups). Draft an ADR candidate for the HA/replication decision.
- [ ] Step 10: Define cache architecture per layer: cached data, source of truth, invalidation trigger, TTL/staleness budget, cold-cache behavior, stampede protection, and warming. Reject caches without ownership.
- [ ] Step 11: Define retention, deletion, and compliance per dataset: retention period, deletion mechanism (TTL, tombstone, scheduled purge, archival), archival strategy, PII handling, audit, and legal-hold behavior. Draft ADR candidates for retention/deletion decisions with regulatory weight.
- [ ] Step 12: Define migration and evolution strategy: tooling, rollout sequencing, online-migration constraints, dual-write/shadow-read needs, backfill, rollback, and compatibility guarantees. Default to expand/migrate/contract.
- [ ] Step 13: Define operational readiness (backup cadence, restore validation, monitoring signals: replication lag, slow queries, lock waits, deadlocks, cache hit ratio, storage growth, connection pool saturation; runbook hooks). Generate `data-architecture.md` from `assets/data-architecture.template.md`, consolidate ADR candidates, and validate against [standards/architecture-schema](../../standards/architecture-schema/README.md) and `references/data-architecture-quality-rubric.md`; revise until both pass or explicitly note any unresolved gap.

## Outputs

Required:

- `data-architecture.md` at `docs/architecture/<product-slug>/data-architecture.md`, with frontmatter and sections per [standards/architecture-schema](../../standards/architecture-schema/README.md).

Optional, when applicable:

- ER diagram or dataset inventory; access-pattern catalog mapped to indexes.
- Replication topology, partitioning/sharding, or cache topology diagrams.
- Consistency matrix and migration sequencing notes.
- ADR drafts for engine, consistency, partitioning, replication, or retention decisions.

Output rules:

- Keep the architecture decision-oriented and operationally concrete, not vendor-decorative.
- Document tradeoffs and the rejected alternative, not only the chosen path.
- Name datasets and boundaries by domain ownership, not by engine.
- Treat operational burden, backups, and migration safety as part of the design, not a later implementation detail.

## Quality checks

- [ ] `references/data-architecture-quality-rubric.md` was loaded before finalizing.
- [ ] `data-architecture.md` validates against [standards/architecture-schema](../../standards/architecture-schema/README.md): frontmatter complete; required sections present; conditional sections present with content or listed under `## Omitted sections` with rationale.
- [ ] Every owned dataset names its owning component, engine, and primary access patterns.
- [ ] Each engine choice is justified against access patterns and consistency needs, not preference.
- [ ] The consistency model is explicit for every write path, with the enforcing mechanism named.
- [ ] Every index maps to a stated access pattern; no "just in case" indexes survive.
- [ ] Partitioning or sharding, if proposed, names the partition key, rebalance rule, and the measured constraint that triggered it.
- [ ] Replication topology states failover RTO/RPO, replica lag tolerance, and read-after-write rules.
- [ ] Every cache layer names its source of truth, invalidation rule, and staleness budget.
- [ ] Every dataset states retention, deletion mechanism, and PII or legal-hold treatment.
- [ ] Migration approach is expand/migrate/contract or has an ADR justifying an alternative.
- [ ] No engine-specific DDL, ORM classes, or vendor SDK calls appear in the architecture.

## References

- Upstream: [`architecture/system-design`](../system-design/SKILL.md).
- Downstream implementation skills: `implementations/data/postgres`, `implementations/data/mongodb`, `implementations/data/redis`, `implementations/data/elasticsearch`, `implementations/data/clickhouse`.
- Related architecture skills: [`backend-architecture`](../backend-architecture/SKILL.md), [`ai-native-engineering`](../ai-native-engineering/SKILL.md) (retrieval corpora ownership), [`security`](../security/SKILL.md), [`reliability`](../reliability/SKILL.md), [`operations`](../operations/SKILL.md).
