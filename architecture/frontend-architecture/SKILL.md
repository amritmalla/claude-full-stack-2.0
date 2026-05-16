---
name: frontend-architecture
description: Use when an approved system design exists and the team needs production-grade frontend application architecture before UI implementation. Produces application-shell structure, routing and rendering strategy, state and data-flow architecture, auth and session handling, design-system boundaries, accessibility posture, performance budgets, resilience behavior, observability strategy, and implementation handoff guidance. Do not use for visual design, component-level styling, framework-specific scaffolding, marketing-page authoring, or backend API design; use frontend-design, implementations/frontend/<framework>, or backend-architecture instead.
---

# Frontend Architecture

## When to use

Invoke after `system-design` has approved a design that includes a user-facing web frontend, and before `implementations/frontend/<framework>` skills generate components, routes, or build configuration.

Do not use when only visual or component design is needed (use [`frontend-design`](../../implementations/frontend/frontend-design/SKILL.md)), when scaffolding a known framework with a known architecture (go directly to the implementation skill), when the surface is a single static marketing page, or when the question is purely about backend APIs (use `backend-architecture`).

## Inputs

Required:

- Approved `system-design.md` and the relevant ADRs.
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

- Architect the application before selecting frameworks. Routing, rendering, state, and data flow are framework-independent decisions; framework selection follows rendering requirements, deployment topology, team constraints, and operational needs.
- Rendering strategy is route-specific. A single app routinely mixes static, server-rendered, streamed, client-rendered, island, and edge routes. Each route or group names its rendering mode, hydration behavior, freshness, SEO need, and interactivity model.
- State has ownership tiers. Distinguish server-cache state, URL/navigation state, ephemeral UI state, and durable client state; each tier defines ownership, lifecycle, invalidation, synchronization, and persistence. Reject global-store-for-everything.
- Data fetching is a contract. Each fetched dataset names where it loads, who owns freshness, caching behavior, invalidation triggers, loading behavior, and offline/failure posture. Reject duplicated client/server fetching and undefined mutation consistency.
- Authentication and session handling are architecture, not implementation. Define token/session storage, refresh flow, route protection, CSRF posture, XSS assumptions, and unauthenticated rendering behavior. Reject localStorage token defaults without threat modeling.
- Treat the design system as a seam, not a leak. State what the design system owns (tokens, primitives, patterns), what the app owns (workflows, compositions), and how theming/tokens propagate. Reject business logic in design-system primitives.
- Accessibility is a baseline constraint, not optional polish. Define WCAG target, keyboard model, focus management, assistive-tech support, and testing posture. A component library is not automatic compliance.
- Performance budgets are architectural constraints set before implementation: LCP, INP, CLS, JS bundle, image strategy, font strategy, third-party script policy. Budget breaches need ADRs.
- Real-time and offline behavior are explicit decisions. Websockets, SSE, polling, optimistic updates, and offline storage each define failure behavior, reconnect semantics, reconciliation, and degraded-mode experience.
- Challenge weak frontend architecture directly and with user impact: over-globalized state, unnecessary CSR, hydration abuse, frontend/backend coupling, component-system leakage.
- When a frontend decision changes a security or privacy boundary (token storage, embedding, third-party scripts, PII rendering), raise an ADR candidate against `system-design`.

## Output contract

`frontend-architecture.md` MUST conform to [standards/architecture-schema](../../standards/architecture-schema/README.md), which is authoritative for its frontmatter, required and conditional sections, conditional-section omission rules, and linkage back to `system-design.md` and its ADRs.

Security, observability, and operational content additionally conforms to [security-standards](../../standards/security-standards/README.md), [observability-standards](../../standards/observability-standards/README.md), and [deployment-standards](../../standards/deployment-standards/README.md). Skill structure conforms to [documentation-standards](../../standards/documentation-standards/README.md).

Use `assets/frontend-architecture.template.md` as the scaffold; it implements the schema. No framework-specific component code, build config, or vendor SDK calls appear in the architecture unless they materially change architecture behavior.

## Progressive references

- Read `references/frontend-architecture-playbook.md` when defining the application shell, routing, rendering strategy, data fetching and caching, state tiers, auth/session handling, the design-system seam, internationalization, accessibility posture, performance architecture, real-time/offline resilience, or client observability, and to check the anti-pattern list.
- Read `references/frontend-architecture-quality-rubric.md` before finalizing and use it as the validation checklist.
- Use `assets/frontend-architecture.template.md` for `frontend-architecture.md`.

## Process

Progress:

ADR candidates are drafted inline as decisions are made (steps 4, 7, 11, 12). Step 14 only consolidates them; it does not retrofit ADRs from prose.

- [ ] Step 1: Load `system-design.md` and relevant ADRs. Identify frontend surfaces, user journeys, API/BFF boundaries, device/network expectations, and SEO/offline/realtime/accessibility constraints.
- [ ] Step 2: Define the application shell: number of apps, deployment boundaries, shared shell vs separate deploys, micro-frontend posture, shared navigation/auth/telemetry, and error-boundary strategy. Reject premature microfrontends.
- [ ] Step 3: Define the routing model: route hierarchy, layouts, nested navigation, dynamic segments, route ownership, not-found/loading/transition behavior, and route-level access constraints.
- [ ] Step 4: Choose the rendering strategy per route or group (SSG, SSR, streamed SSR, CSR, edge, islands). Justify against latency, SEO, interactivity, and operational complexity. Draft an ADR candidate for the rendering decision. See `references/frontend-architecture-playbook.md`.
- [ ] Step 5: Define data fetching and caching: fetch location (server/edge/client), ownership, cache layer (HTTP/framework/client/CDN/edge), invalidation strategy, retry posture, stale-data behavior, mutation flow, and optimistic updates.
- [ ] Step 6: Define the state architecture across all four tiers (server-cache, URL, ephemeral UI, durable client): ownership, synchronization, persistence, invalidation lifecycle, and storage mechanism per tier. Unused tiers stated explicitly.
- [ ] Step 7: Define auth and session handling: token/session type and storage, refresh flow, route guards, RBAC, unauthenticated rendering, CSRF posture, XSS exposure, session expiration, silent refresh, logout propagation, and multi-tab behavior. Draft an ADR candidate for the token-storage decision.
- [ ] Step 8: Define the design-system seam: what the design system owns vs app composition, theming/token propagation, and the contract for extending components. Reject business-logic leakage into primitives.
- [ ] Step 9: Define internationalization and localization: locale routing, translation loading (runtime vs build-time), RTL posture, and date/number/currency/timezone handling.
- [ ] Step 10: Define accessibility posture: WCAG target level, keyboard navigation, focus management, screen-reader expectations, modal/live-region usage, semantic structure, color-contrast, and testing posture.
- [ ] Step 11: Define performance architecture: numeric targets for LCP, INP, CLS, JS bundle, image payload, and third-party impact; lazy-loading, code-splitting boundaries, image/font strategy, hydration constraints, breach actions, and regression monitoring. Draft an ADR candidate for any budget-breaching decision.
- [ ] Step 12: Define real-time, offline, and resilience behavior: websocket/SSE usage, polling fallback, reconnect, offline-capable surfaces, optimistic updates, reconciliation rules, and degraded-mode UX. Draft an ADR candidate for realtime/privacy-boundary decisions.
- [ ] Step 13: Define client observability: error reporting, RUM metrics, session-replay posture, tracing correlation, sampling policy, PII redaction, and environment-specific telemetry behavior.
- [ ] Step 14: Generate `frontend-architecture.md` from `assets/frontend-architecture.template.md`. Consolidate ADR candidates (numbering, status, alternatives, downsides). Validate against [standards/architecture-schema](../../standards/architecture-schema/README.md) and `references/frontend-architecture-quality-rubric.md`; revise until both pass or explicitly note any unresolved gap.

## Outputs

Required:

- `frontend-architecture.md` at `docs/architecture/<product-slug>/frontend-architecture.md`, with frontmatter and sections per [standards/architecture-schema](../../standards/architecture-schema/README.md).

Optional, when applicable:

- Route map with rendering modes annotated; data-flow diagrams.
- State-tier matrix; cache topology.
- Performance-budget sheet; realtime architecture notes.
- ADR drafts for framework selection, rendering strategy, token storage, or performance-budget decisions.

Output rules:

- Keep the architecture decision-oriented and user-impact focused, not framework-decorative.
- Document tradeoffs and the rejected alternative, not only the chosen path.
- Name surfaces and routes by user task, not by framework feature.
- Treat accessibility, performance budgets, and client observability as part of the design, not later implementation detail.

## Quality checks

- [ ] `references/frontend-architecture-quality-rubric.md` was loaded before finalizing.
- [ ] `frontend-architecture.md` validates against [standards/architecture-schema](../../standards/architecture-schema/README.md): frontmatter complete; required sections present; conditional sections present with content or listed under `## Omitted sections` with rationale.
- [ ] Every route or route group names its rendering mode and the reason.
- [ ] Every piece of fetched data names where it is fetched, how it is cached, and how it is invalidated.
- [ ] State decisions cover all four tiers (server-cache, URL, ephemeral UI, durable client) or explicitly say a tier is unused.
- [ ] Auth handling names token storage, refresh flow, route guards, and CSRF/XSS posture.
- [ ] Design-system ownership boundary is explicit: tokens, primitives, compositions.
- [ ] Accessibility posture names a WCAG level and a testing expectation.
- [ ] Performance budgets state numeric targets for LCP, INP, and JS bundle, and define a breach action.
- [ ] Real-time or offline features state a failure fallback.
- [ ] No framework-specific component code, build config, or vendor SDK calls appear unless they materially change architecture behavior.

## References

- Upstream: [`architecture/system-design`](../system-design/SKILL.md).
- Downstream implementation skills: `implementations/frontend/nextjs`, `implementations/frontend/react`, `implementations/frontend/angular`, `implementations/frontend/vue`, `implementations/frontend/svelte`.
- Related architecture skills: [`backend-architecture`](../backend-architecture/SKILL.md), [`security`](../security/SKILL.md), [`performance`](../performance/SKILL.md), [`quality-engineering`](../quality-engineering/SKILL.md). Visual and component design lives in the [`frontend-design`](../../implementations/frontend/frontend-design/SKILL.md) skill.
