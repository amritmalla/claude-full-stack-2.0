# Testing and Deliverables

Use this reference when generating the scaffold and checking file completeness.

## Required deliverables

- `Cargo.toml` with workspace or single-crate layout per architecture
- `Cargo.lock` (committed for binaries)
- `rust-toolchain.toml` pinning channel and components (`rustfmt`, `clippy`)
- `src/main.rs` (thin entrypoint) and library target carrying logic
- `config/default.toml`
- at least two non-default environment overlays (typically `config/dev.toml` and `config/prod.toml`) that differ meaningfully
- `tracing` initialization module (`telemetry`)
- `AppError` enum implementing `IntoResponse`
- health probe handlers (`/health/live`, `/health/ready`)
- `/metrics` exposition wired via `metrics-exporter-prometheus`
- security baseline (auth extractor or layer, CORS, body-size limit, request timeout)
- `Dockerfile` (multi-stage)
- `.dockerignore`
- `.gitignore` (excludes `target/`, local config overlays, IDE state)
- `README.md`
- `Makefile` or `cargo xtask` task runner
- baseline integration test that builds the `axum::Router` in-process and asserts on the health and one domain endpoint

## Optional deliverables

Include when appropriate:

- `config/staging.toml` (only when staging is a real environment, not a copy of prod),
- `config/local.toml` (only when local diverges from dev),
- `docker-compose.yml` for local dev dependencies,
- OpenAPI starter config (`utoipa` or static `openapi.yaml` consumed by the handler types),
- OpenTelemetry starter config (`tracing-opentelemetry` + OTLP exporter),
- Kubernetes probe examples (`Deployment` snippet in `README.md`),
- migration placeholder (e.g., `migrations/0001_init.sql` with a header comment) when a database is confirmed — leave content for the schema skill,
- `.editorconfig` for consistent indentation across editors,
- `rustfmt.toml` and `clippy.toml` when team standardization matters,
- `.gitattributes` for line-ending normalization in mixed-OS teams,
- `deny.toml` for `cargo-deny` (license/security policy in CI),
- `cargo-audit` workflow step.

## Testing foundation

Generate:

- unit tests for pure functions, domain logic, error mapping, and config deserialization,
- integration tests that build the `axum::Router` via a `build_app(state)` constructor and exercise it with `tower::ServiceExt::oneshot` (no network sockets needed),
- `testcontainers-rs` for real database dependencies — never mock `sqlx` query behavior,
- environment isolation via the layered `config` loader (tests select a `test` overlay or override via env vars),
- `tokio::test` for async tests; `#[tokio::test(flavor = "multi_thread")]` when the test exercises spawned tasks.

Avoid brittle over-mocked architectures. Mock external HTTP/event sinks (with `wiremock` or `mockito`), not the repository or database behavior under test.

## No-placeholder rule

Generated deliverables must be functional. Avoid TODO comments or placeholder files standing in for real configuration.

Acceptable placeholders:

- environment variable examples with safe dummy values,
- module-level extension points (empty modules with a one-line doc comment),
- empty migration only if the service has no confirmed schema yet and the README explains why,
- a single sample domain endpoint (e.g., `GET /v1/ping`) so the integration test has something to assert beyond health.

Unacceptable placeholders:

- fake secrets,
- disabled security middleware,
- empty error variants with no `IntoResponse` mapping,
- `/metrics` endpoint without registered metrics,
- tests that compile but assert nothing meaningful,
- `unwrap`/`expect` inside request handlers,
- `unsafe` blocks anywhere in the scaffold.
