---
name: spring-boot-performance-and-resilience
description: Use when tuning or hardening a Spring Boot service for latency, throughput, and resilience after backend architecture has defined per-path SLOs, dependency criticality, and degradation behavior. Produces timeouts, retries with budgets, circuit breakers, bulkheads, rate limiting, connection-pool and thread-pool sizing, caching posture, JVM and container-aware sizing, load-test scaffolding, and gates that defend the stated SLOs. Do not use for choosing the SLOs themselves, redesigning service boundaries, picking the cache topology, JVM image base layer construction, or Kubernetes-level scaling; use performance, reliability, backend-architecture, infrastructure-platform, or implementations/infrastructure/* instead.
---

# Spring Boot Performance and Resilience

## When to use

Invoke when a Spring Boot service must hit a stated latency, throughput, or availability target and the SLOs, dependency criticality, degradation behavior, and retry/timeout budgets have been decided by `performance`, `reliability`, and `backend-architecture`. Use it for new services entering load, for hardening an existing service before scale-up, or for review when production is page-prone, slow, or failing under partial outages.

Do not use for picking SLOs (use `reliability`), for capacity modelling or scaling strategy across components (use `performance`), for designing service boundaries or async contracts (use `backend-architecture`), for choosing the cache substrate or queue (use `data-architecture` or `backend-architecture`), for cluster-level autoscaling, PDBs, or HPA (use `infrastructure-platform` and `implementations/infrastructure/kubernetes`), or for image-level JVM packaging (use `implementations/infrastructure/kubernetes/dockerfile-and-jvm-tuning`).

## Inputs

Required:

- Spring Boot service source tree (or scaffold output).
- Approved per-path SLOs from `reliability` (availability and latency targets, error budget, evaluation window).
- Approved `backend-architecture.md` declaring synchronous and asynchronous dependencies, idempotency and retry semantics per call, and degradation behavior per journey.
- Container memory and CPU limits the service will run under, or the assumption that those land via deployment configuration.

Optional:

- Capacity model and traffic profile (peak RPS, p99 size, burst shape) from `performance`.
- Existing observability surface (`spring-boot-observability-readiness`) — RED metrics and traces are prerequisites for evidence-based tuning.
- Known hot paths, slow queries, or N+1 patterns surfaced from production.
- Cache substrate (Redis, Caffeine, two-tier) chosen by `data-architecture` or `backend-architecture`.
- Load-test environment availability and tooling preference (Gatling, k6, JMeter).
- Cost ceiling per instance or per request.

## Operating rules

- SLOs are the contract. Do not silently change a stated latency or availability target. If tuning cannot meet the target without changing the contract, raise it as an ADR candidate against `reliability` or `performance`.
- Tune with evidence, not intuition. Every change is justified by a metric (RED, USE), a profile, or a load-test result. No speculative pool resizing, no copy-pasted JVM flags.
- Every outbound call has an explicit timeout. The default Spring `RestTemplate` / `WebClient` / JDBC / Redis client timeouts are not acceptable defaults — they are decisions and must be stated.
- Retries have a budget. Define max attempts, backoff (exponential with jitter), and an overall deadline. Retries are only safe on idempotent operations; non-idempotent retries require the contract's idempotency key.
- Circuit breakers protect dependencies, not the service. Pick failure-rate, slow-call, and minimum-call thresholds aligned to dependency criticality from `reliability`. Open-circuit behavior maps to a degradation path defined in `backend-architecture`.
- Bulkheads isolate. Critical paths get their own thread pool or semaphore; do not let a slow downstream starve unrelated paths.
- Connection-pool size is derived, not guessed. For JDBC pools, use a sizing formula tied to peak concurrent in-flight queries and average query time; verify against the database's own connection budget.
- Thread-pool sizing reflects work shape. CPU-bound and I/O-bound paths get different pools. Servlet (Tomcat/Jetty) and WebFlux (Netty) tuning are different problems — do not mix the playbooks.
- Caches are correctness surfaces. Every cache entry has an explicit TTL, an invalidation rule, a size cap, and a stampede mitigation (single-flight or jittered refresh). No unbounded caches. PII is never cached without a documented retention policy.
- JVM and container memory must agree. Heap, metaspace, direct memory, and code cache fit inside the container limit with headroom; `-XX:MaxRAMPercentage` or explicit `-Xmx` is set against the container limit, not the host.
- Rate limiting protects the service and its dependencies. Choose the scope (per-tenant, per-key, global), the algorithm (token bucket, leaky bucket), and the action on exceed (429, queue, shed). Map directly to API contract behavior in `backend-architecture`.
- Load tests are part of the change. A performance or resilience change without a before/after load-test artifact is not done. The test exercises the same SLO surface the change is defending.
- Resilience changes are observable. Every retry, circuit-breaker state transition, bulkhead rejection, and rate-limit hit emits a metric and a structured log line with correlation IDs.

## Output contract

The tuning and resilience wiring MUST conform to:

- [api-standards](../../../../standards/api-standards/README.md) — timeouts, retries, idempotency, and 429 semantics where they affect the external contract surface.
- [security-standards](../../../../standards/security-standards/README.md) — no PII or secrets in cached payloads, logs, or metric labels; rate-limit keys do not leak tenant identity through error responses.
- [observability-standards](../../../../standards/observability-standards/README.md) — RED per path, resilience-event metrics, trace propagation through retries and circuit breakers, structured logs with correlation IDs on every degraded path.
- [deployment-standards](../../../../standards/deployment-standards/README.md) — JVM and pool sizing parameterized via deploy-time configuration, never baked into the image.
- [naming-conventions](../../../../standards/naming-conventions/README.md) — metric names, circuit-breaker names, and configuration keys follow the project's naming rules.

Upstream contracts:

- `reliability` is the source of truth for SLOs, dependency criticality, and graceful-degradation expectations.
- `performance` is the source of truth for capacity model, hot-path identification, caching strategy direction, and load-test plan.
- `backend-architecture.md` is the source of truth for idempotency keys, retry semantics, timeout posture, and degradation behavior per journey. If any of these are silent, this skill pauses and raises an ADR candidate rather than inventing the decision.

## Process

1. Read the SLOs from `reliability`, the capacity and hot-path notes from `performance`, and the dependency and degradation map from `backend-architecture.md`. Restate the per-path latency, availability, and throughput targets the service must defend.
2. Inventory the service surfaces: inbound HTTP paths, outbound HTTP/gRPC calls, JDBC datasources, cache calls, message-broker calls, scheduled jobs. Classify each by criticality and idempotency.
3. Confirm `spring-boot-observability-readiness` is in place. Tuning without RED metrics, traces, and structured logs is guesswork — backfill observability first.
4. Define timeouts per outbound surface. Set connect, read, and overall deadlines on every `RestClient`, `WebClient`, `RestTemplate`, JDBC datasource, Redis client, and Kafka client. Document each in a per-dependency table aligned to the budget from `backend-architecture`.
5. Define retry posture per outbound surface. Use Spring Retry or Resilience4j with exponential backoff plus jitter, a max-attempts cap, and a deadline. Mark non-idempotent paths as `no-retry` unless an idempotency key is enforced end-to-end.
6. Wire circuit breakers around external dependencies using Resilience4j: failure-rate threshold, slow-call threshold, sliding window, minimum-number-of-calls, wait-duration-in-open-state, and half-open trial size. Tie open-state behavior to the degradation path declared in `backend-architecture` (fallback, cached response, 503 with `Retry-After`, or queue).
7. Add bulkheads around independent dependency families. Use Resilience4j bulkhead (semaphore) or a dedicated thread pool per family. Pin sizes to expected concurrency and document the rejection behavior.
8. Size connection pools. For HikariCP, derive `maximumPoolSize` from peak concurrent in-flight queries and average query duration, capped by the database's connection budget divided by replica count. Set `connectionTimeout`, `validationTimeout`, `idleTimeout`, and `maxLifetime`. Repeat for Redis (Lettuce/Jedis) and any HTTP client pools.
9. Size thread pools and servlet container. For Tomcat: set `server.tomcat.threads.max`, `accept-count`, and `connection-timeout` against the capacity model. For WebFlux/Netty: do not block on the event loop — schedule blocking work on a bounded scheduler. For `@Async` and `ThreadPoolTaskExecutor`: bound core/max size and the queue capacity, define rejection policy.
10. Apply caching where `performance` or `backend-architecture` directs. Configure Spring Cache with the chosen substrate (Caffeine for local, Redis for shared, two-tier where called out). For each cache: TTL, max size or memory cap, eviction policy, single-flight or refresh-ahead, and an explicit invalidation rule for writes. Document PII posture and retention.
11. Add rate limiting at the chosen scope. For per-tenant or per-key limits use Bucket4j, Resilience4j RateLimiter, or a gateway-level limiter. Define the algorithm, refill rate, burst, and the response on exceed (`429` with `Retry-After` per API contract).
12. Tune the JVM against the container limit. Set `-XX:MaxRAMPercentage` (or explicit `-Xmx`) so total committed memory (heap + metaspace + direct + code cache + thread stacks) fits in the container limit with headroom. Pick the collector (G1 default, ZGC/Shenandoah for low-pause SLOs) and set GC logging.
13. Generate load-test scaffolding using Gatling, k6, or JMeter. Cover at minimum: steady-state at peak RPS, burst to peak × 2, dependency-outage simulation (timeouts, 5xx from a single dependency) to verify circuit-breaker and fallback behavior, and rate-limit verification.
14. Emit observability for every resilience surface. Resilience4j metrics (`resilience4j.circuitbreaker.calls`, `resilience4j.retry.calls`, `resilience4j.bulkhead.available.concurrent.calls`, `resilience4j.ratelimiter.available.permissions`), HikariCP pool metrics (`hikaricp.connections.active`, `pending`, `usage`), cache hit/miss/eviction (`cache.gets`, `cache.evictions`, `cache.puts`), and JVM metrics (heap, GC pause, thread count). Add structured log lines on every degraded outcome with correlation IDs.
15. Define the gate. State the load-test pass criteria tied to each SLO: p99 latency under target at peak RPS, error budget burn within policy under simulated single-dependency outage, no pool exhaustion or thread starvation under burst.
16. Validate against [observability-standards](../../../../standards/observability-standards/README.md), [security-standards](../../../../standards/security-standards/README.md), and the SLOs in `reliability`. Capture before/after metrics. Fix any divergence before declaring done.

## Outputs

Required:

- Per-dependency timeout, retry, circuit-breaker, and bulkhead configuration (Resilience4j `@Configuration` and/or `application*.yml`).
- Connection-pool and thread-pool configuration (HikariCP, Tomcat/WebFlux, `ThreadPoolTaskExecutor`) with the sizing rationale recorded in comments or an adjacent note.
- Cache configuration per cache region: TTL, size cap, eviction, invalidation rule, PII posture.
- Rate-limiter configuration per scope with response semantics aligned to API contract.
- JVM and container memory configuration parameterized via environment variables.
- Load-test scaffolding (Gatling/k6/JMeter scripts) covering steady-state, burst, dependency outage, and rate-limit verification.
- Observability wiring for resilience events, pool saturation, cache effectiveness, and JVM health.
- Before/after evidence per change: metric snapshots or load-test artifacts.

Optional, when applicable:

- ADR drafts for chosen GC, retry-vs-no-retry decisions, cache substrate trade-offs, or rate-limit scope.
- Runbook inputs for `operations`: how to drain a pool, flush a cache, reset a circuit breaker, raise a rate-limit ceiling.
- Capacity-test results feeding back into `performance`.

Output rules:

- No magic numbers without rationale. Every pool size, timeout, threshold, and TTL is either tied to an SLO or to a measurement; both are documented.
- No defaults left implicit. If a configuration is "the framework default", state that explicitly with the value.
- No JVM flag copy-paste from blog posts. Each flag is justified by the workload, the SLO, or the container shape.
- No retry on non-idempotent paths without an enforced idempotency key.

## Quality checks

- [ ] Every per-path SLO from `reliability` is restated in this skill's output and is the target of at least one load-test scenario.
- [ ] Every outbound surface (HTTP, JDBC, Redis, Kafka, gRPC) has an explicit connect, read, and overall timeout.
- [ ] Every retry-enabled path is idempotent or carries an enforced idempotency key; non-idempotent retries are explicitly disabled.
- [ ] Every external dependency has a circuit breaker tied to the degradation behavior declared in `backend-architecture`.
- [ ] HikariCP `maximumPoolSize` is derived (formula recorded), not guessed, and respects the database's connection budget.
- [ ] Servlet container or reactive scheduler is sized against the capacity model; blocking work on the WebFlux event loop is absent.
- [ ] Every cache has TTL, size cap, eviction policy, invalidation rule, and a documented PII posture.
- [ ] Rate limiting scope, algorithm, refill, burst, and 429 semantics are defined and consistent with the API contract.
- [ ] JVM heap plus metaspace plus direct plus code cache plus thread stacks fits the container memory limit with documented headroom.
- [ ] Resilience4j, HikariCP, cache, and JVM metrics are exposed via Micrometer and visible on dashboards.
- [ ] Load-test scaffolding covers steady-state, burst, simulated dependency outage, and rate-limit verification; pass criteria are stated.
- [ ] Before/after evidence accompanies every tuning change.

## References

- Upstream: [`architecture/reliability`](../../../../architecture/reliability/SKILL.md) — SLOs, dependency criticality, degradation expectations; [`architecture/performance`](../../../../architecture/performance/SKILL.md) — capacity model, hot paths, caching direction, load-test plan; [`architecture/backend-architecture`](../../../../architecture/backend-architecture/SKILL.md) — timeout, retry, idempotency, and degradation contract per journey.
- Related implementation skills: [`spring-boot-service-scaffold`](../spring-boot-service-scaffold/SKILL.md) (baseline this skill builds on), [`spring-boot-observability-readiness`](../spring-boot-observability-readiness/SKILL.md) (prerequisite — evidence-based tuning requires metrics, traces, and logs), [`spring-kafka-event-integration`](../spring-kafka-event-integration/SKILL.md) (producer/consumer timeouts, retry topology, and backpressure compose with this skill's outbound-surface posture).
- Compatible patterns: [`microservices`](../../../../architecture-patterns/microservices/README.md), [`event-driven`](../../../../architecture-patterns/event-driven/README.md), [`real-time-systems`](../../../../architecture-patterns/real-time-systems/README.md).
