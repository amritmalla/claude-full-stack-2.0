# backend-architecture

> Status: draft

## Purpose

Defines backend execution architecture and service behavior from an approved system design: service boundaries, domain behavior, API and async contracts, transactional boundaries, consistency rules, security touchpoints, and implementation handoffs.

Technology-agnostic. Owns *what* a backend service exposes and *how* it behaves, not the framework that runs it. Framework-specific scaffolding lives under [implementations/backend](../../implementations/backend/).

## Owns

- REST / GraphQL / event contracts
- Domain models and aggregates
- Commands, queries, lifecycle states, and invariants
- Transactional boundaries and consistency rules
- Async workflows, queues, jobs, retries, and compensations
- Idempotency and concurrency semantics
- Service-to-service communication patterns
- Backend security and operational touchpoints

## Produces

| Artifact | Conforms to |
|---|---|
| `backend-architecture.md` | [architecture-schema](../../standards/architecture-schema/README.md), [documentation-standards](../../standards/documentation-standards/README.md) |
| `openapi.yaml` (REST contracts, when needed) | [api-standards](../../standards/api-standards/README.md) |
| `api-conventions.md` (REST conventions, when needed) | [api-standards](../../standards/api-standards/README.md), [naming-conventions](../../standards/naming-conventions/README.md) |
| Event/job/workflow notes | [api-standards async/event rules](../../standards/api-standards/README.md) |

## Skills

- [backend-architecture](SKILL.md) - turns approved system design into backend service architecture: boundaries, domain behavior, interface strategy, transactions, consistency, security touchpoints, operations, and implementation handoff notes.

## Standards this architecture domain conforms to

- [architecture-schema](../../standards/architecture-schema/README.md) - system-design traceability and decision structure.
- [api-standards](../../standards/api-standards/README.md) - global REST/async contract rules.
- [security-standards](../../standards/security-standards/README.md) - auth schemes, scopes, secrets.
- [naming-conventions](../../standards/naming-conventions/README.md) - path segments, identifiers, topics.
- [documentation-standards](../../standards/documentation-standards/README.md) - skill structure.

## Upstream inputs

Requires an approved `system-design.md` per [architecture-schema](../../standards/architecture-schema/README.md). Bounded contexts, component interfaces, data ownership, and ADRs in the system design shape the backend architecture produced here.

## Downstream consumers

Backend architecture produced here is the source of truth for:

- [implementations/backend/*](../../implementations/backend/) - server scaffolds, modules, controllers, DTOs, workers, and integration points follow the backend architecture.
- [implementations/data/*](../../implementations/data/) - schema and migration skills consume ownership, transaction, and consistency decisions.
- [implementations/frontend/*](../../implementations/frontend/) - client SDKs and typed fetch layers consume published contracts.
- [architecture/quality-engineering](../quality-engineering/README.md) - contract-driven and workflow-driven integration tests.
