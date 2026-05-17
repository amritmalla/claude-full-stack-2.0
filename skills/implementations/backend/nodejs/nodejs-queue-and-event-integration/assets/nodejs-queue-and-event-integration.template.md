# Node.js Queue and Event Integration — Reference

Use this as the canonical envelope, producer, outbox, consumer, and Testcontainers reference when adding async work to a scaffolded Node.js service. Placeholder tokens use `<kebab-case>` or `<PascalCase>`. Broker, contracts, ordering, and delivery semantics come from `backend-architecture.md`. Versions are pinned examples — replace with the current stable release; never use `^`.

## Directory additions (over the scaffold)

```
src/messaging/
├── envelope.ts                           # versioned envelope + zod schemas per type
├── producer.ts                           # typed publish API; bounded send timeout
├── outbox.ts                             # outbox writer (same txn as domain change)
├── relay.ts                              # outbox → broker poller; at-least-once safe
├── consumer.ts                           # idempotent; retry+backoff; DLQ; shutdown-aware
└── dedupe-store.ts                       # explicit dedupe-key store
test/messaging/
└── integration.test.ts                  # Testcontainers: round trip / dup / DLQ / shutdown
```

## Config schema additions (extend the scaffold zod schema)

```ts
BROKER_URL: z.string().min(1),
QUEUE_NAME: z.string().min(1),          // or TOPIC / QUEUE_URL per broker
CONSUMER_CONCURRENCY: z.coerce.number().int().positive().default(4),
RETRY_MAX_ATTEMPTS: z.coerce.number().int().positive().default(5),
RETRY_BACKOFF_MS: z.coerce.number().int().positive().default(1000),
DLQ_NAME: z.string().min(1),
PRODUCER_SEND_TIMEOUT_MS: z.coerce.number().int().positive().default(5000),
```

`.env.example` gets the same keys with placeholder values; credentials live in the secret store.

## Versioned envelope (src/messaging/envelope.ts)

```ts
import { z } from 'zod';

export const envelope = <T extends z.ZodTypeAny>(payload: T) => z.object({
  id: z.string().uuid(),               // dedupe key
  type: z.string().min(1),
  occurredAt: z.string().datetime(),
  schemaVersion: z.number().int().positive(),
  payload,
});

export const OrderPlaced = envelope(z.object({ orderId: z.string(), total: z.number() }));
// Registry: reject unknown `type` on consume.
```

## Transactional outbox (the dual-write fix)

```ts
// Inside the SAME db transaction as the domain change:
await tx.order.create({ data: order });
await tx.outbox.create({ data: {
  id: messageId, type: 'OrderPlaced', payload, status: 'pending',
} });
// commit — domain state and the intent to publish are now atomic.
```

```ts
// src/messaging/relay.ts — separate process/timer
const rows = await db.outbox.findMany({ where: { status: 'pending' }, take: 100 });
for (const row of rows) {
  await producer.publish(row.type, row.payload, { messageId: row.id }); // at-least-once
  await db.outbox.update({ where: { id: row.id }, data: { status: 'sent' } });
}
```

Never publish inline before the transaction commits.

## Idempotent consumer with bounded retry → DLQ

```ts
// src/messaging/consumer.ts (BullMQ-style; adapt for KafkaJS / SQS)
async function handle(msg: Envelope): Promise<void> {
  if (await dedupeStore.seen(msg.id)) return;          // idempotency: explicit
  await doSideEffect(msg.payload);
  await dedupeStore.mark(msg.id);
}

worker.on('failed', async (job, err) => {
  if (job.attemptsMade >= config.RETRY_MAX_ATTEMPTS) {
    await dlq.add(job.name, { ...job.data, failure: String(err) }); // bounded → DLQ
  }
});
// backoff: { type: 'exponential', delay: config.RETRY_BACKOFF_MS } with jitter.
```

## Shutdown-aware (register a close hook with the scaffold shutdown)

```ts
// in src/container/index.ts wiring — uses the scaffold graceful-shutdown registry
shutdown.register(async () => {
  await worker.pause(true);     // stop fetching
  await worker.close();         // drain in-flight within the scaffold timeout
});
```

The scaffold's `SIGTERM` handler invokes this; incomplete work is not acked and redelivers.

## Testcontainers integration test (real broker)

```ts
// test/messaging/integration.test.ts
const container = await new GenericContainer('<broker-image>:<tag>')
  .withExposedPorts(<port>).start();
// 1. publish → consume → assert exactly one effect
// 2. publish same id twice → assert one effect (idempotency)
// 3. poison payload → assert RETRY_MAX_ATTEMPTS attempts then DLQ has it
// 4. SIGTERM mid-consume → assert in-flight drained, no double-ack, leftover redelivered
```

## package.json additions (pinned examples — pick per broker)

```
bullmq 5.12.0            # Redis-backed queues
kafkajs 2.2.4            # Kafka
@aws-sdk/client-sqs 3.637.0   # SQS
testcontainers 10.13.1   # devDependency — real-broker integration tests
```

## Service README additions

Document: the broker and why (cite `backend-architecture.md`), each message type + schema version, the retry/backoff/DLQ policy, the outbox table and relay cadence, and how to inspect/redrive the DLQ.
