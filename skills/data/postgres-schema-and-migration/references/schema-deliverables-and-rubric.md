# Schema Deliverables and Rubric

Load this before finalizing. Revise until each check passes or explicitly document the unresolved gap.

## Migration SQL deliverables

`V1__init.sql` and subsequent `V{N}__<slug>.sql` files must include:

- table DDL with columns, types, and NOT NULL constraints,
- named FK constraints for every relationship,
- named CHECK constraints for business rules,
- named UNIQUE constraints where applicable,
- indexes for every FK column,
- index justifications as inline SQL comments,
- `created_at` and `updated_at` as `timestamptz NOT NULL DEFAULT now()`,
- enum or CHECK constraints on status/state columns,
- `CREATE INDEX CONCURRENTLY` for indexes added to existing live tables,
- `-- flyway:executeInTransaction=false` directive in files containing non-transactional statements,
- `lock_timeout` before ALTERs on live tables,
- explicit `CREATE EXTENSION IF NOT EXISTS` for any extension the schema relies on (`pgcrypto`, `citext`, `pg_trgm`, etc.) declared in `V1__init.sql`.

## Migration plan deliverables

`migration-plan.md` must include:

- migration summary,
- expand/migrate/contract phase breakdown,
- SQL per phase,
- locks taken and estimated duration,
- pre-migration assertion query,
- post-migration assertion query,
- rollback trigger and rollback steps,
- blast radius if rollback fails,
- backfill batch size, throttling, progress tracking, and idempotency,
- dry-run estimation approach,
- contract safety checklist,
- operational monitoring expectations.

## Required checks

- [ ] Every FK column has an index or documented covering index.
- [ ] Constraints enforce core business integrity.
- [ ] Every index has explicit query-pattern justification.
- [ ] Nullable FKs are justified inline.
- [ ] Migrations are deterministic and ordered.
- [ ] Large-table migrations avoid blocking rewrites.
- [ ] Expand/migrate/contract is used for non-trivial live changes.
- [ ] Backfills are batched and resumable.
- [ ] Rollback strategy exists per migration phase.
- [ ] Query patterns are considered for each index.
- [ ] Timestamp handling is consistent and UTC-based.
- [ ] Pre-migration and post-migration validation queries are defined.
- [ ] Contract phase verifies no old consumers remain.
- [ ] Connection pool implications are acknowledged.
- [ ] The migration could realistically execute safely in production.
- [ ] No two indexes have the same leading-column prefix unless the redundancy is explicitly justified (e.g., a partial index over the same prefix).
- [ ] Required Postgres extensions are declared in `V1__init.sql` (not assumed pre-installed, not scattered across later migrations).
- [ ] Only Flyway `V` files are used for schema changes; `R` is reserved for views/functions/triggers; `U` (undo) files are not used.
- [ ] Migration dry-run against a disposable Postgres was performed and reported clean, **or** the skip is documented in `migration-plan.md` under Deferred Risks.
- [ ] `EXPLAIN` output was captured for the top query patterns named in index justifications and confirms the expected indexes are chosen, **or** the skip is documented.
- [ ] PII / regulated columns are identified and the handling policy is documented (in column comments or `data-classification.md`) where any classified data exists.

## Failure handling

If a check fails:

1. Identify the missing constraint, index rationale, lock analysis, rollback path, or operational assumption.
2. Fix it when the decision is clear.
3. Ask the user for confirmation when the decision changes data ownership, consistency, downtime risk, or rollback behavior.
4. Document intentionally deferred risks in `migration-plan.md`.
