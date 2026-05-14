# backend-systems

> Status: draft

## Purpose

Defines backend execution architecture and service behavior: API contracts, async workflows, domain modeling, transactional boundaries, and execution semantics.

Technology-agnostic. Owns *what* a backend service exposes and *how* it behaves, not the framework that runs it. Framework-specific scaffolding lives under [implementations/backend](../../implementations/backend/).

## Owns

- REST / GraphQL / event contracts
- Domain models and aggregates
- Transactional boundaries
- Async workflows, queues, jobs
- Idempotency and retry semantics
- Service-to-service communication patterns

## Produces

| Artifact | Conforms to |
|---|---|
| `openapi.yaml` (REST contracts) | [api-standards](../../standards/api-standards/README.md) |
| `api-conventions.md` (per-service applied conventions) | [api-standards](../../standards/api-standards/README.md), [naming-conventions](../../standards/naming-conventions/README.md) |
| Domain model docs | TBD |
| Event schemas | [api-standards § Async / event APIs](../../standards/api-standards/README.md) |

## Skills

- [rest-api-contract-design](rest-api-contract-design/SKILL.md) — designs OpenAPI 3.1 REST contracts with resource modeling, standardized errors, cursor pagination, idempotency semantics, versioning, and per-service conventions.

## Standards this capability conforms to

- [api-standards](../../standards/api-standards/README.md) — global REST/async contract rules.
- [security-standards](../../standards/security-standards/README.md) — auth schemes, scopes, secrets.
- [naming-conventions](../../standards/naming-conventions/README.md) — path segments, identifiers, topics.
- [documentation-standards](../../standards/documentation-standards/README.md) — skill structure.

## Upstream inputs

Requires an approved `system-design.md` per [architecture-schema](../../standards/architecture-schema/README.md). Bounded contexts and component interfaces in the system design shape the contracts produced here.

## Downstream consumers

API contracts produced here are the source of truth for:

- [implementations/backend/*](../../implementations/backend/) — server scaffolds and DTOs are generated from the OpenAPI spec, not the other way around.
- [implementations/frontend/*](../../implementations/frontend/) — client SDKs and typed fetch layers.
- [capabilities/testing-quality](../testing-quality/README.md) — contract-driven integration tests.
