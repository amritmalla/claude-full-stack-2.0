# implementations/mobile/flutter

Technology-specific execution skills for Flutter.

## Philosophy

Each Flutter skill speaks as a **senior Flutter engineer**. It generates production-ready code and configuration — it does not invent architectural decisions. [`architecture/mobile-architecture`](../../../architecture/mobile-architecture/SKILL.md) is the source of truth for platform strategy, DI container, state management approach, navigation hierarchy, offline behavior, and observability vendor. If a `mobile-architecture.md` is silent on a decision a skill needs, the skill pauses and raises an ADR candidate rather than guessing.

Skills map to exactly one archetype. Skills are additive — each extends the baseline the scaffold installs.

## Archetypes

| # | Archetype | Skill | Status |
|---|---|---|---|
| 1 | app-scaffold-and-runtime | [flutter-app-scaffold-and-runtime/SKILL.md](flutter-app-scaffold-and-runtime/SKILL.md) | ✓ authored |
| 2 | navigation-and-routing | [flutter-navigation-and-routing/SKILL.md](flutter-navigation-and-routing/SKILL.md) | ✓ authored |
| 3 | state-and-data-fetching | [flutter-state-and-data-fetching/SKILL.md](flutter-state-and-data-fetching/SKILL.md) | ✓ authored |
| 4 | design-system-and-accessibility | [flutter-design-system-and-accessibility/SKILL.md](flutter-design-system-and-accessibility/SKILL.md) | ✓ authored |
| 5 | performance-and-reliability | [flutter-performance-and-reliability/SKILL.md](flutter-performance-and-reliability/SKILL.md) | ✓ authored |

## What each archetype owns

| Archetype | Owns | Defers |
|---|---|---|
| app-scaffold-and-runtime | Project layout, flavors, layered error handling, observability seams, DI/session shell, CI signing scaffolding, platform-channel plumbing the shell installs once | Auth flow and token logic → state-and-data-fetching |
| navigation-and-routing | Route hierarchy, deep links / app links, back stack, auth-gate routing, OS-interruption state restoration | Token refresh → state-and-data-fetching |
| state-and-data-fetching | State wiring, network layer, caching, offline queue, token storage and refresh, push-notification delivery wiring, background sync | Route-level auth gates → navigation-and-routing |
| design-system-and-accessibility | Tokens, theming, components, a11y posture, i18n seam, permission-request UX | Layout decisions → navigation-and-routing |
| performance-and-reliability | Startup/frame budgets, memory/battery telemetry, profiling, crash-free-rate / ANR / graceful-degradation gates, CI gates | Observability vendor → mobile-architecture.md; error-handling code → app-scaffold-and-runtime |

## Upstream

All Flutter skills consume [`architecture/mobile-architecture`](../../../architecture/mobile-architecture/SKILL.md) as the primary upstream. [`architecture/security`](../../../architecture/security/SKILL.md) is the authority on auth provider, session model, and token strategy.

## Standards

All Flutter skills conform to:

- [security-standards](../../../../standards/security-standards/README.md) — no secrets in bundle or committed config.
- [observability-standards](../../../../standards/observability-standards/README.md) — crash, logging, and tracing seam wired.
- [deployment-standards](../../../../standards/deployment-standards/README.md) — env-agnostic build via Flutter flavor mechanism.
- [naming-conventions](../../../../standards/naming-conventions/README.md) — package, feature, and file naming.
