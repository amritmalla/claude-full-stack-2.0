# implementations/frontend

Technology-specific execution skills for frontend.

## Philosophy

Each frontend implementation skill speaks as a **senior frontend engineer** in a specific framework. It implements, hardens, or reviews — it does not invent architectural decisions. Architecture artifacts produced by `architecture/frontend-architecture`, `architecture/performance`, `architecture/security`, and `architecture/operations` are the source of truth; the implementation skill consumes them and emits app shells, route/render configuration, data-fetching wiring, design-system integration, accessibility posture, and bundle/delivery gates.

If an artifact is silent on a needed decision (rendering mode per route, state-tier ownership, design-system seam, perf budget, auth flow), the implementation skill **pauses and raises an ADR candidate** against the upstream domain rather than guessing.

Skills are scoped, not monolithic. Each `SKILL.md`:

- declares its upstream architecture domain(s) and the standards it conforms to,
- requires the upstream artifact when scaffolding or generating new routes/state/design wiring, and runs standalone for review or hardening when the artifact does not yet exist,
- maps to exactly one of five canonical archetypes (below),
- emits concrete code, configuration, route definitions, fetch/cache configuration, and CI gates — not prose-only deliverables.

## Archetypes

Every frontend implementation stack is expected to provide skills drawn from these five archetypes. Only those archetypes the architecture layer actually demands for that stack are produced — there is no fixed baseline.

| # | Archetype | What the skill produces | Primary upstream |
|---|---|---|---|
| 1 | **app-scaffold-and-runtime** | Production-ready app shell: project layout, framework configuration, environment/profile handling, runtime selection (node/edge/static), error boundaries, structured logging client, observability hooks, container or CDN packaging. Sets the **auth provider/wrapper baseline** that downstream skills extend. | `frontend-architecture` |
| 2 | **routing-and-rendering-strategy** | Routing topology, rendering mode per route (CSR/SSR/SSG/ISR/streaming/RSC where applicable), loading and error states, suspense boundaries, redirect/auth-gate wiring, route-level metadata and SEO posture. | `frontend-architecture` (rendering strategy) |
| 3 | **state-management-and-data-fetching** | 4-tier state model (URL, server, global, local), data-fetching layer (TanStack Query, RTK Query, Apollo, native fetch, server actions), cache and revalidation policy, mutation/optimistic-update posture, **auth-token plumbing and refresh**. | `frontend-architecture` (state model, data-fetching strategy) |
| 4 | **design-system-and-accessibility** | Design-system integration (tokens, primitives, theming), component-library composition, accessibility (WCAG AA, keyboard, focus management, ARIA discipline), internationalization seam. | `frontend-architecture` (design-system seam, a11y posture) |
| 5 | **performance-and-delivery-optimization** | Per-route perf budgets, code-splitting and lazy-loading topology, image and font posture, third-party-script audit, Web Vitals (LCP/CLS/INP/TTFB), Lighthouse/Web-Vitals CI gates, bundle analysis, CDN/edge delivery posture. | `performance` + `frontend-architecture` (perf budgets) |

### Auth is cross-cutting

There is no dedicated `auth-and-security` archetype for frontend. Auth surface area is split across the existing five:

- **app-scaffold-and-runtime** — provider/wrapper baseline (e.g. `SessionProvider`, `AuthProvider`), CSP headers, env-aware client ID handling.
- **routing-and-rendering-strategy** — protected-route gates, redirect flows, server-side session checks where rendering is server-side.
- **state-management-and-data-fetching** — token storage and refresh, request-side authorization headers, logout state propagation, CSRF posture.
- **design-system-and-accessibility** — accessible auth UIs (login, MFA, recovery flows).

Each frontend `SKILL.md` that touches an auth concern names the upstream `architecture/security` decisions it implements (auth provider, session model, token strategy) and pauses for an ADR candidate if those decisions are missing.

## Stacks

### Implemented

| Stack | Strategy | Archetype coverage |
|---|---|---|
| [react](react/) | Base — owns all 5 archetypes | 5/5 (all archetypes authored) |

### Planned (future scope)

| Stack | Strategy | Archetype coverage |
|---|---|---|
| [nextjs](nextjs/) | Delta over React — 4 own skills + 1 inherited from react | 0/4 own + inherits design-system |
| [vue](vue/) | Base — owns all 5 archetypes | 0/5 |
| [svelte](svelte/) | Base — owns all 5 archetypes | 0/5 |
| [angular](angular/) | Base — owns all 5 archetypes | 0/5 |

Per-stack READMEs enumerate the proposed skill list and current authoring status.

## Meta-framework strategy

Meta-frameworks built on a base framework are modeled as **deltas**, not duplicates. The base owns the canonical archetypes; the meta-framework authors skills only where its surface meaningfully differs.

- **nextjs over react** — owns its own `app-scaffold-and-runtime`, `routing-and-rendering-strategy`, `state-management-and-data-fetching`, and `performance-and-delivery-optimization` (each substantially diverges from plain React via App Router, RSC, server actions, `next/image`, `next/font`, edge runtime, etc.). Inherits `design-system-and-accessibility` from `react`, with a note in the nextjs README about `'use client'` boundaries and RSC-compatibility for component libraries.

When future meta-frameworks land (Nuxt over Vue, SvelteKit over Svelte, Analog over Angular), they follow the same delta rule — evaluated pairwise.

## Decided design constraints

These constraints are locked for all current and future frontend implementation skills:

- **5 archetypes per base stack, on-demand.** A stack adds only the archetypes its upstream architecture demands. No fixed baseline.
- **Meta-frameworks are deltas.** A meta-framework authors a skill only where it meaningfully diverges from its base; otherwise it inherits and links.
- **Per-skill upstream linkage.** Every `SKILL.md` names its upstream architecture domain(s) and conformance standards directly.
- **Auth is cross-cutting.** No dedicated auth archetype; auth concerns split across scaffold/routing/data-fetching/design-system and reference `architecture/security`.
- **Web Vitals are the perf gate.** Performance work is anchored to LCP, CLS, INP, TTFB measured at the route level. Synthetic bundle-size gates supplement, never replace, real-user-metric gates.
- **Accessibility is non-optional.** Every component-producing skill defines its WCAG conformance posture, keyboard navigation behavior, and screen-reader expectations.

## Standards every frontend implementation skill conforms to

- [api-standards](../../../standards/api-standards/README.md) — the frontend honors the REST/GraphQL/event contracts produced by `backend-architecture`.
- [security-standards](../../../standards/security-standards/README.md) — CSP, token storage discipline, OWASP Top-10 client-side posture, no secrets in bundles.
- [observability-standards](../../../standards/observability-standards/README.md) — RUM (real-user metrics), error reporting, trace correlation from browser to backend.
- [deployment-standards](../../../standards/deployment-standards/README.md) — env-agnostic builds, config injection at deploy time, CDN/edge artifacts.
- [naming-conventions](../../../standards/naming-conventions/README.md) — component, route, and asset naming.
