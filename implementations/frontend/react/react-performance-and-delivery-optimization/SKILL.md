---
name: react-performance-and-delivery-optimization
description: Use when defining, reviewing, or hardening the performance and delivery posture of a React app against Web Vitals budgets after the other react archetypes exist and performance architecture has set per-route budgets. Produces per-route performance budgets, code-splitting and lazy-loading topology, image and font posture, third-party-script audit, Web Vitals instrumentation (LCP/CLS/INP/TTFB), Lighthouse and bundle-analyzer CI gates, and CDN/edge cache-control posture. Do not use for app scaffolding, routing topology, state or data-fetching wiring, or design-system and accessibility work; use the other react archetype skills instead.
---

# React Performance and Delivery Optimization

## When to use

Invoke when establishing performance budgets and delivery optimization for a React app, when translating `performance-architecture.md` per-route budgets into code-splitting/asset/CI posture, or when remediating a Web Vitals regression.

Do not use for: scaffolding (use `react-app-scaffold-and-runtime`), route topology (use `react-routing-and-rendering-strategy`), state/data fetching (use `react-state-management-and-data-fetching`), or design-system/a11y (use `react-design-system-and-accessibility`). For one-off profiling of a single component, that is engineering work, not this architecture-driven skill.

## Inputs

Required:

- The other react archetypes exist (scaffold provides `web-vitals` RUM wiring; routing provides the route segments to split along).
- Approved `performance-architecture.md` with per-route or per-journey budgets: LCP, CLS, INP, TTFB targets and the JS bundle budget, plus the measurement point.

Optional:

- `frontend-architecture.md` rendering decisions (CSR-only here; SSR routes are nextjs).
- Current Lighthouse/RUM data and bundle analysis.
- CDN/edge platform and its cache-control capabilities.
- Third-party script inventory (analytics, tag managers, widgets).
- Device/network target profile from the architecture.

## Operating rules

- Consume the budgets; do not invent them. Per-route LCP/CLS/INP/TTFB and bundle budgets come from `performance-architecture.md`. If a budget for a route under work is missing, pause and raise an ADR candidate against `performance` — do not optimize to an invented target.
- Web Vitals are the gate; synthetic metrics supplement, never replace. The pass/fail is route-level LCP, CLS, INP, TTFB measured at the architecture's measurement point. Bundle-size and Lighthouse gates are supplementary signals, not the primary contract.
- Measure before and after. Every optimization cites a before metric (RUM or Lighthouse on a representative profile) and a re-measured after; no change is justified by intuition.
- Code-split along route segments first, coordinated with the routing skill's boundaries. Component-level lazy-loading is for heavy below-the-fold or interaction-gated UI, each justified. No blanket lazy-everything.
- Images and fonts are the usual LCP/CLS drivers: explicit dimensions or aspect-ratio to prevent CLS, responsive `srcset`/`sizes`, lazy-loading below the fold, prioritized LCP image, and self-hosted or preconnected fonts with `font-display: swap` and a preloaded critical font.
- Every third-party script is audited and justified against its budget cost: load strategy (defer/async/on-interaction/web-worker), failure isolation, and a stated INP/TTFB cost. A script with no owner and no budget justification is removed.
- Long tasks and INP are first-class: identify hydration/handler/render long tasks, apply transition/`useDeferredValue`/memoization only where measured to help, and avoid premature memoization that adds complexity without a measured win.
- CI enforces the gate: a Lighthouse-CI (or RUM-threshold) check and a bundle-budget check fail the build on regression past the architecture's budget; the thresholds are the architecture's numbers, not arbitrary.
- CDN/edge delivery posture is explicit: immutable hashed assets with long max-age, HTML with correct revalidation, compression (brotli), and preconnect/preload for critical origins — without redesigning the platform CDN (consumed from `infrastructure-platform`).
- If meeting a budget requires server rendering the route, that is a `nextjs`-stack handoff, not a CSR workaround; state it rather than degrading UX to hit a number.

## Output contract

The performance and delivery implementation MUST conform to:

- [observability-standards](../../../../standards/observability-standards/README.md) — Web Vitals are reported via RUM with route attribution; regressions are observable, not discovered manually.
- [deployment-standards](../../../../standards/deployment-standards/README.md) — hashed immutable assets, env-agnostic build, correct cache-control; CI gate runs in the pipeline.
- [security-standards](../../../../standards/security-standards/README.md) — third-party scripts respect CSP; no optimization weakens CSP or introduces an unvetted origin.
- [naming-conventions](../../../../standards/naming-conventions/README.md) — chunk and asset naming.

Upstream contract: `performance-architecture.md` is the source of truth for per-route Web Vitals and bundle budgets and the measurement point. `infrastructure-platform` owns the CDN substrate (consumed, not redesigned). If a needed budget is missing, pause and raise an ADR candidate against `performance`. Routes that can only meet budget via SSR are handed to the `nextjs` stack.

## Process

1. Load per-route Web Vitals and bundle budgets and the measurement point from `performance-architecture.md`. Confirm the scaffold's `web-vitals` RUM wiring and the routing segments exist. If a budget for an in-scope route is missing, pause and escalate.
2. Establish the baseline: capture current LCP/CLS/INP/TTFB (RUM or Lighthouse on the architecture's device/network profile) and a bundle analysis per route. Record the gap to budget per route.
3. Design the code-splitting topology: route-level `lazy`/`Suspense` boundaries aligned with the routing skill's segments; identify heavy below-the-fold/interaction-gated components for component-level splitting with justification. Eliminate unjustified eager bundles.
4. Optimize LCP: identify the LCP element per route, prioritize/preload it, fix render-blocking resources, and ensure the critical path (critical CSS, font) is minimal.
5. Optimize CLS: enforce explicit dimensions/aspect-ratio on media and ad/embed slots, reserve space for async UI, and avoid layout-shifting late content injection.
6. Optimize INP: profile interaction long tasks, apply `startTransition`/`useDeferredValue`/targeted memoization only where measured to help, and reduce hydration/handler cost; remove premature memoization with no measured benefit.
7. Image and font posture: responsive `srcset`/`sizes`, lazy below-the-fold, dimensioned media, self-hosted/preconnected fonts with `font-display: swap` and a preloaded critical font.
8. Third-party audit: inventory every external script, assign an owner, state its budget cost, choose a load strategy (defer/async/on-interaction/worker) and failure isolation; remove unjustified scripts; confirm CSP compatibility.
9. CDN/edge delivery: immutable hashed assets with long max-age, HTML revalidation policy, brotli compression, and preconnect/preload for critical origins — using `infrastructure-platform`'s CDN, not a redesign.
10. CI gates: wire Lighthouse-CI (or a RUM-threshold check) and a bundle-budget check with the architecture's numbers as thresholds, failing the build on regression. Wire RUM route-attributed Web Vitals reporting through the scaffold sink.
11. Re-measure: capture after metrics on the same profile per route, confirm movement to within budget, and record any route that cannot meet budget under CSR (raise the `nextjs` handoff).
12. Validate against [observability-standards](../../../../standards/observability-standards/README.md), [deployment-standards](../../../../standards/deployment-standards/README.md), [security-standards](../../../../standards/security-standards/README.md), and [naming-conventions](../../../../standards/naming-conventions/README.md). Revise until all pass or document the gap.

## Outputs

Required:

- Per-route performance budget sheet (from architecture) with measured before/after LCP/CLS/INP/TTFB and bundle size.
- Code-splitting topology: route-level boundaries and justified component-level splits.
- Image and font posture implementation.
- Third-party script audit: per script — owner, budget cost, load strategy, failure isolation, keep/remove decision.
- CI gate configuration: Lighthouse-CI/RUM-threshold + bundle-budget, with the architecture's thresholds.
- RUM Web Vitals reporting with route attribution through the scaffold sink.
- CDN/edge cache-control posture.

Output rules:

- Every optimization cites a measured before and after on the architecture's profile.
- Web Vitals are the primary gate; bundle/Lighthouse are supplementary.
- No optimization invents a budget or weakens CSP/UX to hit a number.
- Routes needing SSR to pass are documented `nextjs` handoffs, not CSR workarounds.

## Quality checks

- [ ] Per-route Web Vitals and bundle budgets are sourced from `performance-architecture.md` (or an ADR candidate is raised).
- [ ] Baseline and post-change metrics are captured on the architecture's device/network profile per route.
- [ ] Code-splitting follows route segments; component-level splits are individually justified; no blanket lazy-loading.
- [ ] LCP element per route is identified and prioritized; render-blocking critical path is minimized.
- [ ] Media and async slots are dimensioned; CLS budget is met per route.
- [ ] INP optimizations (transitions/deferral/memoization) are applied only where measured to help; no premature memoization.
- [ ] Fonts use `font-display: swap` with a preloaded critical font; images use responsive `srcset` and lazy-load below the fold.
- [ ] Every third-party script has an owner, a stated budget cost, a load strategy, and CSP compatibility; unjustified scripts are removed.
- [ ] CI fails the build on Web Vitals/bundle regression past the architecture's thresholds.
- [ ] RUM reports route-attributed Web Vitals through the scaffold sink.
- [ ] CDN posture uses immutable hashed assets and correct cache-control without redesigning the platform CDN.
- [ ] Any route that cannot meet budget under CSR is documented as a `nextjs`-stack handoff.

## References

- Upstream: [`architecture/performance`](../../../../architecture/performance/SKILL.md), [`architecture/frontend-architecture`](../../../../architecture/frontend-architecture/SKILL.md), [`architecture/infrastructure-platform`](../../../../architecture/infrastructure-platform/SKILL.md) (CDN substrate, consumed).
- Builds on: [`react-app-scaffold-and-runtime`](../react-app-scaffold-and-runtime/SKILL.md) (`web-vitals` RUM seam), [`react-routing-and-rendering-strategy`](../react-routing-and-rendering-strategy/SKILL.md) (split boundaries).
- Coordinates with: [`react-state-management-and-data-fetching`](../react-state-management-and-data-fetching/SKILL.md), [`react-design-system-and-accessibility`](../react-design-system-and-accessibility/SKILL.md).
- Compatible patterns: [`microservices`](../../../../architecture-patterns/microservices/README.md), [`cqrs`](../../../../architecture-patterns/cqrs/README.md), [`real-time-systems`](../../../../architecture-patterns/real-time-systems/README.md).
