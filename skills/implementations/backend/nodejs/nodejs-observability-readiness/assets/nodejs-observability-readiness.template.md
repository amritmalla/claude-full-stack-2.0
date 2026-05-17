# Node.js Observability Readiness — Reference

Use this as the canonical OpenTelemetry SDK, RED-metrics, log-correlation, and SLO/alert reference when making a scaffolded Node.js service observable. Placeholder tokens use `<kebab-case>` or `<PascalCase>`. SLO targets come from `architecture/reliability`; critical journeys from `backend-architecture.md`. Versions are pinned examples — replace with the current stable release; never use `^`.

## Directory additions (over the scaffold)

```
src/observability/
├── tracing.ts                            # OTel NodeSDK; replaces the no-op tracer seam
├── metrics.ts                            # prom-client registry; RED instruments
└── logger.ts                             # EXTENDED (not replaced): trace_id/span_id mixin
docs/observability/
└── slo.md                                # SLIs as queries; SLOs cite architecture/reliability
deploy/alerts/
└── <service-name>.rules.yaml             # multi-burn-rate fast + slow rules
```

## Config schema additions (extend the scaffold zod schema)

```ts
OTEL_SERVICE_NAME: z.string().min(1),
OTEL_EXPORTER_OTLP_ENDPOINT: z.string().url(),
OTEL_TRACES_SAMPLER_ARG: z.coerce.number().min(0).max(1).default(0.1),
METRICS_MODE: z.enum(['scrape', 'push']).default('scrape'),
```

`.env.example` gets the same keys with placeholder values.

## Tracing seam fill (src/observability/tracing.ts)

```ts
import { NodeSDK } from '@opentelemetry/sdk-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { resourceFromAttributes } from '@opentelemetry/resources';
import { config } from '../config/index.js';

export const sdk = new NodeSDK({
  resource: resourceFromAttributes({ 'service.name': config.OTEL_SERVICE_NAME }),
  traceExporter: new OTLPTraceExporter({ url: config.OTEL_EXPORTER_OTLP_ENDPOINT }),
  instrumentations: [getNodeAutoInstrumentations()],
});
sdk.start(); // call from main.ts BEFORE creating the HTTP server
```

A dead endpoint causes dropped spans, not failed requests — the exporter is async and non-blocking. Verify it.

## RED metrics (src/observability/metrics.ts)

```ts
import { Registry, Counter, Histogram } from 'prom-client';
export const registry = new Registry();

export const httpRequests = new Counter({
  name: 'http_requests_total', help: 'request count',
  labelNames: ['method', 'route', 'status_class'], registers: [registry],
});
export const httpErrors = new Counter({
  name: 'http_request_errors_total', help: 'errors by class',
  labelNames: ['method', 'route', 'error_class'], registers: [registry],
});
export const httpDuration = new Histogram({
  name: 'http_request_duration_seconds', help: 'latency',
  labelNames: ['method', 'route', 'status_class'],
  buckets: [0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5], // explicit; chosen around the SLO threshold
  registers: [registry],
});
```

`route` is the **route template** (`/orders/:id`), never the raw path. No user id / request id labels.

## Log correlation (extend the scaffold pino logger — do not replace)

```ts
import { trace } from '@opentelemetry/api';
// add to the existing pino options:
mixin() {
  const span = trace.getActiveSpan();
  if (!span) return {};
  const { traceId, spanId } = span.spanContext();
  return { trace_id: traceId, span_id: spanId };
}
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
- Buckets chosen around the 500ms threshold (see metrics.ts).
```

Every target carries its `architecture/reliability` source. A target with no source is an open ADR candidate, not a number.

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

## package.json additions (pinned examples)

```
@opentelemetry/sdk-node 0.52.1
@opentelemetry/auto-instrumentations-node 0.48.0
@opentelemetry/exporter-trace-otlp-http 0.52.1
prom-client 15.1.3
```
