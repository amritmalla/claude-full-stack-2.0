# FastAPI Observability Readiness — Reference

Use this as the canonical OpenTelemetry SDK, RED-metrics, log-correlation, and SLO/alert reference when making a scaffolded FastAPI service observable. Placeholder tokens use `<kebab-case>` or `<PascalCase>`. SLO targets come from `architecture/reliability`; critical journeys from `backend-architecture.md`. Versions are pinned examples — never use unbounded specifiers.

## Directory additions (over the scaffold)

```
app/observability/
├── tracing.py                            # OTel SDK; replaces the no-op tracer seam
├── metrics.py                            # prometheus-client registry; RED instruments
└── logging.py                            # EXTENDED (not replaced): trace_id/span_id processor
docs/observability/
└── slo.md                                # SLIs as queries; SLOs cite architecture/reliability
deploy/alerts/
└── <service-name>.rules.yaml             # multi-burn-rate fast + slow rules
```

## Settings additions (extend the scaffold Settings model)

```python
otel_service_name: str
otel_exporter_otlp_endpoint: str
otel_traces_sampler_arg: float = 0.1
metrics_mode: str = "scrape"          # scrape | push
```

`.env.example` gets the same keys with placeholder values.

## Tracing seam fill (app/observability/tracing.py)

```python
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from app.config import settings

def init_tracing(app) -> None:
    provider = TracerProvider(resource=Resource.create({"service.name": settings.otel_service_name}))
    provider.add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter(endpoint=settings.otel_exporter_otlp_endpoint))
    )
    trace.set_tracer_provider(provider)
    FastAPIInstrumentor.instrument_app(app)   # call during lifespan startup
```

`BatchSpanProcessor` is non-blocking — a dead endpoint drops spans, not requests. Verify it.

## RED metrics (app/observability/metrics.py)

```python
from prometheus_client import Counter, Histogram, CollectorRegistry

registry = CollectorRegistry()
http_requests = Counter("http_requests_total", "request count",
                         ["method", "route", "status_class"], registry=registry)
http_errors = Counter("http_request_errors_total", "errors by class",
                       ["method", "route", "error_class"], registry=registry)
http_duration = Histogram("http_request_duration_seconds", "latency",
                          ["method", "route", "status_class"],
                          buckets=(0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5),  # explicit
                          registry=registry)
```

`route` is the **route template** (`/orders/{id}`), never the raw path. No user id / request id labels.

## Log correlation (extend the scaffold structlog processors — do not replace)

```python
from opentelemetry import trace

def add_trace_context(logger, method_name, event_dict):
    span = trace.get_current_span()
    ctx = span.get_span_context() if span else None
    if ctx and ctx.is_valid:
        event_dict["trace_id"] = format(ctx.trace_id, "032x")
        event_dict["span_id"] = format(ctx.span_id, "016x")
    return event_dict
# insert add_trace_context into the existing structlog processor chain
```

## SLO document (docs/observability/slo.md)

```md
## SLO: API availability
- SLI: sum(rate(http_requests_total{status_class!="5xx"}[5m]))
       / sum(rate(http_requests_total[5m]))
- Target: 99.9% over 30d        # source: architecture/reliability §SLO-1
- Error budget: 0.1% (43m 12s / 30d)

## SLO: API latency
- SLI: histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
- Target: p99 < 500ms over 30d  # source: architecture/reliability §SLO-2
- Buckets chosen around the 500ms threshold (see metrics.py).
```

Every target carries its `architecture/reliability` source. A target with no source is an open ADR candidate.

## Multi-burn-rate alerts (deploy/alerts/<service-name>.rules.yaml)

```yaml
groups:
  - name: <service-name>-slo
    rules:
      - alert: AvailabilityFastBurn        # PAGE
        expr: (1 - <availability-sli>[1h]) > (14.4 * 0.001)
        for: 2m
        annotations: { runbook: "<runbook-url>#availability" }
      - alert: AvailabilitySlowBurn        # TICKET
        expr: (1 - <availability-sli>[6h]) > (3 * 0.001)
        for: 15m
        annotations: { runbook: "<runbook-url>#availability" }
```

Fast burn pages; slow burn tickets. Both are error-budget expressions, not static thresholds. Every alert links a runbook.

## pyproject additions (pinned examples)

```
opentelemetry-sdk==1.27.0
opentelemetry-exporter-otlp-proto-http==1.27.0
opentelemetry-instrumentation-fastapi==0.48b0
prometheus-client==0.21.0
```
