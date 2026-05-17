# FastAPI Async and Task Integration — Reference

Use this as the canonical envelope, producer, outbox, consumer, and Testcontainers reference when adding background work to a scaffolded FastAPI service. Placeholder tokens use `<kebab-case>` or `<PascalCase>`. Broker, contracts, ordering, and delivery semantics come from `backend-architecture.md`. Versions are pinned examples — never use unbounded specifiers.

## Directory additions (over the scaffold)

```
app/messaging/
├── envelope.py                           # versioned Pydantic envelope + per-type models
├── producer.py                           # typed publish API; bounded send timeout
├── outbox.py                             # outbox writer (same txn as domain change)
├── relay.py                              # outbox → broker poller; at-least-once safe
├── consumer.py                           # idempotent task/consumer; retry+backoff; DLQ
└── dedupe_store.py                       # explicit dedupe-key store
tests/messaging/
└── test_integration.py                  # Testcontainers: round trip / dup / DLQ / shutdown
```

## Settings additions (extend the scaffold Settings model)

```python
broker_url: str                         # or kafka_bootstrap_servers
queue_name: str                         # or topic
worker_concurrency: int = 4
retry_max_attempts: int = 5
retry_backoff_s: float = 1.0
dlq_name: str
producer_send_timeout_s: float = 5.0
```

`.env.example` gets the same keys with placeholder values; credentials live in the secret store.

## Versioned envelope (app/messaging/envelope.py)

```python
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class Envelope(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str                               # dedupe key (uuid)
    type: str
    occurred_at: datetime
    schema_version: int
    payload: dict

class OrderPlaced(BaseModel):
    order_id: str
    total: float
# Registry maps `type` → payload model; reject unknown `type` on consume.
```

## Transactional outbox (the dual-write fix)

```python
# Inside the SAME SQLAlchemy transaction as the domain change:
async with session.begin():
    session.add(Order(...))
    session.add(Outbox(id=message_id, type="OrderPlaced",
                        payload=payload, status="pending"))
# commit — domain state and the intent to publish are now atomic.
```

```python
# app/messaging/relay.py — separate process/timer
rows = await repo.fetch_pending_outbox(limit=100)
for row in rows:
    await producer.publish(row.type, row.payload, message_id=row.id)  # at-least-once
    await repo.mark_sent(row.id)
```

Never publish inline before the transaction commits.

## Idempotent consumer/task with bounded retry → DLQ

```python
# app/messaging/consumer.py (arq-style; adapt for Celery / Kafka)
async def handle(ctx, msg: dict) -> None:
    env = Envelope.model_validate(msg)
    if await dedupe_store.seen(env.id):       # idempotency: explicit
        return
    await do_side_effect(env.payload)
    await dedupe_store.mark(env.id)

# on failure: retry with exponential backoff + jitter up to retry_max_attempts,
# then publish to dlq_name with the failure context. Never unbounded.
```

## Shutdown-aware (register a close hook with the scaffold lifespan)

```python
# in app/container.py wiring — uses the scaffold ASGI-lifespan shutdown registry
async def _shutdown_worker() -> None:
    await worker.stop_fetching()
    await worker.drain(timeout=settings.shutdown_timeout_s)  # no ack of incomplete work
lifespan_shutdown.register(_shutdown_worker)
```

The scaffold's `SIGTERM` path invokes this; incomplete work is not acked and redelivers.

## Testcontainers integration test (real broker)

```python
# tests/messaging/test_integration.py
from testcontainers.redis import RedisContainer   # or KafkaContainer
# 1. publish → consume → assert exactly one effect
# 2. publish same id twice → assert one effect (idempotency)
# 3. poison payload → assert retry_max_attempts attempts then DLQ has it
# 4. SIGTERM mid-consume → assert in-flight drained, no double-ack, leftover redelivered
```

## pyproject additions (pinned examples — pick per broker)

```
celery==5.4.0            # or rq==2.0.0 / arq==0.26.1
aiokafka==0.11.0         # Kafka
testcontainers==4.8.1    # dev: real-broker integration tests
```

## Service README additions

Document: the broker and why (cite `backend-architecture.md`), each message type + schema version, the retry/backoff/DLQ policy, the outbox table and relay cadence, and how to inspect/redrive the DLQ.
