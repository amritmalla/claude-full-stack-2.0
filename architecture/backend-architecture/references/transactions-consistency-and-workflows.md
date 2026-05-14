# Transactions, Consistency, and Workflows

Backend architecture must make state-change behavior explicit before implementation begins.

## Transaction Boundaries

For every state-changing workflow, define:

- what must succeed or fail atomically,
- which aggregate or data owner protects the invariant,
- what happens before and after commit,
- which side effects are synchronous,
- which side effects are asynchronous.

Prefer one transaction boundary per aggregate or owned consistency boundary. If a workflow crosses boundaries, name the coordination model instead of pretending the whole flow is atomic.

## Consistency Models

Use clear language:

- Strong consistency: readers must observe the committed result immediately.
- Eventual consistency: downstream state can lag and reconciliation is expected.
- Saga/process manager: multiple local transactions coordinated by events or commands.
- Read model: derived view with explicit freshness expectations.

Document where stale reads are acceptable and where they are not.

## Idempotency and Retries

For unsafe operations, define:

- idempotency key source,
- key scope,
- retention window,
- duplicate request behavior,
- retryable vs non-retryable failures,
- response behavior for completed, in-flight, and failed duplicates.

For async workflows, define:

- message identity,
- deduplication store or strategy,
- ordering assumptions,
- poison-message handling,
- retry backoff,
- dead-letter handling,
- compensation or manual recovery path.

## Failure Modes

Name likely failures and decide behavior:

- dependency timeout,
- partial side effect,
- duplicate command,
- out-of-order event,
- stale read model,
- authorization drift,
- schema or contract mismatch,
- queue backlog.

Every important failure mode should map to an observable signal or runbook hook.
