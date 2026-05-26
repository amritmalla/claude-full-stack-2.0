---
name: rust-service-scaffold
description: Use when creating, modernizing, or production-hardening a Rust web service (axum or actix-web) after backend architecture is approved or intentionally deferred. Produces a production-ready baseline with crate structure, layered configuration, structured tracing, observability, health probes, secure defaults, error handling, testing foundations, Docker packaging, and local run documentation. Do not use for backend architecture, API contract design, event schema design, or feature implementation. Generates the service shell only — boundaries and endpoint shapes belong to backend-architecture, schema content to the data-layer skill, container hardening to the container skill. Leave migrations as an empty placeholder for the schema skill to fill.
---

# Rust Service Scaffold

## When to use

Invoke when starting a new Rust web service, standardizing an internal Rust service baseline, modernizing a legacy Rust service, or preparing a Rust service for container or Kubernetes deployment.

Do not use for pure API contract design, event schema design, frontend applications, infrastructure-only repositories, serverless-only functions, CLI/tooling crates, deep domain modeling, or feature implementation.

## Inputs

Required:

- Service name and business capability.
- Approved architecture direction, or explicit confirmation that architecture decisions are intentionally deferred.

Optional:

- Rust edition / toolchain version.
- Framework preference (axum default; actix-web alternative).
- Deployment target.
- Database and migration tooling.
- Auth model.
- Sync or async communication needs.
- SLO, throughput, or startup expectations.
- Security, compliance, or platform constraints.

## Operating rules

- Never generate tutorial-grade scaffolding. Assume containerized deployment, multiple environments, observability, rolling deploys, and operational ownership.
- Favor idiomatic axum/tower patterns, explicit configuration, and predictable crate layout over clever abstractions or macro-heavy DSLs.
- Observability is mandatory: structured `tracing` logs, trace correlation, health probes, and `/metrics` exposure belong in the baseline.
- Secure by default: no hardcoded secrets, no anonymous admin surfaces, no permissive CORS, no `unsafe` in the scaffold, no panicking handlers reachable from request paths.
- `unwrap`/`expect` are permitted only in `main` before the runtime starts (config load, listener bind, runtime build). Request-handling code returns typed errors via `thiserror` and `IntoResponse`.
- Challenge weak service boundaries before scaffolding. CRUD-only or data-model-driven services may not justify microservice overhead.
- Ask for confirmation with recommended defaults when a decision changes generated files. Use: "I recommend X because Y. Confirm or redirect."
- Confirm the target directory before writing files. Recommend `services/<service-name>/` in a monorepo or repo root for a single-service repo. Refuse to write into a plugin/skill repository (any directory containing `skills/`, `standards/`, `architecture-patterns/`, `marketplace.json`, or this skill's own tree) without explicit user override.
- Derive the crate name by replacing hyphens with underscores and stripping trailing `_api`/`_service` only when the user confirms (e.g., `orders-api` → package name `orders-api`, library target `orders`). Cargo package names use hyphens; Rust module/library identifiers use underscores — never confuse the two.
- A scaffold that does not build is not done. Run `cargo build --locked` and `cargo test --locked` before declaring completion. Fix and re-run on failure.

## Output contract

The generated service shell MUST conform to:

- [api-standards](../../../../../standards/api-standards/README.md) — error envelope shape, cursor pagination shape, rate-limit headers, OpenAPI consumption (if a contract exists, generated handlers and DTOs derive from `openapi.yaml`, not the other way around).
- [security-standards](../../../../../standards/security-standards/README.md) — no committed secrets, no permissive CORS, no anonymous admin surfaces, TLS expectations, dependency scanning (`cargo-audit`/`cargo-deny`) in CI.
- [observability-standards](../../../../../standards/observability-standards/README.md) — structured JSON `tracing` logs with required fields, RED metrics per endpoint, OpenTelemetry trace propagation, W3C `traceparent`.
- [deployment-standards](../../../../../standards/deployment-standards/README.md) — env-agnostic Docker image, config injected at deploy time (no baked secrets, no env-branched code), readiness/liveness probes.
- [naming-conventions](../../../../../standards/naming-conventions/README.md) — env vars in `SCREAMING_SNAKE_CASE`, container images `kebab-case`, Cargo package name `kebab-case`, Rust modules `snake_case`.

Upstream contract: when [backend-architecture](../../../../architecture/backend-architecture/SKILL.md) output exists for the service, the scaffold consumes `backend-architecture.md` as the source of truth for modules, framework choice, and runtime shape. If `openapi.yaml` exists, consume it as the source of truth for endpoint shapes.

## Progressive references

- Read `references/service-discovery-playbook.md` when gathering service context, classifying service type, challenging service boundaries, or choosing runtime assumptions.
- Read `references/production-defaults.md` when generating configuration, crate structure, persistence, Docker, environment overlays, and local run documentation.
- Read `references/security-observability-and-errors.md` when generating security defaults, `/metrics` policy, tracing, health probes, and error handling.
- Read `references/testing-and-deliverables.md` when generating tests, testcontainers setup, deliverable lists, and no-placeholder expectations.
- Read `references/scaffold-quality-rubric.md` before finalizing and use it as the validation checklist.
- Use `assets/README.template.md` for the generated service `README.md`.
- Use `assets/crate-structure.template.md` when choosing the baseline module layout.

## Process

Progress:

- [ ] Step 1: Gather service context: service name, business capability, **target directory**, Rust toolchain (recommend latest stable + 2021 edition), framework (recommend axum), deployment target, database, auth model, communication style, and runtime expectations. Recommend axum + tokio multi-thread runtime + `sqlx` + Postgres + containerized deployment unless project constraints say otherwise. Verify the target directory is not a plugin or skill repository before proceeding.
- [ ] Step 2: Classify the service as CRUD API, orchestration service, async worker, integration gateway, domain service, internal admin service, or event processor. Flag mismatches between service type, transaction model, and communication style.
- [ ] Step 3: Confirm runtime and operational assumptions: statelessness, horizontal scaling, throughput, SLOs, startup behavior, graceful shutdown (tokio `signal` + `axum::serve` `with_graceful_shutdown`), retries, backpressure, and failure tolerance.
- [ ] Step 4: Define persistence and data strategy: database, migration tool (`sqlx migrate` or `refinery`), `sqlx`/`sea-orm`/`diesel` choice, transaction boundaries, idempotency, pool sizing (`PgPoolOptions`), pagination, and optimistic locking where appropriate.
- [ ] Step 5: Define security and exposure model: public/internal API, JWT/OAuth2 auth, RBAC, service-to-service auth (mTLS via rustls), `/metrics` policy, CORS, and secret management.
- [ ] Step 6: Generate observability and error-handling baseline: `tracing` with JSON formatter for non-dev, `tower_http::trace::TraceLayer` with `traceparent` propagation, `metrics-exporter-prometheus`, health probes (`/health/live`, `/health/ready`), one typed error enum implementing `IntoResponse`, and validator-error mapping.
- [ ] Step 7: Generate testing foundation: unit tests (pure functions, error mapping), integration tests via `tokio::test` and `axum::Router` exercised in-process, `testcontainers-rs` for real database dependencies, environment isolation via the `config` layered loader.
- [ ] Step 8: Generate scaffold files and documentation. Include all required deliverables from `references/testing-and-deliverables.md`; include optional deliverables only when they match the confirmed context. Verify cross-file consistency before stopping: env vars in `config/*.toml` match those in `README.md`; environment names match; Cargo package name matches the directory; binary target name matches what the `Dockerfile` runs.
- [ ] Step 9: **Build verification (mandatory).** Run `cargo build --locked` and confirm a successful build, then `cargo test --locked`. If testcontainers cannot run (no Docker available), document the skipped test in the README's Production Notes — do not declare success on a skipped verification without documenting the gap. Run `cargo clippy --all-targets -- -D warnings` and `cargo fmt --check` and fix any findings. Fix and re-run on any failure.
- [ ] Step 10: Validate the scaffold against [standards/api-standards](../../../../../standards/api-standards/README.md), [security-standards](../../../../../standards/security-standards/README.md), [observability-standards](../../../../../standards/observability-standards/README.md), [deployment-standards](../../../../../standards/deployment-standards/README.md), and `references/scaffold-quality-rubric.md`. Revise until all pass or explicitly document any unresolved gap.

## Outputs

- Rust service source tree (`src/`, with `main.rs` thin and a library target carrying logic).
- `Cargo.toml` and committed `Cargo.lock`.
- Layered configuration: `config/default.toml`, plus at least two non-default environment files (typically `config/dev.toml` and `config/prod.toml`) that differ meaningfully, with env-var overrides via the `config` crate.
- Structured `tracing` setup with JSON formatter for non-dev environments.
- Global error type implementing `IntoResponse` and one error envelope shape.
- Health probes, `/metrics`, observability, and security baseline.
- Docker packaging (multi-stage, distroless or `debian:slim` runtime, non-root user) and `.dockerignore`.
- Local run documentation based on `assets/README.template.md`.
- Baseline integration test exercising the `Router` in-process; testcontainers-backed DB test when a database is present.

Output rules:

- Generated files must be functional, not placeholder-heavy.
- Do not commit secrets or environment-branched code.
- Keep crate names, binary targets, and the Docker `CMD` aligned to the service name.
- Prefer feature-sliced modules; use horizontal layering only for small/simple services.
- Document any intentionally deferred production-readiness item.

## Quality checks

- [ ] `references/scaffold-quality-rubric.md` was loaded before finalizing.
- [ ] Required deliverables from `references/testing-and-deliverables.md` are present or explicitly deferred.
- [ ] Generated `README.md` follows `assets/README.template.md`.
- [ ] No committed config contains secrets.
- [ ] `cargo clippy -D warnings` and `cargo fmt --check` pass.
- [ ] The scaffold could realistically pass a production-readiness review.

## References

- `references/service-discovery-playbook.md`
- `references/production-defaults.md`
- `references/security-observability-and-errors.md`
- `references/testing-and-deliverables.md`
- `references/scaffold-quality-rubric.md`
- `assets/README.template.md`
- `assets/crate-structure.template.md`
