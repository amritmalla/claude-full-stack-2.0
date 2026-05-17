---
product: <kebab-case slug>          # matches the system-design / PRD slug
status: draft                       # draft | review | approved | superseded
owner: <name or role>
system_design: <relative path to source system-design.md>
prd: <relative path to source PRD, or null>
version: 0.1.0                      # semver
last_reviewed: YYYY-MM-DD
---

# Data Architecture: [Product or Context Name]

## Overview

[One paragraph: which datasets and engines exist, the bounded contexts that own them, what this architecture optimizes for, the dominant access patterns, and what it intentionally does not do.]

## Dataset Inventory & Ownership

| Dataset | Owning Context | Authoritative Write Path | Engine | Consumers (read) | Consumption Mechanism |
|---|---|---|---|---|---|
| [dataset] | [context] | [service/command] | [engine] | [consumers] | [API / event / read model / projection] |

## Access Patterns

| Dataset | Read Shapes | Write Shapes | Hot Keys / Skew | Read:Write | Latency Target | Transactional Grouping |
|---|---|---|---|---|---|---|
| [dataset] | [point / range / join / agg / search / vector] | [single / batch / append-only] | [risk] | [ratio] | [target] | [grouping] |

## Engine Selection

| Dataset | Engine Class | Engine | Justification | Alternatives Rejected |
|---|---|---|---|---|
| [dataset] | [relational / document / key-value / search / time-series / analytical / vector] | [engine] | [access-pattern / consistency / scaling / cost fit] | [why not X] |

## Consistency & Concurrency Model

| Write Path | Consistency Guarantee | Isolation / Concurrency | Conflict Resolution | Enforcement Mechanism |
|---|---|---|---|---|
| [path] | [strong / read-your-writes / eventual / causal] | [serializable / optimistic / MVCC / lock] | [behavior] | [versioning / txn / outbox / saga] |

## Schema Strategy

| Concern | Decision |
|---|---|
| Normalization posture | [decision] |
| Aggregate boundaries | [decision] |
| Key design | [surrogate / natural] |
| Tenant isolation | [model] |
| Soft-delete policy | [policy] |
| Referential integrity | [rules] |
| Immutable / audit data | [requirements] |

## Indexing Strategy

| Dataset | Access Pattern | Serving Index | Index Type | Write Cost | Cardinality Assumption |
|---|---|---|---|---|---|
| [dataset] | [pattern] | [index] | [composite / covering / partial / GIN/GIST / TTL / search] | [cost] | [assumption] |

## Partitioning & Sharding

*Conditional — include only when a measured constraint demands it; otherwise list under Omitted sections.*

| Dataset | Triggering Constraint | Partition Key | Rebalance Strategy | Cross-Partition Behavior | Hotspot Mitigation |
|---|---|---|---|---|---|
| [dataset] | [throughput / size / tenancy / blast radius / region] | [key] | [strategy] | [query/txn behavior] | [mitigation] |

## Replication & High Availability

*Conditional — include when replication/HA topology is non-trivial; otherwise list under Omitted sections.*

| Engine | Topology | Failover Model | RTO / RPO | Replica Lag Tolerance | Read Routing / Read-after-write | Backup Strategy |
|---|---|---|---|---|---|---|
| [engine] | [primary/replica layout] | [auto/manual] | [RTO/RPO] | [tolerance] | [routing rule] | [backup separate from replicas] |

## Cache Architecture

*Conditional — include when cache layers exist; otherwise list under Omitted sections.*

| Layer | Cached Data | Source of Truth | Invalidation Trigger | TTL / Staleness Budget | Cold-cache Behavior | Stampede Protection |
|---|---|---|---|---|---|---|
| [in-process / distributed / CDN / read model / search projection] | [data] | [source] | [trigger] | [budget] | [behavior] | [protection] |

## Retention & Deletion

| Dataset | Retention Period | Deletion Mechanism | Archival | PII Handling | Audit / Legal Hold |
|---|---|---|---|---|---|
| [dataset] | [period] | [TTL / tombstone / scheduled purge / archival] | [strategy] | [handling] | [behavior] |

## Migration Strategy

| Concern | Decision |
|---|---|
| Tooling | [tool] |
| Phasing | [expand / migrate / contract] |
| Online-migration constraints | [constraints] |
| Dual-write / shadow-read | [requirements] |
| Backfill strategy | [strategy] |
| Rollback expectations | [expectations] |
| Compatibility guarantees | [guarantees] |

## Operational Readiness

| Concern | Decision |
|---|---|
| Backup cadence & restore validation | [decision] |
| Monitoring signals | [replication lag, slow queries, lock waits, deadlocks, cache hit ratio, storage growth, pool saturation] |
| Query-performance monitoring | [approach] |
| Runbook hooks | [hooks] |

## Implementation Handoffs

### implementations/data/<engine>

- [Schema, migration, and index handoff notes per dataset]

### backend-architecture

- [Ownership, transaction, and consistency decisions consumed by backend]

### security

- [Tenant isolation, PII handling, encryption, audit needs]

### reliability / operations

- [Failover, backup/restore, monitoring, runbook handoff]

## ADR Index

| ADR | Title | Status | Summary |
|---|---|---|---|
| NNNN | [title] | [proposed/accepted/...] | [summary] — links to `adrs/NNNN-<slug>.md` |

## Omitted sections

- [Conditional section name]: [one-line rationale for omission].

## Deferred Decisions

- [Decision, owner, deadline].
