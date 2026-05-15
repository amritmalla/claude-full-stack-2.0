---
product: <kebab-case slug>          # matches the system-design / PRD slug
status: draft                       # draft | review | approved | superseded
owner: <name or role>
system_design: <relative path to source system-design.md>
prd: <relative path to source PRD, or null>
version: 0.1.0                      # semver
last_reviewed: YYYY-MM-DD
---

# Frontend Architecture: [Product or Surface Name]

## Overview

[One paragraph: which frontend surfaces exist, their primary user tasks, the API/BFF boundary they consume, what this architecture optimizes for, and what it intentionally does not do.]

## Application Shell

| Concern | Decision |
|---|---|
| Number of apps | [count] |
| Deployment boundaries | [boundaries] |
| Shared shell vs separate deploys | [decision] |
| Micro-frontend posture | [none / justified posture] |
| Shared navigation / auth / telemetry | [ownership] |
| Error-boundary strategy | [strategy] |

## Routing Model

| Route / Group | Layout | Dynamic Segments | Owner | Access Constraint | Not-found / Error Behavior |
|---|---|---|---|---|---|
| [route] | [layout] | [segments] | [owner] | [constraint] | [behavior] |

## Rendering Strategy

| Route / Group | Rendering Mode | Hydration | Freshness | SEO Posture | Justification |
|---|---|---|---|---|---|
| [route] | [SSG / SSR / streamed / CSR / edge / islands] | [full / partial / none] | [static / revalidate / dynamic] | [needed / not] | [latency/SEO/interactivity reason] |

## Data Fetching & Caching

| Data Dependency | Fetch Location | Owner | Cache Layer | Invalidation Trigger | Retry / Stale Behavior |
|---|---|---|---|---|---|
| [data] | [server / edge / client] | [owner] | [HTTP / framework / client / CDN / edge] | [trigger] | [behavior] |

Mutation flow, optimistic updates, and background revalidation: [decisions].

## State Architecture

| Tier | Used? | Ownership | Mechanism | Synchronization | Persistence | Invalidation Lifecycle |
|---|---|---|---|---|---|---|
| Server-cache | [yes/no] | [owner] | [query lib / framework cache] | [rule] | [behavior] | [lifecycle] |
| URL / navigation | [yes/no] | [owner] | [route params] | [rule] | [behavior] | [lifecycle] |
| Ephemeral UI | [yes/no] | [owner] | [local component state] | [rule] | [behavior] | [lifecycle] |
| Durable client | [yes/no] | [owner] | [browser storage] | [rule] | [behavior] | [lifecycle] |

## Auth & Session Handling

| Concern | Decision |
|---|---|
| Token / session type | [cookie / token / session] |
| Storage location | [location] |
| Refresh flow | [flow] |
| Route guards / RBAC | [decision] |
| Unauthenticated rendering | [behavior] |
| CSRF posture | [posture] |
| XSS exposure & assumptions | [assumptions] |
| Session expiration / silent refresh | [behavior] |
| Logout propagation / multi-tab | [behavior] |

## Design System Boundary

| Owned by Design System | Owned by Application |
|---|---|
| [tokens, primitives, patterns, a11y baselines, typography] | [workflows, business compositions, domain components] |

Theming/token propagation: [mechanism]. Component-extension contract: [contract].

## Internationalization & Localization

*Conditional — include when multi-locale or RTL is in scope; otherwise list under Omitted sections.*

| Concern | Decision |
|---|---|
| Locale routing | [strategy] |
| Translation loading | [runtime / build-time] |
| RTL posture | [decision] |
| Date / number / currency / timezone | [handling] |

## Accessibility Posture

| Concern | Decision |
|---|---|
| WCAG target level | [A / AA / AAA] |
| Keyboard navigation model | [model] |
| Focus management on navigation | [behavior] |
| Screen-reader / live-region usage | [expectations] |
| Semantic structure & color contrast | [expectations] |
| Testing posture | [automated / manual / audit] |

## Performance Budgets

| Metric | Target | Breach Action |
|---|---|---|
| LCP | [target] | [action] |
| INP | [target] | [action] |
| CLS | [target] | [action] |
| JS bundle (per route) | [budget] | [action] |
| Image payload | [budget] | [action] |
| Third-party script impact | [policy] | [action] |

Code-splitting boundaries, image/font strategy, hydration constraints, regression monitoring, ownership: [decisions].

## Real-time, Offline & Resilience

*Conditional — include when realtime or offline features exist; otherwise list under Omitted sections.*

| Concern | Decision |
|---|---|
| Transport | [websocket / SSE / polling] |
| Polling fallback | [behavior] |
| Reconnect semantics | [behavior] |
| Offline-capable surfaces | [surfaces] |
| Optimistic updates & reconciliation | [rules] |
| Degraded-mode UX | [experience] |

## Client Observability

| Concern | Decision |
|---|---|
| Error reporting | [tool / approach] |
| RUM metrics | [signals] |
| Session-replay posture | [posture] |
| Tracing correlation | [approach] |
| Sampling policy | [policy] |
| PII redaction | [rules] |
| Environment-specific behavior | [behavior] |

## Implementation Handoffs

### implementations/frontend/<framework>

- [Routing, rendering, state, and data-layer handoff notes]

### backend-architecture

- [BFF / API / streaming contract expectations]

### security

- [Token storage, CSRF/XSS posture, embedding, PII rendering]

### performance / quality-engineering

- [Budget enforcement, regression gates, a11y and E2E testing expectations]

## ADR Index

| ADR | Title | Status | Summary |
|---|---|---|---|
| NNNN | [title] | [proposed/accepted/...] | [summary] — links to `adrs/NNNN-<slug>.md` |

## Omitted sections

- [Conditional section name]: [one-line rationale for omission].

## Deferred Decisions

- [Decision, owner, deadline].
