# django

> Status: scaffold.

## Purpose

Implements `architecture/backend-architecture`, `architecture/security`, `architecture/reliability`, and `architecture/performance` using Django (Python), with Django REST Framework when a REST surface is exposed. Owns the canonical backend surface for this stack: service scaffold, auth and security review, observability readiness, event integration, and performance and resilience.

Architecture decisions (domain boundaries, idempotency and retry strategy, SLO targets, degradation behavior) come from upstream and are taken as inputs here. If an upstream artifact is silent on a needed decision, the skill pauses and raises an ADR candidate rather than guessing.

## Ecosystem (target)

- Django 5.x, Django REST Framework (when REST is exposed)
- Gunicorn/Uvicorn (ASGI), settings-per-environment layout
- Django ORM + migrations, or the data layer declared by architecture
- Celery (or the broker declared by architecture) for async work
- OpenTelemetry Python SDK, structured logging, Prometheus client
- pytest-django + Testcontainers for testing

## Compatible patterns

- [microservices](../../../../architecture-patterns/microservices/README.md)
- [modular-monolith](../../../../architecture-patterns/modular-monolith/README.md)
- [event-driven](../../../../architecture-patterns/event-driven/README.md)

## Skills

### Authored

_None._

### Archetype coverage

| # | Archetype | Skill | Status |
|---|---|---|---|
| 1 | service-scaffold | `django-service-scaffold` | planned |
| 2 | auth-and-security-review | `django-auth-and-security-review` | planned |
| 3 | observability-readiness | `django-observability-readiness` | planned |
| 4 | async-and-event-integration | `django-celery-and-event-integration` | planned |
| 5 | performance-and-resilience-engineering | `django-performance-and-resilience` | planned |

### Planned skill scope (future work)

- **`django-service-scaffold`** — settings layout, apps structure, DRF when REST is exposed, structured logging, health probes, error handling, container packaging.
- **`django-auth-and-security-review`** — auth backends, CSRF, permissions, DRF auth classes, secret handling, OWASP review, security tests.
- **`django-observability-readiness`** — OTel tracing, RED metrics, trace-correlated logs, SLI/SLO definitions, multi-burn-rate alerts.
- **`django-celery-and-event-integration`** — Celery wiring, delivery semantics, transactional outbox, idempotency, retry/DLQ, integration tests.
- **`django-performance-and-resilience`** — ORM query discipline, caching, channel layers, timeouts, retries with budgets, load-test gates.

## Architecture domains implemented

| Architecture domain | How |
|---|---|
| [backend-architecture](../../../architecture/backend-architecture/SKILL.md) | Service shell, contracts, async integration. |
| [security](../../../architecture/security/SKILL.md) | Auth backends, CSRF, permissions, secret handling. |
| [reliability](../../../architecture/reliability/SKILL.md) | SLOs, retries, degradation behavior. |
| [performance](../../../architecture/performance/SKILL.md) | ORM/caching discipline, load-test gates. |
| [operations](../../../architecture/operations/SKILL.md) | Alerts, runbook inputs. |

## Standards this implementation conforms to

- [api-standards](../../../../standards/api-standards/README.md)
- [security-standards](../../../../standards/security-standards/README.md)
- [observability-standards](../../../../standards/observability-standards/README.md)
- [deployment-standards](../../../../standards/deployment-standards/README.md)
- [naming-conventions](../../../../standards/naming-conventions/README.md)

## Upstream inputs

- Approved `backend-architecture.md` declaring domain boundaries, API/event contracts, idempotency and retry strategy.
- Approved `architecture/security` decisions on auth provider, session model, and secret handling.
- Approved `architecture/reliability` decisions on SLOs and degradation behavior.
