# Service Discovery Playbook

Use this playbook to gather decisions that change generated files. Ask no more than three related questions at once and include recommended defaults.

## Service context

Confirm:

- service name,
- business capability,
- **target directory** (where files will be written),
- **organization name** (for the Java package root),
- deployment target,
- Java version,
- Spring Boot version,
- build tool,
- database,
- auth model,
- sync vs async communication,
- container/runtime expectations.

Recommended default:

> I recommend Java 21, Spring Boot 3.x, Maven, Flyway, Postgres, stateless JWT for APIs, and containerized deployment because this gives a modern production baseline with broad platform support. Confirm or redirect.

### Target directory

Recommend `services/<service-name>/` for monorepos and the repository root for single-service repos. Refuse to scaffold into any directory that looks like a plugin or skill repository (contains `architecture/`, `implementations/`, `standards/`, `patterns/`, `marketplace.json`, `.claude-plugin/`, or this skill's own tree) without an explicit user override.

### Java package root derivation

- Strip hyphens and trailing `-api` / `-service` from the service name.
- Drop or hyphenate-collapse common suffixes (`-svc`, `-app`).
- Hyphens are illegal in Java package names — never emit them.
- Default organization namespace: `com.example` when none is given.

Examples:

- `orders-api` + org `acme` → `com.acme.orders`
- `payment-service` + no org → `com.example.payment`
- `notification-worker` + org `globex` → `com.globex.notification`

Confirm the derived package root with the user before generating files.

## Service classification

Classify the service as one:

- CRUD API,
- orchestration service,
- async worker,
- integration gateway,
- domain service,
- internal admin service,
- event processor.

Classification affects package structure, transaction boundaries, resilience strategy, observability, and testing.

Flag mismatches early:

- orchestration-heavy service using long synchronous JPA transactions,
- CRUD-only service split into a microservice without capability ownership,
- event processor without idempotency or dead-letter behavior,
- public API without explicit auth and abuse controls.

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
- distributed monolith patterns.

If the boundary is weak, recommend a modular monolith module or narrower capability before generating files.

## Runtime assumptions

Clarify:

- Kubernetes, VM, PaaS, or local-only target,
- statelessness,
- horizontal scaling,
- expected throughput,
- latency or SLO expectations,
- startup sensitivity,
- multi-region expectations,
- failure tolerance,
- graceful shutdown needs.

Surface hidden complexity: connection pooling, retries, backpressure, startup sequencing, dependency readiness, and rolling deploy behavior.
