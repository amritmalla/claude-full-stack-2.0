# event-driven

## Summary

Event-driven architecture propagates state changes as immutable events published to a broker; consumers react asynchronously. Producers do not know their consumers, which decouples capabilities in time and deployment.

## Problem & forces

Synchronous call graphs couple services' availability and latency: a slow or down dependency fails the caller. The forces — temporal decoupling, fan-out to many consumers, buffering load spikes, and audit/replay — favor moving state propagation off the request path.

## When to use / When not to use

**Use when**

- A state change must notify many independent consumers without the producer knowing them.
- Workloads are spiky and need buffering, or you need replay/audit of changes.
- Services must stay available when downstream consumers are slow or down.

**Avoid when**

- The caller needs an immediate, consistent answer (use a synchronous query).
- Strong end-to-end transactional consistency is required.
- The system is small enough that an in-process call is simpler and sufficient.

## Structure

Producers emit events to a durable broker; consumers subscribe independently. The outbox pattern bridges a local transaction to publication.

```text
service → [local txn + outbox] → relay → broker ─┬→ consumer 1
                                                  ├→ consumer 2
                                                  └→ consumer 3 (replayable)
```

## Key tradeoffs

Gain: producer/consumer decoupling, load buffering, fan-out, replayability. Pay: eventual consistency, harder end-to-end debugging, ordering/idempotency complexity, broker as critical infrastructure.

## Failure modes & mitigations

- **Lost or double-delivered events** — at-least-once delivery is normal. Mitigate with idempotent consumers and an outbox on the producer.
- **Ordering assumptions** — events arrive out of order. Partition by key or carry version numbers.
- **Poison messages** — one bad event stalls a partition. Use dead-letter queues and retry budgets.
- **Schema drift** — producers change payloads. Version event schemas and evolve compatibly.

## Related skills & patterns

- Skills: [`backend-architecture`](../../architecture/backend-architecture/SKILL.md), [`data-architecture`](../../architecture/data-architecture/SKILL.md), [`reliability`](../../architecture/reliability/SKILL.md)
- Patterns: [`cqrs`](../cqrs/README.md) (events feed read models), [`microservices`](../microservices/README.md), [`real-time-systems`](../real-time-systems/README.md), [`ai-rag-platform`](../ai-rag-platform/README.md) (event-driven indexing)
