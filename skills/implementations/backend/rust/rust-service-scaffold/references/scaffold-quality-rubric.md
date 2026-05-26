# Scaffold Quality Rubric

Load this before finalizing. Revise until each check passes or explicitly document the unresolved gap.

## Required checks

- [ ] Service starts with environment overlay isolation (`APP_ENV` selects the overlay file).
- [ ] At least two non-default environment overlays exist and differ meaningfully (typically `dev` + `prod`). Staging is included only when confirmed and only when it is materially different from prod.
- [ ] Configuration deserializes into a typed `Settings` struct; no stringly-typed config access in application code.
- [ ] No secrets exist in committed configuration.
- [ ] Structured JSON `tracing` logs are active in non-dev environments.
- [ ] Logs include `trace_id` and `span_id` (or document why OTel wiring is deferred).
- [ ] `/metrics` exposes Prometheus exposition format and is registered with at least the per-route RED metrics.
- [ ] `/metrics` and any admin surface are authenticated outside dev.
- [ ] Health probes expose `/health/live` and `/health/ready`; readiness checks at least the database pool when persistence exists.
- [ ] Graceful shutdown is wired via `axum::serve(...).with_graceful_shutdown(...)` and a `tokio::signal` handler.
- [ ] Every API error path returns one envelope shape via `AppError: IntoResponse`.
- [ ] Validation errors are mapped to field-level `details` in the envelope.
- [ ] Internal error chains, panic payloads, and driver error strings are not exposed in response bodies.
- [ ] Database migrations are versioned (`sqlx migrate` or `refinery`) when persistence exists.
- [ ] `testcontainers-rs` integration tests are configured when a database exists.
- [ ] Configuration supports containerized deployment (no env-branched code, no baked secrets).
- [ ] `Dockerfile` produces a runnable image; multi-stage build with non-root runtime user.
- [ ] README explains local run, tests, environment variables, environments, and task commands.
- [ ] Crate structure reflects service capability and avoids flat dumping grounds (`handlers/` is not the whole project).
- [ ] `main.rs` is thin and all testable logic lives in the library target.
- [ ] `unwrap`/`expect` appear only in startup code in `main.rs` before the runtime is taking traffic.
- [ ] No `unsafe` blocks in the scaffold.
- [ ] The scaffold could realistically pass a production-readiness review.

## Build verification

- [ ] `cargo build --locked` completed successfully against the generated tree.
- [ ] `cargo test --locked` completed successfully, **or** the test run was explicitly skipped (e.g., no Docker for testcontainers) and the skip is documented in the README's Production Notes.
- [ ] `cargo clippy --all-targets --locked -- -D warnings` passed.
- [ ] `cargo fmt --all -- --check` passed.
- [ ] No verification was claimed without evidence — the skill ran each command and captured the result.

## Cross-file consistency

- [ ] Environment overlay names referenced by `APP_ENV` match those documented in `README.md` under "Environments".
- [ ] Every environment variable consumed by the `config` loader appears in the README's Environment Variables table, and vice versa.
- [ ] The Cargo `package.name` matches the target directory name.
- [ ] The binary target name in `Cargo.toml` matches the `CMD` in the `Dockerfile`.
- [ ] The library crate name (`snake_case`) matches the `lib.rs` path and the import path used by integration tests.
- [ ] Health and metrics endpoints exposed in the router match those documented in the README.
- [ ] The `rust-toolchain.toml` channel matches the toolchain assumed by CI and the `Dockerfile` build stage.

## Failure handling

If a check fails:

1. Identify the missing file, weak default, or unresolved decision.
2. Fix the scaffold when the decision is clear.
3. Ask the user for confirmation when the decision changes architecture, security, persistence, or runtime behavior.
4. Document intentionally deferred items in the README.
