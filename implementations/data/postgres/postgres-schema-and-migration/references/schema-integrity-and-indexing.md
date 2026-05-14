# Schema Integrity and Indexing

Use this reference when designing tables, constraints, data types, indexes, and denormalized structures.

## Naming conventions

Use:

- snake_case throughout,
- plural table names unless the project already has a different convention,
- named FK constraints: `fk_{table}_{column}`,
- named CHECK constraints: `chk_{table}_{rule}`,
- clear names without reserved keywords or ambiguous abbreviations.

## Integrity rules

Use database constraints for core business integrity:

- NOT NULL,
- CHECK,
- UNIQUE,
- FK,
- exclusion constraints where appropriate.

Do not rely only on application validation for durable business rules.

Recommended defaults:

- UTC timestamps,
- `timestamptz` for all timestamp columns,
- `created_at timestamptz NOT NULL DEFAULT now()`,
- `updated_at timestamptz NOT NULL DEFAULT now()`,
- immutable creation timestamps,
- explicit state-machine validation,
- constrained enums via CHECK or enum types with a migration plan for new values.

Reject free-form status fields, unconstrained text enums, silent invalid states, and `timestamp without time zone`.

## Index justification

Every index must include:

```text
Index: idx_orders_customer_status ON orders(customer_id, status)
Supports: Get all pending orders for a customer; customer dashboard query; about 50 calls/s
Write impact: Low; orders table is insert-heavy but customer_id and status rarely change
Cardinality: customer_id high, status low
```

Reject speculative indexing, duplicate indexes, indexing every column, and ORM-generated index sprawl.

## Index types

Consider:

- composite indexes for multi-column lookup and ordering,
- covering indexes with `INCLUDE`,
- partial indexes with `WHERE`,
- GIN indexes for full-text, JSONB, or array containment,
- BRIN indexes for large append-only naturally ordered tables,
- unique indexes for business uniqueness.

Every FK column must be indexed unless covered by a suitable unique or composite index.

## Denormalization

Denormalize only when at least one measured condition is true:

- A normalized query cannot meet latency SLO even with proper indexing and the access pattern is read-heavy, about 100:1 read/write or higher.
- A critical hot-path query requires more than four joins and performance testing confirms joins are the bottleneck.
- Reporting or analytics needs conflict with operational query patterns and a materialized view or projection table is justified.

Document the query pattern, measured performance gap, consistency maintenance strategy, and acceptable staleness window.

Reject "joins are hard", "it will be faster", or "ORM makes this easier" as justification.

## Extensions

Declare required extensions in `V1__init.sql`, not in later migrations. Do not assume any extension is pre-installed.

Common defaults to consider:

- `pgcrypto` — `gen_random_uuid()`, digest functions, column-level encryption (use only with a real key-management plan).
- `citext` — case-insensitive text columns (emails, usernames).
- `pg_trgm` — trigram indexes for fuzzy search and `ILIKE` patterns.
- `uuid-ossp` — legacy UUID generators; prefer `pgcrypto`'s `gen_random_uuid()` for new schemas.

Reject extensions added "in case we need them later" — each one is an operational dependency.

## Cross-cutting tables

These tables appear across many services and should follow consistent shapes when used:

### `idempotency_keys`

Pairs with the `Idempotency-Key` header from `backend-architecture`. Recommended shape:

```sql
CREATE TABLE idempotency_keys (
  key             text         NOT NULL,
  customer_id     bigint       NOT NULL,
  request_hash    text         NOT NULL,
  response_status smallint     NOT NULL,
  response_body   jsonb        NOT NULL,
  created_at      timestamptz  NOT NULL DEFAULT now(),
  expires_at      timestamptz  NOT NULL,
  PRIMARY KEY (customer_id, key)
);

CREATE INDEX idx_idempotency_keys_expires_at
  ON idempotency_keys (expires_at);
```

- Composite PK scopes keys to a caller — different customers may reuse a UUID.
- Store `request_hash` to detect `IDEMPOTENCY_CONFLICT` (same key, different body).
- TTL purge via scheduled job hitting `expires_at`.

### `outbox`

For the transactional outbox pattern when events must be emitted at-least-once with a transactional guarantee.

```sql
CREATE TABLE outbox (
  id            bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  aggregate     text          NOT NULL,
  aggregate_id  text          NOT NULL,
  event_type    text          NOT NULL,
  payload       jsonb         NOT NULL,
  created_at    timestamptz   NOT NULL DEFAULT now(),
  published_at  timestamptz
);

CREATE INDEX idx_outbox_unpublished
  ON outbox (created_at) WHERE published_at IS NULL;
```

A publisher worker reads unpublished rows in order, emits, and marks `published_at`.

### `audit_log`

For services with audit requirements. Append-only, never updated.

```sql
CREATE TABLE audit_log (
  id          bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  actor       text          NOT NULL,
  action      text          NOT NULL,
  entity      text          NOT NULL,
  entity_id   text          NOT NULL,
  payload     jsonb,
  occurred_at timestamptz   NOT NULL DEFAULT now()
);

CREATE INDEX idx_audit_log_entity ON audit_log (entity, entity_id, occurred_at DESC);
```

Plan retention and partitioning early — `audit_log` is the most common unbounded-table mistake.

## JSONB and soft deletes

Use JSONB only when schema flexibility is genuinely required and relational modeling is insufficient. Do not use JSONB as a substitute for normalization.

Avoid soft deletes unless operationally required. If used, define archival semantics, unique-index behavior with `deleted_at`, filtering conventions, and retention/deletion workflows.
