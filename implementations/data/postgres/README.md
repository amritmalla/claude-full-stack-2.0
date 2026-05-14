# postgres

> Status: draft

## Purpose

Implements `capabilities/data-systems` for PostgreSQL: schema design, integrity constraints, indexing strategy, migrations (Flyway / Liquibase), and zero-downtime evolution.

Capability decisions (which bounded contexts own which data, consistency model, retention strategy) come from upstream and are taken as inputs here.

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

## Skills

- [postgres-schema-and-migration](postgres-schema-and-migration/SKILL.md) — produces normalized schema, integrity constraints, indexing strategy, Flyway migrations, and zero-downtime migration plans using expand / migrate / contract.

## Capabilities implemented

| Capability | How |
|---|---|
| [data-systems](../../../capabilities/data-systems/README.md) | Schema definition, migration plans, index strategy, retention rules. |
| [reliability](../../../capabilities/reliability/README.md) | Zero-downtime migrations, backup/recovery hooks. |

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
- [capabilities/testing-quality](../../../capabilities/testing-quality/) — integration tests run against this schema via Testcontainers.
