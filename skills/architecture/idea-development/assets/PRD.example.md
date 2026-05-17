# PRD — orders-api (example output)

> Worked example of a PRD produced by this skill. Use as a style and length anchor, not a copy-paste template. The structure follows `PRD.template.md`; conditional sections (`Why Now`, `Current Alternatives`, `Risks`) are omitted here with rationale at the bottom, because orders-api is a foundational internal service, not an external product.

## Problem

Repeat retail customers who have just paid for a cart have no durable, queryable record of the order on the device they checked out from, and no safe way to cancel within the brief window before fulfillment ships. Flaky mobile retries duplicate orders. Mistaken purchases require emailing support. Both failures land in the most trust-sensitive minutes of the purchase.

## Users

**Primary persona: Priya, repeat retail customer.** Buys from the store 1–3 times a month on a phone over spotty mobile data. Time-pressed, low tolerance for retrying a flow that may have already charged her.

## JTBD

> "After I pay, give me a durable record I can check, and a short window to undo a mistake — without talking to a human."

## Scope

- Authenticated customers can create an order tied to their identity with at-most-once semantics under client retry.
- Customers can fetch any single order they own by id.
- Customers can list their own orders, paginated, newest first.
- Customers can cancel an order they own while it is in a cancellable state.
- Order state transitions are enforced server-side; illegal transitions are rejected with a clear error.

## Non-goals

- **No payment processing.** Card capture, PCI scope, refunds, and chargebacks live in the upstream payments service. orders-api only records that payment succeeded.
- **No fulfillment or inventory logic.** Post-`paid` state is advanced by other services; orders-api does not decide *when* an order ships.
- **No admin, support, or cross-customer access.** No agent endpoints, no bulk operations, no "admin scope" JWTs in v1.
- **No catalog, pricing, or promotions.** Line items arrive pre-priced from the caller and are stored verbatim.
- **No Kafka in v1.** Event emission is stdout-only; durable eventing is deferred to v2.

## Constraints

- Stack fixed: Spring Boot, Postgres 16, Flyway migrations, JWT auth.
- Out-of-scope for PCI: card data never touches this service.
- Idempotency required on every state-changing endpoint.

## Assumptions

- An upstream auth service issues JWTs with a stable `sub` claim carrying `customerId`.
- An upstream payments service is the only caller permitted to advance state to `paid`.
- A fulfillment service is the only caller permitted to advance state to `shipped`.
- Single currency for v1; ISO-4217 added in v2.

## Distribution and Adoption

orders-api is an internal capability, not a product surface. Adoption is captive: the existing checkout client cuts over via feature flag, with the legacy email-confirmation path remaining as fallback for one release. Upstream consumers (payments, fulfillment) integrate via documented endpoints during the same cutover window.

## Success Metrics

| Metric | Unit | Target | Timeframe |
|---|---|---|---|
| p99 latency for `GET /orders/{id}` | ms | < 150 | rolling 7-day window post-launch |
| Duplicate-order rate under client retry with same idempotency key | duplicates per 10,000 create attempts | < 1 | rolling 30-day window |
| Successful customer-initiated cancel on eligible orders | % of cancel requests | > 99.5 | rolling 30-day window |
| Service availability | % successful responses | ≥ 99.9 | rolling 30-day window |

## Open Questions

- Cancellable window: any time before `shipped`, or a hard time budget (e.g., 10 minutes post-create) regardless of state?
- Idempotency-key TTL: server-side retention before a retry is treated as a new request. Working assumption 24h; user deferred final value.
- Data retention: how long do cancelled and shipped orders stay queryable before archival?

## Omitted sections

- **Why Now:** foundational internal service; no external urgency trigger.
- **Current Alternatives:** no incumbent — orders-api replaces an implicit gap, not a tool.
- **Risks:** no material product-level risks remain after scope narrowing; engineering risks (event ordering, idempotency correctness) belong in the tech spec, not the PRD.
