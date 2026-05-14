---
name: frontend-architecture
description: Use when an approved system design exists and the team needs frontend application architecture before UI implementation. Produces application shell and routing model, rendering strategy (SSR, SSG, CSR, streaming, islands), state management posture, data fetching and caching strategy, auth and session handling on the client, design-system seams, accessibility posture, performance and bundle budgets, and implementation handoff notes. Do not use for visual design, component-level styling, framework-specific scaffolding, marketing-page authoring, or backend API design; use frontend-design, implementations/frontend/<framework>, or backend-architecture instead.
---

# Frontend Architecture

## When to use

Invoke after `system-design` has approved a design that includes a user-facing web frontend, and before `implementations/frontend/<framework>` skills generate components, routes, or build configuration.

Do not use when only visual or component design is needed (use `frontend-design`), when scaffolding a known framework with a known architecture (go directly to the implementation skill), when the surface is a single static marketing page, or when the question is purely about backend APIs (use `backend-architecture`).

## Inputs

Required:

- Approved `system-design.md`.
- The frontend surface in scope: web app, admin console, embedded widget, mobile web, or multi-app shell.
- Primary user tasks and the device, network, and accessibility expectations they imply.

Optional:

- PRD sections covering SEO, internationalization, offline behavior, real-time expectations, and supported devices.
- Existing design system, brand system, or component library.
- API contracts from `backend-architecture` (REST, GraphQL, streaming, BFF expectations).
- Auth and identity model (session, OIDC, token storage rules).
- Performance and accessibility SLOs.
- Framework constraints or preferences from the org.

## Operating rules

- Architect the application shape before naming a framework. Routing model, rendering strategy, state model, and data flow are framework-independent decisions.
- Choose rendering per route, not per app. A single app routinely mixes static, server-rendered, streamed, and client-rendered routes. Each route names its rendering mode and why.
- Data fetching is a contract. Define where each piece of data is fetched (server, edge, client), how it is cached, how it is invalidated, and how it behaves offline or under failure.
- State has tiers. Distinguish server-cache state, URL state, ephemeral UI state, and durable client state. Each tier has different ownership, lifetime, and invalidation rules.
- Authentication and session handling are first-class. Define token storage, refresh path, route-level guards, CSRF posture, and what the unauthenticated experience renders.
- Treat the design system as a seam, not a leak. The architecture states what comes from the design system, what is app-owned, and how theming and tokens flow.
- Accessibility is non-negotiable. Define the WCAG level targeted and the keyboard, focus, and assistive-tech expectations per surface type.
- Performance budgets are stated up front: LCP, INP, JS bundle, image strategy, third-party script policy. Decisions that breach budgets need ADRs.
- Real-time features (websockets, SSE, polling) are an explicit architectural decision with a fallback for failure.
- When a frontend decision changes a security or privacy boundary (token storage, embedding, third-party scripts, PII rendering), raise an ADR candidate.

## Process

1. Load `system-design.md` and identify the frontend surfaces, their primary user tasks, and the API or BFF boundary they consume.
2. Define the application shell: number of apps, shared shell vs separate deploys, micro-frontend posture if any, and shared cross-cutting concerns (auth, telemetry, error boundaries).
3. Define the routing model: route hierarchy, layouts, dynamic segments, route-level data dependencies, and not-found and error route behavior.
4. Choose the rendering strategy per route or route group: static, server-rendered, streamed, client-rendered, or island/partial. Justify against SEO, freshness, interactivity, and TTFB needs.
5. Define the data fetching strategy: where each query runs (server, edge, client), the caching layer (HTTP cache, framework cache, client store), invalidation triggers, and mutation flow.
6. Define the state model: server-cache state, URL state, ephemeral UI state, durable client state (storage, sync rules), and the libraries or primitives chosen per tier.
7. Define auth and session handling on the client: token type and storage location, refresh and rotation flow, route guards, role-based access, CSRF and XSS posture, and unauthenticated rendering.
8. Define the design-system seam: what the design system owns (tokens, primitives, patterns), what the app owns (compositions, flows), theming flow, and the contract for adding or extending components.
9. Define internationalization, localization, and content posture: locale routing, translation source, runtime vs build-time loading, RTL support, and date/number/currency handling.
10. Define accessibility posture: target WCAG level, keyboard model, focus management on navigation, live-region usage, and the testing expectation per surface.
11. Define performance budgets: Core Web Vitals targets, JS bundle budget per route, image and font strategy, third-party script policy, and the action taken when a budget is breached.
12. Define real-time, offline, and resilience behavior: websocket or SSE usage, polling fallback, offline-capable routes, optimistic updates, and reconciliation on reconnect.
13. Define observability on the client: error reporting, RUM signals, session replay posture, telemetry sampling, and PII redaction rules.
14. Produce `frontend-architecture.md` with explicit handoffs to `implementations/frontend/<framework>`, `backend-architecture` (BFF/API expectations), `security`, `performance`, and `quality-engineering`.

## Outputs

Required:

- `frontend-architecture.md` covering app shell, routing, rendering strategy per route group, data fetching and caching, state model, auth handling, design-system seam, i18n, accessibility, performance budgets, real-time behavior, observability, and handoff notes.

Optional, when applicable:

- Route map with rendering modes annotated.
- Data flow diagram.
- State tier table.
- Performance budget sheet.
- ADR drafts for framework selection, rendering strategy, or state library choice.

## Quality checks

- [ ] Every route or route group names its rendering mode and the reason.
- [ ] Every piece of fetched data names where it is fetched, how it is cached, and how it is invalidated.
- [ ] State decisions cover all four tiers (server-cache, URL, ephemeral UI, durable client) or explicitly say a tier is unused.
- [ ] Auth handling names token storage, refresh flow, route guards, and CSRF/XSS posture.
- [ ] Design-system ownership boundary is explicit: tokens, primitives, compositions.
- [ ] Accessibility posture names a WCAG level and a testing expectation.
- [ ] Performance budgets state numeric targets for LCP, INP, and JS bundle, and define a breach action.
- [ ] Real-time or offline features state a failure fallback.
- [ ] No framework-specific component code, build config, or vendor SDK calls appear in the architecture unless they materially change behavior.

## References

- Upstream: [`architecture/system-design`](../system-design/SKILL.md).
- Downstream implementation skills: `implementations/frontend/nextjs`, `implementations/frontend/react`, `implementations/frontend/angular`, `implementations/frontend/vue`, `implementations/frontend/svelte`.
- Related architecture skills: [`backend-architecture`](../backend-architecture/SKILL.md), `security`, `performance`, `quality-engineering`. Visual and component design lives in the `frontend-design` skill.
