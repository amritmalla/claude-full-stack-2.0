# implementations/mobile

Technology-specific execution skills for mobile.

## Philosophy

Each mobile implementation skill speaks as a **senior mobile engineer** in a specific platform. It implements, hardens, or reviews — it does not invent architectural decisions. Architecture artifacts produced by `architecture/mobile-architecture`, `architecture/performance`, `architecture/security`, and `architecture/operations` are the source of truth; the implementation skill consumes them and emits app shells, navigation configuration, state and data-fetching wiring, design-system integration, and performance gates.

If an artifact is silent on a needed decision (DI container, state management approach, observability vendor, platform target), the implementation skill **pauses and raises an ADR candidate** against the upstream domain rather than guessing.

Skills are scoped, not monolithic. Each `SKILL.md`:

- declares its upstream architecture domain(s) and the standards it conforms to,
- requires the upstream artifact when scaffolding or generating new wiring, and runs standalone for review or hardening when the artifact does not yet exist,
- maps to exactly one of five canonical archetypes (below),
- emits concrete code, configuration, and CI gates — not prose-only deliverables.

## Archetypes

The five archetypes are derived mobile-first, not copied from the frontend layer. They survive a from-scratch decomposition of what a production mobile app actually needs: a runtime shell, a navigation graph, a data/state engine, a presentation system, and a runtime-budget gate. Three of them carry native-surface weight that has no web equivalent — navigation absorbs deep links and OS-interruption state restoration, data-and-state absorbs push delivery and background sync, design-system absorbs permission-request UX. The native device surface is therefore **distributed across these five** rather than given its own archetype (see below). Security, release, and observability *policy* stay upstream in the `architecture/*` domains; the implementation skills consume those decisions cross-cuttingly.

Every mobile implementation stack is expected to provide skills drawn from these five archetypes. Only those archetypes the architecture layer actually demands for that stack are produced — there is no fixed baseline.

| # | Archetype | What the skill produces | Primary upstream |
|---|---|---|---|
| 1 | **app-scaffold-and-runtime** | Production-ready app shell: project layout, platform configuration, flavor/environment handling, layered error handling, structured logging client, observability seams, DI and session provider baseline, CI signing scaffolding. Sets the **DI and session provider baseline** that downstream skills extend. | `mobile-architecture` |
| 2 | **navigation-and-routing** | Navigation hierarchy, route ownership, **deep-link / app-link handling**, back-stack behavior, auth-gate routing, **OS-interruption state restoration** (process death, backgrounding). Heavier than its frontend analogue: it owns the distributed device-navigation surface. | `mobile-architecture` (navigation architecture) |
| 3 | **state-and-data-fetching** | State management wiring (per `mobile-architecture.md` decision), network layer, caching and revalidation, offline queue, mutation and optimistic-update posture, **auth-token plumbing and refresh**, **push-notification delivery wiring, background sync**. | `mobile-architecture` (state model, offline/sync design) |
| 4 | **design-system-and-accessibility** | Design-system integration (tokens, theming, component library), accessibility posture (screen-reader, dynamic text, reduced motion, contrast, RTL), internationalization seam, **permission-request UX**. | `mobile-architecture` (a11y posture, design-system seam) |
| 5 | **performance-and-reliability** | Startup and frame budgets, memory and battery/power telemetry, profiling gates, background-execution discipline, performance-regression CI gates, **plus crash-free-rate, ANR/watchdog budgets, and graceful-degradation posture as gated runtime metrics** (error-handling *code* stays in app-scaffold-and-runtime). | `performance` + `mobile-architecture` (performance, battery, and reliability budgets) |

### Auth is cross-cutting

There is no dedicated auth archetype for mobile. Auth surface area is split across the existing five:

- **app-scaffold-and-runtime** — DI and session provider baseline (shell only); no token logic or route gates.
- **navigation-and-routing** — auth-gate routing, protected-route transitions, post-login redirect.
- **state-and-data-fetching** — token storage, refresh, request-side auth headers, logout state propagation.
- **design-system-and-accessibility** — accessible auth UIs (login, MFA, recovery flows).

Each mobile `SKILL.md` that touches an auth concern names the upstream `architecture/security` decisions it implements and pauses for an ADR candidate if those decisions are missing.

### Device & platform integration is distributed

There is no dedicated device/platform archetype. Native-bridge surface area — camera, GPS, BLE, NFC, sensors, biometrics, push, background workers, permissions, platform channels, deep linking — is split across the existing five by the concern it actually serves:

- **navigation-and-routing** — deep linking, app links, OS-interruption state restoration.
- **state-and-data-fetching** — push-notification delivery wiring, background sync, background workers feeding the data layer.
- **design-system-and-accessibility** — permission-request UX (rationale prompts, denied/blocked states).
- **app-scaffold-and-runtime** — platform-channel plumbing and capability registration that the shell installs once.
- **cross-cutting (security)** — biometrics, secure storage, jailbreak/root detection: threaded into the touching archetype with policy from `architecture/security`.

A skill that implements a distributed device concern names the archetype boundary it is honoring and defers cleanly to the owning archetype rather than re-implementing it.

## Stacks

### Implemented

| Stack | Strategy | Archetype coverage |
|---|---|---|
| [flutter](flutter/) | Base — owns all 5 archetypes | 5/5 (all archetypes authored) |

### Planned (future scope)

| Stack | Strategy | Archetype coverage |
|---|---|---|
| react-native | Base — owns all 5 archetypes | 0/5 |
| ios | Native iOS (Swift/SwiftUI) — owns all 5 archetypes | 0/5 |
| android | Native Android (Kotlin/Compose) — owns all 5 archetypes | 0/5 |

## Standards every mobile implementation skill conforms to

- [security-standards](../../../standards/security-standards/README.md) — no secrets in bundle or committed config, signing via env vars or CI secret store, OWASP Mobile Top-10 client-side posture.
- [observability-standards](../../../standards/observability-standards/README.md) — crash reporting, structured logging, performance tracing seam wired with environment and flavor tags.
- [deployment-standards](../../../standards/deployment-standards/README.md) — env-agnostic build, flavor/environment separation, signing config not embedding credentials.
- [naming-conventions](../../../standards/naming-conventions/README.md) — app name, package name, feature and file naming.
