# Operational Postgres Review

Use this reference to evaluate performance and operational risks beyond DDL correctness.

## Growth and retention

Clarify:

- expected table growth,
- write rate,
- update/delete churn,
- archival strategy,
- retention windows,
- audit requirements,
- purge requirements,
- reporting workloads.

Avoid unbounded audit, event, or log tables without retention and archival plans.

## Partitioning

Avoid partitioning unless clearly necessary.

Justify partitioning with:

- table size over about 100GB,
- time-based pruning needs,
- operational retention/deletion pressure,
- clear partition key and query alignment,
- proven index or vacuum pressure.

Premature partitioning adds operational complexity and should be challenged.

## Vacuum and bloat

Flag:

- high-churn tables,
- frequent updates to indexed columns,
- soft-delete-heavy tables,
- long-running transactions,
- unbounded queues in relational tables,
- large JSONB updates.

Document autovacuum sensitivity and any tuning expectations when table churn is high.

## Connection pool implications

Call out schemas or query patterns that encourage:

- long transactions,
- many small queries per request,
- dynamic queries that defeat plan caching,
- N+1 access patterns,
- lock waits that hold connections.

Recommend batching, fewer round trips, better indexes, or query redesign where needed.

Pool sizing guidance:

- Start at **10 connections per service instance**. Increase only when measured contention (waits in HikariCP metrics, `pg_stat_activity` saturation) justifies it.
- Cap the **total active connections across all clients** at roughly `cores * 2 + effective_spindle_count` on the database server (HikariCP authors' recommendation). For modern SSD-backed Postgres, effective spindle count is small; treat it as a soft cap, not a target.
- More connections is almost never the answer to slow queries — fix the query or the index.
- For high-fanout workloads, prefer a pooler (PgBouncer in transaction mode) over raw connection growth.

## Replication and read models

Document:

- whether read replicas are expected,
- replica lag tolerance,
- consistency expectations,
- read-after-write requirements,
- logical replication needs,
- sequence collision implications,
- materialized view refresh behavior.

Do not route user-critical read-after-write paths to lagging replicas without an explicit consistency strategy.

## Data classification

For every table, mark columns containing PII, secrets, financial data, or regulated content.

Default policy:

- Encrypt at rest (handled by managed Postgres in almost every modern deployment — confirm, do not assume).
- Never log raw column values for classified columns in application logs.
- Never expose classified columns in DTOs without explicit redaction or aliasing.
- Use `pgcrypto` for column-level encryption only when the threat model justifies it *and* a real key-management plan exists. Column-level encryption without rotation, backups, and break-glass procedures is worse than no encryption.
- Classify before you ship: retro-classifying columns after data lands is materially harder.

Document classification per column in a comment or a short `data-classification.md` alongside the migrations.

## Query review

For important queries, include:

- expected selectivity,
- join shape,
- sort behavior,
- pagination behavior,
- index used,
- EXPLAIN or dry-run plan when available.

Flag accidental table scans on hot paths and indexes that cannot support the requested ordering.
