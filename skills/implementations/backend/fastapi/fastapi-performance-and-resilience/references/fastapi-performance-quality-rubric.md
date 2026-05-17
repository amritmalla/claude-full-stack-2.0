# FastAPI Performance and Resilience Quality Rubric

Load this before declaring the performance and resilience work complete. Revise until each check passes or the unresolved gap is explicitly documented in the service README.

## Budget conformance

- [ ] Every latency/throughput budget, pool size, and SLO number traces to `architecture/performance` or `architecture/reliability`.
- [ ] No threshold (timeout, breaker, pool, SLO) was invented; any missing number is an open ADR candidate.
- [ ] Acceptable degradation behavior is sourced from `architecture/reliability`.

## Async-path discipline

- [ ] No synchronous blocking or CPU-bound work runs on an `async def` path.
- [ ] Blocking I/O uses an async driver or `run_in_threadpool`/`anyio.to_thread`.
- [ ] CPU-bound work runs in a process pool.
- [ ] An event-loop-lag probe is wired into `/readyz` and the metrics seam.

## Worker model

- [ ] The worker model is Gunicorn + `UvicornWorker` (or a documented alternative) per `architecture/performance`.
- [ ] Worker count is settings-driven.
- [ ] Graceful shutdown propagates from the master to every worker via the scaffold ASGI-lifespan (verified).
- [ ] If a single process is used on a multi-core host, the reason is documented.

## Downstream isolation

- [ ] Every external call has an explicit timeout (no unbounded `await`).
- [ ] Every external dependency has a circuit breaker with documented open/half-open/closed thresholds.
- [ ] An open breaker returns a defined degraded response immediately, not a hang (verified).
- [ ] Each dependency has a bulkhead (bounded concurrent calls) so one slow dependency cannot starve others.

## Pools and caching

- [ ] DB and HTTP-client pool sizes are derived from the worker model and downstream limits, and documented.
- [ ] worker_count × per-worker pool does not exceed the downstream connection limit.
- [ ] Caching posture is explicit: what is cached, TTL, invalidation trigger, stampede protection.
- [ ] No unbounded process-local cache.

## Retry budget

- [ ] Retries are capped with exponential backoff and jitter.
- [ ] A global retry-budget cap stops retries from amplifying a downstream outage.
- [ ] Non-idempotent calls are not retried without an idempotency key.
- [ ] The worst-case amplification factor is documented against the dependency's headroom.

## Backpressure

- [ ] Request concurrency is bounded.
- [ ] Saturation sheds load with 429/503 + `Retry-After` rather than collapsing.
- [ ] `/readyz` reflects saturation so the load balancer diverts traffic.

## Load-test gate

- [ ] A load-test script runs the expected traffic shape from `architecture/performance`.
- [ ] The script includes a dependency-failure scenario that exercises the breaker and backpressure.
- [ ] The gate asserts measured p99/throughput against the `architecture/reliability` SLO.
- [ ] The gate runs in CI and fails the build on an SLO miss (verified passing).

## Observability

- [ ] Event-loop lag, breaker state, pool saturation, shed count, and retry rate are observable via the scaffold/observability seam.
- [ ] No second telemetry stack was introduced.

## Build verification

- [ ] `mypy` reports zero errors.
- [ ] `ruff check` passes.
- [ ] The test command passes (or the skip is documented with reason).
- [ ] The boot smoke check passes and the load-test gate passes against the SLO.

## Standards conformance

- [ ] [observability-standards](../../../../../../standards/observability-standards/README.md): event-loop lag, breaker state, saturation, shed count, retry rate observable via the seam.
- [ ] [deployment-standards](../../../../../../standards/deployment-standards/README.md): worker model and pool sizes settings-driven and environment-agnostic; resource limits documented.

## Failure handling

If a check fails:

1. Identify the missing or incorrect discipline, isolation control, or gate.
2. Ask the user for clarification if a budget or SLO number cannot be sourced from `architecture/performance` or `architecture/reliability`.
3. Revise, then re-run `mypy`, `ruff check`, tests, the boot smoke check, and the load-test gate.
4. Keep any unresolved gap explicit in the service README — never invent a threshold to make the gate pass.
