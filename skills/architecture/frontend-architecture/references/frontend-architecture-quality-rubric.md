# Frontend Architecture Quality Rubric

Load this before emitting `frontend-architecture.md`. Revise until each check passes or the unresolved gap is explicitly documented.

## Shell and routing

- [ ] Number of apps, deployment boundaries, and shared-shell strategy are explicit.
- [ ] Micro-frontend posture is justified or explicitly rejected as premature.
- [ ] Route hierarchy, layouts, ownership, and not-found/loading/error behavior are defined.

## Rendering

- [ ] Every route or route group names its rendering mode and the reason.
- [ ] Hydration behavior, freshness, and SEO posture are defined per route group.
- [ ] No CSR-by-default; SEO-critical routes are not client-only.

## State and data

- [ ] All four state tiers (server-cache, URL, ephemeral UI, durable client) are modeled or explicitly marked unused.
- [ ] No global store mixes server-cache and UI state.
- [ ] Every fetched dataset names fetch location, cache ownership, invalidation trigger, and failure behavior.
- [ ] Mutation flow, optimistic updates, and revalidation ownership are defined; no duplicated client/server fetching.

## Auth and security

- [ ] Token/session storage, refresh flow, route guards, and RBAC are defined.
- [ ] CSRF posture, XSS exposure, session expiration, silent refresh, logout propagation, and multi-tab behavior are addressed.
- [ ] No insecure token persistence; no auth hidden in client state.

## Design system, i18n, accessibility

- [ ] Design-system ownership boundary is explicit: tokens, primitives, compositions; no business logic in primitives.
- [ ] Internationalization defines locale routing, translation loading, RTL, and formatting/timezone handling where applicable.
- [ ] Accessibility posture names a WCAG level, keyboard/focus model, and a testing expectation; not delegated entirely to a component library.

## Performance, resilience, observability

- [ ] Performance budgets state numeric targets for LCP, INP, and JS bundle, plus breach actions and regression monitoring.
- [ ] Code-splitting boundaries, image/font strategy, and third-party script policy are defined; no bundle-size blindness.
- [ ] Real-time or offline features state failure fallback, reconnect, and reconciliation behavior.
- [ ] Client observability defines telemetry, sampling, session-replay posture, and PII redaction.

## Linkage and decisions

- [ ] `frontend-architecture.md` conforms to [architecture-schema](../../../../standards/architecture-schema/README.md): frontmatter complete, required sections present, conditional sections present or omitted with rationale.
- [ ] Every ADR candidate has Context, Decision, Consequences (including downsides), and Alternatives considered.
- [ ] No framework-specific component code, build config, or vendor SDK calls leaked into the architecture.
- [ ] At least one weak-architecture risk was surfaced, or the design's intentional simplicity was explained.

## Failure handling

If a check fails:

1. Identify the missing or weak decision.
2. Ask the user for clarification if it cannot be inferred from `system-design.md` or the PRD.
3. Revise `frontend-architecture.md` or the relevant ADR.
4. Keep unresolved questions explicit; do not hide them as assumptions.
