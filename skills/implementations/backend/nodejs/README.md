# implementations/backend/nodejs

Technology-specific execution skills for Node.js (TypeScript) backend services.

## Philosophy

Each Node.js skill speaks as a **senior Node.js engineer**. It generates production-ready code and configuration — it does not invent architectural decisions. [`architecture/backend-architecture`](../../../architecture/backend-architecture/SKILL.md) is the source of truth for framework choice, domain boundaries, data layer, and API/event contracts; [`architecture/security`](../../../architecture/security/SKILL.md), [`architecture/reliability`](../../../architecture/reliability/SKILL.md), and [`architecture/performance`](../../../architecture/performance/SKILL.md) own auth/secret, SLO, and budget decisions respectively. If an upstream artifact is silent on a decision a skill needs, the skill pauses and raises an ADR candidate rather than guessing.

One scaffold skill branches across Express, Fastify, and NestJS per the framework declared in `backend-architecture.md` — there is no per-framework split. Skills map to exactly one archetype and are additive: each extends the baseline `nodejs-service-scaffold` installs.

## Ecosystem

- Node.js 20+ LTS, TypeScript (`strict`)
- Express / Fastify / NestJS (framework-aware scaffold per architecture)
- Prisma / Drizzle / TypeORM, or the data layer declared by architecture
- BullMQ / KafkaJS / SQS for async work
- pino logging, OpenTelemetry JS SDK, prom-client
- Vitest/Jest + supertest + Testcontainers for testing

## Compatible patterns

- [microservices](../../../../architecture-patterns/microservices/README.md)
- [modular-monolith](../../../../architecture-patterns/modular-monolith/README.md)
- [event-driven](../../../../architecture-patterns/event-driven/README.md)

## Archetypes

| # | Archetype | Skill | Status |
|---|---|---|---|
| 1 | service-scaffold | [nodejs-service-scaffold/SKILL.md](nodejs-service-scaffold/SKILL.md) | ✓ authored |
| 2 | auth-and-security-review | [nodejs-auth-and-security-review/SKILL.md](nodejs-auth-and-security-review/SKILL.md) | ✓ authored |
| 3 | observability-readiness | [nodejs-observability-readiness/SKILL.md](nodejs-observability-readiness/SKILL.md) | ✓ authored |
| 4 | async-and-event-integration | [nodejs-queue-and-event-integration/SKILL.md](nodejs-queue-and-event-integration/SKILL.md) | ✓ authored |
| 5 | performance-and-resilience-engineering | [nodejs-performance-and-resilience/SKILL.md](nodejs-performance-and-resilience/SKILL.md) | ✓ authored |

## What each archetype owns

| Archetype | Owns | Defers |
|---|---|---|
| service-scaffold | Framework-aware layout (express/fastify/nest), validated config, structured logging seam, liveness/readiness probes, layered error handling, request context, DI shell, non-root container packaging | Auth flow → auth-and-security-review; observability vendor → observability-readiness; queue wiring → queue-and-event-integration; perf gates → performance-and-resilience |
| auth-and-security-review | Authentication flow (Passport/JWT/OAuth2/OIDC), default-deny authorization, helmet/CSP/HSTS, CSRF, boundary validation, secret handling, OWASP review, security tests | Service shell → service-scaffold; auth *provider* decision → `architecture/security` |
| observability-readiness | OpenTelemetry tracing, prom-client RED metrics, trace-correlated logs, SLI/SLO definitions, multi-burn-rate alert rules | SLO *targets* → `architecture/reliability`; logger/error code → service-scaffold |
| async-and-event-integration | BullMQ/KafkaJS/SQS producers and consumers, transactional outbox, idempotent consumers, retry/DLQ, Testcontainers tests | Broker/contract choice → `backend-architecture.md`; business domain logic |
| performance-and-resilience-engineering | Event-loop discipline, clustering/worker threads, backpressure, circuit breakers/bulkheads, retry budgets, CI load-test gate | Budget/SLO numbers → `architecture/performance` & `architecture/reliability`; observability vendor → observability-readiness |

## Upstream

All Node.js skills consume [`architecture/backend-architecture`](../../../architecture/backend-architecture/SKILL.md) as the primary upstream (framework, domain boundaries, data layer, contracts). [`architecture/security`](../../../architecture/security/SKILL.md) owns auth provider, session model, and secret handling; [`architecture/reliability`](../../../architecture/reliability/SKILL.md) owns SLO targets and the error budget; [`architecture/performance`](../../../architecture/performance/SKILL.md) owns latency/throughput budgets. Skills 2–5 also consume the `nodejs-service-scaffold` baseline. Operational alerts and runbooks feed [`architecture/operations`](../../../architecture/operations/SKILL.md).

## Standards

All Node.js skills conform to the applicable subset of:

- [api-standards](../../../../standards/api-standards/README.md) — contract, error shape, and status semantics.
- [security-standards](../../../../standards/security-standards/README.md) — no secrets in source/config/image; default-deny authorization; fail-fast config.
- [observability-standards](../../../../standards/observability-standards/README.md) — correlated structured logging; RED metrics; multi-burn-rate alerts.
- [deployment-standards](../../../../standards/deployment-standards/README.md) — env-agnostic non-root image; runtime config not baked.
- [naming-conventions](../../../../standards/naming-conventions/README.md) — service, module, and file naming.
