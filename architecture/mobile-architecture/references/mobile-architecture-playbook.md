# Mobile Architecture Playbook

Load this when defining platform strategy, application/navigation architecture, state, offline/sync, device capabilities, performance, accessibility, notifications, error handling, observability, testing, or the failure taxonomy. It expands the operating rules and process steps in `SKILL.md` with the detail needed to produce `mobile-architecture.md`.

## Why this workflow exists

Design reliable, responsive, battery-efficient, recoverable, degraded-network-usable mobile architecture before platform implementation begins. It prevents platform-strategy regret, navigation/state chaos, brittle offline sync, permission and privacy surprises, battery and startup regressions, inaccessible interaction models, and unrecoverable releases.

The goal is not "how screens render" — it is predictable application structure, clear device/backend state ownership, resilient offline behavior, and safe user-facing behavior on constrained devices and unreliable networks.

## Behavioral rules in depth

### 1. Architect before choosing the platform strategy

Native vs cross-platform-native vs hybrid is an architectural decision driven by user reach, UX requirements, device-integration complexity, performance sensitivity, team expertise, release velocity, and long-term ownership cost. Never default to cross-platform without evaluating platform-specific UX, startup performance, memory constraints, animation requirements, offline complexity, and native API access. Record the decision as an ADR.

### 2. The app is a constrained distributed system

Assume unreliable networks, intermittent connectivity, limited battery, and abrupt termination. Define recovery and resumability up front, not as an afterthought.

### 3. State has ownership tiers

Distinguish local UI state, session state, cached remote state, and persistent storage. Each names ownership, synchronization rule, persistence behavior, and invalidation lifecycle. Reject implicit side effects and ambiguous device/backend ownership.

### 4. Offline and sync are explicit decisions

Define what works offline, what partially works, and what fails gracefully — per critical journey. Name authoritative sources, queueing, retry, conflict resolution, and reconciliation. Reject "offline later".

### 5. Device capabilities are contracts

Every camera/location/notification/biometric/sensor/background use names a permission strategy, fallback, privacy posture, battery impact, failure handling, and platform-specific limit. Reject capability use without a denial path.

### 6. Performance and battery are architectural budgets

Set numeric targets before implementation: cold/warm start, transition latency, memory, background, battery, network, storage. Define degradation under low memory, poor connectivity, thermal throttling, and battery saver. Reject background aggressiveness without measurable user value.

### 7. Accessibility is a baseline constraint

Define screen-reader support, dynamic text, reduced motion, contrast, RTL, and font scaling. Accessibility failures are architectural failures, not QA polish.

### 8. Security/privacy and release/operations are callouts, not owned

Summarize the mobile-specific concern and raise an ADR candidate; ownership stays with `security` and `operations`/`infrastructure-platform`. Do not produce an owned security or release design here.

### 9. Challenge weak architecture directly

Be operationally concrete and user-impact focused. Examples:

- "This cross-platform choice ignores the animation and startup requirements of the core flow."
- "Your sync model has no conflict-resolution rule for offline edits."
- "This capability has no permission-denied fallback."
- "Background refresh here has no measurable user value and a real battery cost."
- "Crash recovery for an interrupted purchase flow is undefined."

## Step detail

**Platform & product assessment (step 1).** Identify mobile journeys, supported platforms, device classes, latency-sensitive and offline-sensitive flows, notification-driven behaviors, session expectations, operational constraints.

**Platform strategy (step 2).** Evaluate native, cross-platform-native, hybrid. Document rationale, trade-offs, unsupported scenarios, minimum OS, device classes, tablet/foldable behavior. ADR candidate.

**Application architecture (step 3).** Layers, module boundaries, dependency ownership, feature isolation, shared services, state ownership, side effects, concurrency, lifecycle, DI. Avoid abstraction beyond current platform scope.

**Navigation architecture (step 4).** Hierarchy, route ownership, deep links, modals, auth transitions, tab/shell architecture, back-navigation and restoration after interruption.

**State management (step 5).** Local/session/cached/persistent state, sync ownership, optimistic updates, conflict resolution, rollback, stale-data handling, cache expiration.

**Offline & synchronization (step 6).** Offline capabilities, sync model, queueing, retry, conflict resolution, authoritative sources, reconciliation; explicit works/partial/fails-gracefully per journey.

**Device capability integration (step 7).** Per capability: permission strategy, fallback, privacy, battery impact, failure handling, platform-specific limits.

**Performance & battery (step 8).** Numeric budgets for start, latency, memory, background, battery, network, storage; degradation behavior under stress conditions.

**Security & privacy callouts (step 9).** Summarize auth/token/secure-storage/jailbreak/encryption/privacy-manifest concerns; raise ADR candidates; defer ownership to `security`.

**Accessibility & localization (step 10).** Screen reader, dynamic text, reduced motion, contrast, RTL, font scaling, i18n.

**Notifications & background (step 11).** Push types, delivery, priority, background refresh, routing, opt-in, rate-limiting, silent push; no background work without measurable value.

**Error handling & recovery (step 12).** Global error strategy, retry ceilings, crash recovery, interrupted-session handling, partial-failure behavior, degraded UX.

**Observability & analytics (step 13).** Crash, performance, network tracing, journey/screen analytics, startup/battery telemetry, release monitoring, logging policy, PII redaction, sampling, retention.

**Testing strategy (step 14).** Unit/integration/UI-automation/offline/device-compat/accessibility/perf-regression scope, emulator vs device, release gating, rollback validation.

**Release & operations callouts (step 15).** Summarize channels, staged rollout, store submission, forced-upgrade, deprecation; raise ADR candidates; defer ownership to `operations`/`infrastructure-platform`.

**Failure taxonomy (step 16).** Per failure: detection, mitigation, recovery, observability, user-facing behavior.

## Anti-patterns to detect

Call these out explicitly when detected:

- Cross-platform-by-default without trade-off analysis
- Permanent-network assumption
- Implicit/ambiguous device-backend state ownership
- Offline behavior undefined for critical journeys
- Sync without conflict resolution
- Device capability without permission-denied fallback
- Background aggressiveness without measurable user value
- Startup/memory/battery blindness
- Accessibility deferred to QA
- Notifications without opt-in or rate-limiting
- Crash/interrupted-session recovery undefined
- Owned security or release design instead of callouts
- Vendor SDK detail leaking into architecture
- Premature optimization for unsupported platforms

## Writing style

Systems-oriented, reliability- and battery-aware, accessibility-conscious, operationally rigorous. Avoid framework marketing, screen-level implementation detail, and vendor SDK specifics without operational reasoning. The objective is a resilient mobile architecture — not a working app stack.
