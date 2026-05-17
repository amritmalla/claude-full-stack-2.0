# hexagonal-architecture

## Summary

Hexagonal architecture (ports and adapters) isolates domain logic from external concerns. The domain defines *ports* (interfaces); *adapters* implement them for specific technologies. Dependencies point inward, toward the domain.

## Problem & forces

Business logic entangled with frameworks, databases, and transport is hard to test and expensive to change when infrastructure changes. The forces — testability in isolation, swappable infrastructure, and a framework-independent domain — justify the indirection of ports and adapters.

## When to use / When not to use

**Use when**

- Domain logic is non-trivial and must be unit-tested without infrastructure.
- Infrastructure choices (DB, broker, transport) may change or need to be mocked.
- You want a clear inside/outside boundary within a service or module.

**Avoid when**

- The service is a thin CRUD or pass-through with negligible domain logic.
- The team will treat ports as ceremony and route everything through anemic interfaces.

## Structure

The domain sits at the center. Driving adapters (HTTP, CLI) call inbound ports; the domain calls outbound ports implemented by driven adapters (DB, broker).

```text
HTTP/CLI ─▶ inbound port ─▶ [ domain ] ─▶ outbound port ─▶ DB/broker
            (driving adapter)              (driven adapter)
```

## Key tradeoffs

Gain: domain testable in isolation, infrastructure swappable, framework lock-in contained. Pay: more interfaces and indirection, mapping between domain and adapter models, over-abstraction risk on simple code.

## Failure modes & mitigations

- **Anemic ports** — interfaces that just mirror the DB, leaking persistence into the domain. Define ports from domain needs, not storage.
- **Adapter logic leak** — business rules creep into adapters. Keep adapters mechanical; rules stay in the domain.
- **Abstraction overkill** — ports around trivial code. Apply only where domain logic or swappability is real.

## Related skills & patterns

- Skills: [`backend-architecture`](../../architecture/backend-architecture/SKILL.md), [`quality-engineering`](../../architecture/quality-engineering/SKILL.md)
- Patterns: [`domain-driven-design`](../domain-driven-design/README.md) (defines what the domain is), [`modular-monolith`](../modular-monolith/README.md), [`microservices`](../microservices/README.md)
