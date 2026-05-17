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

- [modular-monolith](../../../architecture-patterns/modular-monolith/README.md)
- [microservices](../../../architecture-patterns/microservices/README.md)
- [event-driven](../../../architecture-patterns/event-driven/README.md) (outbox tables live here)
- [cqrs](../../../architecture-patterns/cqrs/README.md) (read-model projections)

## Engine family

PostgreSQL belongs to **Family A — OLTP relational** in the data layer model. See [`implementations/data/README.md`](../README.md) for the full archetype set and philosophy.

## Skills

### Authored

- [postgres-schema-and-migration](postgres-schema-and-migration/SKILL.md) — produces normalized schema, integrity constraints, indexing strategy, Flyway migrations, and zero-downtime migration plans using expand / migrate / contract.
- [postgres-indexing-and-query-optimization](postgres-indexing-and-query-optimization/SKILL.md) — index audit, `EXPLAIN (ANALYZE, BUFFERS)`-driven query review, `pg_stat_statements` hot-query identification, partitioning validation, N+1 and join-order remediation, autovacuum and bloat posture.
- [postgres-replication-and-ha-readiness](postgres-replication-and-ha-readiness/SKILL.md) — streaming/logical replication topology, sync vs async RPO trade-off, automated failover (Patroni/repmgr/Multi-AZ), replica-lag thresholds, read-replica routing, split-brain prevention, multi-region posture.
- [postgres-backup-and-operational-readiness](postgres-backup-and-operational-readiness/SKILL.md) — backup strategy (pgBackRest/WAL archiving for PITR), rehearsed restore drills with measured RPO/RTO, retention and cost posture, day-2 observability (bloat, wraparound, connection saturation), and runbook inputs.
- [postgres-security-and-data-access-hardening](postgres-security-and-data-access-hardening/SKILL.md) — TLS and connection security, least-privilege role/grant model, RLS tenant isolation, column grants and encryption for PII, `pgaudit` configuration, secret rotation posture, and network-exposure review.

### Archetype coverage

| # | Archetype | Skill | Status |
|---|---|---|---|
| 1 | schema-modeling-and-migration | [`postgres-schema-and-migration`](postgres-schema-and-migration/SKILL.md) | authored |
| 2 | indexing-and-query-optimization | [`postgres-indexing-and-query-optimization`](postgres-indexing-and-query-optimization/SKILL.md) | authored |
| 3 | replication-and-ha-readiness | [`postgres-replication-and-ha-readiness`](postgres-replication-and-ha-readiness/SKILL.md) | authored |
| 4 | backup-and-operational-readiness | [`postgres-backup-and-operational-readiness`](postgres-backup-and-operational-readiness/SKILL.md) | authored |
| 5 | security-and-data-access-hardening | [`postgres-security-and-data-access-hardening`](postgres-security-and-data-access-hardening/SKILL.md) | authored |

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
