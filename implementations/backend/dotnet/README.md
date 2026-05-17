# dotnet

> Status: scaffold.

## Purpose

Implements `architecture/backend-architecture`, `architecture/security`, `architecture/reliability`, and `architecture/performance` using .NET 8+ (ASP.NET Core). Owns the canonical backend surface for this stack: service scaffold, auth and security review, observability readiness, async/event integration, and performance and resilience.

Architecture decisions (minimal API vs MVC, domain boundaries, idempotency and retry strategy, SLO targets) come from upstream and are taken as inputs here. If an upstream artifact is silent on a needed decision, the skill pauses and raises an ADR candidate rather than guessing.

## Ecosystem (target)

- .NET 8+ / ASP.NET Core, minimal API or MVC per architecture
- Options pattern, DI, layered configuration
- EF Core / Dapper, or the data layer declared by architecture
- MassTransit / Confluent.Kafka / Azure Service Bus / hosted services for async work
- OpenTelemetry .NET, Serilog, EventCounters, HealthChecks
- xUnit + Testcontainers for testing

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
| 1 | service-scaffold | `dotnet-service-scaffold` | planned |
| 2 | auth-and-security-review | `dotnet-auth-and-security-review` | planned |
| 3 | observability-readiness | `dotnet-observability-readiness` | planned |
| 4 | async-and-event-integration | `dotnet-async-and-event-integration` | planned |
| 5 | performance-and-resilience-engineering | `dotnet-performance-and-resilience` | planned |

### Planned skill scope (future work)

- **`dotnet-service-scaffold`** — minimal API or MVC, Options pattern, DI, layered configuration, structured logging, health probes, container packaging.
- **`dotnet-auth-and-security-review`** — ASP.NET Core Identity, JWT/OIDC, data protection, antiforgery, OWASP review, security tests.
- **`dotnet-observability-readiness`** — OTel .NET, Serilog, EventCounters, HealthChecks, RED metrics, SLI/SLO definitions, multi-burn-rate alerts.
- **`dotnet-async-and-event-integration`** — MassTransit/Confluent.Kafka/Azure Service Bus/hosted services, delivery semantics, transactional outbox, idempotency, retry/DLQ.
- **`dotnet-performance-and-resilience`** — Polly policies, channels, async patterns, GC profiling, timeouts/retries with budgets, load-test gates.

## Architecture domains implemented

| Architecture domain | How |
|---|---|
| [backend-architecture](../../../architecture/backend-architecture/SKILL.md) | Service shell, contracts, async integration. |
| [security](../../../architecture/security/SKILL.md) | ASP.NET Core Identity, data protection, secret handling. |
| [reliability](../../../architecture/reliability/SKILL.md) | SLOs, Polly resilience, degradation behavior. |
| [performance](../../../architecture/performance/SKILL.md) | Channels/async patterns, GC profiling, load-test gates. |
| [operations](../../../architecture/operations/SKILL.md) | Alerts, runbook inputs. |

## Standards this implementation conforms to

- [api-standards](../../../standards/api-standards/README.md)
- [security-standards](../../../standards/security-standards/README.md)
- [observability-standards](../../../standards/observability-standards/README.md)
- [deployment-standards](../../../standards/deployment-standards/README.md)
- [naming-conventions](../../../standards/naming-conventions/README.md)

## Upstream inputs

- Approved `backend-architecture.md` declaring API style, domain boundaries, API/event contracts, idempotency and retry strategy.
- Approved `architecture/security` decisions on auth provider, session model, and secret handling.
- Approved `architecture/reliability` decisions on SLOs and degradation behavior.
