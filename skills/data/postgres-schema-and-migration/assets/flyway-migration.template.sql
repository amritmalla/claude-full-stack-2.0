-- V{N}__{slug}.sql
-- Purpose: {what changes and why}
-- Safety:  {new schema | expand phase | migrate phase | contract phase}
-- Rollback: {summary or link to migration-plan.md}
--
-- Reminders before editing this file:
--   * `CREATE INDEX CONCURRENTLY` and `REINDEX CONCURRENTLY` cannot run inside a
--     transaction. Add this directive on its own line at the top and keep
--     concurrent operations in their own dedicated migration file:
--       -- flyway:executeInTransaction=false
--   * Adding NOT NULL to an existing column on a non-empty live table is a
--     rewrite. Use expand/migrate/contract: add nullable, backfill, then
--     tighten with NOT NULL + CHECK in a later phase.
--   * Type changes (`ALTER COLUMN ... TYPE`) often rewrite the table. Plan as
--     expand/migrate/contract with shadow column when the table is large.
--   * Renames break old readers and writers. Plan them as
--     add-new -> dual-write -> backfill -> swap readers -> drop-old.
--   * Wrap unsafe single-statement DDL in its own migration file so partial
--     failure does not leave a mixed state.

SET lock_timeout = '5s';
SET statement_timeout = '5min';

-- Extensions (declare in V1__init.sql, not later migrations)
-- CREATE EXTENSION IF NOT EXISTS pgcrypto;     -- gen_random_uuid()
-- CREATE EXTENSION IF NOT EXISTS citext;       -- case-insensitive text
-- CREATE EXTENSION IF NOT EXISTS pg_trgm;      -- trigram indexes for fuzzy search

-- Tables
-- CREATE TABLE example (
--   id           bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
--   created_at   timestamptz NOT NULL DEFAULT now(),
--   updated_at   timestamptz NOT NULL DEFAULT now()
-- );

-- Constraints (use named constraints: fk_*, chk_*, uq_*)
-- ALTER TABLE example
--   ADD CONSTRAINT chk_example_status CHECK (status IN ('created','paid','shipped','cancelled'));

-- Indexes
-- Index:       idx_{table}_{columns}
-- Supports:    {query pattern, caller, expected frequency}
-- Write impact: {low | medium | high} — {why}
-- Cardinality: {column cardinality notes}
-- CREATE INDEX idx_example_status ON example (status) WHERE status <> 'shipped';

-- Validation (paste into migration-plan.md too)
-- SELECT count(*) FROM example;
-- SELECT * FROM example WHERE <invariant violated> LIMIT 1;
