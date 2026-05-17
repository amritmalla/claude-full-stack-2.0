# FastAPI Observability Readiness Playbook

Load this when implementing any owned area of `fastapi-observability-readiness` or defining SLIs/SLOs and alerts. It expands the operating rules and process steps in `SKILL.md` with the detail needed to make a service genuinely observable, not merely instrumented.

## Why this workflow exists

A service with metrics but no trace correlation produces three dashboards no one can join at 3am. Auto-ranged latency histograms make a p99 SLI mathematically meaningless. A single-threshold "p99 > 500ms" alert pages on every traffic blip until on-call mutes it — and then misses the real outage. Unbounded metric labels (user id, raw path) blow up the time-series database and the bill. None of these are caught by tests; they are caught only the first time someone tries to use the telemetry under pressure.

The goal is three correlated signals, latency SLIs that are arithmetically valid, and alerts that page on error-budget burn rather than on noise.

## Behavioral rules in depth

### 1. Consume reliability targets; do not invent them

`architecture/reliability` owns the SLO numbers and the error budget. A latency or availability target is a business risk decision, not an engineering default. If the target is missing, raise an ADR candidate — never write "99.9%" because it looks reasonable. The skill expresses and alerts on the decided targets; it does not set them.

### 2. Replace the seam — never duplicate the logger

`fastapi-service-scaffold` installed a no-op tracer/metrics interface, a structlog logger, and a `contextvars` request context. The real OpenTelemetry SDK fills the seam and reads the active span from the OTel context bound to that same request context. Re-creating the logger or context forks the baseline; the trace id then appears in one copy and not the other.

### 3. Three signals, one identity

| Signal | Carries | Correlation key |
|---|---|---|
| Traces | Span tree, latency, errors | `trace_id` |
| Metrics | RED aggregates | shared resource + route attributes |
| Logs | Structured events | `trace_id` + `span_id` on every in-request line |

A log line without a trace id cannot be pivoted to its trace; a metric spike without shared attributes cannot be narrowed to a route. Correlation is the product, not a nice-to-have.

### 4. RED metrics with explicit buckets

For request-driven work instrument Rate (request counter), Errors (counter by error class), Duration (histogram). The histogram buckets are explicit and documented — chosen around the SLO threshold (e.g. boundaries at 25, 50, 100, 250, 500, 1000, 2500 ms when the SLO is "p99 < 500ms"). Auto-ranged or default buckets make the SLO quantile uncomputable. Document why the buckets were chosen next to the SLI.

### 5. Instrument the boundary; bound the cardinality

Use OpenTelemetry FastAPI/ASGI instrumentation plus the DB/client library instrumentations — that covers most spans for free. Add manual spans only for business-meaningful operations (a payment, a batch job). Never put user id, raw URL path, request id, or any unbounded value on a *metric* label — those belong on a *span* attribute (high-cardinality is fine on traces, fatal on metrics). Use the route template (`/orders/{id}`), never the raw path, as the metric label.

### 6. SLIs are queries, SLOs cite a source

An SLI is a metric expression. An SLO is that SLI plus a target and an error-budget window, and the target is annotated with its `architecture/reliability` source. Prose SLOs ("the API should be fast") are not measurable and not alertable.

### 7. Multi-burn-rate alerting

Per SLO, two rules: a **fast burn (page)** — budget consumed at a high multiple over a short window (e.g. 14.4x over 1h) — and a **slow burn (ticket)** — a low multiple over a long window (e.g. 3x over 6h). This is the Google SRE multi-window multi-burn-rate pattern. A single static threshold either pages on noise or misses slow burns; it does both wrong.

### 8. Export is settings-driven and fail-safe

OTLP endpoint, sampling ratio, and exposure mode come from the scaffold validated settings. A collector or Prometheus outage must degrade to dropped spans / unscraped metrics — never a blocked or crashed request path. The OTLP exporter is batched and non-blocking; verify by pointing it at a dead endpoint and confirming requests still succeed.

## Step detail

**Step 1 — Context.** Load `architecture/reliability` (SLO targets, error budget, windows) and `backend-architecture.md` (critical journeys). Confirm the scaffold telemetry seam. Missing target → ADR candidate.

**Step 2 — Settings.** Add `otel_exporter_otlp_endpoint`, `otel_traces_sampler_arg`, `metrics_mode` (scrape/push), `otel_service_name`, and resource attributes to the scaffold `Settings` and `.env.example` (placeholders).

**Step 3 — Tracing.** `app/observability/tracing.py`: `TracerProvider` with `Resource` attributes, `OTLPSpanExporter` + `BatchSpanProcessor`, `FastAPIInstrumentor` and the DB/client instrumentations. Initialize during lifespan startup so the app is wrapped.

**Step 4 — Metrics.** `app/observability/metrics.py`: a prometheus-client `CollectorRegistry`; `http_requests_total` counter, `http_request_errors_total` by class, `http_request_duration_seconds` histogram with explicit buckets. `/metrics` ASGI app or push per `metrics_mode`. Labels: method, route template, status class only.

**Step 5 — Log correlation.** Extend the scaffold structlog processor chain with a processor reading `trace.get_current_span().get_span_context()` so every in-request line carries `trace_id`/`span_id`. Do not create a second logger.

**Step 6 — SLO doc.** `docs/observability/slo.md`: per critical journey, an SLI query, the target + window from `architecture/reliability` (annotated with source), and the bucket rationale.

**Step 7 — Alerts.** Per SLO, fast-burn (page) and slow-burn (ticket) rules against the error budget, in the operations alerting format; link each to its runbook.

**Step 8 — Verify.** `mypy`, `ruff check`, tests, boot smoke; then locally confirm one request → a trace + RED increment + a log line with the matching `trace_id`; and a dead exporter endpoint does not fail requests. Standards check; document gaps.

## Anti-patterns to detect

Call these out explicitly when found:

- An SLO number with no `architecture/reliability` source (invented target)
- Logs without `trace_id`/`span_id` — three uncorrelated signals
- A second logger or request context instead of extending the scaffold's
- Auto-ranged or default histogram buckets under a latency SLO
- User id, raw path, or request id used as a *metric* label (cardinality blowup)
- A single static-threshold alert instead of multi-burn-rate
- An alert with no linked runbook
- Telemetry export that blocks or crashes the request path when the collector is down
- Manual spans on trivial internal calls (span spam) or none on the business-critical operation
- SLIs written as prose instead of metric queries
- `/metrics` exposed without bounded labels or without network/auth scoping where required
