# microservices

## Summary

Microservices decompose a system into independently deployable services, each owning a bounded slice of domain and its data, communicating over the network. The unit of independence is the deployment, not the module.

## Problem & forces

A single deployable becomes a scaling and organizational bottleneck: teams contend on one release train, one runtime, one datastore. The forces that justify splitting are independent deploy cadence, divergent scaling profiles, team autonomy at scale, and fault isolation — strong enough to outweigh the distributed-systems tax they introduce.

## When to use / When not to use

**Use when**

- Multiple teams need to deploy on independent cadences without coordinating releases.
- Subdomains have sharply different scaling, latency, or availability profiles.
- Fault isolation between capabilities is a hard requirement.

**Avoid when**

- One small team owns the whole system — coordination cost exceeds the benefit.
- Domain boundaries are still unstable; premature splits ossify the wrong seams.
- The driver is "monolith is messy" — that is a modularity problem ([`modular-monolith`](../modular-monolith/README.md) solves it cheaper).

## Structure

Each service owns its data; no shared database. Synchronous calls for queries, asynchronous events for state propagation. A gateway fronts external traffic.

```text
client → API gateway → [service A | service B | service C]
                         │ owns DB_A   │ owns DB_B   │ owns DB_C
                         └── events ──→ broker ──→ subscribers
```

## Key tradeoffs

Gain: independent deploy/scale, fault isolation, team autonomy. Pay: network failure modes, eventual consistency, distributed tracing/observability burden, operational footprint (per-service CI/CD, infra, on-call), and harder cross-service transactions.

## Failure modes & mitigations

- **Distributed monolith** — services that must deploy together. Mitigate by aligning boundaries to bounded contexts ([`domain-driven-design`](../domain-driven-design/README.md)).
- **Synchronous call chains** — latency and cascading failure. Mitigate with async events ([`event-driven`](../event-driven/README.md)), timeouts, and circuit breakers.
- **Shared database coupling** — defeats independence. Enforce one owner per datastore.
- **Observability gaps** — a request spans many hops. Require correlation IDs and distributed tracing from day one.

## Related skills & patterns

- Skills: [`system-design`](../../architecture/system-design/SKILL.md), [`backend-architecture`](../../architecture/backend-architecture/SKILL.md), [`reliability`](../../architecture/reliability/SKILL.md)
- Patterns: [`modular-monolith`](../modular-monolith/README.md) (the cheaper default to start from), [`event-driven`](../event-driven/README.md), [`domain-driven-design`](../domain-driven-design/README.md)
