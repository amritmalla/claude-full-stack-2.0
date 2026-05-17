# fastapi

> Status: scaffold.

## Purpose

Implements `architecture/backend-architecture`, `architecture/security`, `architecture/reliability`, and `architecture/performance` using FastAPI (Python). Owns the canonical backend surface for this stack: service scaffold, auth and security review, observability readiness, async/task integration, and performance and resilience.

Architecture decisions (domain boundaries, idempotency and retry strategy, SLO targets, degradation behavior) come from upstream and are taken as inputs here. If an upstream artifact is silent on a needed decision, the skill pauses and raises an ADR candidate rather than guessing.

## Ecosystem (target)

- FastAPI (Python 3.11+), Pydantic v2, Starlette
- Uvicorn/Gunicorn with `uvicorn.workers`, ASGI lifespan
- SQLAlchemy 2.x + Alembic, or the data layer declared by architecture
- Celery / RQ / arq (or Kafka per architecture) for async work
- OpenTelemetry Python SDK, structured logging (structlog), Prometheus client
- pytest + httpx + Testcontainers for testing

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
| 1 | service-scaffold | `fastapi-service-scaffold` | planned |
| 2 | auth-and-security-review | `fastapi-auth-and-security-review` | planned |
| 3 | observability-readiness | `fastapi-observability-readiness` | planned |
| 4 | async-and-event-integration | `fastapi-async-and-task-integration` | planned |
| 5 | performance-and-resilience-engineering | `fastapi-performance-and-resilience` | planned |

### Planned skill scope (future work)

- **`fastapi-service-scaffold`** — project layout, profile-aware settings (Pydantic Settings), structured logging, health/readiness probes, error handling, ASGI lifespan, container packaging.
- **`fastapi-auth-and-security-review`** — OAuth2/OIDC and API-key flows, dependency-based authz, secret handling, OWASP review, security tests.
- **`fastapi-observability-readiness`** — OTel tracing, RED metrics, trace-correlated logs, SLI/SLO definitions, multi-burn-rate alerts.
- **`fastapi-async-and-task-integration`** — Celery/RQ/arq or Kafka wiring, delivery semantics, transactional outbox, idempotency, retry/DLQ, integration tests.
- **`fastapi-performance-and-resilience`** — timeouts, retries with budgets, circuit breakers, connection-pool sizing, caching posture, load-test gates.

## Architecture domains implemented

| Architecture domain | How |
|---|---|
| [backend-architecture](../../../architecture/backend-architecture/SKILL.md) | Service shell, contracts, async integration. |
| [security](../../../architecture/security/SKILL.md) | Auth flows, secret handling, trust boundaries. |
| [reliability](../../../architecture/reliability/SKILL.md) | SLOs, retries, degradation behavior. |
| [performance](../../../architecture/performance/SKILL.md) | Pool sizing, caching, load-test gates. |
| [operations](../../../architecture/operations/SKILL.md) | Alerts, runbook inputs. |

## Standards this implementation conforms to

- [api-standards](../../../standards/api-standards/README.md)
- [security-standards](../../../standards/security-standards/README.md)
- [observability-standards](../../../standards/observability-standards/README.md)
- [deployment-standards](../../../standards/deployment-standards/README.md)
- [naming-conventions](../../../standards/naming-conventions/README.md)

## Upstream inputs

- Approved `backend-architecture.md` declaring domain boundaries, API/event contracts, idempotency and retry strategy.
- Approved `architecture/security` decisions on auth provider, session model, and secret handling.
- Approved `architecture/reliability` decisions on SLOs and degradation behavior.
