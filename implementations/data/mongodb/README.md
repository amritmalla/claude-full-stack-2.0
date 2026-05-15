# mongodb

> Status: draft

## Purpose

Implements `architecture/data-architecture` for MongoDB: document modeling, schema validation, index strategy, shard-key choice, read/write concern posture, and zero-downtime evolution.

Architecture decisions (which bounded contexts own which collections, consistency posture, sharding choice, replica topology) come from upstream and are taken as inputs here.

## Ecosystem

- MongoDB 6.0+ (replica set or sharded cluster)
- `$jsonSchema` validators (`validationLevel: strict`, `validationAction: error`)
- mongock, mongo-migrate, or hand-rolled idempotent migration scripts
- Testcontainers (or Docker) for migration dry-runs and index verification

## Compatible patterns

- [modular-monolith](../../../patterns/modular-monolith/README.md)
- [microservices](../../../patterns/microservices/README.md)
- [event-driven](../../../patterns/event-driven/README.md) (change-stream consumers; outbox patterns)
- [cqrs](../../../patterns/cqrs/README.md) (read-model projections)

## Engine family

MongoDB belongs to **Family B — Document** in the data layer model. See [`implementations/data/README.md`](../README.md) for the full archetype set and philosophy.

## Skills

### Authored

- [mongodb-data-model-and-migration](mongodb-data-model-and-migration/SKILL.md) — produces document modeling decisions (embed vs reference), `$jsonSchema` validators, index strategy (compound, multikey, text, geo, TTL, partial), shard-key choice if sharded, read/write concern posture, and zero-downtime migration plans using expand-migrate-contract or dual-write.

### Archetype coverage

| # | Archetype | Skill | Status |
|---|---|---|---|
| 1 | data-model-and-migration | [`mongodb-data-model-and-migration`](mongodb-data-model-and-migration/SKILL.md) | authored |
| 2 | indexing-and-query-optimization | `mongodb-indexing-and-query-optimization` | planned |
| 3 | replication-and-ha-readiness | `mongodb-replication-and-ha-readiness` | planned |
| 4 | backup-and-operational-readiness | `mongodb-backup-and-operational-readiness` | planned |
| 5 | security-and-data-access-hardening | `mongodb-security-and-data-access-hardening` | planned |

### Planned skill scope (future work)

- **`mongodb-indexing-and-query-optimization`** — `explain("executionStats")`-driven query review, index audit (compound, multikey, text, geo, TTL, partial, wildcard), aggregation pipeline cost review, projection and collation posture, shard-key effectiveness analysis, hot-collection identification via the profiler.
- **`mongodb-replication-and-ha-readiness`** — replica-set topology and election behavior, read-preference routing (`primary`, `secondaryPreferred`, `nearest`), write-concern selection (`majority`, `w: N`, `j: true`), arbiter posture, oplog window sizing, change-stream availability, multi-region replica placement.
- **`mongodb-backup-and-operational-readiness`** — backup strategy (`mongodump`, filesystem snapshot, Cloud Manager, Atlas continuous backup), oplog-based PITR, restore drills with documented RPO/RTO, oplog-window and replication-lag observability, runbook inputs for primary loss, oplog rollover, and chunk-balancer issues.
- **`mongodb-security-and-data-access-hardening`** — authentication mechanism (SCRAM, x.509, LDAP, Kerberos), RBAC roles and built-in vs custom grants, field-level redaction posture, client-side field-level encryption (CSFLE) for PII, TLS, IP allowlists, and audit-log configuration.

## Architecture domains implemented

| Architecture domain | How |
|---|---|
| [data-architecture](../../../architecture/data-architecture/README.md) | Document modeling, validation, indexing strategy, shard-key choice, retention rules, consistency posture. |
| [reliability](../../../architecture/reliability/README.md) | Zero-downtime migrations, backup/restore hooks, replica-set posture. |

## Standards this implementation conforms to

- [architecture-schema](../../../standards/architecture-schema/README.md) — data ownership rules: each collection is owned by exactly one component.
- [naming-conventions](../../../standards/naming-conventions/README.md) — `camelCase` field names; plural collection names; named indexes.
- [security-standards](../../../standards/security-standards/README.md) — at-rest encryption, PII tagging, no secrets in migrations.
- [deployment-standards](../../../standards/deployment-standards/README.md) — backwards-compatible migrations gating service deploys (expand → migrate → contract).

## Upstream inputs

- Approved `system-design.md` with bounded contexts and data ownership declared.
- Approved `data-architecture.md` selecting MongoDB and declaring sharding, replica, and consistency posture.
- `backend-architecture.md` for domain ownership, transaction boundaries, and idempotency requirements.

## Downstream consumers

- Backend implementation skills consume validators and indexes; ODM/repository wiring (e.g., Spring Data MongoDB) lives in the backend implementation skill, not here.
- [architecture/quality-engineering](../../../architecture/quality-engineering/) — integration tests run against this data model via Testcontainers.
