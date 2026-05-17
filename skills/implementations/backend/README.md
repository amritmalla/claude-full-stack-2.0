# implementations/backend

Technology-specific execution skills for backend.

## Philosophy

Each backend implementation skill speaks as a **senior engineer in a specific stack**. It implements, hardens, or reviews — it does not invent architectural decisions. Architecture artifacts produced by `architecture/backend-architecture`, `architecture/reliability`, `architecture/performance`, and `architecture/security` are the source of truth; the implementation skill consumes them and emits code, configuration, migrations, tests, and runbook inputs.

If an artifact is silent on a needed decision (idempotency key, retry budget, degradation behavior, SLO target), the implementation skill **pauses and raises an ADR candidate** against the upstream domain rather than guessing.

Skills are scoped, not monolithic. Each `SKILL.md`:

- declares its upstream architecture domain(s) and the standards it conforms to,
- requires the upstream artifact when scaffolding or generating new state, and runs standalone for review or hardening when the artifact does not yet exist,
- maps to exactly one of five canonical archetypes (below),
- emits concrete code, configuration, tests, and operational notes — not prose-only deliverables.

## Archetypes

Every backend implementation tech is expected to provide skills drawn from these five archetypes. Only those archetypes the architecture layer actually demands for that stack are produced — there is no fixed baseline.

| # | Archetype | What the skill produces | Primary upstream |
|---|---|---|---|
| 1 | **service-scaffold** | The production-ready service shell: package layout, profile-aware configuration, structured logging, observability hooks, health probes, secure defaults, error handling, testing foundations, container packaging. | `backend-architecture` |
| 2 | **auth-and-security-review** | Authentication and authorization wiring, secret handling, trust-boundary enforcement, security-test coverage — reviewed and hardened against the security standard. | `security` + `backend-architecture` |
| 3 | **observability-readiness** | Metrics (RED/USE), traces, structured logs with trace correlation, SLI/SLO definitions, multi-window multi-burn-rate alerts, dashboards. | `reliability` + `operations` |
| 4 | **async-and-event-integration** | Producer/consumer wiring, delivery semantics, transactional outbox, idempotency, retry/DLQ topology, integration tests against a real or embedded broker. | `backend-architecture` (event contracts) |
| 5 | **performance-and-resilience-engineering** | Timeouts, retries with budgets, circuit breakers, bulkheads, rate limiting, connection-pool and thread-pool sizing, caching posture, JVM/runtime tuning, load-test gates. | `reliability` + `performance` + `backend-architecture` |

## Stacks

### Implemented

| Stack | Status | Skills |
|---|---|---|
| [spring-boot](spring-boot/) | draft, 5/5 archetypes | [service-scaffold](spring-boot/spring-boot-service-scaffold/), [auth-review](spring-boot/spring-security-auth-review/), [observability-readiness](spring-boot/spring-boot-observability-readiness/), [kafka-event-integration](spring-boot/spring-kafka-event-integration/), [performance-and-resilience](spring-boot/spring-boot-performance-and-resilience/) |

### Planned (future scope)

The same five archetypes are intended for every backend stack. The proposed skill list below is locked but not yet authored. Each entry follows the naming pattern `{stack}-{archetype-shortform}` (with stack-idiomatic substitutions for integration brokers and frameworks).

#### fastapi (Python)

| Archetype | Proposed skill |
|---|---|
| service-scaffold | `fastapi-service-scaffold` |
| auth-and-security-review | `fastapi-auth-and-security-review` |
| observability-readiness | `fastapi-observability-readiness` |
| async-and-event-integration | `fastapi-async-and-task-integration` *(Celery / RQ / arq / Kafka per architecture)* |
| performance-and-resilience-engineering | `fastapi-performance-and-resilience` |

#### django (Python)

| Archetype | Proposed skill |
|---|---|
| service-scaffold | `django-service-scaffold` *(settings layout, apps, DRF when REST is exposed)* |
| auth-and-security-review | `django-auth-and-security-review` *(auth backends, CSRF, permissions, DRF auth classes)* |
| observability-readiness | `django-observability-readiness` |
| async-and-event-integration | `django-celery-and-event-integration` |
| performance-and-resilience-engineering | `django-performance-and-resilience` *(ORM, caching, channel layers)* |

#### nodejs (Express / Fastify / NestJS)

A single scaffold skill branches across the three common frameworks per the choice declared in `backend-architecture`.

| Archetype | Proposed skill |
|---|---|
| service-scaffold | `nodejs-service-scaffold` *(framework-aware: express/fastify/nest)* |
| auth-and-security-review | `nodejs-auth-and-security-review` *(passport/JWT/OAuth, helmet, OWASP)* |
| observability-readiness | `nodejs-observability-readiness` *(pino, OTel JS SDK, prom-client)* |
| async-and-event-integration | `nodejs-queue-and-event-integration` *(BullMQ / Kafka.js / SQS)* |
| performance-and-resilience-engineering | `nodejs-performance-and-resilience` *(event-loop, clustering, backpressure, circuit breakers)* |

#### golang

| Archetype | Proposed skill |
|---|---|
| service-scaffold | `golang-service-scaffold` *(stdlib http or chi/echo/gin per architecture; contexts, graceful shutdown)* |
| auth-and-security-review | `golang-auth-and-security-review` *(middleware, JWT/OAuth, mTLS, crypto)* |
| observability-readiness | `golang-observability-readiness` *(OTel Go SDK, slog, prom)* |
| async-and-event-integration | `golang-async-and-event-integration` *(sarama/kafka-go, NATS, SQS, workers, fan-out)* |
| performance-and-resilience-engineering | `golang-performance-and-resilience` *(goroutine discipline, context propagation, rate limiting, circuit breakers, pprof)* |

#### dotnet (.NET 8+, ASP.NET Core)

| Archetype | Proposed skill |
|---|---|
| service-scaffold | `dotnet-service-scaffold` *(minimal API or MVC, options, DI, configuration)* |
| auth-and-security-review | `dotnet-auth-and-security-review` *(ASP.NET Core Identity, JWT/OIDC, data protection, antiforgery)* |
| observability-readiness | `dotnet-observability-readiness` *(OTel .NET, Serilog, EventCounters, HealthChecks)* |
| async-and-event-integration | `dotnet-async-and-event-integration` *(MassTransit / Confluent.Kafka / Azure Service Bus / hosted services)* |
| performance-and-resilience-engineering | `dotnet-performance-and-resilience` *(Polly, channels, async patterns, GC profiling)* |

## Decided design constraints

These constraints are locked for all current and future backend implementation skills:

- **5 archetypes per stack, on-demand.** A stack adds only the archetypes its upstream architecture demands. No fixed baseline.
- **Per-skill upstream linkage.** Every `SKILL.md` names its upstream architecture domain(s) and conformance standards directly. The mapping is restated per skill, not centralised in the layer README.
- **`observability-readiness` is per-stack** for backend (and frontend). Runtime libraries differ across JVM, Python, Node, Go, .NET — duplication is preferred over conditional logic. Where the substrate is shared (Kubernetes, cloud), one shared infrastructure observability skill is sufficient.
- **One scaffold skill per stack** even when the stack hosts multiple frameworks (e.g. Node has express/fastify/nest; the scaffold skill branches on the architecture-declared framework rather than splitting into siblings).
- **Tech overlap is resolved case-by-case.** Meta-frameworks (e.g. Next.js over React) and adjacent stacks (e.g. Spring Boot vs Spring WebFlux) are evaluated pairwise — sometimes they share, sometimes they inherit, sometimes they stand alone.

## Standards every backend implementation skill conforms to

- [api-standards](../../../standards/api-standards/README.md)
- [security-standards](../../../standards/security-standards/README.md)
- [observability-standards](../../../standards/observability-standards/README.md)
- [deployment-standards](../../../standards/deployment-standards/README.md)
- [naming-conventions](../../../standards/naming-conventions/README.md)
