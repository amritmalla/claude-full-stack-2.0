# ADR 0001: Modular monolith on Spring Boot

> Worked ADR example produced by this skill alongside the orders-api system design. Use as a style anchor: short, decision-oriented, downsides explicit, revisit trigger named.

## Status

Accepted

## Context

The orders-api PRD names one primary user (the repeat retail customer), one core workflow (create / fetch / list / cancel an order), a single owning team, and no constraint that requires independent scaling, fault isolation, or independent release cadence between components. The PRD explicitly defers Kafka to v2 and constrains the stack to Spring Boot + Postgres + Flyway + JWT.

Three styles were considered:

- **Modular monolith on Spring Boot** — single deployable, module boundaries enforced by Java packages and Spring component scopes.
- **Microservices** (split Order API / Order Service / Event Emitter into separate deployables) — rejected: no PRD constraint creates independent scale, ownership, or fault-isolation needs; introduces operational burden (service discovery, distributed tracing, deployment coordination) that the team would carry without benefit.
- **Serverless function-per-endpoint** (e.g., AWS Lambda + RDS Proxy) — rejected: local debugging friction, cold-start latency conflicts with the 150ms p99 target on `GET /orders/{id}`, Flyway-managed schema migrations don't fit the per-function lifecycle, and transactional boundaries with Postgres get awkward.

## Decision

Ship orders-api as a single Spring Boot deployable with internal module boundaries (`api/`, `service/`, `persistence/`, `events/`). Modules communicate via plain Java calls. Postgres is shared across modules; module ownership of tables is enforced by code review, not by separate schemas.

## Consequences

**Benefits**

- One deployable, one runtime, one log stream, one set of metrics. Operational surface area matches team size.
- Transactional writes across `orders`, `order_lines`, and `idempotency_keys` are trivial — a single Postgres transaction.
- Refactoring module boundaries is a code-review change, not a service-extraction project.

**Downsides accepted**

- All endpoints scale together. If `GET /orders` ever develops a fan-out read pattern with very different load characteristics from writes, we will be paying for write capacity to serve reads (or vice versa).
- A bug in any module can take down the whole deployable. Failure isolation is module-level (try/catch, bulkheading) rather than process-level.
- Future extraction of a module into its own service is a real refactor — module boundaries inside one process are easier to violate than network boundaries, even with discipline.

**Revisit when**

- Read traffic on `GET /orders` exceeds 10× write traffic and scaling profiles diverge meaningfully.
- A second team takes ownership of a subset of the domain (e.g., a fulfillment team owning state-advancement endpoints).
- The v2 Kafka outbox arrives and the event-emission path needs an isolated failure domain.
- A compliance regime (e.g., a PCI scope creep that lands payment data in this service) forces process-level isolation.
