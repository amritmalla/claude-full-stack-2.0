# multi-tenant-saas

## Summary

Multi-tenant SaaS serves many customer organizations (tenants) from shared infrastructure while isolating each tenant's data and configuration. Tenant identity is a first-class concern threaded through every layer.

## Problem & forces

Running a separate stack per customer does not scale operationally or economically; sharing everything risks data leakage and noisy-neighbor effects. The forces — cost efficiency, per-tenant isolation, customization, and per-tenant scaling — drive the isolation-model decision.

## When to use / When not to use

**Use when**

- A product serves many organizations with similar functionality.
- Operational and cost efficiency require shared infrastructure.
- Tenants need data isolation and some configuration/customization.

**Avoid when**

- A single tenant or a handful of bespoke deployments — single-tenant is simpler.
- Regulatory or contractual terms mandate physically separate infrastructure per tenant (use isolated stacks).

## Structure

Tenant context resolved at the edge and propagated everywhere. Isolation model spans a spectrum: shared schema with a tenant key → schema-per-tenant → database/stack-per-tenant.

```text
request → resolve tenant → tenant-scoped auth → app
                                                 └─ data: shared+key | schema/tenant | db/tenant
```

## Key tradeoffs

Gain: shared infrastructure cost efficiency, one deploy serves all, centralized ops. Pay: cross-tenant leakage risk, noisy-neighbor contention, per-tenant scaling/migration complexity, isolation model is hard to change later.

## Failure modes & mitigations

- **Cross-tenant data leakage** — a missing tenant filter exposes data. Enforce tenant scoping at the data layer (row-level security / mandatory predicates), not just app code.
- **Noisy neighbor** — one tenant degrades others. Apply per-tenant quotas, rate limits, and isolation tiers.
- **Unbounded per-tenant migrations** — schema-per-tenant migrations balloon. Automate and batch; track per-tenant migration state.

## Related skills & patterns

- Skills: [`system-design`](../../skills/architecture/system-design/SKILL.md), [`security`](../../skills/architecture/security/SKILL.md), [`data-architecture`](../../skills/architecture/data-architecture/SKILL.md)
- Patterns: [`microservices`](../microservices/README.md), [`modular-monolith`](../modular-monolith/README.md), [`serverless-platform`](../serverless-platform/README.md)
