# implementations/data

Technology-specific execution skills for data.

## Philosophy

Each data implementation skill speaks as a **senior DBA / data engineer** in a specific engine. It implements, hardens, or reviews — it does not invent architectural decisions. Architecture artifacts produced by `architecture/data-architecture`, `architecture/reliability`, `architecture/performance`, and `architecture/security` are the source of truth; the implementation skill consumes them and emits schemas, document models, index plans, replication topologies, backup/restore procedures, and access controls.

If an artifact is silent on a needed decision (engine choice, shard or partition key, consistency posture, RPO/RTO, PII classification), the implementation skill **pauses and raises an ADR candidate** against the upstream domain rather than guessing.

Skills are scoped, not monolithic. Each `SKILL.md`:

- declares its upstream architecture domain(s) and the standards it conforms to,
- requires the upstream artifact when generating new schema, indexes, replication topology, or access policy, and runs standalone for review or hardening when the artifact does not yet exist,
- maps to exactly one archetype from its **engine family** (below),
- emits concrete DDL, validators, migration scripts, index definitions, replication and backup configuration, and access policies — not prose-only deliverables.

## Engine families

Unlike the backend layer (one archetype set across all stacks), the data layer defines **five engine families**, each with its own five archetypes tuned to the engine's data model and operational profile. Stacks belong to exactly one family.

| Family | Engine model | Stacks |
|---|---|---|
| A | OLTP relational | [postgres](postgres/) |
| B | Document | [mongodb](mongodb/) |
| C | Cache / KV | [redis](redis/) |
| D | Search | [elasticsearch](elasticsearch/) |
| E | Columnar / OLAP | [clickhouse](clickhouse/) |

### Family A — OLTP relational

| # | Archetype | What the skill produces | Primary upstream |
|---|---|---|---|
| 1 | **schema-modeling-and-migration** | Normalized schema, integrity constraints, indexing strategy, retention rules, zero-downtime migrations (expand → migrate → contract). | `data-architecture` + `backend-architecture` (ownership) |
| 2 | **indexing-and-query-optimization** | Index audit, EXPLAIN/ANALYZE-driven query review, hot-query identification, partitioning validation, N+1 and slow-query remediation. | `performance` + `data-architecture` |
| 3 | **replication-and-ha-readiness** | Streaming/logical replication topology, failover behavior, read-replica routing, sync vs async posture, split-brain prevention, multi-region posture. | `reliability` + `data-architecture` |
| 4 | **backup-and-operational-readiness** | Backup strategy (full/incremental, PITR), restore drills, RPO/RTO validation, replication-lag and storage-health observability, runbook inputs. | `operations` + `reliability` |
| 5 | **security-and-data-access-hardening** | At-rest and in-transit encryption, role and grant model, row/column security, tenant isolation, secret handling, PII classification enforcement, audit logging. | `security` + `data-architecture` |

### Family B — Document

| # | Archetype | What the skill produces | Primary upstream |
|---|---|---|---|
| 1 | **data-model-and-migration** | Embed-vs-reference decisions, `$jsonSchema` validators, index strategy (compound/multikey/text/geo/TTL/partial), shard-key choice, read/write concern posture, zero-downtime migrations (expand-migrate-contract or dual-write). | `data-architecture` + `backend-architecture` |
| 2 | **indexing-and-query-optimization** | Query and aggregation pipeline review, index audit via `explain()`, hot-query identification, collation and projection posture, shard-key effectiveness review. | `performance` + `data-architecture` |
| 3 | **replication-and-ha-readiness** | Replica-set topology, election behavior, read-preference routing, write-concern posture, multi-region replica placement, change-stream availability. | `reliability` + `data-architecture` |
| 4 | **backup-and-operational-readiness** | Backup strategy (mongodump / filesystem snapshot / Cloud Manager / Atlas), oplog-based PITR, restore drills, oplog window monitoring, storage-health observability. | `operations` + `reliability` |
| 5 | **security-and-data-access-hardening** | Authentication mechanism, RBAC roles and grants, field-level redaction posture, client-side field-level encryption, TLS, audit-log configuration. | `security` + `data-architecture` |

### Family C — Cache / KV

| # | Archetype | What the skill produces | Primary upstream |
|---|---|---|---|
| 1 | **key-design-and-data-structure** | Key naming convention, TTL strategy, eviction policy (`maxmemory-policy`), data-structure choice (string/hash/list/set/sorted-set/stream/bitmap/hyperloglog/geo), memory budgeting per namespace. | `data-architecture` + `backend-architecture` |
| 2 | **caching-pattern-implementation** | Cache-aside / write-through / write-behind / refresh-ahead implementation, stampede protection (single-flight, jittered TTL), invalidation rules, negative caching, consistency trade-offs. | `performance` + `backend-architecture` |
| 3 | **replication-and-ha-readiness** | Sentinel vs Cluster topology, failover behavior, replica read posture, slot rebalancing strategy, split-brain prevention. | `reliability` + `data-architecture` |
| 4 | **backup-and-operational-readiness** | RDB and AOF posture, persistence trade-offs, restore drills, latency and memory observability, runbook inputs (FLUSHALL guards, BIG-KEY remediation). | `operations` + `reliability` |
| 5 | **security-and-data-access-hardening** | ACL model, TLS, command renaming/disabling, network exposure review, no-PII discipline for cached payloads, retention posture. | `security` + `data-architecture` |

### Family D — Search

| # | Archetype | What the skill produces | Primary upstream |
|---|---|---|---|
| 1 | **index-mapping-and-analyzer-design** | Mapping definitions, dynamic-mapping posture, analyzer/tokenizer/filter selection, field-data discipline, multi-field strategy, runtime fields, alias and template strategy. | `data-architecture` + `backend-architecture` |
| 2 | **query-and-relevance-tuning** | Query DSL review, scoring and relevance tuning, profile-driven optimization, aggregation cost review, search-template and query-rewrite posture. | `performance` + `data-architecture` |
| 3 | **cluster-and-shard-topology** | Primary/replica shard sizing, ILM policy, rollover strategy, hot-warm-cold tiering, shard-allocation awareness, cross-cluster replication where relevant. | `reliability` + `data-architecture` |
| 4 | **backup-and-operational-readiness** | Snapshot repository config, snapshot schedule and retention, restore drills, cluster-health and shard-allocation observability, runbook inputs. | `operations` + `reliability` |
| 5 | **security-and-data-access-hardening** | Role-based access, document-level security, field-level security, TLS and node-to-node encryption, audit logging, API-key model. | `security` + `data-architecture` |

### Family E — Columnar / OLAP

| # | Archetype | What the skill produces | Primary upstream |
|---|---|---|---|
| 1 | **table-engine-and-partitioning** | MergeTree-family engine choice, partition key, order key, primary key, TTL, projections, codec selection, schema evolution posture. | `data-architecture` + `backend-architecture` |
| 2 | **query-and-materialization-review** | Query pattern review, materialized views, projections, skip-indexes, JOIN posture, distributed query planning, query-cost observability. | `performance` + `data-architecture` |
| 3 | **replication-and-sharding-topology** | ReplicatedMergeTree configuration, Distributed engine wiring, ZooKeeper/Keeper posture, shard and replica placement, multi-region posture. | `reliability` + `data-architecture` |
| 4 | **backup-and-operational-readiness** | `clickhouse-backup` configuration, freeze/restore drills, merges and mutations posture, parts-count and merge-lag observability, runbook inputs. | `operations` + `reliability` |
| 5 | **security-and-data-access-hardening** | Row policies, column-level grants, quotas, TLS, audit logging, settings profiles, network exposure review. | `security` + `data-architecture` |

## Stacks

### Implemented

| Stack | Family | Archetype coverage |
|---|---|---|
| [postgres](postgres/) | A — OLTP relational | 5/5 (all archetypes authored) |
| [mongodb](mongodb/) | B — Document | 5/5 (archetype 1 lean; archetypes 2–5 at mature tier) |

### Planned (future scope)

| Stack | Family | Status |
|---|---|---|
| [redis](redis/) | C — Cache / KV | 0/5 |
| [elasticsearch](elasticsearch/) | D — Search | 0/5 |
| [clickhouse](clickhouse/) | E — Columnar / OLAP | 0/5 |

Per-stack READMEs enumerate the proposed skill list and current authoring status.

## Decided design constraints

These constraints are locked for all current and future data implementation skills:

- **Engine-family archetypes are normative, not advisory.** A skill that belongs to a family but does not fit any of its five archetypes is a signal that the family taxonomy is wrong — escalate before authoring outside the model.
- **One skill per archetype per stack.** No archetype-spanning omnibus skills. No archetype-split per sub-engine (e.g., one `replication-and-ha-readiness` skill per stack covers all topologies that engine supports).
- **Per-skill upstream linkage.** Every `SKILL.md` names its upstream architecture domain(s) and conformance standards directly.
- **Migrations are zero-downtime by default.** The expand → migrate → contract discipline (or its engine-specific equivalent) is the floor, not the ceiling. Single-step destructive migrations require an ADR.
- **Backup and restore are paired.** A backup procedure without a documented and rehearsed restore is not done.
- **PII classification is enforced at the engine.** Where the engine supports column-level grants, row policies, document-level security, or field-level encryption, the security archetype uses it. "Application enforces it" is not acceptable for tier-0 data.

## Standards every data implementation skill conforms to

- [architecture-schema](../../../standards/architecture-schema/README.md) — data ownership: each table/collection/index/key-namespace is owned by exactly one component.
- [naming-conventions](../../../standards/naming-conventions/README.md) — engine-idiomatic naming (snake_case for relational; camelCase for document; namespaced keys for KV).
- [security-standards](../../../standards/security-standards/README.md) — at-rest encryption, PII tagging, no secrets in migrations, audit posture.
- [deployment-standards](../../../standards/deployment-standards/README.md) — backwards-compatible migrations gating service deploys.
- [observability-standards](../../../standards/observability-standards/README.md) — replication lag, storage health, query latency, and access-audit signals exposed.
