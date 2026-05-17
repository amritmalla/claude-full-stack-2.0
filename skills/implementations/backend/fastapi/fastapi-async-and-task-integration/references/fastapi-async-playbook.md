# FastAPI Async and Task Integration Playbook

Load this when implementing any owned area of `fastapi-async-and-task-integration` or checking the anti-pattern list. It expands the operating rules and process steps in `SKILL.md` with the detail needed to ship a correct async integration, not a demo.

## Why this workflow exists

Async integration done wrong fails in production in ways tests never show: a dual write (DB commit succeeds, event publish fails) leaves the system permanently inconsistent; a non-idempotent task double-charges a card on a normal redelivery; an unbounded retry turns one poison message into an infinite hot loop that drains the broker; and a worker that ignores `SIGTERM` acks work it never finished, silently losing it on every deploy. None of these surface under a single happy-path test — only against a real broker with duplicates, failures, and shutdown.

The goal is exactly-effectively-once behavior built from at-least-once delivery plus idempotency plus an outbox — with bounded failure handling and a real-broker test that proves it.

## Behavioral rules in depth

### 1. Consume the integration architecture; do not invent it

Broker, message/event contracts, ordering, partitioning, and at-least-once-vs-effectively-once are `backend-architecture.md` decisions. Picking Celery because it is familiar, or assuming ordering the contract never promised, is inventing architecture. Missing decision → ADR candidate.

### 2. Extend the scaffold; never duplicate its primitives

The producer, consumer, and relay register in the scaffold DI providers, read connection settings from the validated settings seam, log through the scaffold structlog logger, and stop via the scaffold ASGI-lifespan shutdown. A second settings reader or a hand-rolled shutdown forks the baseline and the two drift.

### 3. At-least-once is the default; idempotency is mandatory

Unless the broker and contract guarantee effectively-once, assume every message can arrive more than once (redelivery after a worker crash, visibility-timeout expiry, rebalance). Every consumer/task therefore has an explicit dedupe key — the message id or a business key — checked against a store before the side effect. "The task is probably safe to re-run" is not idempotency.

### 4. The transactional outbox kills the dual-write hazard

A handler that writes the database and then publishes an event has two failure windows: publish fails after commit (event lost) or commit fails after publish (phantom event). The fix: write the domain change and an outbox row in the same SQLAlchemy transaction; a separate relay reads the outbox and publishes. The publish now derives from committed state, and the relay is itself at-least-once (so the consumer's idempotency still matters).

| Approach | Failure mode |
|---|---|
| Publish inside request, before commit | Phantom event if commit fails |
| Publish after commit, no outbox | Lost event if publish fails |
| Outbox in the same transaction + relay | Safe — publish derives from committed state |

### 5. Failure handling is bounded and explicit

A retry policy has a backoff (exponential + jitter) and a hard max-attempt count. On exhaustion the message goes to a dead-letter destination with its failure context — never retried forever, never silently dropped. The DLQ is monitored; a message there is a known, inspectable failure, not a black hole.

### 6. Workers respect shutdown

On `SIGTERM` (wired through the scaffold ASGI-lifespan / worker shutdown): stop fetching new messages, finish in-flight tasks within the timeout, ack only completed work, and let unfinished work redeliver. A worker that keeps fetching during drain, or acks a batch it did not finish, loses messages on every rolling deploy.

### 7. Producers are bounded; outages degrade, not hang

A producer send has a timeout and never makes a synchronous blocking broker call on the async request path. For transactional events the degradation path is the outbox (the row is committed; the relay will retry). For fire-and-forget work a broker outage is a handled, logged error with a bounded wait — never an unbounded hang holding a request open or blocking the event loop.

### 8. No real-broker test, no done

Testcontainers spins up the actual broker. The suite must prove: (a) successful round trip; (b) a duplicate delivery causes exactly one effect; (c) a poison message retries with backoff and lands in the DLQ after max attempts; (d) `SIGTERM` mid-consume drains cleanly with no lost or double-acked work. Mock-only tests cannot show redelivery or rebalance behavior.

## Step detail

**Step 1 — Context.** Load `backend-architecture.md` (broker, contracts, ordering, semantics) and `architecture/reliability` (redelivery/DLQ, consumer SLO). Confirm scaffold + transactional store. Missing decision → ADR candidate.

**Step 2 — Settings.** Add broker URL/credentials ref, queue/topic names, worker concurrency, `retry_max_attempts`, `retry_backoff_s`, DLQ target to the scaffold `Settings` and `.env.example` (placeholders).

**Step 3 — Envelope + schemas.** Versioned Pydantic envelope `{ id, type, occurred_at, schema_version, payload }`; a model per `type`; validate on produce and consume; reject unknown `type`.

**Step 4 — Producer.** Typed publish API in the DI providers, bounded send timeout. DB-tied events → write the outbox row in the domain transaction, not an inline publish.

**Step 5 — Outbox relay.** Poller/CDC reading unsent rows → publish → mark sent. The relay is idempotent and at-least-once safe (a crash mid-publish must not lose or double-mark beyond what consumer idempotency tolerates).

**Step 6 — Consumer/task.** DI-registered, dedupe-key store check before side effect, bounded retry+backoff, max-attempt → DLQ. Wire stop/drain into the scaffold lifespan/worker shutdown.

**Step 7 — Observability seam.** Log produce/consume/retry/DLQ/lag with correlation through the scaffold logger; expose metric hooks for `fastapi-observability-readiness` — do not wire OTel/prometheus here.

**Step 8 — Testcontainers tests.** Real broker; assert round trip, duplicate→one effect, poison→retry→DLQ, SIGTERM→clean drain.

**Step 9 — Verify.** `mypy`, `ruff check`, integration tests, boot smoke. Standards check (api-standards, observability-standards). Document gaps.

## Anti-patterns to detect

Call these out explicitly when found:

- Broker/contract/semantics chosen here instead of read from `backend-architecture.md`
- DB write then inline publish (dual-write hazard) instead of a transactional outbox
- Consumer/task assumed idempotent with no explicit dedupe key/store
- Unbounded retry, or retry with no DLQ (poison loops forever)
- Messages silently dropped on failure instead of dead-lettered
- Worker ignoring `SIGTERM` / acking work it did not finish
- Producer send with no timeout, or a synchronous blocking broker call on the async path
- Second settings reader, logger, or shutdown path instead of the scaffold's
- Messages not envelope/schema-validated, or unknown types accepted
- OTel/prometheus wired here instead of leaving a seam for `fastapi-observability-readiness`
- Tests mock the broker only — no Testcontainers proof of redelivery/DLQ/shutdown
