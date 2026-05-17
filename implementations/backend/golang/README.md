# golang

> Status: scaffold.

## Purpose

Implements `architecture/backend-architecture`, `architecture/security`, `architecture/reliability`, and `architecture/performance` using Go. Owns the canonical backend surface for this stack: service scaffold, auth and security review, observability readiness, async/event integration, and performance and resilience.

Architecture decisions (router/framework choice, domain boundaries, idempotency and retry strategy, SLO targets) come from upstream and are taken as inputs here. If an upstream artifact is silent on a needed decision, the skill pauses and raises an ADR candidate rather than guessing.

## Ecosystem (target)

- Go 1.22+, stdlib `net/http` or chi/echo/gin per architecture
- `context` propagation, graceful shutdown, `errgroup`
- sqlc / pgx / GORM, or the data layer declared by architecture
- sarama / kafka-go / NATS / SQS for async work
- OpenTelemetry Go SDK, `log/slog`, Prometheus client
- `testing` + Testcontainers-go for testing

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
| 1 | service-scaffold | `golang-service-scaffold` | planned |
| 2 | auth-and-security-review | `golang-auth-and-security-review` | planned |
| 3 | observability-readiness | `golang-observability-readiness` | planned |
| 4 | async-and-event-integration | `golang-async-and-event-integration` | planned |
| 5 | performance-and-resilience-engineering | `golang-performance-and-resilience` | planned |

### Planned skill scope (future work)

- **`golang-service-scaffold`** — stdlib `http` or chi/echo/gin per architecture, context plumbing, graceful shutdown, structured `slog`, health probes, container packaging.
- **`golang-auth-and-security-review`** — middleware-based authn/authz, JWT/OAuth, mTLS, crypto review, secret handling, security tests.
- **`golang-observability-readiness`** — OTel Go SDK, `slog`, Prometheus, RED metrics, SLI/SLO definitions, multi-burn-rate alerts.
- **`golang-async-and-event-integration`** — sarama/kafka-go/NATS/SQS wiring, worker fan-out, delivery semantics, transactional outbox, idempotency, retry/DLQ.
- **`golang-performance-and-resilience`** — goroutine discipline, context cancellation, rate limiting, circuit breakers, pprof-driven tuning, load-test gates.

## Architecture domains implemented

| Architecture domain | How |
|---|---|
| [backend-architecture](../../../architecture/backend-architecture/SKILL.md) | Service shell, contracts, async integration. |
| [security](../../../architecture/security/SKILL.md) | Middleware authn/authz, mTLS, secret handling. |
| [reliability](../../../architecture/reliability/SKILL.md) | SLOs, retries, degradation behavior. |
| [performance](../../../architecture/performance/SKILL.md) | Goroutine/context discipline, pprof, load-test gates. |
| [operations](../../../architecture/operations/SKILL.md) | Alerts, runbook inputs. |

## Standards this implementation conforms to

- [api-standards](../../../standards/api-standards/README.md)
- [security-standards](../../../standards/security-standards/README.md)
- [observability-standards](../../../standards/observability-standards/README.md)
- [deployment-standards](../../../standards/deployment-standards/README.md)
- [naming-conventions](../../../standards/naming-conventions/README.md)

## Upstream inputs

- Approved `backend-architecture.md` declaring router/framework choice, domain boundaries, API/event contracts, idempotency and retry strategy.
- Approved `architecture/security` decisions on auth provider, session model, and secret handling.
- Approved `architecture/reliability` decisions on SLOs and degradation behavior.
