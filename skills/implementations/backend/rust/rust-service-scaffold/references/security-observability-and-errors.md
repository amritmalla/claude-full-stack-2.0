# Security, Observability, and Errors

Use this reference when generating operationally safe defaults.

## Security baseline

Clarify:

- public vs internal API,
- JWT/OAuth2 auth,
- RBAC needs,
- service-to-service auth (mTLS via rustls),
- `/metrics` access policy,
- CORS expectations (`tower-http::cors`),
- request body and timeout limits (`tower-http::limit`, `tower::timeout`),
- secret management strategy.

Defaults:

- stateless JWT for APIs (verify via `jsonwebtoken` with explicit `Validation`; never accept `alg: none`),
- RBAC abstraction from the start, applied as a `tower` layer or extractor — never inline in handlers,
- `/metrics` and any admin surface authenticated outside dev,
- `/health/live` available without auth for probes; `/health/ready` may include a lightweight dependency check,
- externalized secrets,
- deny-by-default security posture,
- `tower-http::limit::RequestBodyLimitLayer` set with an explicit byte cap,
- per-route timeouts via `tower::timeout::TimeoutLayer` — do not rely solely on upstream load-balancer timeouts.

Never scaffold hardcoded secrets, anonymous admin surfaces, open non-health endpoints in non-dev, permissive CORS without justification, or `unsafe` blocks in handler code.

## Observability baseline

Generate:

- `tracing` initialization in `telemetry::init` — `tracing_subscriber::fmt` with the JSON formatter in non-dev profiles, pretty formatter in dev,
- `tower_http::trace::TraceLayer` on the router for per-request spans,
- W3C `traceparent` propagation via `tracing-opentelemetry` when OTel is configured,
- `metrics` facade with `metrics-exporter-prometheus` exposing `/metrics`,
- RED metrics per route (request count, error count, duration histogram) via a `tower` layer or `metrics` middleware,
- readiness/liveness handlers in `health`,
- operational metadata in startup logs (service name, version from `env!("CARGO_PKG_VERSION")`, environment, git SHA if available),
- log fields include `trace_id` and `span_id` once OTel is wired.

Missing observability is a production defect.

## Health endpoints

Expose:

- `GET /health/live` — returns 200 if the process is up. No dependency checks.
- `GET /health/ready` — returns 200 only when the service can accept traffic. Checks: database pool can acquire a connection within a short deadline; downstream critical dependencies are reachable (use a cached check, not a per-request probe).
- `GET /metrics` — Prometheus exposition format.

Configure:

- fast cold-start probe responses,
- dependency-aware readiness with timeouts,
- metrics endpoint bound to the same listener by default; split to a separate admin port when policy requires it.

## Error handling

Define a single `AppError` enum in the `error` module. Use `thiserror` for the variants and implement `IntoResponse` so every error path produces the same envelope.

```rust
#[derive(thiserror::Error, Debug)]
pub enum AppError {
    #[error("resource not found")]
    NotFound,
    #[error("validation failed")]
    Validation(Vec<FieldError>),
    #[error("unauthorized")]
    Unauthorized,
    #[error(transparent)]
    Internal(#[from] anyhow::Error),
}
```

Wire emission so every API error returns one envelope shape:

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Resource not found",
    "traceId": "abc123",
    "details": []
  }
}
```

Rules:

- never leak `Debug` output, panic payloads, or `sqlx`/driver error strings into the response body,
- never expose persistence internals,
- map validator (`validator` crate) errors into `AppError::Validation` with field-level `details`,
- include the correlation identifier (`trace_id` from the current `tracing` span),
- use consistent status-code mapping (`NotFound → 404`, `Validation → 400`, `Unauthorized → 401`, `Internal → 500`),
- log `Internal` variants at `error` level with the source chain (`{:?}`); log client-error variants at `warn` or `info` at most,
- keep domain errors separate from transport errors — domain modules return their own error types and convert into `AppError` at the handler boundary.
