# react

> Status: scaffold.

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

- [microservices](../../../patterns/microservices/README.md) (BFF-backed React SPA)
- [cqrs](../../../patterns/cqrs/README.md) (read-model-driven UI)
- [real-time-systems](../../../patterns/real-time-systems/README.md) (subscription-driven UI)

## Skills

### Authored

_None._

### Archetype coverage

| # | Archetype | Skill | Status |
|---|---|---|---|
| 1 | app-scaffold-and-runtime | `react-app-scaffold-and-runtime` | planned |
| 2 | routing-and-rendering-strategy | `react-routing-and-rendering-strategy` | planned |
| 3 | state-management-and-data-fetching | `react-state-management-and-data-fetching` | planned |
| 4 | design-system-and-accessibility | `react-design-system-and-accessibility` | planned |
| 5 | performance-and-delivery-optimization | `react-performance-and-delivery-optimization` | planned |

### Planned skill scope (future work)

- **`react-app-scaffold-and-runtime`** — Vite (or Webpack) project layout, env/profile handling, error boundaries (top-level + route-level), structured logging client, RUM + error-reporting wiring, auth provider/wrapper baseline (`AuthProvider`/`SessionContext`), CSP and security headers via host config, container or static-CDN packaging.
- **`react-routing-and-rendering-strategy`** — React Router 6 topology (data routers, nested routes, loaders/actions), CSR-only posture (SSR is meta-framework territory), suspense boundaries, loading/error UI per route, route-level metadata, protected-route gates and redirect flows tied to the auth provider from scaffold.
- **`react-state-management-and-data-fetching`** — 4-tier state discipline (URL via Router, server via TanStack Query, global via Zustand/RTK, local via `useState`/`useReducer`), query/mutation conventions, cache and revalidation policy, optimistic updates, auth-token storage and refresh, authorization headers, logout state propagation, CSRF token wiring.
- **`react-design-system-and-accessibility`** — design tokens (CSS variables / Tailwind theme / vanilla-extract), primitive composition (Radix / React Aria / Headless UI), theming and dark-mode strategy, WCAG 2.2 AA conformance posture, keyboard navigation and focus-management discipline, ARIA usage rules, screen-reader testing, i18n seam (react-i18next / FormatJS).
- **`react-performance-and-delivery-optimization`** — per-route perf budgets, code-splitting via `lazy`/`Suspense`, route-level chunking, third-party-script audit, image (`<img loading="lazy">`, `srcset`) and font posture (`font-display: swap`, preload, self-host), Web Vitals (LCP/CLS/INP/TTFB) via `web-vitals`, Lighthouse CI and bundle-analyzer gates, CDN cache-control posture.

## Architecture domains implemented

| Architecture domain | How |
|---|---|
| [frontend-architecture](../../../architecture/frontend-architecture/README.md) | App shell, routing, rendering, state, design-system seam, a11y. |
| [performance](../../../architecture/performance/README.md) | Per-route Web Vitals budgets and CI gates. |
| [security](../../../architecture/security/README.md) | Auth provider wiring, CSP, token storage discipline, no secrets in bundles. |

## Standards this implementation conforms to

- [api-standards](../../../standards/api-standards/README.md)
- [security-standards](../../../standards/security-standards/README.md)
- [observability-standards](../../../standards/observability-standards/README.md)
- [deployment-standards](../../../standards/deployment-standards/README.md)
- [naming-conventions](../../../standards/naming-conventions/README.md)

## Upstream inputs

- Approved `frontend-architecture.md` declaring rendering strategy per route, state-tier model, design-system seam, perf budgets, and a11y posture.
- Approved `architecture/security` decisions on auth provider, session model, and token strategy.
- `backend-architecture.md` for API contracts the frontend consumes.
