# spring-boot

> Status: draft

## Purpose

Implements backend architecture domains using the Spring ecosystem. This is the *how* layer — framework-specific scaffolding, configuration, and hardening. Architecture decisions (API shape, domain modeling, auth strategy) come from [architecture/](../../../architecture/) and are taken as inputs here.

## Ecosystem

- Spring Boot 3.x
- Spring Security
- Spring Data JPA / Hibernate
- Spring Kafka (where event-driven)
- Spring Cache + Redis
- Gradle (Kotlin DSL) or Maven
- Testcontainers
- Flyway

## Compatible patterns

- [modular-monolith](../../../patterns/modular-monolith/README.md)
- [microservices](../../../patterns/microservices/README.md)
- [event-driven](../../../patterns/event-driven/README.md)
- [cqrs](../../../patterns/cqrs/README.md)
- [hexagonal-architecture](../../../patterns/hexagonal-architecture/README.md)

## Skills

- [spring-boot-service-scaffold](spring-boot-service-scaffold/SKILL.md) — produces a production-ready service shell: package structure, profile-aware configuration, structured logging, observability, health probes, secure defaults, error handling, testing foundations, Docker packaging.
- [spring-security-auth-review](spring-security-auth-review/SKILL.md) — reviews and hardens authentication / authorization for a Spring Boot service using Spring Security, JWT, OAuth2, sessions, or service-to-service auth.
- [observability-readiness](observability-readiness/SKILL.md) — produces or audits Micrometer/Prometheus metrics, OpenTelemetry tracing, structured logs with trace correlation, SLI/SLO definitions, and multi-window multi-burn-rate alerts.

## Architecture domains implemented

| Architecture domain | How |
|---|---|
| [backend-architecture](../../../architecture/backend-architecture/README.md) | Service scaffold follows backend boundaries, modules, workers, controllers, DTOs, and REST contracts produced by `backend-architecture`. |
| [security](../../../architecture/security/README.md) | Spring Security configuration; auth review skill enforces [security-standards](../../../standards/security-standards/README.md). |
| [reliability](../../../architecture/reliability/README.md) | Actuator health probes, structured logging, OpenTelemetry hooks per [observability-standards](../../../standards/observability-standards/README.md). |
| [testing-quality](../../../architecture/testing-quality/README.md) | Testcontainers-based integration test foundations. |

## Standards this implementation conforms to

- [api-standards](../../../standards/api-standards/README.md) — generated controllers respect the global REST contract.
- [security-standards](../../../standards/security-standards/README.md) — auth, secrets, TLS, dependency scanning posture.
- [observability-standards](../../../standards/observability-standards/README.md) — structured JSON logs, RED metrics, OTel traces.
- [deployment-standards](../../../standards/deployment-standards/README.md) — image build, config injection, env-agnostic artifacts.
- [naming-conventions](../../../standards/naming-conventions/README.md) — package names, env vars, container images.

## Upstream inputs

- Approved `system-design.md` (selects Spring Boot as the runtime for one or more components).
- Approved `backend-architecture.md` from [backend-architecture](../../../architecture/backend-architecture/SKILL.md), plus `openapi.yaml` and `api-conventions.md` for any service exposing REST.

## Downstream consumers

- [implementations/data/postgres](../../data/postgres/) — Flyway migrations land in the scaffold's `db/migration/` directory.
- [implementations/infrastructure/*](../../infrastructure/) — built artifacts (Docker images) are deployed through the platform stack.
