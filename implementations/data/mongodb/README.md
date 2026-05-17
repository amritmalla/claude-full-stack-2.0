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

- [modular-monolith](../../../architecture-patterns/modular-monolith/README.md)
- [microservices](../../../architecture-patterns/microservices/README.md)
- [event-driven](../../../architecture-patterns/event-driven/README.md) (change-stream consumers; outbox patterns)
- [cqrs](../../../architecture-patterns/cqrs/README.md) (read-model projections)

## Engine family

MongoDB belongs to **Family B — Document** in the data layer model. See [`implementations/data/README.md`](../README.md) for the full archetype set and philosophy.

## Skills

### Skill tier

The four archetype-scoped skills (2–5) are authored at **mature tier** — each is a directory of `SKILL.md` + `references/<name>-playbook.md` + `references/<name>-quality-rubric.md` + `assets/<name>.template.md`, following the `implementations/mobile/flutter` mature-tier exemplar. This is a **deliberate divergence** from the mostly-lean single-file convention used elsewhere in the data tier (the postgres archetypes 2–5 are lean; only `postgres-schema-and-migration` is mature). The mongodb stack is therefore mixed-tier by design: `mongodb-data-model-and-migration` is lean; the indexing/replication/backup/security successors are mature.

### Authored

- [mongodb-data-model-and-migration](mongodb-data-model-and-migration/SKILL.md) — *archetype 1, lean*. Document modeling (embed vs reference), `$jsonSchema` validators, index strategy, shard-key choice, read/write concern posture, zero-downtime migrations (expand-migrate-contract / dual-write).
- [mongodb-indexing-and-query-optimization](mongodb-indexing-and-query-optimization/SKILL.md) — *archetype 2, mature*. `explain("executionStats")`-driven review, index audit, ESR, aggregation cost review, collation/projection posture, shard-key effectiveness — tunes the engine, hands model changes back to archetype 1.
- [mongodb-replication-and-ha-readiness](mongodb-replication-and-ha-readiness/SKILL.md) — *archetype 3, mature*. Member topology and elections, concern survivability, read-preference routing, oplog-window sizing, change-stream availability, multi-region placement, rehearsed failover.
- [mongodb-backup-and-operational-readiness](mongodb-backup-and-operational-readiness/SKILL.md) — *archetype 4, mature*. Backup mechanism, oplog-based PITR, a **rehearsed** restore drill with measured RPO/RTO, oplog/lag/backup-age observability, concrete runbook inputs.
- [mongodb-security-and-data-access-hardening](mongodb-security-and-data-access-hardening/SKILL.md) — *archetype 5, mature*. Auth mechanism, least-privilege RBAC, TLS, CSFLE for classification-marked PII, role-scoped redaction, network exposure, audit logging, negative-tested.

### Archetype coverage

| # | Archetype | Skill | Status |
|---|---|---|---|
| 1 | data-model-and-migration | [`mongodb-data-model-and-migration`](mongodb-data-model-and-migration/SKILL.md) *(lean)* | ✓ authored |
| 2 | indexing-and-query-optimization | [`mongodb-indexing-and-query-optimization`](mongodb-indexing-and-query-optimization/SKILL.md) *(mature)* | ✓ authored |
| 3 | replication-and-ha-readiness | [`mongodb-replication-and-ha-readiness`](mongodb-replication-and-ha-readiness/SKILL.md) *(mature)* | ✓ authored |
| 4 | backup-and-operational-readiness | [`mongodb-backup-and-operational-readiness`](mongodb-backup-and-operational-readiness/SKILL.md) *(mature)* | ✓ authored |
| 5 | security-and-data-access-hardening | [`mongodb-security-and-data-access-hardening`](mongodb-security-and-data-access-hardening/SKILL.md) *(mature)* | ✓ authored |

All five Family B archetypes are authored. Cross-archetype handoffs are named in each skill; ODM/repository code remains the backend implementation skill's ownership.

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
