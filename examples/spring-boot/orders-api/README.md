# orders-api (reference example)

Minimal e-commerce order service used as the canonical input for every skill in this plugin.

## Domain

**Endpoints**

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/orders` | Create an order (idempotency-key required) |
| `GET` | `/orders/{id}` | Fetch a single order |
| `GET` | `/orders?customerId=...` | List orders for a customer (cursor-paginated) |
| `POST` | `/orders/{id}/cancel` | Cancel an order (idempotency-key required) |

**State machine:** `created → paid → shipped → cancelled`

**Persistence:** Postgres 16 via Flyway-managed schema.
**Auth:** JWT (customer scope).
**Events:** logs `order.created` to stdout (Kafka deferred to v0.2).

## Why this domain

- **State transitions** force real schema design, idempotency, and auth scope checks.
- **Money** forces real error handling and integration tests with rollback.
- **Events** set up observability and tracing naturally.
- **Boring** keeps the focus on the skills, not the domain.

## Skill outputs

Every skill in this plugin is exercised against `orders-api`. The output produced by each skill is committed under [`.skill-outputs/<skill-name>/`](.skill-outputs/) for reference. Running the [`idea-to-production-spring-boot`](../../../workflows/idea-to-production-spring-boot/) workflow chains all 12 skills against this service end-to-end.

## Status

This directory ships intentionally incomplete. The skills *produce* the code; this directory exists to receive their outputs.
