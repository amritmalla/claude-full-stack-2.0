# real-time-systems

## Summary

Real-time systems push state to clients with low, bounded latency — live dashboards, collaboration, messaging, presence — rather than relying on client polling. Connection and subscription management become core architecture.

## Problem & forces

Request/response with polling is wasteful and laggy for data that changes continuously. The forces — sub-second freshness, server-initiated push, many concurrent long-lived connections, and fan-out — justify a streaming transport and stateful edge.

## When to use / When not to use

**Use when**

- Users need sub-second updates (live data, presence, collaboration, notifications).
- The server must initiate delivery; clients cannot efficiently poll.
- Fan-out of one change to many subscribers is common.

**Avoid when**

- Periodic refresh (seconds–minutes) is acceptable — polling or caching is simpler.
- Update volume and concurrency are low enough that push infrastructure is unjustified overhead.

## Structure

Clients hold long-lived connections (WebSocket/SSE) to a gateway tier that manages subscriptions; backend changes flow via a stream/broker and fan out.

```text
source → stream/broker → fan-out tier → [WS/SSE gateway] ⇄ clients
                                          (subscriptions, presence, backpressure)
```

## Key tradeoffs

Gain: low-latency push, efficient fan-out, live UX. Pay: stateful connection management, scaling and backpressure complexity, reconnection/missed-update handling, harder testing and observability.

## Failure modes & mitigations

- **Missed updates on reconnect** — clients drop and lose events. Provide resumable streams (cursors/sequence numbers) and snapshot-on-connect.
- **Fan-out overload** — hot topics saturate the tier. Shard subscriptions; apply backpressure and conflation.
- **Connection storms** — mass reconnect after a blip. Use jittered backoff and connection draining.

## Related skills & patterns

- Skills: [`backend-architecture`](../../architecture/backend-architecture/SKILL.md), [`performance`](../../architecture/performance/SKILL.md), [`reliability`](../../architecture/reliability/SKILL.md)
- Patterns: [`event-driven`](../event-driven/README.md) (the transport for changes), [`cqrs`](../cqrs/README.md) (subscription-fed read models), [`microservices`](../microservices/README.md)
