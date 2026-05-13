---
name: postgres-schema-and-migration
description: Use when designing, reviewing, or evolving a PostgreSQL schema for a production system. Produces normalized schema design, integrity constraints, indexing strategy, Flyway or Liquibase migrations, and zero-downtime migration plans using expand/migrate/contract. Do not use for schemaless databases, NoSQL stores, graph databases, analytics warehouses, or ORM-only modeling discussions. Sits downstream of system-design-from-prd (bounded contexts and ownership) and rest-api-contract-design (idempotency requirements); pairs with spring-boot-service-scaffold (Flyway directory) and integration-test-strategy (Testcontainers tests run against this schema).
---

# Postgres Schema and Migration

## When to use

Invoke when designing a new PostgreSQL schema, introducing a service persistence layer, planning schema evolution, reviewing indexes, performing production migrations, or preparing large-scale data changes.

Do not use for schemaless databases, NoSQL/document stores, graph databases, analytics warehouses, or ORM-only modeling discussions.

## Inputs

Required:

- Domain entities, relationships, and ownership boundaries.
- Known access patterns or API/system design context.

Optional:

- Existing schema or Flyway/Liquibase migrations.
- System design bounded contexts.
- Table sizes, write rates, and query SLOs.
- Retention, audit, compliance, or deletion requirements.
- Multi-tenant model.
- Migration tooling preference.
- Operational constraints such as lock tolerance, maintenance windows, and rollback requirements.

## Operating rules

- Production safety beats convenience. Optimize for uptime, lock minimization, rollback safety, and operational predictability.
- Respect bounded contexts. Each context owns its tables; cross-context access happens through defined interfaces, not shared writes.
- Model business integrity in the database with NOT NULL, CHECK, UNIQUE, FK, and exclusion constraints where appropriate.
- Access patterns drive indexing. Every index needs a query pattern, cardinality expectation, and write-impact note.
- Use expand/migrate/contract for non-trivial live changes. Never combine schema rewrite, data migration, and application cutover in one deployment.
- Challenge ORM-first schemas, giant JSON blobs, EAV, nullable ownership FKs, premature denormalization, and unsafe one-step migrations.
- Confirm the target directory before writing files. Recommend `src/main/resources/db/migration/` for Spring Boot + Flyway, or `db/migration/` for standalone. Refuse to scaffold into a plugin/skill repository.
- Write `migration-plan.md` when the migration includes any of: (a) a column drop, type change, or NOT NULL tightening on an existing table; (b) a backfill touching > 10k rows; (c) an index added to a table with sustained writes; (d) a rename; (e) any rewrite operation (`ALTER TYPE`, `ALTER COLUMN ... USING`); (f) anything that takes a lock for > 1 second. `V1__init.sql` against an empty database does not need a migration plan.
- A migration that has not been dry-run against a real Postgres is not done. Run the full migration sequence against a disposable Postgres (Docker or Testcontainers) before declaring completion. Capture `EXPLAIN` output for the top query patterns named in index justifications.

## Progressive references

- Read `references/domain-and-access-modeling.md` when discovering entities, relationships, ownership, bounded contexts, tenants, identities, lifecycle states, and access patterns.
- Read `references/schema-integrity-and-indexing.md` when designing tables, constraints, data types, timestamps, indexes, denormalization, JSONB, and soft deletes.
- Read `references/migration-safety-playbook.md` when planning production changes, expand/migrate/contract phases, backfills, locks, rollback, validation queries, and contract safety.
- Read `references/operational-postgres-review.md` when evaluating table growth, partitioning, retention, vacuum sensitivity, replication, connection pools, and operational risks.
- Read `references/schema-deliverables-and-rubric.md` before finalizing and use it as the deliverable checklist and quality rubric.
- Use `assets/flyway-migration.template.sql` for migration SQL files such as `V1__init.sql`.
- Use `assets/migration-plan.template.md` for `migration-plan.md`.
- The canonical worked example for this skill lives at `examples/spring-boot/orders-api/.skill-outputs/postgres-schema-and-migration/` in the plugin repo. Consult it for index-justification style, expand/migrate/contract phasing, and cross-cutting table shapes before generating.

## Process

Progress:

- [ ] Step 1: Gather domain and access patterns: entities, relationships, ownership rules, lifecycle states, query patterns, write frequency, reporting needs, retention, scale assumptions, pagination, transactional boundaries, and **target migration directory** (default `src/main/resources/db/migration/` for Spring Boot + Flyway). Verify the target is not a plugin or skill repository.
- [ ] Step 2: Choose identity and primary key strategy intentionally: `bigserial`, UUID, ULID/KSUID-style IDs, or rare composite natural keys. Justify based on write throughput, distribution, ordering, external exposure, debugging, and multi-region concerns.
- [ ] Step 3: Model relational structure: tables, schemas, ownership boundaries, foreign keys, many-to-many entities, tenant model, and lifecycle constraints.
- [ ] Step 4: Define integrity rules: NOT NULL, uniqueness, CHECK constraints, enum/state restrictions, timestamp consistency, delete/retention semantics, and database-enforced business rules.
- [ ] Step 5: Design indexing strategy from known queries, joins, sorting, uniqueness, pagination, and operational workflows. Reject blind indexes and duplicate ORM defaults.
- [ ] Step 6: Evaluate operational characteristics: expected growth, partitioning, archival, retention enforcement, autovacuum sensitivity, replication, long transactions, query count per request, and connection pool implications.
- [ ] Step 7: Choose migration tooling, defaulting to Flyway unless Liquibase is required. Plan non-trivial live changes using expand/migrate/contract.
- [ ] Step 8: Generate migration SQL and `migration-plan.md` (when one of the six triggers in operating rules applies). Include lock analysis, validation queries, rollback triggers, rollback steps, blast radius, backfill strategy, and monitoring expectations. Enable required Postgres extensions explicitly in `V1__init.sql` (typically `pgcrypto` for `gen_random_uuid()`).
- [ ] Step 9: **Migration dry-run (mandatory).** Apply the full migration sequence against a disposable Postgres — `docker run --rm -e POSTGRES_PASSWORD=x -p 5432:5432 postgres:16` or a Testcontainers session — and confirm clean apply. Then run `EXPLAIN` (or `EXPLAIN ANALYZE` on seed data) for the top query patterns named in index justifications, capture the plans, and confirm the expected indexes are chosen. If Docker is unavailable, document the skipped dry-run in `migration-plan.md` under Deferred Risks — do not silently skip.
- [ ] Step 10: Validate all artifacts against `references/schema-deliverables-and-rubric.md`. Revise until checks pass or explicitly document any unresolved gap.

## Outputs

- `V1__init.sql` and subsequent `V{N}__<slug>.sql` migration files.
- `migration-plan.md` for non-trivial live changes.

Optional outputs when appropriate:

- Rollback scripts per phase.
- Backfill worker pseudocode.
- Index analysis notes.
- Partitioning recommendations with justification.
- Query optimization guidance with EXPLAIN notes.

Output rules:

- Migration SQL must be deterministic, ordered, and environment-safe.
- No placeholder SQL, undocumented assumptions, or missing rollback plan for production changes.
- Use named constraints and consistent snake_case naming.
- Document denormalization only when it has measured justification and a maintenance strategy.
- Make unsafe migrations explicit and recommend safer phased alternatives.

## Quality checks

- [ ] `references/schema-deliverables-and-rubric.md` was loaded before finalizing.
- [ ] Migration SQL follows `assets/flyway-migration.template.sql`.
- [ ] `migration-plan.md` follows `assets/migration-plan.template.md` when a migration plan is needed.
- [ ] Every index has an explicit query-pattern justification.
- [ ] The migration could realistically execute safely in production.

## References

- `references/domain-and-access-modeling.md`
- `references/schema-integrity-and-indexing.md`
- `references/migration-safety-playbook.md`
- `references/operational-postgres-review.md`
- `references/schema-deliverables-and-rubric.md`
- `assets/flyway-migration.template.sql`
- `assets/migration-plan.template.md`
