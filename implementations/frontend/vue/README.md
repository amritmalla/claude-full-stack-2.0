# vue

> Status: scaffold.

## Purpose

Implements `architecture/frontend-architecture` using Vue 3 as a standalone SPA or as the base for a meta-framework (Nuxt, when added). Owns the canonical Vue surface: app shell and runtime, routing and rendering, state and data fetching, design system and accessibility, performance and delivery.

Architecture decisions (rendering strategy per route, state-tier model, design-system seam, perf budgets, auth flow) come from upstream and are taken as inputs here.

## Strategy

Vue is a **base** stack in the frontend layer model. It owns all 5 archetypes; future Nuxt skills inherit where surfaces do not meaningfully diverge.

## Ecosystem (target)

- Vue 3.4+ (Composition API default, `<script setup>`)
- Vue Router 4+
- Pinia for global state
- TanStack Query (Vue) or VueUse composables for server state
- Vite (default) as bundler
- Vitest + Vue Test Utils + Playwright for testing
- Design-system primitives via Radix Vue, Headless UI Vue, or vue-aria
- web-vitals + Sentry/Datadog for RUM

## Compatible patterns

- [microservices](../../../architecture-patterns/microservices/README.md) (BFF-backed Vue SPA)
- [cqrs](../../../architecture-patterns/cqrs/README.md)
- [real-time-systems](../../../architecture-patterns/real-time-systems/README.md)

## Skills

### Authored

_None._

### Archetype coverage

| # | Archetype | Skill | Status |
|---|---|---|---|
| 1 | app-scaffold-and-runtime | `vue-app-scaffold-and-runtime` | planned |
| 2 | routing-and-rendering-strategy | `vue-routing-and-rendering-strategy` | planned |
| 3 | state-management-and-data-fetching | `vue-state-management-and-data-fetching` | planned |
| 4 | design-system-and-accessibility | `vue-design-system-and-accessibility` | planned |
| 5 | performance-and-delivery-optimization | `vue-performance-and-delivery-optimization` | planned |

### Planned skill scope (future work)

- **`vue-app-scaffold-and-runtime`** — Vite project layout, `<script setup>` and Composition API conventions, env/profile handling, top-level and component-level error handling (`errorHandler`, `onErrorCaptured`), structured logging plugin, RUM + error-reporting wiring, auth provider plugin baseline, CSP and security headers via host config, container or static-CDN packaging.
- **`vue-routing-and-rendering-strategy`** — Vue Router 4 topology, nested routes, navigation guards, lazy route components, CSR posture (SSR is meta-framework territory), `<Suspense>` boundaries, loading/error views per route, route meta and SEO, protected-route navigation guards tied to the auth plugin from scaffold.
- **`vue-state-management-and-data-fetching`** — 4-tier state discipline (URL via Router, server via TanStack Query Vue, global via Pinia, local via `ref`/`reactive`), Pinia store conventions, query/mutation patterns, cache and revalidation policy, optimistic updates, auth-token storage and refresh, authorization headers, logout propagation, CSRF wiring.
- **`vue-design-system-and-accessibility`** — design tokens, primitive composition (Radix Vue / Headless UI Vue), theming and dark-mode strategy, WCAG 2.2 AA conformance posture, `v-focus` and focus-management discipline, ARIA usage rules in templates, screen-reader testing, i18n seam (vue-i18n).
- **`vue-performance-and-delivery-optimization`** — per-route perf budgets, async components and route-level chunking, third-party-script audit, image and font posture, Web Vitals (LCP/CLS/INP/TTFB) via `web-vitals`, Lighthouse CI and `rollup-plugin-visualizer` bundle gates, CDN cache-control posture.

## Architecture domains implemented

| Architecture domain | How |
|---|---|
| [frontend-architecture](../../../architecture/frontend-architecture/README.md) | App shell, routing, rendering, state, design-system seam, a11y. |
| [performance](../../../architecture/performance/README.md) | Per-route Web Vitals budgets and CI gates. |
| [security](../../../architecture/security/README.md) | Auth plugin wiring, CSP, token storage discipline, no secrets in bundles. |

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
