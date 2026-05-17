# FastAPI Performance and Resilience Playbook

Load this when implementing any owned area of `fastapi-performance-and-resilience` or checking the anti-pattern list. It expands the operating rules and process steps in `SKILL.md` with the detail needed to make a service hold its SLO under load and failure.

## Why this workflow exists

FastAPI performance failures are structural, not micro-optimizations. One synchronous blocking call inside an `async def` route stalls the entire event loop — the service does not slow down, every concurrent request stops. A retry with no budget turns a downstream blip into a self-inflicted DDoS that keeps the dependency down. A default-sized connection pool under burst exhausts and every request hangs. No backpressure means a traffic spike does not degrade gracefully, it OOMs the worker. A single Uvicorn process on a 16-core box wastes 15 cores. None of these show on a laptop with one user; they all show in the first real incident — and a load-test gate is the only thing that catches them before then.

The goal is a service that keeps the event loop free, uses every core deliberately, fails downstream calls fast and in isolation, caches and sheds load on purpose, and has proven all of that against the SLO in CI.

## Behavioral rules in depth

### 1. Consume the budget; do not invent the threshold

`architecture/performance` owns latency/throughput budgets and pool sizing; `architecture/reliability` owns the SLO and acceptable degradation. A breaker threshold, a timeout, a pool size, or a "good enough p99" is a risk decision tied to those numbers — not an engineering guess. Missing number → ADR candidate, not a plausible-looking default.

### 2. Extend the scaffold; reuse the observability seam

Timeouts, breaker thresholds, pool sizes, and the worker count read from the scaffold validated settings. Resilience signals (event-loop lag, breaker state, saturation) flow through the observability seam `fastapi-observability-readiness` owns — this skill emits the metrics, it does not stand up a second telemetry stack. Shutdown ties to the scaffold ASGI-lifespan.

### 3. The event loop is sacred

A single synchronous blocking or CPU-bound call inside an `async def` path blocks *all* concurrency — one event loop per worker. Detection: measurable event-loop lag (`asyncio` slow-callback / a lag probe). Remediation: blocking I/O → an async driver (`asyncpg`, `httpx.AsyncClient`) or `run_in_threadpool`/`anyio.to_thread.run_sync`; CPU work (crypto, image, large serialization) → a `ProcessPoolExecutor`. Lag feeds `/readyz` so a starved worker is pulled from rotation. A common trap: a sync DB driver used from an async route.

### 4. Match the worker model to the workload

| Model | Fits | Mechanism |
|---|---|---|
| Gunicorn + UvicornWorker, N workers | Stateless request/response, scale to cores | `-w N -k uvicorn.workers.UvicornWorker` |
| Single Uvicorn | Dev, or behind an external process scaler | one loop; document why cores are unused |
| Process pool (within a worker) | CPU-bound tasks | offloaded executors, not the request loop |

Pick per `architecture/performance`. Worker count is settings-driven (commonly `2*cores+1`, but verify against the budget). Graceful shutdown must reach every worker via the scaffold ASGI-lifespan, or a deploy drops in-flight requests on N-1 workers silently.

### 5. Every external call is bounded and isolated

Three controls per dependency: a **timeout** (explicit deadline; no unbounded `await`), a **circuit breaker** (open after a failure-rate threshold, half-open probe, closed on recovery; an open breaker returns a *defined degraded response* immediately, not a hang), and a **bulkhead** (bounded concurrent calls per dependency so one slow dependency cannot consume the whole worker's capacity). Without isolation, one slow dependency takes down endpoints that do not even use it.

### 6. Connection pools are sized, not defaulted

DB and HTTP-client pool size must account for: worker count × per-worker pool ≤ the downstream's connection limit. A default SQLAlchemy/`httpx` pool multiplied across workers silently exceeds the database's `max_connections` under load and every request blocks waiting for a connection. Derive the number from the worker model and the downstream limit; document it against `architecture/performance`.

### 7. Retries have a budget

Uncontrolled retries are an amplification weapon: 3 retries × every client during a brownout = 4x load on an already-failing dependency. Controls: capped attempts, exponential backoff with jitter (no synchronized retry storms), and a *global retry-budget* (e.g. retries ≤ 10% of requests) that stops retrying when exhausted. Never retry a non-idempotent call without an idempotency key.

### 8. Caching is deliberate; backpressure is deliberate degradation

A cache without an explicit TTL, invalidation trigger, and stampede protection (single-flight / lock) is a correctness bug and a thundering-herd risk; an unbounded process-local dict is a memory leak. Under saturation the choice is collapse or shed: bounded concurrency with a 429/503 + `Retry-After` shed path keeps the service alive, and `/readyz` reflecting saturation diverts traffic. Unbounded acceptance is a deferred OOM.

### 9. Resilience is verified, not asserted

The load-test gate runs the expected traffic shape (RPS, burst, payload mix from `architecture/performance`) *and* a dependency-failure scenario (kill/slow a dependency mid-test), then asserts measured p99/throughput against the `architecture/reliability` SLO. It runs in CI and fails the build on a miss. "We added a breaker" without a test that trips it is a comment, not resilience.

## Step detail

**Step 1 — Context.** Load `architecture/performance` (budgets, pool sizing, payload limits) and `architecture/reliability` (SLO, error budget, degradation). Confirm scaffold. Missing number → ADR candidate.

**Step 2 — Settings.** Add `worker_count`, per-dependency `*_timeout_s`, `breaker_*` thresholds, `bulkhead_*` limits, `db_pool_size`, `http_pool_size`, `retry_budget_pct`, cache TTLs, `max_concurrency` to the scaffold `Settings` and `.env.example`.

**Step 3 — Async discipline.** Find sync/blocking calls in `async def`; move to async drivers or `run_in_threadpool`/`anyio.to_thread`; CPU → `ProcessPoolExecutor`. Add an event-loop-lag probe → `/readyz` + metrics seam.

**Step 4 — Worker model.** Configure Gunicorn + `UvicornWorker`, worker count from settings; propagate `SIGTERM` to workers through the scaffold lifespan.

**Step 5 — Isolation.** Wrap each dependency client in timeout + breaker (e.g. `purgatory`/custom) + bulkhead (an `asyncio.Semaphore`). Define each breaker's thresholds and the degraded response.

**Step 6 — Pools + caching.** Size DB/HTTP pools from worker model × downstream limit; implement a cache with explicit TTL, invalidation, and single-flight stampede protection. Document both vs `architecture/performance`.

**Step 7 — Retry budget.** Capped attempts + backoff+jitter + global budget limiter; idempotency-key gate for non-idempotent calls; document worst-case amplification vs dependency headroom.

**Step 8 — Backpressure + gate.** Bounded concurrency with 429/503 + `Retry-After`; `/readyz` reflects saturation. k6/Locust script: expected shape + dependency-failure scenario; assert p99/throughput vs SLO; wire as a CI gate.

**Step 9 — Verify.** `mypy`, `ruff check`, tests, boot smoke, then the load-test gate (passing, with the failure scenario exercising breaker/backpressure). Standards check; document gaps.

## Anti-patterns to detect

Call these out explicitly when found:

- A breaker/timeout/pool/SLO threshold with no `architecture/*` source (invented number)
- A synchronous blocking call (sync DB driver, `requests`, `time.sleep`, heavy CPU) inside an `async def` path
- A single Uvicorn process on a multi-core box with no documented reason
- Graceful shutdown that reaches the master but not the workers
- `await` on a network call with no timeout
- A circuit breaker that, when open, hangs instead of returning a defined degraded response
- No bulkhead — one slow dependency starves unrelated routes
- Default/unbounded connection pool; worker_count × pool exceeding the downstream limit
- Cache with no TTL/invalidation/stampede protection, or an unbounded process-local dict
- Retries with no cap, no jitter, or no global budget (outage amplification)
- Retrying a non-idempotent call without an idempotency key
- Unbounded request acceptance — no shed-load path, deferred OOM
- A second telemetry stack instead of the observability seam
- "Added a breaker/backpressure" with no load test that actually trips it
