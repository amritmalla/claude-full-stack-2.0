# svelte

> Status: scaffold.

## Purpose

Implements `architecture/frontend-architecture` using Svelte 5 as a standalone SPA or as the base for a meta-framework (SvelteKit, when added). Owns the canonical Svelte surface: app shell and runtime, routing and rendering, state and data fetching, design system and accessibility, performance and delivery.

Architecture decisions (rendering strategy per route, state-tier model, design-system seam, perf budgets, auth flow) come from upstream and are taken as inputs here.

## Strategy

Svelte is a **base** stack in the frontend layer model. It owns all 5 archetypes; future SvelteKit skills inherit where surfaces do not meaningfully diverge.

## Ecosystem (target)

- Svelte 5+ (runes: `$state`, `$derived`, `$effect`, `$props`)
- svelte-routing or svelte-spa-router for standalone SPA routing (SvelteKit owns routing in meta-framework form)
- Svelte stores + runes for global state
- TanStack Query (Svelte) or `@tanstack/svelte-query` for server state
- Vite (default) as bundler
- Vitest + @testing-library/svelte + Playwright for testing
- Design-system primitives via Bits UI, Melt UI, or skeleton-svelte
- web-vitals + Sentry/Datadog for RUM

## Compatible patterns

- [microservices](../../../architecture-patterns/microservices/README.md)
- [cqrs](../../../architecture-patterns/cqrs/README.md)
- [real-time-systems](../../../architecture-patterns/real-time-systems/README.md)

## Skills

### Authored

_None._

### Archetype coverage

| # | Archetype | Skill | Status |
|---|---|---|---|
| 1 | app-scaffold-and-runtime | `svelte-app-scaffold-and-runtime` | planned |
| 2 | routing-and-rendering-strategy | `svelte-routing-and-rendering-strategy` | planned |
| 3 | state-management-and-data-fetching | `svelte-state-management-and-data-fetching` | planned |
| 4 | design-system-and-accessibility | `svelte-design-system-and-accessibility` | planned |
| 5 | performance-and-delivery-optimization | `svelte-performance-and-delivery-optimization` | planned |

### Planned skill scope (future work)

- **`svelte-app-scaffold-and-runtime`** — Vite + Svelte project layout, runes-based component conventions, env/profile handling, top-level error handling, structured logging context, RUM + error-reporting wiring, auth context baseline, CSP and security headers via host config, container or static-CDN packaging.
- **`svelte-routing-and-rendering-strategy`** — svelte-routing or svelte-spa-router topology, nested routes, lazy-loaded route components, CSR posture (SSR is SvelteKit territory), loading/error states, route-level metadata, protected-route gates tied to the auth context from scaffold.
- **`svelte-state-management-and-data-fetching`** — 4-tier state discipline (URL via router, server via `@tanstack/svelte-query`, global via stores / shared runes, local via component-scoped runes), store conventions, query/mutation patterns, cache and revalidation policy, optimistic updates, auth-token storage and refresh, authorization headers, logout propagation, CSRF wiring.
- **`svelte-design-system-and-accessibility`** — design tokens, primitive composition (Bits UI / Melt UI / skeleton), theming and dark-mode strategy, WCAG 2.2 AA conformance posture, `use:` action discipline for focus management, ARIA usage in markup, screen-reader testing, i18n seam (svelte-i18n / Paraglide).
- **`svelte-performance-and-delivery-optimization`** — per-route perf budgets, dynamic `import()` and route-level chunking, third-party-script audit, image and font posture, Web Vitals (LCP/CLS/INP/TTFB) via `web-vitals`, Lighthouse CI and `rollup-plugin-visualizer` bundle gates, CDN cache-control posture.

## Architecture domains implemented

| Architecture domain | How |
|---|---|
| [frontend-architecture](../../../architecture/frontend-architecture/README.md) | App shell, routing, rendering, state, design-system seam, a11y. |
| [performance](../../../architecture/performance/README.md) | Per-route Web Vitals budgets and CI gates. |
| [security](../../../architecture/security/README.md) | Auth context wiring, CSP, token storage discipline, no secrets in bundles. |

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
