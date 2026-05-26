# Service Discovery Playbook

Use this playbook to gather decisions that change generated files. Ask no more than three related questions at once and include recommended defaults.

## Service context

Confirm:

- service name,
- business capability,
- **target directory** (where files will be written),
- deployment target,
- Rust toolchain (edition, MSRV),
- web framework (axum vs actix-web),
- async runtime topology (multi-thread vs current-thread),
- database,
- auth model,
- sync vs async communication,
- container/runtime expectations.

Recommended default:

> I recommend Rust stable (latest) on edition 2021, axum + tokio multi-thread runtime, `sqlx` against Postgres, stateless JWT for APIs, and containerized deployment. This gives a modern production baseline with a strong middleware ecosystem (`tower`/`tower-http`) and compile-time-checked queries. Confirm or redirect.

### Target directory

Recommend `services/<service-name>/` for monorepos and the repository root for single-service repos. Refuse to scaffold into any directory that looks like a plugin or skill repository (contains `skills/`, `standards/`, `architecture-patterns/`, `marketplace.json`, `.claude-plugin/`, or this skill's own tree) without an explicit user override.

### Crate naming

- Cargo package names use `kebab-case` (e.g., `orders-api`).
- Rust module and library identifiers use `snake_case` (e.g., `orders_api`).
- The binary target name should match the Cargo package name to keep the Docker `CMD` predictable.
- If a library target is emitted, default it to the package name with `_api`/`_service` suffix stripped (e.g., package `orders-api` → library `orders`). Confirm with the user before generating.

Examples:

- `orders-api` → package `orders-api`, library crate `orders`, binary `orders-api`.
- `payment-service` → package `payment-service`, library crate `payment`, binary `payment-service`.
- `notification-worker` → package `notification-worker`, library crate `notification_worker`, binary `notification-worker`.

## Service classification

Classify the service as one:

- CRUD API,
- orchestration service,
- async worker,
- integration gateway,
- domain service,
- internal admin service,
- event processor.

Classification affects crate structure, transaction boundaries, resilience strategy, observability, and testing.

Flag mismatches early:

- orchestration-heavy service running long-blocking work on the tokio runtime without `spawn_blocking`,
- CRUD-only service split into a microservice without capability ownership,
- event processor without idempotency or dead-letter behavior,
- public API without explicit auth and abuse controls,
- worker-shaped service emitting an HTTP API only because "everything has an API".

## Boundary critique

Challenge:

- shared database between services,
- CRUD microservices with no capability boundary,
- god-service boundaries,
- transactional RPC chains,
- excessive synchronous coupling,
- data-model-driven service names,
- custom auth before platform auth is resolved,
- premature event-driven complexity,
- distributed monolith patterns,
- "Rust because performance" without a measured constraint upstream architecture has named.

If the boundary is weak, recommend a modular monolith module or narrower capability before generating files.

## Runtime assumptions

Clarify:

- Kubernetes, VM, PaaS, or local-only target,
- statelessness,
- horizontal scaling,
- expected throughput (RPS) and request latency targets,
- startup sensitivity (cold start, image-pull latency),
- multi-region expectations,
- failure tolerance,
- graceful shutdown needs (`SIGTERM` handling, in-flight request drain window),
- whether CPU-bound work exists (drives `spawn_blocking` discipline and worker-thread sizing).

Surface hidden complexity: connection pooling, retries with budgets, backpressure (concurrency-limit layer), startup sequencing, dependency readiness, and rolling deploy behavior.
