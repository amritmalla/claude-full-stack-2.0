---
name: spring-boot-service-scaffold
description: Use when starting a new Spring Boot service or hardening an existing
  one for production. Generates a layered project layout, profile-based
  configuration, Actuator endpoints, structured JSON logging, and a global error
  envelope so the service is production-ready on day one.
---

# Spring Boot Service Scaffold

## When to use

Invoke at the start of a new Spring Boot service after architecture is approved, or when reviewing an existing service that lacks production-grade scaffolding (profiles, health endpoints, structured logging, error envelope). Do not invoke for framework-agnostic API contract work — use `rest-api-contract-design` first.

## Inputs

- Service name (kebab-case) and Maven `groupId`/`artifactId`.
- Java version (≥ 21 recommended) and Spring Boot version (≥ 3.x).
- Persistence target (Postgres assumed for this plugin's reference stack).
- Auth model (link to `spring-security-auth-review` if JWT/OAuth2).

## Process

1. Generate `pom.xml` (or `build.gradle.kts`) with: Spring Boot starter web, validation, actuator, data-jpa, security; Flyway; Postgres driver; Testcontainers; Logback JSON encoder.
2. Create package layout: `controller/`, `service/`, `repository/`, `domain/`, `config/`.
3. Create `application.yml` plus `application-dev.yml`, `application-staging.yml`, `application-prod.yml`. Externalize secrets via env vars; commit no secrets.
4. Configure Actuator: expose `health`, `info`, `metrics`, `prometheus`. Gate non-`health` endpoints behind auth in non-dev profiles.
5. Wire health probes: `/actuator/health/liveness`, `/actuator/health/readiness`, `/actuator/health/startup`.
6. Add a global `@RestControllerAdvice` that returns a consistent error envelope: `{ "error": { "code", "message", "traceId", "details": [] } }`.
7. Configure Logback with a JSON encoder for non-`dev` profiles; include `traceId` and `spanId` MDC fields.
8. Add a `Makefile` (or task list in README) for: `run`, `test`, `lint`, `package`.

## Outputs

- Project skeleton with the file tree listed above.
- `pom.xml`, `application.yml` + profile overlays, `GlobalExceptionHandler.java`, `logback-spring.xml`.

## Quality checks

- [ ] `/actuator/health/liveness` returns 200 in < 50 ms cold.
- [ ] Actuator endpoints other than `health` require authentication in non-dev profiles.
- [ ] No secrets in committed config; secrets resolved via env vars or a secret manager.
- [ ] Non-dev profiles emit structured JSON logs with `traceId`.
- [ ] Every error response from the service uses the same envelope shape.

## References

(None in v0.1.)
