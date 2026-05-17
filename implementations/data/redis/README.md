# redis

> Status: scaffold.

## Purpose

Implements `architecture/data-architecture` for Redis as a cache, key-value store, or low-latency data structure server: key design, TTL and eviction strategy, caching pattern implementation, replication topology, persistence posture, and access hardening.

Architecture decisions (which workloads use Redis, consistency posture, cluster vs Sentinel, persistence trade-offs, tenant isolation) come from upstream and are taken as inputs here.

## Engine family

Redis belongs to **Family C — Cache / KV** in the data layer model. See [`implementations/data/README.md`](../README.md) for the full archetype set and philosophy.

## Ecosystem (target)

- Redis 7.x (standalone, Sentinel, or Cluster)
- RDB and AOF persistence
- ACL-based authentication (Redis 6+)
- Redis Streams, Sorted Sets, HyperLogLog where the workload demands
- Lettuce / Jedis / node-redis clients on the application side (client wiring lives in the backend implementation skill, not here)

## Compatible patterns

- [microservices](../../../architecture-patterns/microservices/README.md) (per-service cache namespaces)
- [event-driven](../../../architecture-patterns/event-driven/README.md) (Redis Streams as a lightweight broker)
- [real-time-systems](../../../architecture-patterns/real-time-systems/README.md)

## Skills

### Authored

_None._

### Archetype coverage

| # | Archetype | Skill | Status |
|---|---|---|---|
| 1 | key-design-and-data-structure | `redis-key-design-and-data-structure` | planned |
| 2 | caching-pattern-implementation | `redis-caching-pattern-implementation` | planned |
| 3 | replication-and-ha-readiness | `redis-replication-and-ha-readiness` | planned |
| 4 | backup-and-operational-readiness | `redis-backup-and-operational-readiness` | planned |
| 5 | security-and-data-access-hardening | `redis-security-and-data-access-hardening` | planned |

### Planned skill scope (future work)

- **`redis-key-design-and-data-structure`** — key naming convention with namespace and tenant prefixing, TTL strategy per namespace, eviction policy selection (`allkeys-lru`, `volatile-lru`, `allkeys-lfu`, `noeviction`), data-structure choice (string vs hash vs sorted-set vs stream vs bitmap vs HyperLogLog vs geo), memory budgeting per namespace, BIG-KEY and HOT-KEY prevention.
- **`redis-caching-pattern-implementation`** — cache-aside / write-through / write-behind / refresh-ahead implementation, stampede protection (single-flight, jittered TTL, mutex-based locking), invalidation rules (tag-based, version-based, event-driven), negative caching posture, consistency trade-offs documented per workload.
- **`redis-replication-and-ha-readiness`** — Sentinel vs Cluster topology selection, failover behavior, replica read posture (consistent-only or staleness-tolerant), Cluster slot rebalancing strategy, split-brain prevention, multi-AZ placement, client-side topology refresh.
- **`redis-backup-and-operational-readiness`** — RDB and AOF posture, persistence trade-offs (durability vs latency), restore drills with documented RPO/RTO, latency-percentile and memory-fragmentation observability, runbook inputs (FLUSHALL guards, BIG-KEY remediation, replica resync, eviction storms).
- **`redis-security-and-data-access-hardening`** — ACL model (per-user command/key/channel grants), TLS configuration, dangerous-command renaming or disabling (`FLUSHALL`, `CONFIG`, `KEYS`), network exposure review, no-PII-in-cache discipline, retention posture, secret rotation.

## Architecture domains implemented

| Architecture domain | How |
|---|---|
| [data-architecture](../../../architecture/data-architecture/README.md) | Key design, eviction, caching patterns, persistence posture. |
| [reliability](../../../architecture/reliability/README.md) | Sentinel/Cluster topology, persistence trade-offs, failover. |
| [performance](../../../architecture/performance/README.md) | Caching patterns, stampede protection, hot-key remediation. |
| [security](../../../architecture/security/README.md) | ACLs, TLS, command hardening, no-PII discipline. |

## Standards this implementation conforms to

- [architecture-schema](../../../standards/architecture-schema/README.md) — key-namespace ownership: each namespace is owned by exactly one component.
- [naming-conventions](../../../standards/naming-conventions/README.md) — namespaced colon-separated keys (`{tenant}:{domain}:{entity}:{id}`).
- [security-standards](../../../standards/security-standards/README.md) — TLS, ACL, no secrets cached, audit posture.
- [observability-standards](../../../standards/observability-standards/README.md) — latency, memory, eviction, replication-lag signals exposed.

## Upstream inputs

- Approved `data-architecture.md` selecting Redis for specific workloads and declaring topology, persistence posture, and consistency trade-offs.
- `backend-architecture.md` for caching strategy direction, idempotency-key namespace ownership, and tenant-isolation requirements.
