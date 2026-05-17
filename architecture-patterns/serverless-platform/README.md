# serverless-platform

## Summary

A serverless platform runs code as managed, event-triggered functions (or managed containers) with no server provisioning, automatic scaling to demand, and pay-per-use billing. Operational responsibility shifts to the provider.

## Problem & forces

Maintaining always-on capacity for spiky or low-volume workloads wastes money and operational effort. The forces — elastic scale-to-zero, no infrastructure ops, fast iteration, and usage-based cost — justify ceding control to a managed runtime.

## When to use / When not to use

**Use when**

- Workloads are spiky, event-driven, or low/variable volume (scale-to-zero pays off).
- Minimizing infrastructure operations and time-to-first-deploy matters.
- Glue, integrations, and async jobs dominate over steady high-throughput compute.

**Avoid when**

- Sustained high-throughput or latency-critical paths (cold starts, per-invocation cost hurt).
- Long-running or stateful processing that fights function time/memory limits.
- Heavy vendor lock-in is unacceptable for the workload.

## Structure

Events (HTTP, queue, schedule, storage) trigger stateless functions; state lives in managed services.

```text
event source → [function] → managed state (DB / queue / object store)
   (HTTP/queue/cron)  (stateless, autoscaled, scale-to-zero)
```

## Key tradeoffs

Gain: no server ops, automatic elastic scaling, pay-per-use, fast iteration. Pay: cold-start latency, execution/time/memory limits, local-testing and debugging friction, provider lock-in, cost unpredictability at high volume.

## Failure modes & mitigations

- **Cold starts on latency paths** — first invocation is slow. Use provisioned concurrency or keep latency-critical paths off serverless.
- **Runaway cost/concurrency** — traffic spikes bill unboundedly. Set concurrency caps, budgets, and alerts.
- **Distributed debugging gaps** — many tiny functions. Mandate structured logs and distributed tracing.
- **Statefulness smuggled in** — functions assume warm state. Keep functions stateless; externalize all state.

## Related skills & patterns

- Skills: [`infrastructure-platform`](../../skills/architecture/infrastructure-platform/SKILL.md), [`backend-architecture`](../../skills/architecture/backend-architecture/SKILL.md), [`performance`](../../skills/architecture/performance/SKILL.md)
- Patterns: [`event-driven`](../event-driven/README.md) (natural trigger model), [`microservices`](../microservices/README.md), [`multi-tenant-saas`](../multi-tenant-saas/README.md)
