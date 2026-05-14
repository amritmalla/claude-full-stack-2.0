# System Design — orders-api (example output)

> Worked example produced by this skill from the orders-api PRD. Uses the conditional-section rules: Persistence Strategy is folded into Components, and Operational Considerations is merged into Failure Modes because the design has one runtime topology.

## Overview

orders-api is the system of record for customer-owned orders in an e-commerce platform. It exposes a small synchronous HTTP API for customers (via the storefront client) and accepts state-advancement calls from upstream services (payments, fulfillment). It optimizes for **durability of the order record**, **idempotency under client retry**, and **operational simplicity** for a single team. It intentionally does not optimize for cross-region availability, multi-tenant isolation, or sub-50ms tail latency.

## Architecture Style

**Modular monolith on Spring Boot, single Postgres, synchronous HTTP.** Justified by: one primary persona, one core workflow, a single team, no independent-scale profile in the PRD, and explicit deferral of Kafka to v2. Simpler alternatives considered: a serverless function-per-endpoint design (rejected — local debugging, transactional boundaries with Postgres, and Flyway migrations all favor a single deployable). Microservices considered and rejected: no PRD constraint creates independent scale, ownership, or fault-isolation needs. See [ADR 0001](adrs/0001-modular-monolith-on-spring-boot.md).

## Bounded Contexts

| Name | Responsibility | Owned Data | Upstream | Downstream |
|---|---|---|---|---|
| Order Lifecycle | Create, fetch, list, cancel, enforce state machine | `orders`, `order_lines`, `idempotency_keys` | Storefront client (customer JWT), Payments service (paid), Fulfillment service (shipped) | Event log (stdout in v1) |

One context is correct here. Splitting "Order Read" and "Order Write" was considered and rejected: there is no divergent read model in v1, and CQRS without divergent reads is the canonical anti-pattern.

## Components

### Order API (HTTP)
- **Responsibility:** terminate customer and service-to-service HTTP, enforce auth and ownership scope, route to Order Service.
- **Interfaces:** `POST /orders`, `GET /orders/{id}`, `GET /orders`, `POST /orders/{id}/cancel`, plus internal `POST /orders/{id}/advance-state` for upstream services.
- **Persistence:** none (stateless).
- **Consistency:** strong; reads from primary Postgres.

### Order Service
- **Responsibility:** state-machine enforcement, idempotency resolution, line-item validation, event emission.
- **Interfaces:** internal module called from Order API.
- **Persistence:** Postgres via Flyway-managed schema. `orders` is the source of truth. `idempotency_keys` table stores `(key, customer_id, response_hash, created_at)` with 24h TTL.
- **Consistency:** transactional within a single Postgres write.
- **Scaling:** vertical for v1; horizontal stateless replicas behind Postgres if needed. See [ADR 0002](adrs/0002-postgres-as-system-of-record.md).

### Event Emitter
- **Responsibility:** emit `order.created` to the event sink.
- **Interfaces:** stdout in v1, Kafka topic in v2.
- **Persistence:** none.
- **Consistency:** best-effort in v1 (logs are not a durable contract); transactional outbox in v2. See [ADR 0003](adrs/0003-stdout-events-defer-kafka.md).

## Data Flow

1. Customer → Storefront → `POST /orders` with JWT and `Idempotency-Key` header.
2. Order API verifies JWT, extracts `customerId` from `sub`, hands off to Order Service.
3. Order Service checks `idempotency_keys` — if hit, returns the stored response hash; if miss, opens a transaction, inserts `orders` + `order_lines` + `idempotency_keys` atomically.
4. On commit, Event Emitter writes `order.created` to stdout.
5. State advancement (`paid`, `shipped`) arrives via internal endpoint from upstream services, also idempotent, also a single transaction.

**Source of truth:** `orders` table. **Write owner:** Order Service. **Read pattern:** primary-read only in v1; no replicas, no cache. **Idempotency:** required on all state-changing endpoints, 24h key retention. **Reconciliation:** none needed — single store, single writer.

## Failure Modes

| Component | Failure | User Impact | Detection | Recovery | Degradation |
|---|---|---|---|---|---|
| Postgres primary | Outage | All endpoints 503 | Liveness probe + Postgres connection metric | Restart / failover; replay any in-flight from client | None — fail fast, return 503 with `Retry-After` |
| Order Service | Idempotency-key TTL race (two concurrent retries with same key) | Theoretical duplicate order | Unique constraint on `(customer_id, idempotency_key)` | DB rejects second insert; service returns the first response | Built into the schema |
| Event Emitter (stdout) | Log pipeline drops `order.created` | Downstream consumers miss event; order itself is fine | Compare order count vs event count in dashboards | Manual replay from `orders` table | Documented in v1 — stdout is best-effort, not a contract |
| Auth | JWT verification fails (expired / invalid signature) | 401 to customer | Standard Spring Security metrics | Customer re-authenticates | None |
| Upstream state advancer (payments / fulfillment) | Calls `advance-state` with illegal transition | 409 to caller | Server-side state-machine guard | Caller surfaces error; state stays correct | None — illegal transitions are rejected |

Operational notes folded in: Spring Boot Actuator for liveness/readiness, structured JSON logs, p99 latency + Postgres connection-pool metrics, Flyway runs on startup, no feature flags in v1. See [ADR 0004](adrs/0004-jwt-auth-with-customer-scope.md) for the auth decision.

## Security and Compliance

- **Auth:** JWT issued by upstream auth service, claim `sub` = `customerId`. No admin scope in v1. See [ADR 0004](adrs/0004-jwt-auth-with-customer-scope.md).
- **Authorization:** every read and write is filtered by `customerId` derived from the JWT. Cross-customer reads are impossible by construction, not by check.
- **Sensitive data:** no PCI — payment is upstream. Line items are pre-priced and contain no card data. Customer PII limited to `customerId` (opaque) and shipping address (out of scope for v1; address resolution is an upstream concern).
- **Retention:** orders retained indefinitely in v1. Archival policy is an open question deferred from the PRD.
- **Auditability:** all state transitions logged with `actor`, `from`, `to`, `at`. No separate audit table in v1 — application logs are the audit trail.

## ADR Index

| # | Title | Status | Summary |
|---|---|---|---|
| 0001 | Modular monolith on Spring Boot | Accepted | Single deployable; rejected microservices and serverless. |
| 0002 | Postgres as system of record | Accepted | Single transactional store; rejected document DB and event sourcing. |
| 0003 | stdout events in v1, defer Kafka to v2 | Accepted | Acknowledges stdout is best-effort; documents the v2 transactional outbox plan. |
| 0004 | JWT auth with customer scope only | Accepted | No admin scope; cross-customer access impossible by construction. |

## Omitted sections

- **Persistence Strategy:** folded into Components — one Postgres store, one mapping, no warrant for a separate section.
- **Operational Considerations:** merged into Failure Modes — single runtime topology, no durable operational decisions that aren't already captured as failures or in ADR 0004.
