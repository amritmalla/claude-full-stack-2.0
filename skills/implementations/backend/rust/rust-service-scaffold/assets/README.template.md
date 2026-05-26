# [Service Name]

[One-paragraph description of the service capability and ownership boundary.]

## Prerequisites

- Rust [toolchain version, pinned in `rust-toolchain.toml`]
- Docker
- [Database or local dependency, if applicable]

## Run Locally

```bash
# Native
APP_ENV=dev cargo run

# Via Docker
docker build -t [service-name]:dev .
docker run --rm -p 8080:8080 --env-file .env.dev [service-name]:dev
```

## Run Tests

```bash
cargo test --locked
```

Integration tests requiring a database use `testcontainers-rs` and need a running Docker daemon. If Docker is unavailable, run unit tests only: `cargo test --locked --lib`.

## Environments

- `dev`: [local development behavior]
- `staging`: [pre-production behavior]
- `prod`: [production behavior]

Select via `APP_ENV=<name>`. Configuration loads `config/default.toml`, then `config/<APP_ENV>.toml`, then any `APP__*` environment variables.

## Environment Variables

| Variable | Required | Description | Example |
|---|---:|---|---|
| `APP_ENV` | Yes | Environment overlay to load | `dev` |
| `[APP__NAME]` | Yes | [description] | `[safe example]` |

## Health and Metrics

- Liveness: `GET /health/live`
- Readiness: `GET /health/ready`
- Metrics: `GET /metrics` (Prometheus exposition)

## Task Commands

| Command | Description |
|---|---|
| `make run` | Run the service against the `dev` overlay |
| `make test` | Run all tests (`cargo test --locked`) |
| `make lint` | Run `cargo clippy --all-targets -- -D warnings` |
| `make fmt` | Run `cargo fmt --all` |

## Production Notes

[Document intentionally deferred production-readiness items, operational assumptions, and deployment expectations. Examples: testcontainers-backed tests skipped due to no local Docker; OTel exporter wired only in non-dev; rate-limit layer scaffolded but not yet tuned.]
