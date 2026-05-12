# Architecture Tradeoffs

Use this reference when choosing architecture style or critiquing complexity.

## Default stance

Default to a modular monolith unless the PRD strongly justifies distribution.

Prefer:

- fewer deployable units,
- synchronous request flows for simple user-facing workflows,
- boring storage,
- explicit module boundaries,
- and operational simplicity.

Distributed systems are a cost, not a feature.

## Architecture styles

Evaluate these options:

- Monolith: best for very small products, prototypes, or single-team systems with simple boundaries.
- Modular monolith: best default for most v1 products with multiple domains but one team and shared deployment.
- Microservices: justify only when independent scaling, independent release ownership, fault isolation, or organizational boundaries outweigh operational cost.
- Serverless: useful for spiky workloads, event handlers, low-ops cron-like jobs, or managed integration glue; risky for complex domain cores and local debugging.
- Event-driven hybrid: useful when workflows are asynchronous, long-running, integration-heavy, or require decoupled processing; risky when used to avoid clear ownership.
- Batch-oriented: useful for scheduled imports, reconciliation, reporting, or data processing where latency is not user-critical.

## Complexity triggers

Only introduce distributed complexity when at least one is true:

- The PRD requires independent scale profiles across components.
- Reliability needs require fault isolation beyond module boundaries.
- Different teams own different business capabilities.
- Workflows are naturally asynchronous or long-running.
- External integrations require retries, buffering, or replay.
- Compliance or tenancy constraints require hard isolation.

## Simpler alternatives to consider

Before choosing a complex pattern, consider:

- module boundaries inside one deployable,
- background jobs instead of an event mesh,
- a single relational database with clear ownership rules,
- read replicas or materialized views instead of service extraction,
- scheduled reconciliation instead of distributed transactions,
- managed provider features instead of custom infrastructure.

## Anti-patterns

Flag and simplify:

- microservices for a single small team,
- queues used as domain boundaries,
- CQRS without divergent read/write needs,
- event sourcing without audit, replay, or temporal requirements,
- service meshes before there are many services,
- multi-region architecture without explicit availability or latency requirements,
- "future-proofing" that is not tied to a PRD constraint.

## Decision format

For the chosen style, document:

- chosen architecture style,
- PRD constraints that justify it,
- simpler alternatives considered,
- why alternatives were chosen or rejected,
- operational tradeoffs accepted,
- and future limitations.
