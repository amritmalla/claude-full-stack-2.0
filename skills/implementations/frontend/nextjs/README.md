# nextjs

> Status: scaffold.

## Purpose

Implements `architecture/frontend-architecture` for Next.js: App Router topology, rendering strategy per route (RSC, SSR, SSG, ISR, streaming, PPR), server actions and server-side data fetching, runtime selection (node vs edge), and delivery optimization with `next/image`, `next/font`, and route-segment caching.

Architecture decisions (rendering strategy, runtime per route, ISR/PPR posture, edge vs node, auth flow) come from upstream and are taken as inputs here.

## Strategy

Next.js is a **meta-framework** over React. It is modeled as a **delta**: it owns the archetypes where its surface meaningfully diverges from plain React, and inherits from `react` where it does not.

| # | Archetype | Strategy |
|---|---|---|
| 1 | app-scaffold-and-runtime | **Own** — App Router layout, `next.config`, middleware, route-segment config, env, runtime per route diverge substantially. |
| 2 | routing-and-rendering-strategy | **Own** — App Router, RSC, streaming, parallel/intercepting routes, layouts/templates, route handlers, `generateStaticParams`, PPR are Next-specific. |
| 3 | state-management-and-data-fetching | **Own** — Server actions, `fetch` caching/revalidation, `use()`, `useTransition`, `useOptimistic`, `cookies()`/`headers()` in server components diverge meaningfully. |
| 4 | design-system-and-accessibility | **Inherit** from [`react-design-system-and-accessibility`](../react/README.md) with a Next-specific note (below). |
| 5 | performance-and-delivery-optimization | **Own** — `next/image`, `next/font`, route-segment caching, edge runtime, partial prerendering, dynamic imports are Next-specific. |

### Design-system inheritance note

The React design-system skill applies directly to Next.js with one constraint: **RSC compatibility**. Component libraries built on React state, refs, or browser APIs must be wrapped in or imported from a `'use client'` boundary. The inherited `react-design-system-and-accessibility` skill expects the nextjs skill consumer to:

- mark client-only components with `'use client'`,
- prefer server components by default for static markup,
- audit third-party libraries for RSC compatibility before adoption.

If a library is fundamentally incompatible with RSC (heavy reliance on `useLayoutEffect`, context-mutating providers above the root), prefer an RSC-native alternative or document the exception as an ADR.

## Ecosystem (target)

- Next.js 14+ (App Router default; Pages Router only when migrating)
- React Server Components (RSC) and Server Actions
- Edge and Node runtimes
- `next/image`, `next/font`, `next/script`
- Middleware for auth gating and rewrites
- Vercel / self-hosted Node / containerized deployment
- `@vercel/analytics` or self-hosted RUM for Web Vitals
- Partial Prerendering (PPR) where stable

## Compatible patterns

- [microservices](../../../../architecture-patterns/microservices/README.md) (Next as a frontend over multiple BFFs)
- [cqrs](../../../../architecture-patterns/cqrs/README.md) (RSC consuming a read model)
- [event-driven](../../../../architecture-patterns/event-driven/README.md) (revalidation triggered by upstream events)

## Skills

### Authored

_None._

### Archetype coverage

| # | Archetype | Skill | Status |
|---|---|---|---|
| 1 | app-scaffold-and-runtime | `nextjs-app-scaffold-and-runtime` | planned |
| 2 | routing-and-rendering-strategy | `nextjs-routing-and-rendering-strategy` | planned |
| 3 | state-management-and-data-fetching | `nextjs-state-management-and-data-fetching` | planned |
| 4 | design-system-and-accessibility | inherits [`react-design-system-and-accessibility`](../react/README.md) | inherited |
| 5 | performance-and-delivery-optimization | `nextjs-performance-and-delivery-optimization` | planned |

### Planned skill scope (future work)

- **`nextjs-app-scaffold-and-runtime`** — App Router directory layout (`app/`, route groups, parallel routes, intercepting routes), `next.config.{js,ts}` with route-segment defaults, middleware (auth gating, rewrites, A/B), env/profile handling for client vs server, runtime selection (`runtime: 'edge' | 'nodejs'`) per route, top-level error boundaries (`error.tsx`, `global-error.tsx`), structured logging client, RUM wiring (`@vercel/analytics` or self-hosted), auth provider wrapper baseline (NextAuth.js / Clerk / Auth.js), CSP and security headers via `next.config` headers, container or Vercel packaging.
- **`nextjs-routing-and-rendering-strategy`** — App Router topology with layouts/templates/loading/error files, rendering mode per route (static / dynamic / streaming / RSC / PPR), `generateStaticParams` and `generateMetadata`, route handlers (`route.ts`) for API endpoints, parallel and intercepting routes for modals and split views, server-side session checks and redirect flows tied to middleware and the auth provider from scaffold.
- **`nextjs-state-management-and-data-fetching`** — server-component fetch with `cache`/`no-store`/`force-cache`, `revalidate` (time-based) and `revalidateTag`/`revalidatePath` (on-demand), server actions for mutations with progressive-enhancement form posture, `useOptimistic` and `useTransition` patterns, client-side TanStack Query where interactivity demands it, auth-token plumbing across server and client (cookies via `cookies()`, refresh via middleware), CSRF posture for server actions.
- **`nextjs-performance-and-delivery-optimization`** — `next/image` (sizing, `priority`, `placeholder`, remote patterns), `next/font` (self-host, preload, subsetting), `next/script` strategy (`beforeInteractive`/`afterInteractive`/`lazyOnload`), dynamic imports (`next/dynamic`) with `ssr: false` discipline, route-segment caching strategy, edge vs node runtime selection by latency profile, partial prerendering (PPR) where stable, Lighthouse CI + Web Vitals gates per route, bundle analysis via `@next/bundle-analyzer`.

## Architecture domains implemented

| Architecture domain | How |
|---|---|
| [frontend-architecture](../../../architecture/frontend-architecture/README.md) | App Router scaffold, rendering per route, state across server/client, delivery. |
| [performance](../../../architecture/performance/README.md) | Web Vitals per route, edge runtime, route-segment caching, PPR. |
| [security](../../../architecture/security/README.md) | Middleware-based auth gating, CSP headers, server-side session checks. |

## Standards this implementation conforms to

- [api-standards](../../../../standards/api-standards/README.md)
- [security-standards](../../../../standards/security-standards/README.md)
- [observability-standards](../../../../standards/observability-standards/README.md)
- [deployment-standards](../../../../standards/deployment-standards/README.md)
- [naming-conventions](../../../../standards/naming-conventions/README.md)

## Upstream inputs

- Approved `frontend-architecture.md` declaring rendering mode per route, RSC posture, runtime targets (edge/node), perf budgets.
- Approved `architecture/security` decisions on auth provider, session model, and CSRF posture for server actions.
- `backend-architecture.md` for API contracts and any BFF/route-handler boundaries owned by Next.

## Related

- Base stack: [`react`](../react/README.md) — Next.js inherits `design-system-and-accessibility` from React.
