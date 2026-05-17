---
name: mongodb-data-model-and-migration
description: Use when designing, reviewing, or evolving a MongoDB data model for a production system. Produces collection and document modeling decisions (embed vs reference), `$jsonSchema` validators, index strategy (compound, multikey, text, geo, TTL, partial), shard key choice and partitioning posture if sharded, read and write concern selection, document-shape evolution migrations using expand-migrate-contract or dual-write, and operational notes for online schema changes. Do not use for relational schemas, analytics warehouses, graph stores, ORM-only modeling discussions, or Mongo change-stream event integration. Sits downstream of system-design (bounded contexts) and data-architecture (ownership, consistency posture, sharding decision); pairs with backend-architecture (domain ownership, transaction boundaries) and the relevant backend implementation skill (ODM wiring, repository code).
---

# MongoDB Data Model and Migration

## When to use

Invoke when designing a new MongoDB data model, introducing a service persistence layer on MongoDB, evolving an existing document shape, reviewing index strategy, choosing or revising a shard key, or planning a production data migration.

Do not use for relational schemas (use `postgres-schema-and-migration`), analytics warehouses, graph databases, ORM- or ODM-only modeling discussions, or Mongo-as-event-source (change streams) integration.

## Inputs

Required:

- Domain entities, relationships, and ownership boundaries from `system-design.md` and (if available) `backend-architecture.md`.
- Primary access patterns: read shapes, write shapes, hot keys, and transactional groupings.
- Approved `data-architecture.md` decisions on consistency posture, sharding, and replica topology.

Optional:

- Existing collections, validators, indexes, or migration scripts.
- Collection sizes, document size distribution, write rates, and query SLOs.
- Retention, audit, compliance, or deletion requirements (drives TTL indexes and soft-vs-hard-delete posture).
- Multi-tenant model (drives shard key or partition key choice).
- MongoDB topology: standalone, replica set, or sharded cluster; version; managed (Atlas) vs self-hosted.
- Operational constraints: lock tolerance, maintenance windows, rollback expectations.

## Operating rules

- Production safety beats convenience. Optimize for uptime, lock minimization, rollback safety, and predictable replica-set behavior.
- Respect bounded contexts. Each context owns its collections; cross-context access happens through defined interfaces, not shared writes.
- Model the read first. Document shape follows the dominant access pattern; embed when read together and bounded in size, reference when reused or unbounded.
- Document size is a contract, not a suggestion. Embeds that can grow unboundedly become a defect at scale.
- Schema is enforced. Every collection has a `$jsonSchema` validator with `validationLevel: strict` and `validationAction: error` for new collections; `warn` only during a documented evolution window.
- Access patterns drive indexing. Every index names the query pattern it serves, cardinality expectation, and write-impact note. Compound index order follows the ESR rule (equality, sort, range).
- Shard key choice is the single most consequential decision in a sharded deployment. It is decided here with explicit justification of cardinality, frequency, monotonicity, and resulting chunk distribution. Hashed keys are not free.
- Read concern and write concern are explicit per operation class: writes that mutate state default to `w: "majority"`; reads with consistency requirements use `readConcern: "majority"` or `linearizable`; relaxed concerns require justification.
- Multi-document transactions are a fallback, not a default. They impose throughput and operational cost. Prefer single-document atomicity via document shape; use transactions only when the domain demands it.
- Use expand-migrate-contract or dual-write for any document-shape change touching a non-trivial subset of an existing collection. Never combine shape change, backfill, and application cutover in a single deploy.
- Challenge ODM-first models, giant unbounded arrays, the bucket pattern when a relational schema would be clearer, low-cardinality shard keys, and unsafe one-step migrations.
- A migration that has not been dry-run against a real MongoDB (Docker or Testcontainers) is not done. Capture `explain("executionStats")` for the top query patterns named in index justifications.

## Output contract

Generated data models and migrations MUST conform to:

- [naming-conventions](../../../../standards/naming-conventions/README.md) — `camelCase` field names; plural collection names unless a singular better fits ownership semantics; named indexes.
- [architecture-schema § data ownership](../../../../standards/architecture-schema/README.md) — each collection is owned by exactly one component; no cross-component writes.
- [security-standards](../../../../standards/security-standards/README.md) — PII tagging at field level; no secrets in migration scripts; at-rest encryption assumed; PII redaction posture for change-stream consumers (out of scope here, but noted).
- [deployment-standards](../../../../standards/deployment-standards/README.md) — backwards-compatible evolution only (expand → migrate → contract). A service deploy MUST NOT require a not-yet-run migration.

Upstream contract: `data-architecture.md` is the source of truth for engine choice, sharding decision, replica topology, and consistency posture. `backend-architecture.md` is the source of truth for domain ownership, transaction boundaries, and idempotency requirements. If either is silent on a decision this skill needs, pause and raise an ADR candidate rather than inventing it.

## Process

1. Load `system-design.md`, `data-architecture.md`, and `backend-architecture.md` (if present). Confirm MongoDB is the chosen engine for the data in scope, the bounded context that owns it, and the consistency posture required.
2. Inventory entities, relationships, and access patterns: per entity, list read shapes, write shapes, expected document size and growth, hot keys, and transactional groupings.
3. Decide embed vs reference per relationship. Embed when read together, bounded in size, and stable in lifecycle; reference when reused, unbounded, or independently lifecycled. Document the size ceiling for every embedded array.
4. Define the document shape per collection: required fields, optional fields, types, enum domains, identifier strategy (`_id` natural vs surrogate), versioning field (`schemaVersion`), and tenant key if multi-tenant.
5. Generate `$jsonSchema` validators with `validationLevel: strict` and `validationAction: error` for new collections. For evolving collections, plan the validator lifecycle alongside the shape change.
6. Define index strategy: per access pattern, name the index, the fields and order (ESR), partial-filter expression if applicable, TTL where retention is policy, and unique constraints. Reject indexes without a stated query pattern.
7. Define read and write concern per operation class. State the consistency rationale per concern choice. Flag any read path that uses `readConcern: "local"` on a sharded or multi-region cluster.
8. If sharded, choose the shard key. Justify against cardinality, write frequency distribution, monotonicity (avoid monotonically increasing keys without hashing), query routing (will most queries be single-shard?), and resulting chunk distribution. Document the failure mode if the shard key is wrong.
9. Define retention and deletion: per collection, retention period, deletion mechanism (TTL index, scheduled job, soft delete), audit and legal-hold behavior, and PII-specific handling.
10. Define the migration approach for the change at hand: identify whether it is additive (safe expand), in-place modification (requires phased migrate), or removal (safe contract after consumers drop the field). Choose expand-migrate-contract or dual-write accordingly.
11. Generate migration scripts in the project's chosen tool (mongock, mongo-migrate, or hand-rolled idempotent scripts). Each migration is idempotent, re-runnable, and produces a verifiable end state.
12. Write `migration-plan.md` when the migration includes any of: (a) a required-field addition to existing documents; (b) a field rename or type change; (c) a backfill touching > 10k documents; (d) an index added to a collection with sustained writes; (e) a shard-key change (requires resharding plan); (f) a validator tightening from `warn` to `error`; (g) any operation requiring downtime or a maintenance window.
13. Dry-run the migration sequence against a disposable MongoDB (Docker or Testcontainers). Run `explain("executionStats")` for the top query patterns named in index justifications. Capture results in the migration plan.
14. Validate against [naming-conventions](../../../../standards/naming-conventions/README.md), [security-standards](../../../../standards/security-standards/README.md), [deployment-standards](../../../../standards/deployment-standards/README.md), and `data-architecture.md`. Fix any divergence before declaring done.

## Outputs

Required:

- Collection inventory with owning component, document shape narrative, and embed-vs-reference decisions per relationship.
- `$jsonSchema` validator per collection.
- Index strategy table per collection: index name, fields, justification (query pattern + cardinality + write impact), and partial/TTL/unique flags.
- Read/write concern decision per operation class.
- Migration scripts (idempotent) implementing the change.

Conditional, when applicable:

- `migration-plan.md` (per the trigger conditions above).
- Shard key decision document with cardinality, frequency, monotonicity, and chunk-distribution analysis.
- ADR drafts for shard-key choice, transaction usage, or relaxed read/write concerns.

Output rules:

- Generated artifacts must be functional, not placeholder-heavy.
- No secrets, environment-specific bootstrap, or credentials in migration scripts.
- Every index, validator, and migration must be reproducible from source without manual intervention.
- A shape change without `migration-plan.md` (when triggered) is not done.

## Quality checks

- [ ] Every collection names an owning component traceable to `system-design.md` or `backend-architecture.md`.
- [ ] Every embedded array states a size ceiling and the access pattern that justifies embedding.
- [ ] Every collection has a `$jsonSchema` validator; new collections use `validationLevel: strict` and `validationAction: error`.
- [ ] Every index maps to a named access pattern; no "just in case" indexes survive.
- [ ] Compound index field order follows ESR (equality, sort, range) or has a documented exception.
- [ ] Read and write concern are explicit per operation class; relaxed concerns are justified.
- [ ] If sharded, the shard key is justified against cardinality, frequency, monotonicity, and chunk distribution.
- [ ] Multi-document transactions, if used, name the domain invariant that justifies them.
- [ ] Migration approach is expand-migrate-contract or dual-write; never a single-deploy shape change + backfill + cutover.
- [ ] `migration-plan.md` exists for any migration matching the triggers.
- [ ] Migration sequence was dry-run against a real MongoDB; `explain("executionStats")` captured for top queries.

## References

- Upstream: [`architecture/system-design`](../../../../architecture/system-design/SKILL.md), [`architecture/data-architecture`](../../../../architecture/data-architecture/SKILL.md), [`architecture/backend-architecture`](../../../../architecture/backend-architecture/SKILL.md).
- Related implementation skills: backend ecosystem skills consume this schema (ODM/repository wiring lives there, not here).
- Compatible patterns: [`modular-monolith`](../../../../architecture-patterns/modular-monolith/README.md), [`microservices`](../../../../architecture-patterns/microservices/README.md), [`event-driven`](../../../../architecture-patterns/event-driven/README.md) (outbox or change-stream patterns), [`cqrs`](../../../../architecture-patterns/cqrs/README.md) (read-model projections).
