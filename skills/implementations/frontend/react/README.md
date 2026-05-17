# react

> Status: active — all 5 archetypes authored.

## Purpose

Implements `architecture/frontend-architecture` using React as a standalone SPA or as the base for a meta-framework. Owns the canonical React surface: app shell and runtime, routing and rendering, state and data fetching, design system and accessibility, performance and delivery.

Architecture decisions (rendering strategy per route, state-tier model, design-system seam, perf budgets, auth flow) come from upstream and are taken as inputs here.

## Strategy

React is a **base** stack in the frontend layer model. It owns all 5 archetypes; meta-frameworks (e.g. nextjs) inherit from these where their surface does not meaningfully diverge.

## Ecosystem (target)

- React 18+ (concurrent features, Suspense, transitions)
- React Router 6+ (or framework-native routing where applicable)
- TanStack Query (default) or RTK Query / Apollo / Relay for server state
- Zustand / Redux Toolkit / Jotai for global client state
- Vite (default) or Webpack as bundler
- Vitest / Jest + React Testing Library + Playwright for testing
- Design-system primitives via Radix, Headless UI, or React Aria
- web-vitals + Sentry/Datadog for RUM

## Compatible patterns

- [microservices](../../../../architecture-patterns/microservices/README.md) (BFF-backed React SPA)
- [cqrs](../../../../architecture-patterns/cqrs/README.md) (read-model-driven UI)
- [real-time-systems](../../../../architecture-patterns/real-time-systems/README.md) (subscription-driven UI)

## Skills

### Authored

- [react-app-scaffold-and-runtime](react-app-scaffold-and-runtime/SKILL.md) — Vite/Webpack project layout, env/profile handling, layered error boundaries, structured logging client, RUM + error-reporting wiring, auth provider/wrapper baseline (seam only), CSP/security headers, container or static-CDN packaging.
- [react-routing-and-rendering-strategy](react-routing-and-rendering-strategy/SKILL.md) — React Router 6 data-router topology, CSR-only posture, per-route loading/error UI, suspense/transition boundaries, route-level metadata, protected-route gates and redirect flows wired to the scaffold auth seam.
- [react-state-management-and-data-fetching](react-state-management-and-data-fetching/SKILL.md) — 4-tier state discipline (URL/server/global/local), TanStack Query server-state layer, query/mutation conventions, optimistic-update posture, and the auth-token storage/refresh/CSRF/logout lifecycle the scaffold and routing skills deferred.
- [react-design-system-and-accessibility](react-design-system-and-accessibility/SKILL.md) — design-token wiring, accessible primitive composition (Radix/React Aria/Headless UI), theming/dark-mode, WCAG 2.2 AA posture, focus/keyboard/ARIA discipline, i18n seam, accessible auth UIs. Inherited by meta-frameworks.
- [react-performance-and-delivery-optimization](react-performance-and-delivery-optimization/SKILL.md) — per-route Web Vitals budgets, code-splitting topology, image/font posture, third-party-script audit, LCP/CLS/INP/TTFB instrumentation, Lighthouse and bundle CI gates, CDN cache-control posture.

### Archetype coverage

| # | Archetype | Skill | Status |
|---|---|---|---|
| 1 | app-scaffold-and-runtime | [`react-app-scaffold-and-runtime`](react-app-scaffold-and-runtime/SKILL.md) | authored |
| 2 | routing-and-rendering-strategy | [`react-routing-and-rendering-strategy`](react-routing-and-rendering-strategy/SKILL.md) | authored |
| 3 | state-management-and-data-fetching | [`react-state-management-and-data-fetching`](react-state-management-and-data-fetching/SKILL.md) | authored |
| 4 | design-system-and-accessibility | [`react-design-system-and-accessibility`](react-design-system-and-accessibility/SKILL.md) | authored |
| 5 | performance-and-delivery-optimization | [`react-performance-and-delivery-optimization`](react-performance-and-delivery-optimization/SKILL.md) | authored |

## Architecture domains implemented

| Architecture domain | How |
|---|---|
| [frontend-architecture](../../../architecture/frontend-architecture/SKILL.md) | App shell, routing, rendering, state, design-system seam, a11y. |
| [performance](../../../architecture/performance/SKILL.md) | Per-route Web Vitals budgets and CI gates. |
| [security](../../../architecture/security/SKILL.md) | Auth provider wiring, CSP, token storage discipline, no secrets in bundles. |

## Standards this implementation conforms to

- [api-standards](../../../../standards/api-standards/README.md)
- [security-standards](../../../../standards/security-standards/README.md)
- [observability-standards](../../../../standards/observability-standards/README.md)
- [deployment-standards](../../../../standards/deployment-standards/README.md)
- [naming-conventions](../../../../standards/naming-conventions/README.md)

## Upstream inputs

- Approved `frontend-architecture.md` declaring rendering strategy per route, state-tier model, design-system seam, perf budgets, and a11y posture.
- Approved `architecture/security` decisions on auth provider, session model, and token strategy.
- `backend-architecture.md` for API contracts the frontend consumes.
