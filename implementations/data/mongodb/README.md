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

## Skills

- [mongodb-data-model-and-migration](mongodb-data-model-and-migration/SKILL.md) — produces document modeling decisions (embed vs reference), `$jsonSchema` validators, index strategy (compound, multikey, text, geo, TTL, partial), shard-key choice if sharded, read/write concern posture, and zero-downtime migration plans using expand-migrate-contract or dual-write.

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
