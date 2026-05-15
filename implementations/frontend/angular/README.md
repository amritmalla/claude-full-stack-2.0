# angular

> Status: scaffold.

## Purpose

Implements `architecture/frontend-architecture` using Angular 17+ as a standalone application, including standalone components, signals, and the new control flow. Owns the canonical Angular surface: app shell and runtime, routing and rendering, state and data fetching, design system and accessibility, performance and delivery.

Architecture decisions (rendering strategy per route, state-tier model, design-system seam, perf budgets, auth flow) come from upstream and are taken as inputs here.

## Strategy

Angular is a **base** stack in the frontend layer model. It owns all 5 archetypes; future Analog skills inherit where surfaces do not meaningfully diverge.

## Ecosystem (target)

- Angular 17+ (standalone components default, signals, new control flow `@if`/`@for`/`@switch`, deferrable views)
- Angular Router with functional guards and resolvers
- NgRx Signals / Component Store (or NgRx classic) for global state
- Angular HttpClient with interceptors for data fetching, or TanStack Query (Angular)
- esbuild-based application builder (default in Angular 17+)
- Jest / Karma + Playwright / Cypress for testing
- Angular CDK + Angular Material / Spartan UI / Taiga UI for design-system primitives
- web-vitals + Sentry/Datadog for RUM
- Angular SSR (with hydration) when architecture demands server rendering

## Compatible patterns

- [microservices](../../../patterns/microservices/README.md)
- [cqrs](../../../patterns/cqrs/README.md)
- [real-time-systems](../../../patterns/real-time-systems/README.md)

## Skills

### Authored

_None._

### Archetype coverage

| # | Archetype | Skill | Status |
|---|---|---|---|
| 1 | app-scaffold-and-runtime | `angular-app-scaffold-and-runtime` | planned |
| 2 | routing-and-rendering-strategy | `angular-routing-and-rendering-strategy` | planned |
| 3 | state-management-and-data-fetching | `angular-state-management-and-data-fetching` | planned |
| 4 | design-system-and-accessibility | `angular-design-system-and-accessibility` | planned |
| 5 | performance-and-delivery-optimization | `angular-performance-and-delivery-optimization` | planned |

### Planned skill scope (future work)

- **`angular-app-scaffold-and-runtime`** — Angular CLI project layout (esbuild application builder), standalone-component default, env/profile handling via `environments/` plus runtime config, `provideExperimentalZonelessChangeDetection` posture, global `ErrorHandler` and route-level error UIs, structured logging service, RUM + error-reporting wiring, auth provider service baseline, CSP and security headers via host config, container or static-CDN packaging.
- **`angular-routing-and-rendering-strategy`** — Angular Router topology with functional guards (`CanActivateFn`) and resolvers, lazy-loaded routes, deferrable views (`@defer`), CSR vs Angular SSR (with hydration and event replay) per route, loading and error UIs, route data and SEO via title/meta strategies, protected-route guards tied to the auth provider from scaffold.
- **`angular-state-management-and-data-fetching`** — 4-tier state discipline (URL via Router, server via HttpClient + TanStack Query Angular or RxJS resource patterns, global via NgRx Signals / Component Store, local via component signals), `HttpInterceptor` chain for auth, retry, and tracing, cache and revalidation policy, optimistic updates, auth-token storage and refresh, CSRF interceptor wiring, logout propagation.
- **`angular-design-system-and-accessibility`** — design tokens (CSS variables / Material theming / Tailwind), Angular CDK primitives (a11y, overlay, portal, drag-drop), component-library composition (Material / Spartan / Taiga), theming and dark-mode strategy, WCAG 2.2 AA conformance posture, `FocusMonitor` and focus-trap discipline, ARIA via CDK directives, screen-reader testing, i18n seam (`@angular/localize` or Transloco).
- **`angular-performance-and-delivery-optimization`** — per-route perf budgets in `angular.json`, route-level lazy loading, deferrable views (`@defer` with `on viewport`/`on idle`/`on interaction`), `OnPush` and signals adoption for change-detection cost, third-party-script audit, image (`NgOptimizedImage`) and font posture, Web Vitals (LCP/CLS/INP/TTFB) via `web-vitals`, Lighthouse CI and source-map-explorer bundle gates, CDN cache-control posture, SSR hydration verification.

## Architecture domains implemented

| Architecture domain | How |
|---|---|
| [frontend-architecture](../../../architecture/frontend-architecture/README.md) | App shell, routing, rendering (CSR/SSR), state, design-system seam, a11y. |
| [performance](../../../architecture/performance/README.md) | Per-route Web Vitals budgets, deferrable views, change-detection cost. |
| [security](../../../architecture/security/README.md) | Auth provider wiring, CSP, interceptor-based token handling, no secrets in bundles. |

## Standards this implementation conforms to

- [api-standards](../../../standards/api-standards/README.md)
- [security-standards](../../../standards/security-standards/README.md)
- [observability-standards](../../../standards/observability-standards/README.md)
- [deployment-standards](../../../standards/deployment-standards/README.md)
- [naming-conventions](../../../standards/naming-conventions/README.md)

## Upstream inputs

- Approved `frontend-architecture.md` declaring rendering strategy per route, SSR posture, state-tier model, design-system seam, perf budgets, and a11y posture.
- Approved `architecture/security` decisions on auth provider, session model, and token strategy.
- `backend-architecture.md` for API contracts the frontend consumes.
