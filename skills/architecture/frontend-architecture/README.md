# frontend-architecture

> Status: draft

## Purpose

Defines frontend application architecture from an approved system design: application-shell structure, routing and rendering strategy, state and data-flow architecture, auth and session handling, design-system boundaries, accessibility posture, performance budgets, resilience behavior, and client observability.

Technology-agnostic and framework-agnostic first. Owns *how the application is structured and behaves*, not the visual design or the framework that renders it. Visual and component design lives in the [`frontend-design`](../../implementations/frontend/frontend-design/SKILL.md) skill; framework-specific scaffolding lives under [implementations/frontend](../../implementations/frontend/).

## Owns

- Application shell and micro-frontend posture
- Routing model and route-level rendering strategy
- State tiers (server-cache, URL, ephemeral UI, durable client)
- Data fetching and caching contracts
- Client auth and session handling
- Design-system seam and theming propagation
- Accessibility posture and testing expectations
- Performance budgets and breach actions
- Real-time/offline resilience and client observability

## Produces

| Artifact | Conforms to |
|---|---|
| `frontend-architecture.md` | [architecture-schema](../../../standards/architecture-schema/README.md), [documentation-standards](../../../standards/documentation-standards/README.md) |
| ADR drafts (framework, rendering, token storage, performance budget) | [architecture-schema](../../../standards/architecture-schema/README.md) |

## Skills

- [frontend-architecture](SKILL.md) - turns an approved system design into frontend application architecture: shell, routing, rendering, state, data flow, auth, design-system seam, accessibility, performance, resilience, observability, and implementation handoffs.

## Standards this architecture domain conforms to

- [architecture-schema](../../../standards/architecture-schema/README.md) - `frontend-architecture.md` artifact structure and system-design traceability.
- [security-standards](../../../standards/security-standards/README.md) - token storage, CSRF/XSS posture, PII rendering.
- [observability-standards](../../../standards/observability-standards/README.md) - client telemetry and RUM signals.
- [deployment-standards](../../../standards/deployment-standards/README.md) - performance-budget gates and rollout.
- [documentation-standards](../../../standards/documentation-standards/README.md) - skill structure.

## Upstream inputs

Requires an approved `system-design.md` per [architecture-schema](../../../standards/architecture-schema/README.md) whose design includes a user-facing web frontend. Bounded contexts, component interfaces, API/BFF boundaries, and ADRs shape the frontend architecture produced here.

## Downstream consumers

Frontend architecture produced here is the source of truth for:

- [implementations/frontend/*](../../implementations/frontend/) - Next.js, React, Angular, Vue, and Svelte skills follow routing, rendering, state, and data-layer decisions.
- [architecture/backend-architecture](../backend-architecture/README.md) - BFF/API and streaming contract expectations.
- [architecture/security](../security/SKILL.md) - token storage, CSRF/XSS, embedding, and PII-rendering boundaries.
- [architecture/performance](../performance/SKILL.md) - performance-budget enforcement and regression gates.
