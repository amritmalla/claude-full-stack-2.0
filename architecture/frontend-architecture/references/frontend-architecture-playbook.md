# Frontend Architecture Playbook

Load this when defining the application shell, routing, rendering, state, or any frontend-architecture decision. It expands the operating rules and process steps in `SKILL.md` with the detail needed to produce `frontend-architecture.md`.

## Why this workflow exists

Design scalable, resilient, accessible, performance-aware frontend architecture before framework implementation begins. It prevents frontend monolith sprawl, accidental rendering bottlenecks, state-management chaos, brittle client-server contracts, inaccessible interaction models, auth/session vulnerabilities, and performance regressions hidden until production.

The goal is not "how pages render" — it is predictable application structure, sustainable evolution, clear state ownership, operational performance, and safe user-facing behavior at scale.

## Behavioral rules in depth

### 1. Architect before selecting frameworks

Routing, rendering, state, and data flow are architectural concerns first. Framework selection follows rendering requirements, deployment topology, team constraints, and operational needs. Reject "we use React for everything" and framework-first architecture.

### 2. Rendering strategy is route-specific

A frontend app is rarely fully SSR, fully CSR, or fully static. Each route or group defines rendering mode, hydration behavior, freshness expectations, SEO needs, and interactivity model. Modes: static generation, server rendering, streamed rendering, client rendering, islands/partial hydration, edge rendering. Reject single-rendering-strategy assumptions without justification.

### 3. State has ownership tiers

Distinguish server-cache state, URL/navigation state, ephemeral UI state, and durable client state. Each tier defines ownership, lifecycle, invalidation behavior, synchronization rules, and persistence expectations. Reject global-store-for-everything architecture.

### 4. Data fetching is a contract

Every fetched dataset defines where it loads, who owns freshness, caching behavior, invalidation triggers, loading behavior, and offline/failure posture. Reject ad hoc client fetching, duplicated caching layers, and undefined mutation consistency.

### 5. Authentication is architecture, not implementation

Frontend auth impacts security boundaries, rendering, caching, and operational risk. Define token/session storage, refresh flow, route protection, CSRF posture, XSS assumptions, and unauthenticated rendering behavior. Reject localStorage token defaults without threat modeling and auth handled "somewhere later."

### 6. Accessibility is a baseline constraint

Define WCAG target, keyboard interaction model, focus-management expectations, assistive-technology support, and accessibility testing requirements. Reject accessibility deferred until QA and component libraries treated as automatic compliance.

### 7. Performance budgets are architectural constraints

Define targets before implementation: LCP, INP, bundle budgets, image strategy, font strategy, third-party script policy. If a decision violates budgets, surface it explicitly and recommend an ADR.

### 8. Real-time and offline behavior are explicit decisions

Any architecture using websockets, SSE, polling, optimistic updates, or offline storage defines failure behavior, reconnect semantics, reconciliation rules, and degraded-mode experience. Reject "realtime later" ambiguity.

### 9. Challenge weak architecture directly

Be operationally concrete and user-impact focused. Examples of the kind of feedback to give:

- "This dashboard route should not require client rendering."
- "Your cache invalidation ownership is unclear."
- "This global store mixes server-cache and UI state."
- "Your auth flow exposes tokens unnecessarily to XSS risk."
- "This route's SEO requirement conflicts with client-only rendering."

## Step detail

**Surface discovery (step 1).** Surface types: web app, admin console, embedded widget, mobile web, multi-app shell, public marketing surface, authenticated application surface. Clarify SEO, offline, realtime, and accessibility constraints per surface.

**Application shell (step 2).** Decide mono-frontend vs multi-app, micro-frontend posture, shared navigation, shared auth/session, telemetry ownership, and error-boundary strategy. Reject premature microfrontends and hidden cross-app coupling.

**Routing (step 3).** Define route hierarchy, layouts, nested navigation, dynamic segments, route ownership, not-found/loading/transition behavior, and route-specific access constraints. Reject flat route sprawl and inconsistent layout ownership.

**Rendering (step 4).** Strategies: SSG, SSR, streamed SSR, CSR, edge rendering, islands. Justify each against latency, SEO, interactivity, and operational complexity. Reject CSR-by-default and SSR for purely interactive/private surfaces without value.

**Data fetching & caching (step 5).** Cache layers: HTTP cache, framework cache, client cache, CDN, edge cache. Clarify mutation flow, optimistic updates, background revalidation, and cache invalidation ownership. Reject duplicated client/server fetching and invalidation ambiguity.

**State (step 6).** Mechanisms: URL params, local component state, client cache/query libraries, browser storage, centralized stores. Reject monolithic global stores and server-cache mixed with UI state.

**Auth & session (step 7).** Review CSRF posture, XSS exposure, session expiration, silent refresh, logout propagation, cookie vs token auth, edge/session awareness, and multi-tab behavior. Reject insecure token persistence and auth assumptions hidden in frontend state.

**Design-system seam (step 8).** Design system may own tokens, primitives, interaction patterns, accessibility baselines, typography. Application owns workflows, business compositions, domain components. Reject business logic leaking into design-system primitives.

**Internationalization (step 9).** Define locale routing, translation loading strategy, runtime vs build-time localization, RTL posture, and date/number/currency/timezone handling. Reject string-based localization without layout awareness.

**Accessibility posture (step 10).** Clarify modal behavior, live-region usage, semantic structure, and color-contrast expectations alongside WCAG target, keyboard rules, focus management, and screen-reader expectations. Reject accessibility delegated entirely to component libraries.

**Performance architecture (step 11).** Numeric targets for LCP, INP, CLS, JS bundle, image payload, third-party impact. Define lazy-loading, code-splitting boundaries, image optimization, font-loading, hydration constraints, breach actions, regression monitoring, and ownership. Reject unbounded bundle growth and third-party script sprawl.

**Realtime, offline & resilience (step 12).** Define websocket/SSE usage, polling fallback, reconnect behavior, offline-capable surfaces, optimistic update behavior, reconciliation rules, degraded-mode UX, and eventual-consistency handling. Reject realtime dependencies without fallback.

**Client observability (step 13).** Define error reporting, telemetry collection, RUM metrics, session-replay posture, tracing correlation, privacy boundaries, sampling policy, PII redaction, and environment-specific behavior. Reject unrestricted session replay and telemetry leaking sensitive data.

## Anti-patterns to detect

Call these out explicitly when detected:

- CSR-by-default architecture
- Hydration overuse
- Global-store-for-everything
- Server-cache mixed with UI state
- Undefined cache invalidation
- Insecure token storage
- Premature microfrontends
- Component-library-driven architecture
- Accessibility deferred to QA
- Third-party script sprawl
- Bundle-size blindness
- Realtime without fallback
- Over-fetching on navigation
- Duplicate client/server data fetching
- Auth hidden in client state
- Unbounded persistent browser storage
- SEO-critical routes using client-only rendering
- Design-system/business-logic coupling

## Writing style

Systems-oriented, performance-aware, accessibility-conscious, operationally rigorous. Avoid framework marketing, component-level implementation detail, and frontend trends without operational reasoning. The objective is a scalable, resilient frontend architecture — not just a working UI stack.
