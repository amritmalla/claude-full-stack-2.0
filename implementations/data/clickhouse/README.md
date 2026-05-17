# clickhouse

> Status: scaffold.

## Purpose

Implements `architecture/data-architecture` for ClickHouse as an analytical / columnar store: table engine and partitioning, query and materialization review, replication and sharding topology, backup posture, and access hardening.

Architecture decisions (which workloads use ClickHouse, ingestion path, partition strategy, retention, tenant isolation) come from upstream and are taken as inputs here.

## Engine family

ClickHouse belongs to **Family E — Columnar / OLAP** in the data layer model. See [`implementations/data/README.md`](../README.md) for the full archetype set and philosophy.

## Ecosystem (target)

- ClickHouse 24.x+ (self-hosted, ClickHouse Cloud, or managed equivalent)
- MergeTree family engines (`MergeTree`, `Replicated*`, `ReplacingMergeTree`, `SummingMergeTree`, `AggregatingMergeTree`, `CollapsingMergeTree`)
- ZooKeeper or ClickHouse Keeper for replicated tables
- `clickhouse-backup` (or equivalent) for backup/restore
- Materialized views and projections for query acceleration
- Distributed engine for sharded reads/writes

## Compatible patterns

- [event-driven](../../../architecture-patterns/event-driven/README.md) (event-stream ingest)
- [cqrs](../../../architecture-patterns/cqrs/README.md) (analytical read side)
- [microservices](../../../architecture-patterns/microservices/README.md) (per-domain analytical stores)

## Skills

### Authored

_None._

### Archetype coverage

| # | Archetype | Skill | Status |
|---|---|---|---|
| 1 | table-engine-and-partitioning | `clickhouse-table-engine-and-partitioning` | planned |
| 2 | query-and-materialization-review | `clickhouse-query-and-materialization-review` | planned |
| 3 | replication-and-sharding-topology | `clickhouse-replication-and-sharding-topology` | planned |
| 4 | backup-and-operational-readiness | `clickhouse-backup-and-operational-readiness` | planned |
| 5 | security-and-data-access-hardening | `clickhouse-security-and-data-access-hardening` | planned |

### Planned skill scope (future work)

- **`clickhouse-table-engine-and-partitioning`** — MergeTree-family engine choice tied to read/write shape (plain, `Replacing`, `Summing`, `Aggregating`, `Collapsing`, `VersionedCollapsing`), partition key sized for monthly/daily granularity at the table's scale, `ORDER BY` and `PRIMARY KEY` selection driven by predicate shape, TTL with `DELETE`/`TO DISK`/`TO VOLUME` actions, codec selection (`ZSTD`, `LZ4`, `Delta`, `DoubleDelta`, `Gorilla`), projections, schema-evolution posture.
- **`clickhouse-query-and-materialization-review`** — query pattern review against `system.query_log`, materialized-view selection (incremental aggregation), projection design, skip-indexes (`minmax`, `set`, `bloom_filter`, `ngrambf_v1`), JOIN posture (`ANY` vs `ALL`, `GLOBAL` vs local, dictionaries for star joins), distributed query planning, query-cost observability via `query_log` and `query_thread_log`.
- **`clickhouse-replication-and-sharding-topology`** — `ReplicatedMergeTree` configuration, Distributed engine wiring, ZooKeeper or ClickHouse Keeper posture (cluster size, latency), shard and replica placement, replication-lag observability, multi-region posture, cross-replica consistency expectations.
- **`clickhouse-backup-and-operational-readiness`** — `clickhouse-backup` configuration, `ALTER TABLE ... FREEZE` for atomic part snapshots, restore drills with documented RPO/RTO, observability for parts count, merge lag, mutations queue, ZooKeeper health, runbook inputs (parts explosion, mutation stalls, replica resync, broken distributed DDL).
- **`clickhouse-security-and-data-access-hardening`** — TLS configuration, role and grant model, row policies for tenant isolation, column-level grants for PII, quotas and settings profiles to bound resource use, audit-log configuration, dictionary-source security, network exposure review.

## Architecture domains implemented

| Architecture domain | How |
|---|---|
| [data-architecture](../../../architecture/data-architecture/README.md) | Engine choice, partitioning, ordering, retention via TTL. |
| [reliability](../../../architecture/reliability/README.md) | Replication topology, Keeper/ZooKeeper posture, backup/restore. |
| [performance](../../../architecture/performance/README.md) | Materialized views, projections, skip-indexes, JOIN posture. |
| [security](../../../architecture/security/README.md) | Roles, row policies, column grants, quotas, audit. |

## Standards this implementation conforms to

- [architecture-schema](../../../standards/architecture-schema/README.md) — table ownership: each table is owned by exactly one component.
- [naming-conventions](../../../standards/naming-conventions/README.md) — `snake_case` table and column names; `_local`/`_distributed` suffix discipline for sharded setups.
- [security-standards](../../../standards/security-standards/README.md) — TLS, row policies for tenant isolation, column grants for PII, audit posture.
- [observability-standards](../../../standards/observability-standards/README.md) — query latency, parts count, merge lag, mutation queue, replication lag, Keeper health exposed.

## Upstream inputs

- Approved `data-architecture.md` selecting ClickHouse for analytical workloads and declaring partitioning strategy, retention, replication, and tenant-isolation posture.
- `backend-architecture.md` (or stream/ingestion-path architecture) for ingestion semantics, idempotency posture, and write-batch shape.
