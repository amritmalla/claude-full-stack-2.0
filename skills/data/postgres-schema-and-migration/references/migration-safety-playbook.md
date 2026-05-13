# Migration Safety Playbook

Use this reference when planning production schema evolution.

## Four required questions

Every migration plan must answer:

- What locks are taken?
- How long could they last?
- Can this be paused?
- Can this be rolled back safely?

If any answer is missing, the migration plan is incomplete.

## Expand / migrate / contract

Use expand/migrate/contract for all non-trivial live changes.

Expand:

- add compatible structures,
- add nullable columns,
- add new tables,
- add shadow indexes,
- add dual-write capability,
- deploy backward-compatible code.

Migrate:

- move data incrementally,
- use batched backfills,
- keep transactions bounded,
- make jobs resumable,
- verify consistency,
- expose progress and pause controls.

Contract:

- drop old columns,
- tighten constraints,
- remove compatibility logic,
- finalize NOT NULL,
- remove deprecated indexes.

Contract only after validation confirms no old readers or writers remain.

## Backfills

Requirements:

- batch by primary key or stable cursor,
- keep transactions short,
- make execution idempotent,
- track progress,
- throttle between batches,
- define retry behavior,
- define pause/resume behavior.

Recommended starting point: batches no larger than 10k rows, tuned downward for wide rows or high write pressure.

## Lock and rewrite safety

Avoid:

- table rewrites on large tables without dry-run estimation,
- blocking ALTERs on tables with sustained writes,
- updates touching more than 100k rows in one transaction,
- long transactions over 5 seconds on hot tables,
- lock-heavy operations during peak traffic,
- synchronous full-table backfills,
- unbounded deletes.

Prefer:

- `CREATE INDEX CONCURRENTLY`,
- `lock_timeout` before live-table ALTERs,
- phased rollouts,
- batched deletes,
- shadow columns,
- validation before cutover,
- feature-flagged migrations.

## Validation and rollback

Each phase needs:

- pre-migration assertion query,
- post-migration assertion query,
- dry-run estimation approach,
- rollback trigger,
- rollback steps,
- blast radius if rollback fails,
- data consistency implications,
- monitoring expectations.

If rollback is impossible, say why and define mitigation. Never assume rollback is trivial.

## Flyway file conventions

- Use `V{N}__{slug}.sql` (versioned) files only. They are immutable once applied — Flyway tracks them in `flyway_schema_history` and rejects changes to the checksum.
- Do not use `U{N}__{slug}.sql` (undo) migrations. They encourage believing rollback is trivial, which it almost never is for data-touching changes. Roll back via a forward `V{N+1}__revert_{slug}.sql` after a real plan.
- Use `R__{slug}.sql` (repeatable) only for objects that should be *replaced* rather than versioned: views, materialized view bodies, functions, triggers, stored procedures. Repeatable migrations re-run whenever their checksum changes.
- One unsafe DDL statement per migration file. If it fails halfway, you want to know exactly which file is half-applied.
- `CREATE INDEX CONCURRENTLY` and similar non-transactional statements need `-- flyway:executeInTransaction=false` at the top of their own dedicated file.

## Contract safety checklist

- [ ] All code writing to old columns has been removed or disabled for at least one release cycle.
- [ ] All read paths use new structures.
- [ ] Logs or query stats show no old consumers remain.
- [ ] Backfill validation confirms old and new data are consistent.
- [ ] Rollback plan exists if old consumers are discovered after contract.
