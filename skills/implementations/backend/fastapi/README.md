# implementations/backend/fastapi

Technology-specific execution skills for FastAPI (Python) backend services.

## Philosophy

Each FastAPI skill speaks as a **senior FastAPI/Python engineer**. It generates production-ready code and configuration — it does not invent architectural decisions. [`architecture/backend-architecture`](../../../architecture/backend-architecture/SKILL.md) is the source of truth for domain boundaries, data layer, and API/event contracts; [`architecture/security`](../../../architecture/security/SKILL.md), [`architecture/reliability`](../../../architecture/reliability/SKILL.md), and [`architecture/performance`](../../../architecture/performance/SKILL.md) own auth/secret, SLO, and budget decisions respectively. If an upstream artifact is silent on a decision a skill needs, the skill pauses and raises an ADR candidate rather than guessing.

FastAPI is a single framework — there is no framework branching. Skills map to exactly one archetype and are additive: each extends the baseline `fastapi-service-scaffold` installs.

## Ecosystem

- FastAPI (Python 3.11+), Pydantic v2, Starlette
- Uvicorn/Gunicorn with `uvicorn.workers`, ASGI lifespan
- SQLAlchemy 2.x + Alembic, or the data layer declared by architecture
- Celery / RQ / arq (or Kafka per architecture) for async work
- OpenTelemetry Python SDK, structlog, prometheus-client
- pytest + httpx + Testcontainers for testing
- pinned deps with a hashed lockfile; `ruff` + `mypy`

## Compatible patterns

- [microservices](../../../../architecture-patterns/microservices/README.md)
- [modular-monolith](../../../../architecture-patterns/modular-monolith/README.md)
- [event-driven](../../../../architecture-patterns/event-driven/README.md)

## Archetypes

| # | Archetype | Skill | Status |
|---|---|---|---|
| 1 | service-scaffold | [fastapi-service-scaffold/SKILL.md](fastapi-service-scaffold/SKILL.md) | ✓ authored |
| 2 | auth-and-security-review | [fastapi-auth-and-security-review/SKILL.md](fastapi-auth-and-security-review/SKILL.md) | ✓ authored |
| 3 | observability-readiness | [fastapi-observability-readiness/SKILL.md](fastapi-observability-readiness/SKILL.md) | ✓ authored |
| 4 | async-and-event-integration | [fastapi-async-and-task-integration/SKILL.md](fastapi-async-and-task-integration/SKILL.md) | ✓ authored |
| 5 | performance-and-resilience-engineering | [fastapi-performance-and-resilience/SKILL.md](fastapi-performance-and-resilience/SKILL.md) | ✓ authored |

## What each archetype owns

| Archetype | Owns | Defers |
|---|---|---|
| service-scaffold | Project layout, Pydantic Settings config, structlog seam + request context, liveness/readiness probes, layered error handling, ASGI lifespan, `Depends` DI shell + principal seam, non-root container | Auth flow → auth-and-security-review; observability vendor → observability-readiness; task wiring → async-and-task-integration; perf gates → performance-and-resilience; data client → data layer |
| auth-and-security-review | OAuth2/OIDC + API-key flows, dependency-based default-deny authz, secure headers, Pydantic boundary validation, secret handling, OWASP review, security tests | Service shell → service-scaffold; auth *provider* decision → `architecture/security` |
| observability-readiness | OpenTelemetry tracing, prometheus-client RED metrics, trace-correlated structlog, SLI/SLO definitions, multi-burn-rate alert rules | SLO *targets* → `architecture/reliability`; logger/error code → service-scaffold |
| async-and-event-integration | Celery/RQ/arq or Kafka producers and consumers, transactional outbox, idempotent tasks, retry/DLQ, Testcontainers tests | Broker/contract choice → `backend-architecture.md`; business domain logic |
| performance-and-resilience-engineering | Async-path discipline, worker model, connection-pool sizing, caching posture, circuit breakers/bulkheads, retry budgets, CI load-test gate | Budget/SLO numbers → `architecture/performance` & `architecture/reliability`; observability vendor → observability-readiness |

## Upstream

All FastAPI skills consume [`architecture/backend-architecture`](../../../architecture/backend-architecture/SKILL.md) as the primary upstream (domain boundaries, data layer, contracts). [`architecture/security`](../../../architecture/security/SKILL.md) owns auth provider, session model, and secret handling; [`architecture/reliability`](../../../architecture/reliability/SKILL.md) owns SLO targets and the error budget; [`architecture/performance`](../../../architecture/performance/SKILL.md) owns latency/throughput budgets and pool sizing. Skills 2–5 also consume the `fastapi-service-scaffold` baseline. Operational alerts and runbooks feed [`architecture/operations`](../../../architecture/operations/SKILL.md).

## Standards

All FastAPI skills conform to the applicable subset of:

- [api-standards](../../../../standards/api-standards/README.md) — contract, error shape, and status semantics.
- [security-standards](../../../../standards/security-standards/README.md) — no secrets in source/settings/image; default-deny authorization; fail-fast settings.
- [observability-standards](../../../../standards/observability-standards/README.md) — correlated structured logging; RED metrics; multi-burn-rate alerts.
- [deployment-standards](../../../../standards/deployment-standards/README.md) — env-agnostic non-root image; runtime config not baked.
- [naming-conventions](../../../../standards/naming-conventions/README.md) — service, module, and file naming.
