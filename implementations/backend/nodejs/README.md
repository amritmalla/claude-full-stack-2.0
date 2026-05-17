# nodejs

> Status: scaffold.

## Purpose

Implements `architecture/backend-architecture`, `architecture/security`, `architecture/reliability`, and `architecture/performance` using Node.js. One scaffold skill branches across Express, Fastify, and NestJS per the framework declared in `backend-architecture` — there is no per-framework split.

Architecture decisions (framework choice, domain boundaries, idempotency and retry strategy, SLO targets) come from upstream and are taken as inputs here. If an upstream artifact is silent on a needed decision, the skill pauses and raises an ADR candidate rather than guessing.

## Ecosystem (target)

- Node.js 20+ LTS, TypeScript
- Express / Fastify / NestJS (framework-aware scaffold per architecture)
- Prisma / Drizzle / TypeORM, or the data layer declared by architecture
- BullMQ / KafkaJS / SQS for async work
- pino logging, OpenTelemetry JS SDK, prom-client
- Vitest/Jest + supertest + Testcontainers for testing

## Compatible patterns

- [microservices](../../../architecture-patterns/microservices/README.md)
- [modular-monolith](../../../architecture-patterns/modular-monolith/README.md)
- [event-driven](../../../architecture-patterns/event-driven/README.md)

## Skills

### Authored

_None._

### Archetype coverage

| # | Archetype | Skill | Status |
|---|---|---|---|
| 1 | service-scaffold | `nodejs-service-scaffold` | planned |
| 2 | auth-and-security-review | `nodejs-auth-and-security-review` | planned |
| 3 | observability-readiness | `nodejs-observability-readiness` | planned |
| 4 | async-and-event-integration | `nodejs-queue-and-event-integration` | planned |
| 5 | performance-and-resilience-engineering | `nodejs-performance-and-resilience` | planned |

### Planned skill scope (future work)

- **`nodejs-service-scaffold`** — framework-aware layout (express/fastify/nest), env/config handling, structured logging, health probes, error handling, container packaging.
- **`nodejs-auth-and-security-review`** — Passport/JWT/OAuth, helmet, OWASP review, secret handling, security tests.
- **`nodejs-observability-readiness`** — pino + OTel JS SDK + prom-client, RED metrics, trace-correlated logs, SLI/SLO definitions, multi-burn-rate alerts.
- **`nodejs-queue-and-event-integration`** — BullMQ/KafkaJS/SQS wiring, delivery semantics, transactional outbox, idempotency, retry/DLQ, integration tests.
- **`nodejs-performance-and-resilience`** — event-loop discipline, clustering, backpressure, circuit breakers, timeouts/retries with budgets, load-test gates.

## Architecture domains implemented

| Architecture domain | How |
|---|---|
| [backend-architecture](../../../architecture/backend-architecture/SKILL.md) | Service shell, contracts, async integration. |
| [security](../../../architecture/security/SKILL.md) | Auth flows, helmet, secret handling. |
| [reliability](../../../architecture/reliability/SKILL.md) | SLOs, retries, degradation behavior. |
| [performance](../../../architecture/performance/SKILL.md) | Event-loop/backpressure discipline, load-test gates. |
| [operations](../../../architecture/operations/SKILL.md) | Alerts, runbook inputs. |

## Standards this implementation conforms to

- [api-standards](../../../standards/api-standards/README.md)
- [security-standards](../../../standards/security-standards/README.md)
- [observability-standards](../../../standards/observability-standards/README.md)
- [deployment-standards](../../../standards/deployment-standards/README.md)
- [naming-conventions](../../../standards/naming-conventions/README.md)

## Upstream inputs

- Approved `backend-architecture.md` declaring framework choice, domain boundaries, API/event contracts, idempotency and retry strategy.
- Approved `architecture/security` decisions on auth provider, session model, and secret handling.
- Approved `architecture/reliability` decisions on SLOs and degradation behavior.
