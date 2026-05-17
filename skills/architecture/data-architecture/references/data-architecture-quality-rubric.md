# Data Architecture Quality Rubric

Load this before emitting `data-architecture.md`. Revise until each check passes or the unresolved gap is explicitly documented.

## Ownership and boundaries

- [ ] Every dataset names exactly one owning bounded context and one authoritative write path.
- [ ] Cross-context access is via API, event, replicated read model, or projection — no ad hoc cross-service joins.
- [ ] No shared-write databases or multi-owner datasets survive.
- [ ] Every dataset traces to the approved system design or is marked as an open decision.

## Engine and access patterns

- [ ] Access patterns are inventoried per dataset before engine selection.
- [ ] Each engine choice is justified against query shape, write behavior, consistency, scaling, operational maturity, and cost.
- [ ] Rejected engine alternatives are stated, not just the chosen one.
- [ ] No one-engine-for-everything or organization-default thinking without justification.

## Consistency and concurrency

- [ ] Every write path declares its consistency guarantee, concurrency model, conflict resolution, and enforcement mechanism.
- [ ] Lost-update and write-skew prevention is explicit where concurrent writes occur.
- [ ] No implied consistency, "eventual somehow," or hidden distributed transactions.

## Schema and indexing

- [ ] Normalization posture, aggregate boundaries, key design, tenant isolation, and soft-delete policy are defined.
- [ ] No giant shared aggregates, EAV schemas, or JSON blobs replacing structure.
- [ ] Every index maps to a named access pattern, justifies write overhead, and has operational ownership.
- [ ] No speculative or ORM-sprawl indexes survive.

## Partitioning, replication, and cache

- [ ] Partitioning or sharding, if proposed, names the partition key, rebalance rule, cross-partition behavior, hotspot mitigation, and the measured constraint that triggered it.
- [ ] Replication topology states failover RTO/RPO, replica lag tolerance, and read-after-write rules; replicas are not treated as backups.
- [ ] Every cache layer names source of truth, invalidation rule, staleness budget, stampede protection, and cold-cache behavior.

## Retention, migration, and operations

- [ ] Every dataset states retention duration, deletion mechanism, archival, PII handling, and legal-hold behavior.
- [ ] No undefined retention or soft-delete-forever systems.
- [ ] Migration approach is expand/migrate/contract, or an ADR justifies an alternative.
- [ ] Operational monitoring (replication lag, slow queries, lock waits, deadlocks, cache hit ratio, storage growth, pool saturation) and restore validation are defined.

## Linkage and decisions

- [ ] `data-architecture.md` conforms to [architecture-schema](../../../../standards/architecture-schema/README.md): frontmatter complete, required sections present, conditional sections present or omitted with rationale.
- [ ] Every ADR candidate has Context, Decision, Consequences (including downsides), and Alternatives considered.
- [ ] No engine-specific DDL, ORM classes, or vendor SDK calls leaked into the architecture.
- [ ] At least one weak-architecture risk was surfaced, or the design's intentional simplicity was explained.

## Failure handling

If a check fails:

1. Identify the missing or weak decision.
2. Ask the user for clarification if it cannot be inferred from `system-design.md` or the PRD.
3. Revise `data-architecture.md` or the relevant ADR.
4. Keep unresolved questions explicit; do not hide them as assumptions.
