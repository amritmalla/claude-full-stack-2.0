# elasticsearch

> Status: scaffold.

## Purpose

Implements `architecture/data-architecture` for Elasticsearch as a search and analytics engine: mapping and analyzer design, query and relevance tuning, cluster and shard topology, snapshot/restore posture, and access hardening.

Architecture decisions (which workloads use Elasticsearch, ingestion path, tiering strategy, tenant isolation, retention) come from upstream and are taken as inputs here.

## Engine family

Elasticsearch belongs to **Family D — Search** in the data layer model. See [`implementations/data/README.md`](../README.md) for the full archetype set and philosophy.

## Ecosystem (target)

- Elasticsearch 8.x (or OpenSearch where dictated by architecture)
- Index Lifecycle Management (ILM)
- Snapshot repositories (S3 / GCS / Azure Blob / shared filesystem)
- Security features (roles, document-level security, field-level security, audit logging)
- Ingest pipelines and Logstash/Beats where part of the architecture

## Compatible patterns

- [microservices](../../../architecture-patterns/microservices/README.md)
- [cqrs](../../../architecture-patterns/cqrs/README.md) (search-side read model)
- [event-driven](../../../architecture-patterns/event-driven/README.md) (event-driven index updates)

## Skills

### Authored

_None._

### Archetype coverage

| # | Archetype | Skill | Status |
|---|---|---|---|
| 1 | index-mapping-and-analyzer-design | `elasticsearch-index-mapping-and-analyzer-design` | planned |
| 2 | query-and-relevance-tuning | `elasticsearch-query-and-relevance-tuning` | planned |
| 3 | cluster-and-shard-topology | `elasticsearch-cluster-and-shard-topology` | planned |
| 4 | backup-and-operational-readiness | `elasticsearch-backup-and-operational-readiness` | planned |
| 5 | security-and-data-access-hardening | `elasticsearch-security-and-data-access-hardening` | planned |

### Planned skill scope (future work)

- **`elasticsearch-index-mapping-and-analyzer-design`** — explicit mapping over dynamic, field-type selection (`keyword` vs `text` vs `numeric` vs `date`), analyzer/tokenizer/filter chains for each `text` field, multi-field strategy (e.g. `text` plus `keyword`), `doc_values` and `fielddata` discipline, runtime fields posture, alias and index-template strategy, reindex-as-migration plan.
- **`elasticsearch-query-and-relevance-tuning`** — query DSL review (`bool`, `function_score`, `dis_max`, `rescore`), `_profile`-driven optimization, scoring and relevance tuning, aggregation cost review (cardinality, terms, composite), search-template and query-rewrite posture, kNN/vector-search posture where applicable.
- **`elasticsearch-cluster-and-shard-topology`** — primary/replica shard sizing tied to index size and query latency, ILM policy (hot → warm → cold → frozen → delete), rollover strategy (size, age, document count), shard-allocation awareness (zone/rack), dedicated master/data/ingest/coordinating nodes, cross-cluster replication and search where relevant.
- **`elasticsearch-backup-and-operational-readiness`** — snapshot repository configuration (S3/GCS/Azure/shared FS), SLM snapshot lifecycle policy, restore drills with documented RPO/RTO, cluster-health (`yellow`/`red`) and shard-allocation observability, runbook inputs (unassigned shards, master loss, disk-watermark breach, ILM stall).
- **`elasticsearch-security-and-data-access-hardening`** — TLS and node-to-node encryption, role-based access, document-level security for tenant isolation, field-level security for PII, API-key vs user-credential posture, audit-log configuration, IP allowlist, anonymous-access prohibition.

## Architecture domains implemented

| Architecture domain | How |
|---|---|
| [data-architecture](../../../architecture/data-architecture/README.md) | Mapping, analyzer design, index topology, retention via ILM. |
| [reliability](../../../architecture/reliability/README.md) | Shard topology, replica counts, snapshot/restore posture. |
| [performance](../../../architecture/performance/README.md) | Query review, relevance tuning, aggregation cost control. |
| [security](../../../architecture/security/README.md) | Roles, DLS/FLS, TLS, audit, network exposure. |

## Standards this implementation conforms to

- [architecture-schema](../../../standards/architecture-schema/README.md) — index ownership: each index/alias is owned by exactly one component.
- [naming-conventions](../../../standards/naming-conventions/README.md) — kebab-case index names with date or rollover suffix; alias-first read paths.
- [security-standards](../../../standards/security-standards/README.md) — TLS, DLS/FLS for tenant and PII isolation, audit.
- [observability-standards](../../../standards/observability-standards/README.md) — cluster health, shard allocation, query latency, ingest rate, indexing back-pressure signals.

## Upstream inputs

- Approved `data-architecture.md` selecting Elasticsearch for specific workloads and declaring tiering, retention, tenant-isolation, and ingestion path.
- `backend-architecture.md` for search-contract direction, index-update semantics (event-driven vs polled vs sync), and idempotency posture.
