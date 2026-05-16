---
product: <kebab-case slug>          # matches the system-design / PRD slug
status: draft                       # draft | review | approved | superseded
owner: <name or role>
system_design: <relative path to source system-design.md>
prd: <relative path to source PRD, or null>
version: 0.1.0                      # semver
last_reviewed: YYYY-MM-DD
---

# Mobile Architecture: [Product or App Name]

## Executive Summary

[One paragraph: which mobile app(s) and platforms exist, primary user journeys, the API boundary consumed, what this architecture optimizes for (reliability, responsiveness, battery, recoverability, degraded-network usability), and what it intentionally does not do.]

## Platform Strategy

| Concern | Decision |
|---|---|
| Strategy | [native / cross-platform-native / hybrid] |
| Rationale & tradeoffs | [reasoning; rejected alternatives] |
| Supported platforms | [iOS / Android / ...] |
| Minimum OS versions | [versions] |
| Device classes | [phone / tablet / foldable] |
| Unsupported scenarios | [explicit] |

## Application Architecture

| Concern | Decision |
|---|---|
| Layers & module boundaries | [decision] |
| Feature isolation | [decision] |
| Shared services | [decision] |
| State ownership | [decision] |
| Side-effect handling | [decision] |
| Concurrency model | [decision] |
| Lifecycle handling | [decision] |
| Dependency injection | [approach] |

## Navigation Architecture

| Concern | Decision |
|---|---|
| Navigation hierarchy | [decision] |
| Route ownership | [decision] |
| Deep-link handling | [decision] |
| Modal strategy | [decision] |
| Auth transitions | [decision] |
| Tab / shell architecture | [decision] |
| Back-navigation & restoration | [behavior] |

## State Management Strategy

| State | Ownership | Mechanism | Sync | Persistence | Invalidation |
|---|---|---|---|---|---|
| Local UI | [owner] | [mechanism] | [rule] | [behavior] | [lifecycle] |
| Session | [owner] | [mechanism] | [rule] | [behavior] | [lifecycle] |
| Cached remote | [owner] | [mechanism] | [rule] | [behavior] | [lifecycle] |
| Persistent | [owner] | [mechanism] | [rule] | [behavior] | [lifecycle] |

Optimistic updates, conflict resolution, rollback, stale-data handling: [decisions].

## Offline & Synchronization Design

| Concern | Decision |
|---|---|
| Offline capabilities | [what works offline] |
| Synchronization model | [model] |
| Queueing & retry | [policy] |
| Conflict resolution | [rules] |
| Authoritative sources | [sources] |
| Reconciliation rules | [rules] |
| Degraded-mode behavior | [works / partially works / fails gracefully per journey] |

## Device Capability Integration

| Capability | Permission Strategy | Fallback | Privacy | Battery Impact | Failure Handling |
|---|---|---|---|---|---|
| [camera/location/...] | [strategy] | [behavior] | [posture] | [impact] | [handling] |

## Performance & Battery Budgets

| Metric | Target | Degradation Behavior |
|---|---|---|
| Cold start | [target] | [behavior] |
| Warm start | [target] | [behavior] |
| Screen transition latency | [target] | [behavior] |
| Memory usage | [budget] | [behavior under low memory] |
| Background execution | [budget] | [behavior] |
| Battery impact | [budget] | [behavior under battery saver] |
| Network utilization | [budget] | [behavior under poor connectivity] |
| Storage growth | [budget] | [behavior] |

## Security & Privacy Callouts

*Callout section — ownership belongs to [`security`](../../security/SKILL.md). Summarize mobile-specific concerns and raise ADR candidates; do not produce an owned security design here.*

| Concern | Callout / ADR Candidate |
|---|---|
| Auth / token handling | [summary → ADR NNNN] |
| Secure storage | [summary → ADR NNNN] |
| Jailbreak / root posture | [summary → ADR NNNN] |
| At-rest encryption | [summary → ADR NNNN] |
| Privacy manifests | [summary → ADR NNNN] |

## Accessibility & Localization

| Concern | Decision |
|---|---|
| Screen-reader support | [expectations] |
| Dynamic text / font scaling | [behavior] |
| Reduced motion | [behavior] |
| Color contrast | [expectations] |
| RTL support | [decision] |
| Internationalization | [constraints] |

## Notifications & Background Behavior

*Conditional — include when notifications or background work exist; otherwise list under Omitted sections.*

| Concern | Decision |
|---|---|
| Push types | [types] |
| Delivery expectations | [expectations] |
| Priority classes | [classes] |
| Background refresh | [behavior] |
| Routing / deep-link behavior | [behavior] |
| Opt-in & rate-limiting | [policy] |
| Silent-notification handling | [behavior] |

## Error Handling & Recovery

| Concern | Decision |
|---|---|
| Global error strategy | [strategy] |
| Retry behavior & ceilings | [policy] |
| Crash recovery | [behavior] |
| Interrupted-session handling | [behavior] |
| Partial-failure behavior | [behavior] |
| Degraded-mode UX | [experience] |

## Observability & Analytics

| Concern | Decision |
|---|---|
| Crash reporting | [tool / approach] |
| Performance telemetry | [signals] |
| Network tracing | [approach] |
| Journey / screen analytics | [signals] |
| Startup & battery telemetry | [signals] |
| Release monitoring | [approach] |
| Logging policy & PII redaction | [rules] |
| Sampling & retention | [policy] |

## Testing Strategy

| Concern | Decision |
|---|---|
| Unit / integration boundaries | [scope] |
| UI automation scope | [scope] |
| Offline testing | [strategy] |
| Device compatibility coverage | [matrix] |
| Accessibility testing | [scope] |
| Performance regression testing | [scope] |
| Emulator vs physical device | [expectations] |
| Release gating & rollback validation | [criteria] |

## Release & Operations Callouts

*Callout section — ownership belongs to [`operations`](../../operations/SKILL.md) / [`infrastructure-platform`](../../infrastructure-platform/SKILL.md). Summarize and raise ADR candidates; do not produce an owned release design here.*

| Concern | Callout / ADR Candidate |
|---|---|
| Release channels | [summary → ADR NNNN] |
| Staged rollout & rollback | [summary → ADR NNNN] |
| Store submission ownership | [summary → ADR NNNN] |
| Forced-upgrade policy | [summary → ADR NNNN] |
| Version support & deprecation | [summary → ADR NNNN] |

## Failure Taxonomy

| Failure | Detection | Mitigation | Recovery | Observability | User-facing Behavior |
|---|---|---|---|---|---|
| Startup failure | [d] | [m] | [r] | [o] | [b] |
| Network failure | [d] | [m] | [r] | [o] | [b] |
| Sync conflict | [d] | [m] | [r] | [o] | [b] |
| Rendering degradation | [d] | [m] | [r] | [o] | [b] |
| App termination | [d] | [m] | [r] | [o] | [b] |
| Permission denial | [d] | [m] | [r] | [o] | [b] |
| Notification delivery failure | [d] | [m] | [r] | [o] | [b] |
| API incompatibility | [d] | [m] | [r] | [o] | [b] |
| Storage exhaustion | [d] | [m] | [r] | [o] | [b] |
| Background execution failure | [d] | [m] | [r] | [o] | [b] |

## ADR Index

| ADR | Title | Status | Summary |
|---|---|---|---|
| NNNN | [title] | [proposed/accepted/...] | [summary] — links to `adrs/NNNN-<slug>.md` |

## Implementation Handoffs

### implementations/mobile/<ecosystem>

- [Platform, navigation, state, offline, and performance handoff notes]

### backend-architecture

- [API / sync / contract expectations]

### security

- [Mobile security/privacy callouts to be owned and resolved here]

### operations / infrastructure-platform

- [Release/signing/rollout callouts to be owned and resolved here]

### quality-engineering

- [Offline, accessibility, device-compatibility, and performance-regression testing expectations]

## Omitted sections

- [Conditional section name]: [one-line rationale for omission].

## Deferred Decisions

- [Decision, owner, deadline].
