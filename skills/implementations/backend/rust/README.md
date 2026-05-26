# rust

> Status: scaffold; 1/5 archetypes authored.

## Purpose

Implements `architecture/backend-architecture`, `architecture/security`, `architecture/reliability`, and `architecture/performance` using Rust. Owns the canonical backend surface for this stack: service scaffold, auth and security review, observability readiness, async/event integration, and performance and resilience.

Architecture decisions (framework choice, domain boundaries, idempotency and retry strategy, SLO targets) come from upstream and are taken as inputs here. If an upstream artifact is silent on a needed decision, the skill pauses and raises an ADR candidate rather than guessing.

## Ecosystem (target)

- Rust stable (latest), 2021 edition
- `tokio` async runtime; `axum` (default) or `actix-web` per architecture
- `tower` / `tower-http` middleware layers
- `tracing` + `tracing-subscriber` (JSON in non-dev), `tracing-opentelemetry`
- `config` (figment) for layered configuration; `serde` for typed config
- `sqlx` (compile-time checked) or `sea-orm`/`diesel` per architecture; `refinery` or `sqlx migrate` for migrations
- `rdkafka` / `lapin` / `aws-sdk-sqs` for async integration
- `metrics` + `metrics-exporter-prometheus`
- `thiserror` for library errors, `anyhow` for application errors
- `tokio::test` + `testcontainers-rs` for integration tests

## Compatible patterns

- [microservices](../../../../architecture-patterns/microservices/README.md)
- [modular-monolith](../../../../architecture-patterns/modular-monolith/README.md)
- [event-driven](../../../../architecture-patterns/event-driven/README.md)

## Skills

### Authored

- [rust-service-scaffold](rust-service-scaffold/) — draft.

### Archetype coverage

| # | Archetype | Skill | Status |
|---|---|---|---|
| 1 | service-scaffold | `rust-service-scaffold` | authored (draft) |
| 2 | auth-and-security-review | `rust-auth-and-security-review` | planned |
| 3 | observability-readiness | `rust-observability-readiness` | planned |
| 4 | async-and-event-integration | `rust-async-and-event-integration` | planned |
| 5 | performance-and-resilience-engineering | `rust-performance-and-resilience` | planned |

### Planned skill scope (future work)

- **`rust-auth-and-security-review`** — `tower-http` auth layers, JWT via `jsonwebtoken`, OAuth via `oauth2`, rustls, password hashing with `argon2`, secret handling, security tests.
- **`rust-observability-readiness`** — `tracing` + `tracing-opentelemetry`, OTel Rust SDK, `metrics` + `metrics-exporter-prometheus`, RED metrics, SLI/SLO definitions, multi-burn-rate alerts.
- **`rust-async-and-event-integration`** — `rdkafka` / `lapin` / `aws-sdk-sqs` wiring, worker fan-out via `tokio::spawn`, delivery semantics, transactional outbox, idempotency, retry/DLQ topology.
- **`rust-performance-and-resilience`** — tokio runtime tuning, `tower` layers for timeout/retry/concurrency-limit, circuit breakers, connection-pool sizing, `tokio-console`, `flamegraph`-driven tuning, load-test gates.

## Architecture domains implemented

| Architecture domain | How |
|---|---|
| [backend-architecture](../../../architecture/backend-architecture/SKILL.md) | Service shell, contracts, async integration. |
| [security](../../../architecture/security/SKILL.md) | Middleware authn/authz, rustls, secret handling. |
| [reliability](../../../architecture/reliability/SKILL.md) | SLOs, retries, degradation behavior via `tower`. |
| [performance](../../../architecture/performance/SKILL.md) | Tokio runtime discipline, pool sizing, profiling. |
| [operations](../../../architecture/operations/SKILL.md) | Alerts, runbook inputs. |

## Standards this implementation conforms to

- [api-standards](../../../../standards/api-standards/README.md)
- [security-standards](../../../../standards/security-standards/README.md)
- [observability-standards](../../../../standards/observability-standards/README.md)
- [deployment-standards](../../../../standards/deployment-standards/README.md)
- [naming-conventions](../../../../standards/naming-conventions/README.md)

## Upstream inputs

- Approved `backend-architecture.md` declaring framework choice (axum vs actix-web), domain boundaries, API/event contracts, idempotency and retry strategy.
- Approved `architecture/security` decisions on auth provider, session model, and secret handling.
- Approved `architecture/reliability` decisions on SLOs and degradation behavior.
