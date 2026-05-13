# Migration Plan

## Summary

[What is changing and why.]

## Scope

[Tables, columns, indexes, constraints, affected services, and expected data volume.]

## Phase 1: Expand

- SQL:
- Locks:
- Estimated duration:
- Pre-migration assertion:
- Post-migration assertion:
- Rollback trigger:
- Rollback steps:
- Blast radius:

## Phase 2: Migrate

- Backfill strategy:
- Batch size:
- Throttling:
- Progress tracking:
- Idempotency guarantee:
- Locks:
- Estimated duration:
- Pre-migration assertion:
- Post-migration assertion:
- Rollback trigger:
- Rollback steps:
- Blast radius:

## Phase 3: Contract

- SQL:
- Locks:
- Estimated duration:
- Contract safety checks:
- Pre-migration assertion:
- Post-migration assertion:
- Rollback trigger:
- Rollback steps:
- Blast radius:

## Dry Run

[Staging clone, recent backup, EXPLAIN-based estimate, or other approach.]

## Monitoring

[Metrics, logs, lock monitoring, replication lag, error rate, progress query, alert thresholds.]

## Deferred Risks

[Only intentionally deferred migration risks.]
