# FastAPI Async and Task Integration Quality Rubric

Load this before declaring the async/task integration complete. Revise until each check passes or the unresolved gap is explicitly documented in the service README.

## Architecture conformance

- [ ] Broker, message/event contracts, ordering, and delivery semantics trace to `backend-architecture.md`.
- [ ] No broker or semantic choice was invented; any missing decision is an open ADR candidate.
- [ ] Redelivery/DLQ expectations and the consumer SLO trace to `architecture/reliability` (or documented deferral).

## Scaffold integration

- [ ] Producer, consumer, and relay are registered in the scaffold DI providers.
- [ ] Broker connection settings resolve through the scaffold validated settings seam.
- [ ] Produce/consume logging goes through the scaffold structlog logger (no second logger).
- [ ] Worker stop/drain is wired into the scaffold ASGI-lifespan / worker shutdown.

## Delivery correctness

- [ ] Events tied to a DB write use a transactional outbox; no inline publish-before-commit exists.
- [ ] The outbox relay is idempotent and at-least-once safe.
- [ ] Every consumer/task is idempotent via an explicit dedupe-key store (message id or business key).
- [ ] A duplicate delivery is test-verified to produce exactly one effect.

## Failure handling

- [ ] Retry uses bounded backoff (exponential + jitter) with a hard max-attempt count.
- [ ] Exceeding max attempts routes the message to a DLQ with failure context (test-verified).
- [ ] No message path retries unbounded or drops silently.

## Shutdown behavior

- [ ] On `SIGTERM` the worker stops fetching new messages.
- [ ] In-flight tasks drain within the bounded timeout.
- [ ] Incomplete work is not acked; it redelivers (test-verified).

## Envelope and schema

- [ ] Messages use a versioned Pydantic envelope (`id`, `type`, `occurred_at`, `schema_version`, `payload`).
- [ ] Each message type has a Pydantic model validated on both produce and consume.
- [ ] Unknown message types are rejected.

## Producer resilience

- [ ] Producer send is bounded by a timeout.
- [ ] No synchronous blocking broker call is made on the async request path.
- [ ] A broker outage degrades to the outbox (transactional) or a handled error (fire-and-forget) — never an unbounded hang.

## Observability seam

- [ ] Produce, consume, retry, DLQ, and consumer lag are logged with correlation.
- [ ] Metric hooks are exposed for `fastapi-observability-readiness`; no OTel/prometheus vendor wired here.

## Tests (Testcontainers, real broker)

- [ ] Successful round trip is asserted.
- [ ] Duplicate delivery handled idempotently is asserted.
- [ ] Poison message → retry → DLQ is asserted.
- [ ] `SIGTERM` mid-consume drains cleanly with no lost or double-acked work.

## Build verification

- [ ] `mypy` reports zero errors.
- [ ] `ruff check` passes.
- [ ] The integration test command passes (or the skip is documented with reason).
- [ ] The boot smoke check still passes with the integration wired.

## Standards conformance

- [ ] [api-standards](../../../../../../standards/api-standards/README.md): payloads match the declared contract; versioned, schema-validated envelope on produce and consume.
- [ ] [observability-standards](../../../../../../standards/observability-standards/README.md): produce/consume correlated through the scaffold logger; retry/DLQ/lag observable.

## Failure handling

If a check fails:

1. Identify the missing or incorrect delivery, idempotency, or shutdown behavior.
2. Ask the user for clarification if the decision cannot be inferred from `backend-architecture.md` or `architecture/reliability`.
3. Revise, then re-run `mypy`, `ruff check`, the integration tests, and the boot smoke check.
4. Keep any unresolved gap explicit in the service README — never assume idempotency or delivery semantics silently.
