---
name: postgres-schema-and-migration
description: Use when designing a Postgres schema for a new service or planning a
  schema change for an existing one. Produces an initial schema with appropriate
  indexes and a zero-downtime migration plan using the expand/migrate/contract
  pattern with Flyway or Liquibase.
---

# Postgres Schema and Migration

## When to use

Invoke when the domain model is settled and persistence design is needed, or when an existing schema requires a non-trivial change (new column, type change, constraint addition) on a live system. Do not invoke for schemaless or NoSQL stores.

## Inputs

- Domain model: entities, relationships, state machines.
- Expected access patterns and read/write ratio.
- For a change: the existing schema and the desired end state.

## Process

1. Translate entities to tables. Choose PK type (`bigserial` for high-write, `uuid` for distributed-id needs). Justify.
2. Define foreign keys for every relationship. Add an index covering every FK column.
3. Add additional indexes for known access patterns. Justify each.
4. Define constraints: NOT NULL, CHECK, UNIQUE. Reject nullable FKs unless explicitly justified.
5. Write the initial migration (`V1__init.sql`) using the project's migration tool (Flyway assumed).
6. For schema changes on live systems, produce a multi-step plan using expand/migrate/contract:
   - **Expand**: add new column/table NULL-able, no blocking locks; deploy app reading old and new.
   - **Migrate**: backfill in batches; switch writes to the new column; verify consistency.
   - **Contract**: drop the old column/table; tighten constraints (`SET NOT NULL`).
7. Document the rollback for each step.
8. Emit migration files plus `migration-plan.md` describing the phases, expected duration, and rollback for each.

## Outputs

- `V1__init.sql` (or successive `V{N}__*.sql` files for changes).
- `migration-plan.md` for non-trivial changes.

## Quality checks

- [ ] Every FK column has an index.
- [ ] No nullable FKs unless justified inline.
- [ ] Every schema change avoids blocking `ALTER` statements on large tables.
- [ ] Every multi-step migration has a documented rollback per step.
- [ ] Backfill operations are batched (≤ 10k rows per batch) to avoid long transactions.

## References

(None in v0.1.)
