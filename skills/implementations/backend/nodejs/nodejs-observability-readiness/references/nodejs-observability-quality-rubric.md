# Node.js Observability Readiness Quality Rubric

Load this before declaring the observability work complete. Revise until each check passes or the unresolved gap is explicitly documented in the service README.

## Tracing

- [ ] The OpenTelemetry Node SDK is initialized with resource attributes and an OTLP exporter.
- [ ] Auto-instrumentation covers HTTP, the framework, and the DB/client libraries.
- [ ] The SDK starts before the HTTP server (the framework is instrumented).
- [ ] The scaffold no-op tracer seam is replaced; no telemetry TODO remains.
- [ ] Manual spans exist only for business-meaningful operations (no span spam, no missing critical span).

## Metrics (RED)

- [ ] A request-rate counter, an error counter by class, and a duration histogram are exposed.
- [ ] The duration histogram uses explicit, documented buckets chosen around the SLO threshold.
- [ ] Metric labels are bounded (method, route template, status class) — no user id, raw path, or request id.
- [ ] `/metrics` is exposed (or a push exporter is configured) per the config mode.
- [ ] `/metrics` is network- or auth-scoped where the architecture requires it.

## Log correlation

- [ ] Every in-request log line carries `trace_id` and `span_id`.
- [ ] Correlation extends the scaffold pino logger and request context — no second logger.
- [ ] A local request was verified to produce a trace, a RED increment, and a log line sharing the trace id.

## SLIs and SLOs

- [ ] `docs/observability/slo.md` exists and is referenced from the service README.
- [ ] Every SLI is a concrete metric query, not prose.
- [ ] Every SLO cites a target and error-budget window sourced from `architecture/reliability`.
- [ ] No SLO target is invented; any missing target is an open ADR candidate, not a guessed number.
- [ ] The histogram bucket rationale is documented next to the latency SLI.

## Alerting

- [ ] Each SLO has a fast-burn (page) and a slow-burn (ticket) rule.
- [ ] Alert rules are expressed against the error budget, not a single static threshold.
- [ ] Each alert links to a runbook location.

## Export resilience

- [ ] OTLP endpoint, sampling, and exposure mode resolve through the scaffold validated config seam.
- [ ] Pointing the exporter at a dead endpoint does not block or crash the request path (verified).

## Build verification

- [ ] `tsc --noEmit` reports zero errors.
- [ ] The lint command passes.
- [ ] The test command passes (or the skip is documented with reason).
- [ ] The boot smoke check still passes with telemetry enabled.

## Standards conformance

- [ ] [observability-standards](../../../../../../standards/observability-standards/README.md): three correlated signals; RED metrics with documented buckets; SLIs as queries; multi-burn-rate alerts tied to an error budget; bounded cardinality; config-driven fail-safe export.

## Failure handling

If a check fails:

1. Identify the missing or incorrect instrumentation, SLI, or alert.
2. Ask the user for clarification if an SLO target cannot be sourced from `architecture/reliability`.
3. Revise, then re-run `tsc --noEmit`, lint, tests, the boot smoke check, and the local three-signal correlation check.
4. Keep any unresolved gap explicit in the service README — never invent an SLO number to close a gap silently.
