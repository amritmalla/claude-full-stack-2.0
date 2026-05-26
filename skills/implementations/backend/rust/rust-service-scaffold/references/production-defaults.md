# Production Defaults

Use these defaults when generating configuration, crate structure, persistence, Docker packaging, and local run documentation.

## Crate structure

Prefer feature-sliced modules for larger services. Use the baseline layered structure only for small/simple services.

Baseline (layered) modules:

- `config` — typed configuration via `serde` + the `config` crate.
- `app` — `Router` construction, layer composition, application state.
- `routes` — HTTP route registration.
- `handlers` — request handlers returning `Result<Json<T>, AppError>`.
- `domain` — domain types, free of HTTP/persistence concerns.
- `repo` — persistence access (`sqlx`/`sea-orm`/`diesel`).
- `dto` — request/response shapes derived from `domain` or `openapi.yaml`.
- `error` — `AppError` enum implementing `IntoResponse`.
- `telemetry` — `tracing` and metrics initialization.
- `health` — liveness/readiness handlers.

`main.rs` stays thin: load config, init telemetry, build the runtime, build the router, bind the listener, run with graceful shutdown. All testable logic lives in the library target.

Call out when a service may outgrow horizontal layers and should move to feature-sliced modules.

## Configuration

Use the `config` crate with layered sources:

1. `config/default.toml` — base, environment-agnostic settings.
2. `config/<env>.toml` — environment overlay, selected by `APP_ENV` (default `dev`).
3. Environment variables — prefixed (e.g., `APP__`) and overriding any file value.

Required files:

- `config/default.toml`.
- At least two non-default environment files that differ meaningfully — typically `config/dev.toml` and `config/prod.toml`.

Conditional files:

- `config/staging.toml` — include only when the user confirms a staging environment exists. Do not ship an overlay that is a copy of `prod`.
- `config/local.toml` — include when local development differs materially from `dev`.

Defaults:

- externalize all secrets via environment variables,
- UTC timezone,
- explicit UTF-8 (the default for Rust strings — verify nothing forces a different encoding),
- fail-fast startup on missing required config (deserialize into a typed struct; do not stringly-type access),
- container-friendly bind address (`0.0.0.0`) and separate admin/metrics port when policy requires it,
- graceful shutdown deadline configured explicitly.

Environments must differ meaningfully. Do not create identical overlay files.

## Persistence

Recommended defaults:

- migrations from the start via `sqlx migrate` or `refinery`,
- versioned migrations (timestamped or sequential),
- `PgPoolOptions` (or equivalent) explicitly configured for `max_connections`, `acquire_timeout`, `idle_timeout`, `max_lifetime`,
- explicit transaction boundaries via `pool.begin()` — no implicit ambient transactions,
- UTC timestamps (`time::OffsetDateTime` or `chrono::DateTime<Utc>`),
- pagination limits enforced server-side for collection endpoints,
- optimistic locking where data contention is possible,
- domain types never derived directly from database rows in the handler layer; use a `repo` mapping step.

Challenge giant aggregate roots, row-type leakage through handlers, transactional RPC chains, shared database coupling, and ambient transaction sprawl.

Leave the first migration as an empty placeholder (e.g., `migrations/0001_init.sql` with a header comment) for the schema skill to fill.

## Docker and runtime

Generate:

- multi-stage `Dockerfile`: a `cargo-chef`-cached build stage and a minimal runtime stage (distroless `cc` or `debian:slim`),
- `.dockerignore` excluding `target/`, `.git/`, local config overlays, and editor artifacts,
- non-root runtime user,
- pinned base image digests when policy requires reproducible builds,
- `CMD` invoking the binary target directly (no shell wrapper),
- explicit `EXPOSE` for the HTTP port and the metrics port if separated,
- graceful shutdown support: handler for `SIGTERM` via `tokio::signal`, wired through `axum::serve(...).with_graceful_shutdown(...)`.

Keep runtime configuration externalized via environment variables. Do not bake environment-specific values into the image.

## Local documentation

Generated `README.md` should include:

- purpose and service capability,
- prerequisites (Rust toolchain version, Docker),
- how to run locally (`cargo run` and via Docker),
- how to run tests,
- environment variable reference,
- environment overlay descriptions,
- health and metrics endpoints,
- available Make targets or `cargo xtask` commands.
