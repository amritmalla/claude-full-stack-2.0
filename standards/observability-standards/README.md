# observability-standards

Contract for logs, metrics, traces, and alerts. Every implementation skill that produces a runnable service MUST conform.

## The three signals

| Signal | Purpose | Required for |
|---|---|---|
| **Logs** | Discrete events, debugging context | Every service |
| **Metrics** | Aggregated numeric time-series | Every service |
| **Traces** | Cross-service request flow | Any service with ≥1 downstream call |

## Logs

- Structured JSON, one event per line, written to stdout. Log routing is the platform's job, not the app's.
- Required fields: `timestamp` (ISO 8601 UTC), `level`, `service`, `version`, `trace_id`, `span_id`, `message`.
- Levels: `DEBUG`, `INFO`, `WARN`, `ERROR`. `FATAL` reserved for crash-on-exit only.
- No PII, secrets, or tokens. Mask at the logging adapter.
- Correlation: every log entry inside a request MUST carry the originating `trace_id`.

## Metrics

- Emit via OpenTelemetry Metrics SDK or Prometheus-compatible endpoint.
- Naming: `<domain>_<entity>_<action>_<unit>` (`http_requests_total`, `db_query_duration_seconds`).
- Every service MUST expose RED metrics for each endpoint:
  - **R**ate (requests/sec)
  - **E**rrors (errors/sec, by 4xx/5xx)
  - **D**uration (histogram, with p50/p95/p99)
- And USE metrics for each significant resource:
  - **U**tilization
  - **S**aturation
  - **E**rrors

## Traces

- OpenTelemetry-compatible. W3C `traceparent` header propagated on every outbound call.
- Sampling: head-based, 100% for errors and tier-0 services, 1-10% otherwise.
- Every span MUST have: service name, operation name, status, and at least one business attribute (`user_id_hash`, `tenant_id`, `order_id`, ...).

## SLOs

Every tier-0 / tier-1 component declares SLOs in its `architecture-schema` component file:

```yaml
slos:
  availability:
    target: 99.9
    window: 30d
  latency_p99:
    target_ms: 500
    window: 30d
```

Error budget burn drives alerting, not raw thresholds.

## Alerts

- Page on symptoms (user-visible), not causes (CPU, memory). Cause-based alerts go to a non-paging channel.
- Every alert has: a runbook link, an owner, a severity, and an SLO it defends.
- Alerts without runbooks are deleted.

## Dashboards

- One service overview dashboard per service: RED + USE + dependency health.
- One product dashboard per top-level user journey: end-to-end latency, conversion, error rate.
- Dashboards as code (Grafana JSON or Terraform), versioned in repo.

## Reference stack

Default opinionated stack (overridable by implementation):

- Logs: OpenTelemetry → Loki / CloudWatch / Datadog
- Metrics: OpenTelemetry / Prometheus → Grafana
- Traces: OpenTelemetry → Tempo / Jaeger / Datadog APM
- Alerts: Alertmanager / cloud-native alerting

## Anti-patterns

- Unstructured `printf` logs in production.
- Alerting on every error (alert fatigue) instead of error rate against SLO.
- Metric cardinality explosions (high-cardinality labels like user ID on every request metric).
- Dashboards built by-hand in the UI with no source of truth.
- Trace IDs that don't propagate across async boundaries (queue / event consumers).
