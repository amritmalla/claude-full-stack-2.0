# postgres

> Status: draft

## Purpose

Implements `architecture/data-architecture` for PostgreSQL: schema design, integrity constraints, indexing strategy, migrations (Flyway / Liquibase), and zero-downtime evolution.

Architecture decisions (which bounded contexts own which data, consistency model, retention strategy) come from upstream and are taken as inputs here.

## Ecosystem

- PostgreSQL 14+
- Flyway (default) or Liquibase
- Testcontainers for migration verification
- `pg_dump` / logical replication for migration rehearsals

## Compatible patterns

- [modular-monolith](../../../patterns/modular-monolith/README.md)
- [microservices](../../../patterns/microservices/README.md)
- [event-driven](../../../patterns/event-driven/README.md) (outbox tables live here)
- [cqrs](../../../patterns/cqrs/README.md) (read-model projections)

## Engine family

PostgreSQL belongs to **Family A — OLTP relational** in the data layer model. See [`implementations/data/README.md`](../README.md) for the full archetype set and philosophy.

## Skills

### Authored

- [postgres-schema-and-migration](postgres-schema-and-migration/SKILL.md) — produces normalized schema, integrity constraints, indexing strategy, Flyway migrations, and zero-downtime migration plans using expand / migrate / contract.

### Archetype coverage

| # | Archetype | Skill | Status |
|---|---|---|---|
| 1 | schema-modeling-and-migration | [`postgres-schema-and-migration`](postgres-schema-and-migration/SKILL.md) | authored |
| 2 | indexing-and-query-optimization | `postgres-indexing-and-query-optimization` | planned |
| 3 | replication-and-ha-readiness | `postgres-replication-and-ha-readiness` | planned |
| 4 | backup-and-operational-readiness | `postgres-backup-and-operational-readiness` | planned |
| 5 | security-and-data-access-hardening | `postgres-security-and-data-access-hardening` | planned |

### Planned skill scope (future work)

- **`postgres-indexing-and-query-optimization`** — index audit (B-tree, hash, GIN, GiST, BRIN, partial, expression, covering), `EXPLAIN (ANALYZE, BUFFERS)`-driven query review, `pg_stat_statements` hot-query identification, partitioning validation (range/list/hash), N+1 and join-order remediation, autovacuum and bloat posture.
- **`postgres-replication-and-ha-readiness`** — streaming and logical replication topology, synchronous vs asynchronous trade-offs, replica lag monitoring, Patroni or RDS Multi-AZ failover behavior, read-replica routing strategy, split-brain prevention, multi-region posture.
- **`postgres-backup-and-operational-readiness`** — `pg_basebackup` and WAL archiving for PITR, restore drills with documented RPO/RTO, retention/cost posture, observability for replication lag, storage health, and connection saturation; runbook inputs for failover, vacuum-freeze emergencies, and connection exhaustion.
- **`postgres-security-and-data-access-hardening`** — TLS configuration, role and grant model, row-level security policies for tenant isolation, column-level grants for PII, `pgcrypto` and TDE posture, `pgaudit` configuration, secret rotation, and network exposure review.

## Architecture domains implemented

| Architecture domain | How |
|---|---|
| [data-architecture](../../../architecture/data-architecture/README.md) | Schema definition, migration plans, index strategy, retention rules. |
| [reliability](../../../architecture/reliability/README.md) | Zero-downtime migrations, backup/recovery hooks. |

## Standards this implementation conforms to

- [architecture-schema](../../../standards/architecture-schema/README.md) — data ownership rules: each table is owned by exactly one component.
- [naming-conventions](../../../standards/naming-conventions/README.md) — `snake_case` plural tables, singular columns.
- [security-standards](../../../standards/security-standards/README.md) — at-rest encryption, PII tagging, no secrets in migrations.
- [deployment-standards](../../../standards/deployment-standards/README.md) — backwards-compatible migrations gating service deploys (expand → migrate → contract).

## Upstream inputs

- Approved `system-design.md` with bounded contexts and data ownership declared.
- Where relevant, `openapi.yaml` for idempotency / concurrency requirements that shape constraints.

## Downstream consumers

- [implementations/backend/spring-boot](../../backend/spring-boot/) — Flyway migrations land in the scaffold's `db/migration/` directory.
- [architecture/quality-engineering](../../../architecture/quality-engineering/) — integration tests run against this schema via Testcontainers.
