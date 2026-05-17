# Node.js Performance and Resilience Playbook

Load this when implementing any owned area of `nodejs-performance-and-resilience` or checking the anti-pattern list. It expands the operating rules and process steps in `SKILL.md` with the detail needed to make a service hold its SLO under load and failure.

## Why this workflow exists

Node performance failures are structural, not micro-optimizations. One synchronous CPU loop on the event loop freezes every concurrent request — the service does not slow down, it stops. A retry with no budget turns a downstream blip into a self-inflicted DDoS that keeps the dependency down. No backpressure means a traffic burst does not degrade gracefully, it OOMs the process. A single Node process on a 16-core box wastes 15 cores while latency climbs. None of these show on a laptop with one user; they all show in the first real incident — and a load-test gate is the only thing that catches them before then.

The goal is a service that keeps the event loop free, uses every core deliberately, fails downstream calls fast and in isolation, sheds load on purpose, and has proven all of that against the SLO in CI.

## Behavioral rules in depth

### 1. Consume the budget; do not invent the threshold

`architecture/performance` owns latency/throughput budgets; `architecture/reliability` owns the SLO and acceptable degradation. A breaker threshold, a timeout, or a "good enough p99" is a risk decision tied to those numbers — not an engineering guess. Missing number → ADR candidate, not a plausible-looking default.

### 2. Extend the scaffold; reuse the observability seam

Timeouts, breaker thresholds, pool sizes, and the scale model read from the scaffold validated config. Resilience signals (event-loop lag, breaker state, saturation) flow through the observability seam `nodejs-observability-readiness` owns — this skill emits the metrics, it does not stand up a second telemetry stack. Shutdown ties to the scaffold hook.

### 3. The event loop is sacred

A single blocking or CPU-bound operation on the main thread blocks *all* concurrency — Node is one event loop. Detection: measurable event-loop lag (`perf_hooks` monitorEventLoopDelay). Remediation: CPU work → `worker_threads` or a separate process; blocking I/O → async API; large JSON / crypto / compression → off-thread. Lag is wired into `/readyz` so a starved instance is pulled from rotation.

### 4. Match the scale model to the workload

| Model | Fits | Mechanism |
|---|---|---|
| Clustering | Stateless request/response, scale to cores | Primary forks N workers, shared listen socket |
| Worker threads | CPU-bound tasks within one process | Pool of threads, message-passed work |
| Single process | I/O-bound, low traffic, or behind an external scaler | One loop; document why cores are unused |

Pick per `architecture/performance`. Worker count is config-driven (default = CPU count). Graceful shutdown must reach every worker via the scaffold hook, or a deploy drops in-flight requests on N-1 workers silently.

### 5. Every external call is bounded and isolated

Three controls per dependency:

- **Timeout** — an explicit deadline; no unbounded `await fetch(...)`.
- **Circuit breaker** — open after a failure-rate threshold, half-open probe, closed on recovery; an open breaker returns a *defined degraded response* immediately, not a hang.
- **Bulkhead** — bounded concurrent calls per dependency so one slow dependency cannot consume the whole worker's capacity and starve unrelated routes.

Without isolation, one slow dependency takes down endpoints that do not even use it.

### 6. Retries have a budget

Uncontrolled retries are an amplification weapon: 3 retries × every client during a downstream brownout = 4x load on an already-failing dependency, which guarantees it stays down. Controls: capped attempts, exponential backoff with jitter (no synchronized retry storms), and a *global retry-budget* (e.g. retries ≤ 10% of requests) that stops retrying when the budget is exhausted. Never retry a non-idempotent call without an idempotency key.

### 7. Backpressure is deliberate degradation

Under saturation the choice is collapse or shed. Bounded request concurrency / queue depth with a shed-load path — 429 or 503 with `Retry-After` — keeps the service alive and honest. `/readyz` reflects saturation so the load balancer diverts traffic instead of piling it on. Unbounded acceptance is not resilience; it is a deferred OOM.

### 8. Resilience is verified, not asserted

The load-test gate runs the expected traffic shape (RPS, burst, payload mix from `architecture/performance`) *and* a dependency-failure scenario (kill/slow a dependency mid-test), then asserts measured p99/throughput against the `architecture/reliability` SLO. It runs in CI and fails the build on a miss. "We added a breaker" without a test that trips it is a comment, not resilience.

## Step detail

**Step 1 — Context.** Load `architecture/performance` (budgets, payload limits) and `architecture/reliability` (SLO, error budget, degradation). Confirm scaffold. Missing number → ADR candidate.

**Step 2 — Config.** Add `SCALE_MODEL`, `WORKER_COUNT`, per-dependency `*_TIMEOUT_MS`, `BREAKER_*` thresholds, `BULKHEAD_*` limits, `RETRY_BUDGET`, `MAX_CONCURRENCY` to the scaffold zod schema and `.env.example`.

**Step 3 — Event loop.** Find CPU/blocking work; move to `worker_threads` or a subprocess; async-ify blocking I/O. Add `monitorEventLoopDelay` probe → `/readyz` + metrics seam.

**Step 4 — Scale model.** Implement clustering or a worker pool per architecture; worker count from config; propagate `SIGTERM` from primary to workers through the scaffold shutdown.

**Step 5 — Isolation.** Wrap each dependency client in timeout + breaker (e.g. `opossum`) + bulkhead (bounded concurrency). Define each breaker's open/half-open thresholds and the degraded response.

**Step 6 — Retry budget.** Capped attempts + backoff+jitter + global budget limiter; idempotency-key gate for non-idempotent calls; document worst-case amplification vs dependency headroom.

**Step 7 — Backpressure.** Bounded concurrency/queue with 429/503 + `Retry-After` shed path; `/readyz` reflects saturation.

**Step 8 — Load-test gate.** k6/autocannon/Artillery script: expected shape + dependency-failure scenario; assert p99/throughput vs SLO; wire as a CI gate.

**Step 9 — Verify.** `tsc --noEmit`, lint, tests, boot smoke, then the load-test gate (passing, with the failure scenario exercising breaker/backpressure). Standards check; document gaps.

## Anti-patterns to detect

Call these out explicitly when found:

- A breaker/timeout/SLO threshold with no `architecture/*` source (invented number)
- Synchronous CPU-bound work (JSON, crypto, compression, loops) on the main event loop
- A single Node process on a multi-core box with no documented reason
- Graceful shutdown that reaches the primary but not the workers
- `await` on a network call with no timeout
- A circuit breaker that, when open, hangs instead of returning a defined degraded response
- No bulkhead — one slow dependency starves unrelated routes
- Retries with no cap, no jitter, or no global budget (outage amplification)
- Retrying a non-idempotent call without an idempotency key
- Unbounded request acceptance — no shed-load path, deferred OOM
- A second telemetry stack instead of the observability seam
- "Added a breaker/backpressure" with no load test that actually trips it
