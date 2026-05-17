---
name: spring-boot-service-scaffold
description: Use when creating, modernizing, or production-hardening a Spring Boot service after backend architecture is approved or intentionally deferred. Produces a production-ready baseline with package structure, profile-aware configuration, structured logging, observability, health probes, secure defaults, error handling, testing foundations, Docker packaging, and local run documentation. Do not use for backend architecture, API contract design, event schema design, or feature implementation. Generates the service shell only — backend boundaries and endpoint shapes belong to backend-architecture, schema content to postgres-schema-and-migration, container hardening to dockerfile-and-jvm-tuning. Leave Flyway migrations as an empty placeholder for the schema skill to fill.
---

# Spring Boot Service Scaffold

## When to use

Invoke when starting a new Spring Boot service, standardizing an internal service baseline, upgrading a legacy Spring Boot service, or preparing a service for container or Kubernetes deployment.

Do not use for pure API contract design, event schema design, frontend applications, infrastructure-only repositories, serverless-only functions, deep domain modeling, or feature implementation.

## Inputs

Required:

- Service name and business capability.
- Approved architecture direction, or explicit confirmation that architecture decisions are intentionally deferred.

Optional:

- Java and Spring Boot versions.
- Maven or Gradle preference.
- Deployment target.
- Database and migration tooling.
- Auth model.
- Sync or async communication needs.
- SLO, throughput, or startup expectations.
- Security, compliance, or platform constraints.

## Operating rules

- Never generate tutorial-grade scaffolding. Assume containerized deployment, multiple environments, observability, rolling deploys, and operational ownership.
- Favor standard Spring Boot patterns, explicit configuration, and predictable package layout over clever abstractions.
- Observability is mandatory: structured logs, trace correlation, health probes, and metrics exposure belong in the baseline.
- Secure by default: no hardcoded secrets, open actuator endpoints, permissive CORS, anonymous admin surfaces, or disabled protections without explanation.
- Challenge weak service boundaries before scaffolding. CRUD-only or data-model-driven services may not justify microservice overhead.
- Ask for confirmation with recommended defaults when a decision changes generated files. Use: "I recommend X because Y. Confirm or redirect."
- Confirm the target directory before writing files. Recommend `services/<service-name>/` in a monorepo or repo root for a single-service repo. Refuse to write into a plugin/skill repository (any directory containing `skills/`, `standards/`, `architecture-patterns/`, `marketplace.json`, or this skill's own tree) without explicit user override.
- Derive the Java package root by stripping hyphens and trailing `-api`/`-service` from the service name (e.g., `orders-api` → `com.<org>.orders`). Hyphens are illegal in Java packages — never emit them. Recommend `com.example` when no organization name is provided.
- A scaffold that does not build is not done. Run `mvn -q -DskipTests verify` (or Gradle equivalent) and the baseline test before declaring completion. Fix and re-run on failure.

## Output contract

The generated service shell MUST conform to:

- [api-standards](../../../../../standards/api-standards/README.md) — error envelope shape, cursor pagination shape, rate-limit headers, OpenAPI consumption (if a contract exists, generated controllers/DTOs derive from `openapi.yaml`, not the other way around).
- [security-standards](../../../../../standards/security-standards/README.md) — no committed secrets, no permissive actuator/CORS, no anonymous admin surfaces, TLS expectations, dependency scanning in CI.
- [observability-standards](../../../../../standards/observability-standards/README.md) — structured JSON logs with required fields, RED metrics per endpoint, OpenTelemetry trace propagation, W3C `traceparent`.
- [deployment-standards](../../../../../standards/deployment-standards/README.md) — env-agnostic Docker image, config injected at deploy time (no baked secrets, no env-branched code), readiness/liveness probes.
- [naming-conventions](../../../../../standards/naming-conventions/README.md) — env vars in `SCREAMING_SNAKE_CASE`, container images `kebab-case`, Java package derivation from service name.

Upstream contract: when [backend-architecture](../../../../architecture/backend-architecture/SKILL.md) output exists for the service, the scaffold consumes `backend-architecture.md` as the source of truth for modules and runtime shape. If `openapi.yaml` exists, consume it as the source of truth for endpoint shapes.

## Progressive references

- Read `references/service-discovery-playbook.md` when gathering service context, classifying service type, challenging service boundaries, or choosing runtime assumptions.
- Read `references/production-defaults.md` when generating configuration, package structure, persistence, Docker, profile overlays, and local run documentation.
- Read `references/security-observability-and-errors.md` when generating security defaults, actuator policy, logging, tracing, health probes, and error handling.
- Read `references/testing-and-deliverables.md` when generating tests, Testcontainers setup, deliverable lists, and no-placeholder expectations.
- Read `references/scaffold-quality-rubric.md` before finalizing and use it as the validation checklist.
- Use `assets/README.template.md` for the generated service `README.md`.
- Use `assets/package-structure.template.md` when choosing the baseline package layout.

## Process

Progress:

- [ ] Step 1: Gather service context: service name, business capability, **target directory** (where the scaffold will be written), **organization name** (for Java package root), Java version, Spring Boot version, build tool, deployment target, database, auth model, communication style, and runtime expectations. Recommend Java 21, Spring Boot 3.x, Maven, Flyway, and containerized deployment unless project constraints say otherwise. Verify the target directory is not a plugin or skill repository before proceeding.
- [ ] Step 2: Classify the service as CRUD API, orchestration service, async worker, integration gateway, domain service, internal admin service, or event processor. Flag mismatches between service type, transaction model, and communication style.
- [ ] Step 3: Confirm runtime and operational assumptions: statelessness, horizontal scaling, throughput, SLOs, startup behavior, graceful shutdown, retries, backpressure, and failure tolerance.
- [ ] Step 4: Define persistence and data strategy: database, Flyway migrations, transaction boundaries, auditing, soft delete, idempotency, caching, pagination, and optimistic locking where appropriate.
- [ ] Step 5: Define security and exposure model: public/internal API, JWT/OAuth2/session auth, RBAC, service-to-service auth, actuator policy, CORS, CSRF posture, and secret management.
- [ ] Step 6: Generate observability and error-handling baseline: structured JSON logs for non-dev, trace/span correlation, Micrometer, Prometheus, health probes, global exception handling, validation mapping, and one error envelope.
- [ ] Step 7: Generate testing foundation: unit test setup, integration test baseline, Testcontainers, profile-aware test configuration, and mock boundaries.
- [ ] Step 8: Generate scaffold files and documentation. Include all required deliverables from `references/testing-and-deliverables.md`; include optional deliverables only when they match the confirmed context. Verify cross-file consistency before stopping: env vars in `application*.yml` match those in `README.md`; profile names match; package root in `Application.java` matches the directory tree; `<artifactId>` matches the directory and README title.
- [ ] Step 9: **Build verification (mandatory).** Run `mvn -q -DskipTests verify` (or Gradle equivalent) and confirm a successful build. Then run `mvn -q test` for the baseline integration test. If Testcontainers cannot run (no Docker available), document the skipped test in the README's Production Notes — do not declare success on a skipped verification without documenting the gap. Fix and re-run on any failure.
- [ ] Step 10: Validate the scaffold against [standards/api-standards](../../../../../standards/api-standards/README.md), [security-standards](../../../../../standards/security-standards/README.md), [observability-standards](../../../../../standards/observability-standards/README.md), [deployment-standards](../../../../../standards/deployment-standards/README.md), and `references/scaffold-quality-rubric.md`. Revise until all pass or explicitly document any unresolved gap.

## Outputs

- Spring Boot service source tree.
- Build file: `pom.xml` or `build.gradle.kts`.
- Profile-aware `application*.yml` configuration.
- Structured logging configuration.
- Global error handling.
- Health, actuator, observability, and security baseline.
- Docker packaging and ignore files.
- Local run documentation based on `assets/README.template.md`.
- Baseline integration test with Testcontainers when a database is present.

Output rules:

- Generated files must be functional, not placeholder-heavy.
- Do not commit secrets or environment-specific branching in code.
- Keep package names and generated class names aligned to the service name.
- Prefer capability-oriented structure; use layered structure only for small/simple services.
- Document any intentionally deferred production-readiness item.

## Quality checks

- [ ] `references/scaffold-quality-rubric.md` was loaded before finalizing.
- [ ] Required deliverables from `references/testing-and-deliverables.md` are present or explicitly deferred.
- [ ] Generated `README.md` follows `assets/README.template.md`.
- [ ] No committed config contains secrets.
- [ ] The scaffold could realistically pass a production-readiness review.

## References

- `references/service-discovery-playbook.md`
- `references/production-defaults.md`
- `references/security-observability-and-errors.md`
- `references/testing-and-deliverables.md`
- `references/scaffold-quality-rubric.md`
- `assets/README.template.md`
- `assets/package-structure.template.md`
