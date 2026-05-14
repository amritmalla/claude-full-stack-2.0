---
name: observability-readiness
description: Use when preparing a service for production observability or auditing
  an existing service for gaps. Produces Micrometer/Prometheus metrics,
  OpenTelemetry tracing, structured logs with trace correlation, defined SLIs and
  SLOs, and multi-window multi-burn-rate alerts tied to those SLOs.
---

# Observability Readiness

## When to use

Invoke before promoting a service to production, or when an existing service is page-prone, slow to diagnose, or has alert fatigue. Use after the service is running locally; do not invoke for greenfield design (use `system-design-from-prd` instead).

## Inputs

- Running service spec (endpoints, latency expectations, error budget).
- Target metrics backend (Prometheus assumed) and tracing backend (Tempo/Jaeger/OTel collector).
- Log aggregator (Loki/CloudWatch/etc.).

## Output contract

Generated instrumentation MUST conform to [observability-standards](../../../../standards/observability-standards/README.md). That standard is authoritative for:

- Logs: structured JSON to stdout; required fields (`timestamp`, `level`, `service`, `version`, `trace_id`, `span_id`, `message`); no PII / secrets / tokens.
- Metrics: RED per endpoint, USE per significant resource; metric naming `<domain>_<entity>_<action>_<unit>`.
- Traces: OpenTelemetry, W3C `traceparent` propagation, head-based sampling (100% for errors and tier-0).
- SLOs declared in the component file per [architecture-schema](../../../../standards/architecture-schema/README.md); multi-window multi-burn-rate alerts defend SLOs, not raw thresholds.
- Every alert has a runbook (see [architecture/operations](../../../../architecture/operations/README.md)).

Component tier (from architecture-schema) drives instrumentation depth and sampling rate.

## Process

1. **Metrics**: enable Micrometer with the Prometheus registry. Expose `/actuator/prometheus`. Add custom metrics for each business-meaningful counter and histogram (e.g., `orders_created_total`, `orders_create_duration_seconds`).
2. **Tracing**: configure OpenTelemetry SDK with the OTLP exporter. Sample at ≥ 10% in prod (or use tail sampling). Propagate W3C `traceparent` on all outbound calls.
3. **Logs**: emit JSON logs with `traceId` and `spanId` MDC fields so logs join to traces in the backend.
4. **SLIs**: choose 2–4 SLIs per service. Typical set: availability (good responses / total), latency (p99 < threshold), error rate, freshness (for async pipelines).
5. **SLOs**: assign a 28-day target to each SLI (e.g., 99.9% availability, p99 < 300 ms). Document the error budget.
6. **Alerts**: write multi-window multi-burn-rate alerts (e.g., 14.4× burn over 1h, 6× burn over 6h). Alert on SLO burn, never on raw thresholds. Each alert names a runbook URL.
7. **Dashboards**: list the dashboards required (golden signals: rate, errors, duration, saturation). Reference them by name.
8. Emit `observability.md`, Spring config snippets, `prometheus/rules.yaml` (alerts), and the dashboard list.

## Outputs

- `observability.md`.
- Spring config: Micrometer + OpenTelemetry wiring.
- `prometheus/rules.yaml`.
- Dashboard inventory.

## Quality checks

- [ ] Every SLI has a corresponding SLO with a 28-day target.
- [ ] All alerts are multi-window multi-burn-rate against an SLO; none alert on raw threshold.
- [ ] Logs include `traceId` and `spanId` MDC fields.
- [ ] Tracing sample rate is documented and > 0% in prod.
- [ ] Every alert names a runbook URL.

## References

(None in v0.1.)
