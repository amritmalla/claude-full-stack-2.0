# Node.js Performance and Resilience — Reference

Use this as the canonical event-loop, scale-model, circuit-breaker, backpressure, and load-test reference when hardening a scaffolded Node.js service. Placeholder tokens use `<kebab-case>` or `<PascalCase>`. Budgets come from `architecture/performance`; SLO targets from `architecture/reliability`. Versions are pinned examples — replace with the current stable release; never use `^`.

## Directory additions (over the scaffold)

```
src/resilience/
├── event-loop.ts                         # monitorEventLoopDelay probe → /readyz + metrics
├── cluster.ts                            # scale model: clustering or worker-thread pool
├── breaker.ts                            # per-dependency timeout + circuit breaker + bulkhead
├── retry.ts                              # capped backoff+jitter + global retry budget
└── backpressure.ts                       # bounded concurrency + shed-load (429/503)
load/
└── <service-name>.loadtest.js            # k6/autocannon: traffic shape + failure scenario
```

## Config schema additions (extend the scaffold zod schema)

```ts
SCALE_MODEL: z.enum(['cluster', 'worker-threads', 'single']),
WORKER_COUNT: z.coerce.number().int().positive().default(0), // 0 = os.cpus().length
HTTP_DEP_TIMEOUT_MS: z.coerce.number().int().positive().default(2000),
BREAKER_ERROR_THRESHOLD_PCT: z.coerce.number().min(1).max(100).default(50),
BREAKER_RESET_MS: z.coerce.number().int().positive().default(10_000),
BULKHEAD_MAX_CONCURRENT: z.coerce.number().int().positive().default(20),
RETRY_MAX_ATTEMPTS: z.coerce.number().int().min(0).default(2),
RETRY_BUDGET_PCT: z.coerce.number().min(0).max(100).default(10),
MAX_INFLIGHT_REQUESTS: z.coerce.number().int().positive().default(200),
```

`.env.example` gets the same keys with placeholder values. Defaults shown are illustrative — set from `architecture/performance`.

## Event-loop lag probe (src/resilience/event-loop.ts)

```ts
import { monitorEventLoopDelay } from 'node:perf_hooks';
const h = monitorEventLoopDelay({ resolution: 20 });
h.enable();
export const eventLoopLagMs = () => h.mean / 1e6;
// Register a /readyz dependency check: lag under threshold → ready.
// Emit eventLoopLagMs() through the observability metrics seam.
```

## Scale model (src/resilience/cluster.ts — clustering example)

```ts
import cluster from 'node:cluster';
import os from 'node:os';
import { config } from '../config/index.js';

export function withCluster(start: () => void) {
  const n = config.WORKER_COUNT || os.availableParallelism();
  if (config.SCALE_MODEL === 'cluster' && cluster.isPrimary) {
    for (let i = 0; i < n; i++) cluster.fork();
    process.on('SIGTERM', () => {            // propagate to workers
      for (const w of Object.values(cluster.workers ?? {})) w?.kill('SIGTERM');
    });
  } else {
    start(); // worker (or single): scaffold graceful shutdown handles drain
  }
}
```

CPU-bound work uses `node:worker_threads` instead — never run it inline on the request path.

## Timeout + breaker + bulkhead (src/resilience/breaker.ts)

```ts
import CircuitBreaker from 'opossum';
import { config } from '../config/index.js';

const opts = {
  timeout: config.HTTP_DEP_TIMEOUT_MS,                 // explicit deadline
  errorThresholdPercentage: config.BREAKER_ERROR_THRESHOLD_PCT,
  resetTimeout: config.BREAKER_RESET_MS,               // half-open after this
  capacity: config.BULKHEAD_MAX_CONCURRENT,            // bulkhead
};

export function guarded<T>(name: string, call: () => Promise<T>, degraded: () => T) {
  const cb = new CircuitBreaker(call, opts);
  cb.fallback(degraded);   // open breaker → defined degraded response, NOT a hang
  return cb.fire();
}
```

## Retry budget (src/resilience/retry.ts)

```ts
// Capped attempts + exponential backoff + jitter + a global budget.
// Stop retrying when retries in the window exceed RETRY_BUDGET_PCT of requests.
// Guard: never retry a non-idempotent call without an idempotency key.
```

## Backpressure / shed load (src/resilience/backpressure.ts)

```ts
let inflight = 0;
export function admit(): boolean {
  if (inflight >= config.MAX_INFLIGHT_REQUESTS) return false; // caller → 503
  inflight++; return true;
}
export function release() { inflight--; }
// On reject: respond 503 + Retry-After; flip /readyz to not-ready while saturated.
```

## Load-test gate (load/<service-name>.loadtest.js — k6 sketch)

```js
import http from 'k6/http';
import { check } from 'k6';

export const options = {
  scenarios: {
    expected: { executor: 'ramping-vus', stages: [/* shape from architecture/performance */] },
  },
  thresholds: {
    http_req_duration: ['p(99)<500'],   // from architecture/reliability SLO
    http_req_failed:   ['rate<0.001'],  // error budget
  },
};
export default function () {
  check(http.get(`${__ENV.TARGET}/`), { 'status 200': (r) => r.status === 200 });
}
// A second scenario kills/slows a dependency mid-run to exercise breaker + backpressure.
// CI runs this and FAILS the build if a threshold is breached.
```

## package.json additions (pinned examples)

```
opossum 8.1.4            # circuit breaker + bulkhead
# load tester: k6 (binary, run in CI) OR autocannon 7.15.0 (devDependency)
```

## Service README additions

Document: the scale model and worker count (cite `architecture/performance`), every timeout/breaker/bulkhead threshold and its source, the retry budget and worst-case amplification factor, the shed-load behavior, and how to run the load-test gate locally and in CI.
