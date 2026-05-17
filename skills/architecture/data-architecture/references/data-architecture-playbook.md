# Data Architecture Playbook

Load this when inventorying access patterns, selecting engines, or making any data-architecture decision. It expands the operating rules and process steps in `SKILL.md` with the detail needed to produce `data-architecture.md`.

## Why this workflow exists

Design operationally safe, scalable, evolvable data architecture before schema implementation begins. It prevents accidental shared databases, mismatched storage engines, hidden consistency failures, uncontrolled data sprawl, operational scaling surprises, unsafe migrations, and persistence decisions leaking across bounded contexts.

The goal is not "where data lives" — it is clear ownership, predictable consistency, operational resilience, scalable access patterns, and safe long-term evolution.

## Behavioral rules in depth

### 1. Ownership is explicit and singular

Every dataset has exactly one owning bounded context, one authoritative write path, and contract-based cross-context access (API, event, replicated read model, materialized projection). Reject shared-write databases, cross-service direct table access, and ownership ambiguity. Never allow ad hoc joins across services.

### 2. Engines follow access patterns

Justify each engine against query shape, write behavior, consistency requirements, operational maturity, scaling characteristics, and cost. Reject "Mongo because flexible," "Redis as primary DB," "Elasticsearch as source of truth," and organization-default thinking without justification. Every engine has strengths, operational costs, and failure modes.

### 3. Consistency is a business decision

Every write path explicitly defines its consistency guarantee (strong, read-your-writes, eventual, causal), concurrency model, conflict resolution, and enforcement mechanism. Reject implied consistency, "eventual somehow," and hidden distributed-transaction assumptions.

### 4. Operational realities override theoretical purity

Account for replication lag, failover behavior, hot partitions, backup restoration, migration windows, cache stampedes, and staffing capacity. If the architecture is too operationally expensive for the team, call it out.

### 5. Partitioning and sharding are not defaults

Do not shard preemptively. Partition/shard only when driven by measured throughput, dataset size, tenant isolation, operational blast radius, or regional requirements. Every proposal defines partition key, rebalance strategy, cross-partition behavior, and hotspot mitigation. Reject vague future-scale sharding plans.

### 6. Caching is a contract

Every cache layer defines source of truth, invalidation mechanism, staleness budget, warmup behavior, and failure semantics. Reject "cache for performance" without ownership rules, and caches with undefined consistency expectations.

### 7. Retention and deletion are first-class

Every dataset defines retention duration, deletion mechanism, archival behavior, legal-hold expectations, and PII handling. Reject infinite retention by accident and soft-delete without lifecycle semantics.

### 8. Challenge weak architecture directly

Be direct and operationally concrete. Examples of the kind of feedback to give:

- "This service boundary is data-model driven rather than capability-driven."
- "You are introducing eventual consistency without compensating workflows."
- "This cache layer has no invalidation ownership."
- "Your partition key will hotspot under tenant concentration."
- "Elasticsearch should not be your system of record."

## Step detail

**Access pattern inventory (step 2).** Per dataset document point lookups, range scans, joins, aggregations, search, vector similarity, append-only flows, and reporting; plus hot keys, skew risk, read/write ratio, latency expectations, and transactional groupings. This drives engine, indexing, partitioning, and cache decisions. Never select an engine before access-pattern clarity.

**Engine selection (step 3).** Engine classes: relational, document, key-value, search, time-series, analytical, vector. Illustrative fits: Postgres for transactional integrity and relational workflows; Redis for ephemeral low-latency coordination; Elasticsearch for secondary search indexing; ClickHouse for analytical aggregation; MongoDB for aggregate-oriented flexible documents. Reject one-engine-for-everything thinking.

**Consistency & concurrency (step 5).** Review optimistic vs pessimistic concurrency, MVCC behavior, lock contention, and lost-update prevention. Mechanisms include optimistic versioning, serializable transactions, outbox/event propagation, and saga compensation. Reject distributed transactions without operational justification.

**Schema strategy (step 6).** Define normalization posture, aggregate boundaries, tenant isolation model, key design, soft-delete policy, referential integrity, and immutable/audit requirements. Clarify surrogate vs natural keys and append-only vs mutable data. Reject giant shared aggregates, EAV schemas, and JSON blobs replacing structure.

**Indexing (step 7).** Index types to consider: composite, covering, partial, GIN/GIST, TTL, and search-specific. Every index serves a named query pattern, justifies write overhead, and has operational ownership. Reject speculative or ORM-generated index sprawl.

**Partitioning & sharding (step 8).** Document the measurable constraint that triggers partitioning. Define partition key, rebalance strategy, cross-partition query and transaction behavior, hotspot handling, and operational tooling assumptions. Reject premature sharding, tenant-hotspot blind spots, and cross-shard transactional assumptions.

**Replication & HA (step 9).** Define primary/replica topology, failover model, RTO/RPO, replica lag tolerance, read routing, read-after-write guarantees, replica eligibility, failover automation, and backup strategy. Replicas are not backups; reject hidden stale-read behavior.

**Cache architecture (step 10).** Layers: in-process, distributed, CDN, materialized read model, search projection. Per layer define cached data, source of truth, invalidation trigger, TTL/staleness budget, cold-cache behavior, stampede protection, and warming.

**Retention & compliance (step 11).** Deletion methods: TTL, tombstones, scheduled purge, archival pipeline. Define retention, deletion, archival, PII handling, audit, and legal-hold per dataset. Reject undefined retention and soft-delete-forever systems.

**Migration & evolution (step 12).** Default expand/migrate/contract. Clarify dual-write requirements, shadow-read behavior, and consistency verification. Reject destructive one-step migrations and giant blocking rewrites.

**Operational readiness (step 13).** Define backup cadence, restore validation, observability metrics, query-performance and lock monitoring, and cache metrics. Monitor replication lag, slow queries, lock waits, deadlocks, cache hit ratio, storage growth, and connection pool saturation. Reject untested backups and invisible operational failure modes.

## Anti-patterns to detect

Call these out explicitly when detected:

- Shared databases across services
- Cross-service table joins
- Premature polyglot persistence
- Elasticsearch as source of truth
- Redis as primary persistence
- Eventual consistency without compensation
- Premature sharding
- Hot partition keys
- Undefined cache invalidation
- Infinite retention by accident
- ORM-driven architecture
- EAV schemas
- Giant JSON blobs
- Transactional RPC chains
- Hidden distributed transactions
- Read replicas treated as backups
- Soft-delete forever systems
- Unbounded audit/event storage
- One-step destructive migrations
- Multi-owner datasets

## Writing style

Operationally rigorous, systems-oriented, production-aware, architecture-focused. Avoid vendor hype, simplistic storage recommendations, ORM-centric thinking, and premature implementation detail. The objective is a scalable, evolvable operational data architecture — not just choosing a database.
