# FastAPI Performance and Resilience — Reference

Use this as the canonical async-discipline, worker-model, circuit-breaker, pool/cache, and load-test reference when hardening a scaffolded FastAPI service. Placeholder tokens use `<kebab-case>` or `<PascalCase>`. Budgets come from `architecture/performance`; SLO targets from `architecture/reliability`. Versions are pinned examples — never use unbounded specifiers.

## Directory additions (over the scaffold)

```
app/resilience/
├── event_loop.py                         # lag probe → /readyz + metrics
├── breaker.py                            # per-dependency timeout + circuit breaker + bulkhead
├── retry.py                              # capped backoff+jitter + global retry budget
├── pools.py                              # sized DB/HTTP client pools
├── cache.py                              # explicit TTL + invalidation + single-flight
└── backpressure.py                       # bounded concurrency + shed-load (429/503)
gunicorn.conf.py                          # worker model: UvicornWorker, worker count
load/
└── <service-name>.loadtest.js            # k6/Locust: traffic shape + failure scenario
```

## Settings additions (extend the scaffold Settings model)

```python
worker_count: int = 0                  # 0 = derive (e.g. 2*cpu+1), verify vs budget
http_dep_timeout_s: float = 2.0
breaker_error_threshold_pct: float = 50.0
breaker_reset_s: float = 10.0
bulkhead_max_concurrent: int = 20
db_pool_size: int = 5                  # worker_count * db_pool_size <= db max_connections
http_pool_size: int = 20
retry_max_attempts: int = 2
retry_budget_pct: float = 10.0
cache_ttl_s: int = 30
max_inflight_requests: int = 200
```

`.env.example` gets the same keys with placeholder values. Defaults are illustrative — set from `architecture/performance`.

## Event-loop lag probe (app/resilience/event_loop.py)

```python
import asyncio, time

_lag_ms = 0.0
async def _sample():
    global _lag_ms
    while True:
        t = time.perf_counter()
        await asyncio.sleep(0.25)
        _lag_ms = max(0.0, (time.perf_counter() - t - 0.25) * 1000)

def event_loop_lag_ms() -> float: return _lag_ms
# Register a /readyz check: lag under threshold → ready. Emit via the metrics seam.
```

## Worker model (gunicorn.conf.py)

```python
import os
bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"
worker_class = "uvicorn.workers.UvicornWorker"
workers = int(os.getenv("WORKER_COUNT") or (os.cpu_count() or 1) * 2 + 1)
graceful_timeout = int(os.getenv("SHUTDOWN_TIMEOUT_S", "10"))  # drain in-flight
# The scaffold ASGI-lifespan shutdown runs per worker on SIGTERM.
```

CPU-bound work uses a `ProcessPoolExecutor` — never run it inline on the request loop.

## Timeout + breaker + bulkhead (app/resilience/breaker.py)

```python
import asyncio

class Dependency:
    def __init__(self, name, timeout_s, threshold_pct, reset_s, max_concurrent, degraded):
        self._sem = asyncio.Semaphore(max_concurrent)   # bulkhead
        self._degraded = degraded
        # track rolling failure rate; open/half-open/closed per threshold_pct/reset_s

    async def call(self, coro_factory):
        if self._is_open:
            return self._degraded()                     # NOT a hang
        async with self._sem:
            try:
                return await asyncio.wait_for(coro_factory(), self._timeout_s)
            except Exception:
                self._record_failure()
                raise
```

## Retry budget (app/resilience/retry.py)

```python
# Capped attempts + exponential backoff + jitter + a global budget.
# Stop retrying when retries in the window exceed retry_budget_pct of requests.
# Guard: never retry a non-idempotent call without an idempotency key.
```

## Caching (app/resilience/cache.py)

```python
# Explicit TTL; invalidation on the documented trigger; single-flight lock so a
# cache miss under load does not stampede the backend. Bounded size — never an
# unbounded module-level dict.
```

## Backpressure / shed load (app/resilience/backpressure.py)

```python
import asyncio
_inflight = 0
def admit() -> bool:
    global _inflight
    if _inflight >= settings.max_inflight_requests:
        return False                                    # caller → 503 + Retry-After
    _inflight += 1
    return True
# On reject: 503 + Retry-After; flip /readyz to not-ready while saturated.
```

## Load-test gate (load/<service-name>.loadtest.js — k6 sketch)

```js
import http from 'k6/http';
import { check } from 'k6';
export const options = {
  scenarios: { expected: { executor: 'ramping-vus', stages: [/* shape from architecture/performance */] } },
  thresholds: {
    http_req_duration: ['p(99)<500'],    // from architecture/reliability SLO
    http_req_failed:   ['rate<0.001'],   // error budget
  },
};
export default function () {
  check(http.get(`${__ENV.TARGET}/`), { 'status 200': (r) => r.status === 200 });
}
// A second scenario kills/slows a dependency mid-run to exercise breaker + backpressure.
// CI runs this and FAILS the build if a threshold is breached.
```

## pyproject additions (pinned examples)

```
gunicorn==23.0.0          # worker manager (already in scaffold)
# load tester: k6 (binary, run in CI) OR locust==2.31.6 (devDependency)
```

## Service README additions

Document: the worker model and worker count (cite `architecture/performance`), every timeout/breaker/bulkhead/pool threshold and its source, the caching posture, the retry budget and worst-case amplification factor, the shed-load behavior, and how to run the load-test gate locally and in CI.
