# data-architecture

> Status: draft

## Purpose

Defines the operational data layer from an approved system design: data ownership boundaries, engine selection, consistency model, schema strategy, indexing posture, partitioning and replication topology, cache architecture, retention and deletion policy, and migration strategy.

Technology-agnostic and operationally focused. Owns *which* datasets exist, *who* owns them, and *how* they behave operationally, not the engine-specific DDL that implements them. Engine-specific schema and migration work lives under [implementations/data](../../implementations/data/).

## Owns

- Dataset ownership boundaries and authoritative write paths
- Engine selection justified by access patterns
- Consistency and concurrency model per write path
- Schema, key design, and tenant isolation strategy
- Indexing posture mapped to named access patterns
- Partitioning/sharding posture and replication/HA topology
- Cache architecture and invalidation contracts
- Retention, deletion, and compliance policy
- Migration strategy and operational readiness

## Produces

| Artifact | Conforms to |
|---|---|
| `data-architecture.md` | [architecture-schema](../../standards/architecture-schema/README.md), [documentation-standards](../../standards/documentation-standards/README.md) |
| ADR drafts (engine, consistency, partitioning, replication, retention) | [architecture-schema](../../standards/architecture-schema/README.md) |

## Skills

- [data-architecture](SKILL.md) - turns an approved system design into operational data architecture: ownership boundaries, engine selection, consistency, schema, indexing, partitioning, replication, cache, retention, migration, operations, and implementation handoffs.

## Standards this architecture domain conforms to

- [architecture-schema](../../standards/architecture-schema/README.md) - `data-architecture.md` artifact structure and system-design traceability.
- [security-standards](../../standards/security-standards/README.md) - tenant isolation, PII handling, encryption, audit.
- [observability-standards](../../standards/observability-standards/README.md) - data-layer monitoring signals.
- [deployment-standards](../../standards/deployment-standards/README.md) - migration phasing and rollback.
- [documentation-standards](../../standards/documentation-standards/README.md) - skill structure.

## Upstream inputs

Requires an approved `system-design.md` per [architecture-schema](../../standards/architecture-schema/README.md) whose design declares bounded contexts and data ownership. Those boundaries, component interfaces, and ADRs shape the data architecture produced here.

## Downstream consumers

Data architecture produced here is the source of truth for:

- [implementations/data/*](../../implementations/data/) - Postgres, MongoDB, Redis, Elasticsearch, and ClickHouse schema and migration skills follow ownership, consistency, and indexing decisions.
- [architecture/backend-architecture](../backend-architecture/README.md) - transactional boundaries and consistency expectations.
- [architecture/ai-native-engineering](../ai-native-engineering/README.md) - retrieval corpora ownership and ingestion lifecycle.
- [architecture/security](../security/SKILL.md) - tenant isolation, retention, and audit boundaries.
