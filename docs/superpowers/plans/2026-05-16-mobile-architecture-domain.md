# mobile-architecture Domain Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Author the `architecture/mobile-architecture` domain skill at mature-sibling tier (SKILL.md + README + template + playbook + quality-rubric) and register its `mobile-architecture.md` artifact in `standards/architecture-schema`.

**Architecture:** Markdown-only authoring mirroring the `frontend-architecture` sibling exactly (section order, link style, schema-entry shape). Self-contained domain owning the mobile-native core plus state/perf/a11y; mobile security/privacy and release/ops are callout/ADR-candidate sections deferring to `security` and `operations`/`infrastructure-platform`. Standalone artifact (Approach A) with optional non-binding cross-references to `frontend-architecture.md`.

**Tech Stack:** Markdown only. Validation = SKILL_SPEC.md + documentation-standards (frontmatter `name`==dir, `description` starts "Use when" and ≤1024 chars and link/secret-free; SKILL.md ≤~200 lines, `##`-only headings, no `---` rules; repo-relative links resolve; schema cross-refs resolve) via PowerShell structural checks.

**Spec:** [docs/superpowers/specs/2026-05-16-mobile-architecture-domain-design.md](../specs/2026-05-16-mobile-architecture-domain-design.md)

**Execution environment:** Main checkout `D:\projects\claude-full-stack-2.0`, branch `master` (user opted out of worktrees). Commit directly to `master`. Use the PowerShell tool for all verification (Windows).

---

## File Structure

- Create `architecture/mobile-architecture/SKILL.md` — the imperative recipe (router of the 17-step process), ≤~200 lines.
- Create `architecture/mobile-architecture/README.md` — Purpose/Owns/Produces/Skills/Standards/Upstream/Downstream, `> Status: draft`.
- Create `architecture/mobile-architecture/assets/mobile-architecture.template.md` — the 18-section artifact scaffold (§9/§15 are callout sections).
- Create `architecture/mobile-architecture/references/mobile-architecture-playbook.md` — deep per-area enumerations + anti-patterns.
- Create `architecture/mobile-architecture/references/mobile-architecture-quality-rubric.md` — grouped checklists + Failure handling.
- Modify `standards/architecture-schema/README.md` — add the file-layout line and the `## \`mobile-architecture.md\`` entry (parallel to `frontend-architecture.md`).

Each file is independent content; tasks are ordered so cross-references resolve by the end (the SKILL.md links to its own references/assets and to the schema; the schema links back to the SKILL).

---

### Task 1: Create SKILL.md

**Files:**
- Create: `architecture/mobile-architecture/SKILL.md`

- [ ] **Step 1: Write the file with exactly this content**

Create `architecture/mobile-architecture/SKILL.md` with EXACTLY (UTF-8 no BOM; every `—` a literal em dash U+2014; `##`-only headings; no `---` horizontal rules in the body):

```markdown
---
name: mobile-architecture
description: Use when a product requires native or cross-platform-native mobile application architecture after an approved system design and before mobile implementation begins. Produces platform strategy, application and navigation architecture, state and offline/sync design, device-capability integration, performance and battery budgets, accessibility and localization, notifications and background behavior, error handling, observability, testing strategy, failure taxonomy, and implementation handoffs. Do not use for mobile-web or PWA (use frontend-architecture), backend service design (use backend-architecture), UI or visual design (use frontend-design), vendor-specific SDK implementation, deep mobile security (use security), or store-release and signing depth (use operations or infrastructure-platform).
---

# Mobile Architecture

## When to use

Invoke after `architecture/system-design` has approved a product that includes a native or cross-platform-native mobile application, and before `implementations/mobile/<ecosystem>` skills generate platform code. Covers iOS, Android, cross-platform-native (React Native / Flutter / KMP), hybrid, tablet/foldable, and companion apps.

Do not use when the product has no mobile client, for pure backend architecture (use [`backend-architecture`](../backend-architecture/SKILL.md)), for mobile-web or PWA (use [`frontend-architecture`](../frontend-architecture/SKILL.md)), for UI or visual design (use [`frontend-design`](../../implementations/frontend/frontend-design/SKILL.md)), for vendor-specific SDK implementation, or when the architecture is finalized and only implementation remains.

## Inputs

Required:

- Approved `system-design.md` and the relevant ADRs.
- Mobile product requirements and the primary user journeys.
- Supported platforms and minimum OS versions.
- Performance and offline expectations.

Optional:

- Backend / API contracts; identity and session model.
- Design system or UX guidelines; accessibility requirements.
- Analytics, notification, and device-capability requirements.
- Security / compliance constraints; release cadence; regional constraints.
- The product's `frontend-architecture.md` (optional, non-binding cross-reference for shared concerns).

## Operating rules

- Treat the mobile app as a constrained distributed system: assume unreliable networks, intermittent connectivity, limited battery, and abrupt termination; design for recovery and resumability.
- Architect before choosing native vs cross-platform-native vs hybrid; the platform-target decision is an ADR, not a prescription, and is never defaulted to cross-platform without evaluating UX, startup, memory, animation, offline, and native-API trade-offs.
- Define device/backend state ownership explicitly; navigation, state, sync, and caching are first-class architectural concerns.
- Minimize background work unless product-critical; define degraded behavior explicitly for every critical journey.
- Native platform conventions take precedence over framework convenience; accessibility and responsiveness are mandatory architectural qualities.
- Mobile security/privacy and release/operations are callouts here, not owned: summarize the mobile-specific concern and raise an ADR candidate against `system-design`; ownership stays with `security` and `operations`/`infrastructure-platform`.
- No device feature without measurable user value; no premature optimization for unsupported platforms; no vendor SDK detail unless it materially changes architecture behavior.
- Mobile-web/PWA is out of scope and belongs to `frontend-architecture`.

## Output contract

`mobile-architecture.md` MUST conform to [standards/architecture-schema](../../standards/architecture-schema/README.md), which is authoritative for its frontmatter, the 18-section required/conditional structure, conditional-omission rules, the §9/§15 callout framing, and `system-design.md` traceability. Skill structure conforms to [documentation-standards](../../standards/documentation-standards/README.md). Use `assets/mobile-architecture.template.md` as the scaffold. The artifact is independently valid without a `frontend-architecture.md`; cross-references to it are optional and non-binding.

## Progressive references

- Read `references/mobile-architecture-playbook.md` when defining any owned area or checking the anti-pattern list.
- Read `references/mobile-architecture-quality-rubric.md` before finalizing and use it as the validation checklist.
- Use `assets/mobile-architecture.template.md` for `mobile-architecture.md`.

## Process

ADR candidates are drafted inline as decisions are made (notably the platform-target decision and the §9/§15 callouts). The final step consolidates them; it does not retrofit ADRs from prose.

- [ ] Step 1: Load `system-design.md` and relevant ADRs. Identify mobile surfaces, user journeys, supported platforms, device capabilities, network/session assumptions, and operational constraints; mark latency-sensitive and offline-sensitive flows.
- [ ] Step 2: Decide platform strategy (native vs cross-platform-native vs hybrid). Document rationale, trade-offs, unsupported scenarios, minimum OS, device classes, tablet/foldable behavior. Draft an ADR candidate for the platform-target decision.
- [ ] Step 3: Define application architecture: layers, module boundaries, dependency ownership, feature isolation, shared services, state ownership, side-effect handling, concurrency model, lifecycle, dependency injection. Avoid over-abstraction beyond current platform scope.
- [ ] Step 4: Define navigation architecture: hierarchy, route ownership, deep-link handling, modal strategy, auth transitions, tab/shell architecture, back-navigation and state restoration after interruption.
- [ ] Step 5: Define state management: local UI, session, cached remote, persistent storage, synchronization ownership, optimistic updates, conflict resolution, rollback, stale-data handling, cache expiration.
- [ ] Step 6: Define offline & synchronization architecture: offline capabilities, sync model, queueing, retry, conflict resolution, authoritative sources, reconciliation; state explicitly what works offline, what partially works, and what fails gracefully.
- [ ] Step 7: Define device-capability integration: per capability state permission strategy, fallback behavior, privacy expectations, battery impact, failure handling, and platform-specific limits.
- [ ] Step 8: Define performance & battery budgets: cold/warm start, transition latency, interaction responsiveness, memory, background execution, battery, network, storage growth; degradation under low memory, poor connectivity, thermal throttling, and battery-saver.
- [ ] Step 9: Security & privacy callouts: summarize mobile-specific auth/token/secure-storage/jailbreak/encryption concerns and draft ADR candidates. Defer ownership to [`security`](../security/SKILL.md); do not produce an owned security design here.
- [ ] Step 10: Define accessibility & localization: screen-reader support, dynamic text, reduced motion, color contrast, RTL, font scaling, internationalization. Accessibility failures are architectural failures.
- [ ] Step 11: Define notifications & background behavior: push types, delivery expectations, priority classes, background refresh, routing, opt-in, rate-limiting, silent notifications. No background execution without measurable user value.
- [ ] Step 12: Define error handling & recovery: global error strategy, retry ceilings, crash recovery, interrupted-session handling, partial-failure behavior, degraded-mode UX.
- [ ] Step 13: Define observability & analytics: crash reporting, performance telemetry, network tracing, journey/screen analytics, startup and battery telemetry, release monitoring, logging policy, PII redaction, sampling, retention.
- [ ] Step 14: Define testing strategy: unit/integration/UI-automation/offline/device-compat/accessibility/performance-regression scope, emulator vs physical-device expectations, release gating, rollback validation.
- [ ] Step 15: Release & operations callouts: summarize channels, staged rollout, store submission, forced-upgrade, deprecation as ADR candidates. Defer ownership to [`operations`](../operations/SKILL.md) / [`infrastructure-platform`](../infrastructure-platform/SKILL.md).
- [ ] Step 16: Define the failure taxonomy: startup, network, sync conflict, rendering degradation, termination, permission denial, notification failure, API incompatibility, storage exhaustion, background failure; per failure define detection, mitigation, recovery, observability, and user-facing behavior.
- [ ] Step 17: Generate `mobile-architecture.md` from `assets/mobile-architecture.template.md`. Consolidate ADR candidates (numbering, status, alternatives, downsides). Validate against [standards/architecture-schema](../../standards/architecture-schema/README.md) and `references/mobile-architecture-quality-rubric.md`; revise until both pass or explicitly note any unresolved gap.

## Outputs

Required:

- `mobile-architecture.md` at `docs/architecture/<product-slug>/mobile-architecture.md`, with frontmatter and the 18-section structure per [standards/architecture-schema](../../standards/architecture-schema/README.md).

Optional, when applicable:

- Navigation diagrams; state-ownership maps; offline-sync diagrams; notification-routing diagrams.
- Performance-budget tables; failure-mode matrices; ADR drafts.

Output rules:

- Keep the architecture decision-oriented and user-impact focused, not framework-decorative.
- Document tradeoffs and the rejected alternative, not only the chosen path.
- Keep security/privacy and release/operations as callouts and ADR candidates, never owned designs.
- No vendor SDK detail unless it materially changes architecture behavior.

## Quality checks

- [ ] `references/mobile-architecture-quality-rubric.md` was loaded before finalizing.
- [ ] `mobile-architecture.md` validates against [standards/architecture-schema](../../standards/architecture-schema/README.md): frontmatter complete; required sections present; conditional sections present with content or listed under `## Omitted sections` with rationale.
- [ ] Platform strategy records rationale and trade-offs as an ADR candidate.
- [ ] Navigation ownership and state-restoration behavior are defined.
- [ ] State ownership and synchronization rules are explicit.
- [ ] Offline behavior is defined for every critical user journey.
- [ ] Device-capability usage names a permission strategy, privacy posture, and fallback.
- [ ] Performance and battery budgets state measurable targets and degradation behavior.
- [ ] Accessibility posture is explicitly documented.
- [ ] Notification and interruption policies are documented.
- [ ] Error handling and degraded behavior are defined.
- [ ] Observability includes crash, latency, and release telemetry with PII redaction.
- [ ] Testing covers offline, accessibility, and device compatibility.
- [ ] Security/privacy and release/operations appear only as callouts / ADR candidates, not owned designs.
- [ ] No vendor SDK implementation detail appears unless it materially changes architecture behavior.

## References

- Upstream: [`architecture/system-design`](../system-design/SKILL.md).
- Related: [`backend-architecture`](../backend-architecture/SKILL.md), [`security`](../security/SKILL.md) (mobile security callouts), [`operations`](../operations/SKILL.md) / [`infrastructure-platform`](../infrastructure-platform/SKILL.md) (release/signing callouts), [`performance`](../performance/SKILL.md), [`quality-engineering`](../quality-engineering/SKILL.md), [`frontend-architecture`](../frontend-architecture/SKILL.md) (optional shared cross-reference; mobile-web/PWA boundary).
- Downstream implementation skills: future `implementations/mobile/<ecosystem>` (e.g. `ios`, `android`, `cross-platform`).
```

- [ ] **Step 2: Verify frontmatter, length, headings, no `---` rules**

PowerShell tool:
```
$f='architecture/mobile-architecture/SKILL.md'
Get-Content $f | Select-String '^name:'
$d=(Get-Content $f | Select-String '^description: ').ToString()
"starts-ok=$($d -like 'description: Use when*') desc-len=$($d.Length) lines=$((Get-Content $f).Count) dir=$(Split-Path (Split-Path $f -Parent) -Leaf)"
"no-link=$(-not ($d -match '\]\('))  no-secret=$(-not ($d -match 'X-Goog-Api-Key|AQ\.'))"
$body = Get-Content $f | Select-Object -Skip 4
"body-hr-count=$(@($body | Select-String '^---\s*$').Count)"
```
Expected: `name: mobile-architecture`; `starts-ok=True`; `desc-len` < 1024; `lines` ≤ 210; `dir=mobile-architecture`; `no-link=True  no-secret=True`; `body-hr-count=0`.

- [ ] **Step 3: Verify section set/order**

PowerShell tool:
```
(Get-Content architecture/mobile-architecture/SKILL.md | Select-String '^## ').Line
```
Expected, in order: `## When to use`, `## Inputs`, `## Operating rules`, `## Output contract`, `## Progressive references`, `## Process`, `## Outputs`, `## Quality checks`, `## References` (9 headings).

- [ ] **Step 4: Verify repo-relative links resolve**

PowerShell tool:
```
Push-Location architecture/mobile-architecture
$paths = '../system-design/SKILL.md','../backend-architecture/SKILL.md','../security/SKILL.md','../operations/SKILL.md','../infrastructure-platform/SKILL.md','../performance/SKILL.md','../quality-engineering/SKILL.md','../frontend-architecture/SKILL.md','../../implementations/frontend/frontend-design/SKILL.md','../../standards/architecture-schema/README.md','../../standards/documentation-standards/README.md'
foreach ($p in $paths) { "$p => $(Test-Path $p)" }
Pop-Location
```
Expected: every line `=> True`. (`references/` and `assets/` targets are created in later tasks; they are NOT linked with on-disk-checked relative paths here other than by name — do not assert them in this step.)

- [ ] **Step 5: Commit**

```
git add architecture/mobile-architecture/SKILL.md
git commit -m "feat(mobile): add mobile-architecture domain SKILL.md

Mature-sibling-tier domain skill: native/cross-platform-native mobile
architecture after system-design. Self-contained (owns platform/app/
nav/state/offline/perf/a11y); security/privacy and release/ops are
callout/ADR-candidate steps deferring to security and operations.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 2: Create README.md

**Files:**
- Create: `architecture/mobile-architecture/README.md`

- [ ] **Step 1: Write the file with exactly this content**

Create `architecture/mobile-architecture/README.md` with EXACTLY (UTF-8 no BOM):

```markdown
# mobile-architecture

> Status: draft

## Purpose

Defines mobile application architecture from an approved system design: platform strategy, application and navigation architecture, state and offline/sync design, device-capability integration, performance and battery budgets, accessibility and localization, notifications and background behavior, error handling and recovery, observability, testing strategy, and a failure taxonomy.

Technology-agnostic and framework-agnostic first. Covers native (iOS/Android) and cross-platform-native (React Native, Flutter, KMP). Mobile-web and PWA are out of scope and belong to [`frontend-architecture`](../frontend-architecture/README.md). Deep mobile security/privacy and store-release/signing are not owned here — they are raised as callouts and ADR candidates and owned by [`security`](../security/SKILL.md) and [`operations`](../operations/SKILL.md) / [`infrastructure-platform`](../infrastructure-platform/SKILL.md).

## Owns

- Platform-target strategy (native vs cross-platform-native vs hybrid) as an ADR
- Application architecture and module boundaries
- Navigation architecture and state restoration
- State management and cache ownership
- Offline-first and synchronization strategy
- Device-capability integration and permission posture
- Performance and battery budgets
- Accessibility and localization
- Notifications and background behavior
- Error handling, recovery, and the failure taxonomy
- Observability and analytics posture
- Testing strategy

Not owned (callouts only): mobile security/privacy design, store-release/signing/rollout.

## Produces

| Artifact | Conforms to |
|---|---|
| `mobile-architecture.md` | [architecture-schema](../../standards/architecture-schema/README.md), [documentation-standards](../../standards/documentation-standards/README.md) |
| ADR drafts (platform target, offline/sync, security callouts, release callouts) | [architecture-schema](../../standards/architecture-schema/README.md) |

## Skills

- [mobile-architecture](SKILL.md) - turns an approved system design into mobile application architecture: platform strategy, app and navigation architecture, state, offline/sync, device capabilities, performance and battery, accessibility, notifications, error handling, observability, testing, failure taxonomy, and implementation handoffs.

## Standards this architecture domain conforms to

- [architecture-schema](../../standards/architecture-schema/README.md) - `mobile-architecture.md` artifact structure and system-design traceability.
- [security-standards](../../standards/security-standards/README.md) - mobile security/privacy callout posture.
- [observability-standards](../../standards/observability-standards/README.md) - mobile telemetry and crash/latency signals.
- [deployment-standards](../../standards/deployment-standards/README.md) - release/rollout callout posture.
- [documentation-standards](../../standards/documentation-standards/README.md) - skill structure.

## Upstream inputs

Requires an approved `system-design.md` per [architecture-schema](../../standards/architecture-schema/README.md) whose design includes a native or cross-platform-native mobile surface. Bounded contexts, component interfaces, API boundaries, and ADRs shape the mobile architecture produced here.

## Downstream consumers

Mobile architecture produced here is the source of truth for:

- Future `implementations/mobile/<ecosystem>` - iOS, Android, and cross-platform-native skills follow platform, navigation, state, offline, and performance decisions.
- [architecture/security](../security/SKILL.md) - owns the mobile security/privacy decisions raised here as callouts.
- [architecture/operations](../operations/SKILL.md) / [architecture/infrastructure-platform](../infrastructure-platform/SKILL.md) - own the release/signing/rollout decisions raised here as callouts.
- [architecture/performance](../performance/SKILL.md) - performance and battery budget enforcement.
```

- [ ] **Step 2: Verify status, headings, links**

PowerShell tool:
```
$f='architecture/mobile-architecture/README.md'
(Get-Content $f | Select-String '^> Status:').Line
(Get-Content $f | Select-String '^## ').Line
Push-Location architecture/mobile-architecture
foreach ($p in '../frontend-architecture/README.md','../security/SKILL.md','../operations/SKILL.md','../infrastructure-platform/SKILL.md','../../standards/architecture-schema/README.md','../../standards/security-standards/README.md','../../standards/observability-standards/README.md','../../standards/deployment-standards/README.md','../../standards/documentation-standards/README.md','SKILL.md') { "$p => $(Test-Path $p)" }
Pop-Location
```
Expected: `> Status: draft`; headings `## Purpose`, `## Owns`, `## Produces`, `## Skills`, `## Standards this architecture domain conforms to`, `## Upstream inputs`, `## Downstream consumers`; every link `=> True` (SKILL.md exists from Task 1).

- [ ] **Step 3: Commit**

```
git add architecture/mobile-architecture/README.md
git commit -m "feat(mobile): add mobile-architecture README

Purpose/Owns/Produces/Skills/Standards/Upstream/Downstream, Status:
draft. Notes security/privacy and release/ops are callouts owned by
their domains.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 3: Create assets/mobile-architecture.template.md

**Files:**
- Create: `architecture/mobile-architecture/assets/mobile-architecture.template.md`

- [ ] **Step 1: Write the file with exactly this content**

Create `architecture/mobile-architecture/assets/mobile-architecture.template.md` with EXACTLY (UTF-8 no BOM; the leading `---`/`---` is YAML frontmatter and is intended; no other `---` rules):

```markdown
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
```

- [ ] **Step 2: Verify the 18 sections + frontmatter**

PowerShell tool:
```
$f='architecture/mobile-architecture/assets/mobile-architecture.template.md'
(Get-Content $f)[0]
$h=(Get-Content $f | Select-String '^## ').Line
$h
"count=$($h.Count)"
```
Expected: line 1 is `---`; the `## ` headings are exactly, in order: `## Executive Summary`, `## Platform Strategy`, `## Application Architecture`, `## Navigation Architecture`, `## State Management Strategy`, `## Offline & Synchronization Design`, `## Device Capability Integration`, `## Performance & Battery Budgets`, `## Security & Privacy Callouts`, `## Accessibility & Localization`, `## Notifications & Background Behavior`, `## Error Handling & Recovery`, `## Observability & Analytics`, `## Testing Strategy`, `## Release & Operations Callouts`, `## Failure Taxonomy`, `## ADR Index`, `## Implementation Handoffs`, `## Omitted sections`, `## Deferred Decisions`; `count=20` (18 content sections + Omitted + Deferred, matching the frontend template's trailing two).

- [ ] **Step 3: Verify callout sections name their owning domain**

PowerShell tool:
```
$f='architecture/mobile-architecture/assets/mobile-architecture.template.md'
"sec9-callout=$([bool](Select-String -Path $f -Pattern 'Security & Privacy Callouts'))"
"sec15-callout=$([bool](Select-String -Path $f -Pattern 'Release & Operations Callouts'))"
"defers-security=$([bool](Select-String -Path $f -Pattern 'ownership belongs to \[`security`\]'))"
"defers-ops=$([bool](Select-String -Path $f -Pattern 'ownership belongs to \[`operations`\]'))"
```
Expected: all four `=True`.

- [ ] **Step 4: Commit**

```
git add architecture/mobile-architecture/assets/mobile-architecture.template.md
git commit -m "feat(mobile): add mobile-architecture artifact template

18-section scaffold; Security & Privacy and Release & Operations are
callout sections deferring ownership to security and operations.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 4: Create references/mobile-architecture-playbook.md

**Files:**
- Create: `architecture/mobile-architecture/references/mobile-architecture-playbook.md`

- [ ] **Step 1: Write the file with exactly this content**

Create `architecture/mobile-architecture/references/mobile-architecture-playbook.md` with EXACTLY (UTF-8 no BOM):

```markdown
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
```

- [ ] **Step 2: Verify structure and link**

PowerShell tool:
```
$f='architecture/mobile-architecture/references/mobile-architecture-playbook.md'
(Get-Content $f | Select-String '^## ').Line
"lines=$((Get-Content $f).Count)"
```
Expected headings: `## Why this workflow exists`, `## Behavioral rules in depth`, `## Step detail`, `## Anti-patterns to detect`, `## Writing style` (mirrors the frontend playbook section set); `lines` > 60.

- [ ] **Step 3: Commit**

```
git add architecture/mobile-architecture/references/mobile-architecture-playbook.md
git commit -m "feat(mobile): add mobile-architecture playbook

Deep per-area enumerations, behavioral rules, step detail, and an
anti-pattern list; security/release framed as callouts.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 5: Create references/mobile-architecture-quality-rubric.md

**Files:**
- Create: `architecture/mobile-architecture/references/mobile-architecture-quality-rubric.md`

- [ ] **Step 1: Write the file with exactly this content**

Create `architecture/mobile-architecture/references/mobile-architecture-quality-rubric.md` with EXACTLY (UTF-8 no BOM):

```markdown
# Mobile Architecture Quality Rubric

Load this before emitting `mobile-architecture.md`. Revise until each check passes or the unresolved gap is explicitly documented.

## Platform & application

- [ ] Platform strategy (native / cross-platform-native / hybrid) has rationale, trade-offs, and rejected alternatives, recorded as an ADR.
- [ ] Minimum OS versions and device classes (phone/tablet/foldable) are explicit.
- [ ] Application layers, module boundaries, concurrency, and lifecycle handling are defined without over-abstraction.

## Navigation & state

- [ ] Navigation hierarchy, route ownership, deep-link handling, and state restoration after interruption are defined.
- [ ] Local, session, cached-remote, and persistent state each name ownership, sync rule, persistence, and invalidation.
- [ ] Optimistic updates, conflict resolution, and rollback behavior are defined.

## Offline & device

- [ ] Offline behavior is defined for every critical user journey (works / partially works / fails gracefully).
- [ ] Sync model names authoritative sources, queueing, retry, conflict resolution, and reconciliation.
- [ ] Every device capability names permission strategy, fallback, privacy posture, battery impact, and failure handling.

## Performance, accessibility, notifications

- [ ] Performance and battery budgets state measurable targets and degradation behavior under low memory, poor connectivity, thermal throttling, and battery saver.
- [ ] Accessibility posture names screen-reader support, dynamic text, reduced motion, contrast, RTL, and font scaling.
- [ ] Notification and interruption policies (types, delivery, priority, opt-in, rate-limiting, silent push) are documented where notifications exist.

## Resilience, observability, testing

- [ ] Error handling defines retry ceilings, crash recovery, interrupted-session handling, and degraded-mode UX.
- [ ] The failure taxonomy covers each named failure with detection, mitigation, recovery, observability, and user-facing behavior.
- [ ] Observability includes crash, latency, startup, and release telemetry with PII redaction and sampling.
- [ ] Testing covers offline, accessibility, and device-compatibility, with release gating and rollback validation.

## Callouts, linkage, decisions

- [ ] Security/privacy and release/operations appear only as callouts / ADR candidates — no owned security or release design.
- [ ] `mobile-architecture.md` conforms to [architecture-schema](../../../standards/architecture-schema/README.md): frontmatter complete, required sections present, conditional sections present or omitted with rationale.
- [ ] Every ADR candidate has Context, Decision, Consequences (including downsides), and Alternatives considered.
- [ ] No vendor SDK implementation detail leaked into the architecture unless it materially changes architecture behavior.
- [ ] At least one weak-architecture risk was surfaced, or the design's intentional simplicity was explained.

## Failure handling

If a check fails:

1. Identify the missing or weak decision.
2. Ask the user for clarification if it cannot be inferred from `system-design.md` or the PRD.
3. Revise `mobile-architecture.md` or the relevant ADR.
4. Keep unresolved questions explicit; do not hide them as assumptions.
```

- [ ] **Step 2: Verify structure and schema link resolves**

PowerShell tool:
```
$f='architecture/mobile-architecture/references/mobile-architecture-quality-rubric.md'
(Get-Content $f | Select-String '^## ').Line
Push-Location architecture/mobile-architecture/references
"schema=$(Test-Path '../../../standards/architecture-schema/README.md')"
Pop-Location
```
Expected headings: `## Platform & application`, `## Navigation & state`, `## Offline & device`, `## Performance, accessibility, notifications`, `## Resilience, observability, testing`, `## Callouts, linkage, decisions`, `## Failure handling`; `schema=True`.

- [ ] **Step 3: Commit**

```
git add architecture/mobile-architecture/references/mobile-architecture-quality-rubric.md
git commit -m "feat(mobile): add mobile-architecture quality rubric

Grouped binary checklists plus a Failure handling section, mirroring
the frontend-architecture rubric; enforces the security/release
callout-only rule.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 6: Register mobile-architecture.md in architecture-schema

**Files:**
- Modify: `standards/architecture-schema/README.md` (file-layout block ~line 11–12; insert a new entry before `## \`platform-architecture.md\``)

- [ ] **Step 1: Add the file-layout line**

In `standards/architecture-schema/README.md`, find this exact line (currently line 11):

`├── frontend-architecture.md   # OPTIONAL — only when the design has a user-facing frontend (see "frontend-architecture.md")`

Insert immediately AFTER it a new line:

`├── mobile-architecture.md     # OPTIONAL — only when the design has a native or cross-platform-native mobile app (see "mobile-architecture.md")`

(Do not alter any other line in the tree.)

- [ ] **Step 2: Insert the mobile-architecture.md schema entry**

In `standards/architecture-schema/README.md`, find this exact line (the start of the next entry, currently line 156):

`## \`platform-architecture.md\``

Insert immediately BEFORE it the following block, followed by a blank line:

```markdown
## `mobile-architecture.md`

Secondary artifact. Present only when `system-design.md` includes a native or cross-platform-native mobile application. Produced by [`architecture/mobile-architecture`](../../architecture/mobile-architecture/SKILL.md); consumed by `implementations/mobile/<ecosystem>`. One file per system. Mobile-web and PWA are not in scope here — those remain in `frontend-architecture.md`.

### Frontmatter (required)

```yaml
---
product: <kebab-case slug>         # matches the system-design slug
status: draft | review | approved | superseded
owner: <name or role>
system_design: <relative path to source system-design.md>
prd: <relative path to source PRD, or null>
version: <semver, starts at 0.1.0>
last_reviewed: YYYY-MM-DD
---
```

### Required sections

| Section | Purpose |
|---|---|
| `## Executive Summary` | Mobile app(s) and platforms present, primary user journeys, API boundary, what it optimizes for and intentionally does not. |
| `## Platform Strategy` | Native vs cross-platform-native vs hybrid with rationale, trade-offs, rejected alternatives, minimum OS, device classes. |
| `## Application Architecture` | Layers, module boundaries, state ownership, side effects, concurrency, lifecycle, dependency injection. |
| `## Navigation Architecture` | Hierarchy, route ownership, deep links, modals, auth transitions, tab/shell, back-navigation and restoration. |
| `## State Management Strategy` | Local/session/cached/persistent state: ownership, mechanism, sync, persistence, invalidation; optimistic updates and conflict resolution. |
| `## Offline & Synchronization Design` | Offline capabilities, sync model, queueing, retry, conflict resolution, authoritative sources, reconciliation, degraded-mode per journey. |
| `## Device Capability Integration` | Per capability: permission strategy, fallback, privacy, battery impact, failure handling, platform limits. |
| `## Performance & Battery Budgets` | Measurable targets (start, latency, memory, background, battery, network, storage) with degradation behavior. |
| `## Security & Privacy Callouts` | Callout only — mobile-specific security/privacy concerns summarized as ADR candidates; ownership belongs to `security`. |
| `## Accessibility & Localization` | Screen-reader support, dynamic text, reduced motion, contrast, RTL, font scaling, internationalization. |
| `## Error Handling & Recovery` | Global error strategy, retry ceilings, crash recovery, interrupted-session handling, degraded-mode UX. |
| `## Observability & Analytics` | Crash, performance, network, journey/screen, startup/battery telemetry, release monitoring, PII redaction, sampling, retention. |
| `## Testing Strategy` | Unit/integration/UI-automation/offline/device-compat/accessibility/perf-regression scope, release gating, rollback validation. |
| `## Release & Operations Callouts` | Callout only — release channels, staged rollout, store submission, forced-upgrade, deprecation as ADR candidates; ownership belongs to `operations`/`infrastructure-platform`. |
| `## Failure Taxonomy` | Per failure: detection, mitigation, recovery, observability, user-facing behavior. |
| `## Implementation Handoffs` | Explicit handoffs to `implementations/mobile/<ecosystem>`, `backend-architecture`, `security`, `operations`/`infrastructure-platform`, `quality-engineering`. |
| `## ADR Index` | Table: ADR number, Title, Status, Summary. Links to `adrs/NNNN-<slug>.md`. Shares the system's monotonic ADR numbering. |

### Conditional sections

Include if material; otherwise omit and add a one-line rationale under `## Omitted sections`.

| Section | When to include |
|---|---|
| `## Notifications & Background Behavior` | Push notifications or background work exist. Defines push types, delivery, priority, opt-in, rate-limiting, and silent-notification handling. |

`mobile-architecture.md` shares the system's ADR numbering, immutability rule, and supersede chain (see "ADRs"). It does not redefine bounded contexts, components, or data flow — those remain owned by `system-design.md`. It does not own security/privacy or release/operations design — those are callouts whose decisions are owned by `security` and `operations`/`infrastructure-platform`. Cross-references to a product's `frontend-architecture.md` are optional and non-binding; `mobile-architecture.md` is independently valid without one.
```

- [ ] **Step 3: Verify the edits**

PowerShell tool:
```
$f='standards/architecture-schema/README.md'
"layout-line=$([bool](Select-String -Path $f -Pattern '^├── mobile-architecture\.md'))"
"entry-present=$([bool](Select-String -Path $f -Pattern '^## `mobile-architecture\.md`'))"
"callout9=$([bool](Select-String -Path $f -Pattern 'Security & Privacy Callouts.*ownership belongs to `security`|Callout only — mobile-specific security'))"
"order-ok=$((Select-String -Path $f -Pattern '^## `mobile-architecture\.md`').LineNumber -lt (Select-String -Path $f -Pattern '^## `platform-architecture\.md`').LineNumber)"
Push-Location standards/architecture-schema
"backlink=$(Test-Path '../../architecture/mobile-architecture/SKILL.md')"
Pop-Location
```
Expected: `layout-line=True`, `entry-present=True`, `callout9=True`, `order-ok=True` (mobile entry sits before platform entry, after frontend), `backlink=True`.

- [ ] **Step 4: Commit**

```
git add standards/architecture-schema/README.md
git commit -m "feat(mobile): register mobile-architecture.md in architecture-schema

Adds the file-layout entry and the mobile-architecture.md schema entry
(16 required sections + conditional Notifications), parallel to
frontend-architecture.md. Security and Release sections are callouts;
frontend cross-refs optional and non-binding.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 7: Cross-file verification and trigger prompts

**Files:** none modified — verification only; results recorded in PR/commit notes.

- [ ] **Step 1: Whole-skill structural sweep**

PowerShell tool:
```
$base='architecture/mobile-architecture'
"skill-lines=$((Get-Content $base/SKILL.md).Count)"
"skill-name=$((Get-Content $base/SKILL.md | Select-String '^name: mobile-architecture').Count)"
"files=$((Get-ChildItem -Recurse -File $base | Measure-Object).Count)"
Get-ChildItem -Recurse -File $base | ForEach-Object { $_.FullName.Replace((Get-Location).Path + '\','') }
```
Expected: `skill-lines` ≤ 210; `skill-name=1`; `files=5` (SKILL.md, README.md, assets/mobile-architecture.template.md, references/mobile-architecture-playbook.md, references/mobile-architecture-quality-rubric.md).

- [ ] **Step 2: All repo-relative links from SKILL.md and README resolve**

PowerShell tool:
```
Push-Location architecture/mobile-architecture
$ok=$true
foreach ($p in '../system-design/SKILL.md','../backend-architecture/SKILL.md','../security/SKILL.md','../operations/SKILL.md','../infrastructure-platform/SKILL.md','../performance/SKILL.md','../quality-engineering/SKILL.md','../frontend-architecture/SKILL.md','../frontend-architecture/README.md','../../implementations/frontend/frontend-design/SKILL.md','../../standards/architecture-schema/README.md','../../standards/documentation-standards/README.md','../../standards/security-standards/README.md','../../standards/observability-standards/README.md','../../standards/deployment-standards/README.md','SKILL.md') { if (-not (Test-Path $p)) { $ok=$false; "MISSING $p" } }
"all-links-ok=$ok"
Pop-Location
```
Expected: `all-links-ok=True` (no `MISSING` lines).

- [ ] **Step 3: Secret scan (no key anywhere)**

PowerShell tool:
```
$h=Get-ChildItem -Recurse -File architecture/mobile-architecture | Select-String -Pattern 'AQ\.[A-Za-z0-9_\-]{8,}|X-Goog-Api-Key'
"leak=$(@($h).Count)"
```
Expected: `leak=0`.

- [ ] **Step 4: Trigger-prompt verification (record outcomes for PR notes)**

Should match `mobile-architecture`:
1. "We have an approved system-design.md with a native iOS + Android app — define the mobile application architecture."
2. "Design the offline-sync and navigation architecture for our React Native app before we build it."
3. "We need the mobile platform strategy (native vs cross-platform) and state model for the new companion app."

Should NOT match `mobile-architecture`:
1. "Make our web app responsive on mobile browsers / a PWA." → `frontend-architecture` (mobile-web/PWA negative-scoped).
2. "Implement the Keychain token storage and certificate pinning for the iOS app." → `security` (deep mobile security negative-scoped; mobile-architecture only raises callouts).

Expected: 3 match, 2 excluded as noted.

- [ ] **Step 5: Record results**

Record `skill-lines`, `files=5`, `all-links-ok=True`, `leak=0`, and the 3+2 trigger outcomes in the PR description (or alongside the commits if no PR). No file change, no commit.

---

## Self-Review

**1. Spec coverage (against the revised spec):**
- Mature-sibling tier files (SKILL.md, README, template, playbook, quality-rubric) → Tasks 1–5.
- Name `mobile-architecture`, frontmatter "Use when"/≤1024/link-secret-free, ≤~200 lines, `##`-only, no `---` rules → Task 1 Steps 2–3.
- Sibling section order → Task 1 Step 3 (matches `frontend-architecture`).
- Owned domains (platform/app/nav/state/offline/device/perf/a11y/notifications/error/observability/testing/failure taxonomy) → Task 1 Process Steps 1–16; template sections; playbook; rubric.
- Security/privacy and release/ops as **callouts only** → Task 1 Steps 9/15 + Operating rules + Quality checks; template §"Security & Privacy Callouts"/"Release & Operations Callouts" (Task 3 Step 3 asserts deferral text); rubric "Callouts" check; schema entry callout framing (Task 6).
- State/perf/a11y **owned/restated** (not reuse-by-reference) → present as full template sections + process steps + schema required sections.
- 18-section artifact structure with §9/§15 reframed as callouts → Task 3 (template) + Task 6 (schema). Template uses the spec's 18 logical sections; "Notifications & Background Behavior" is the schema's conditional section and ADR Index/Implementation Handoffs are required, matching the frontend sibling's shape.
- Approach A standalone + optional non-binding frontend cross-ref → SKILL Output contract; schema closing paragraph (Task 6).
- architecture-schema extension (file-layout line + entry parallel to frontend, before platform) → Task 6.
- Name normalization (implementations/mobile/<ecosystem>, quality-engineering, frontend-architecture) → used throughout Tasks 1/2/3/6; no `frontend-mobile-*`/`qa-testing`/`frontend-web-architecture` strings.
- Out of scope (no implementations/mobile/*, no ROADMAP/README registry edits, no owned security/release) → no task creates those; Task 7 Step 1 asserts exactly 5 files under the domain.
- SKILL_SPEC + documentation-standards quality bar incl. 3+2 trigger prompts → Task 1 verifications + Task 7.
No gaps.

**2. Placeholder scan:** Bracketed tokens (`[decision]`, `<product-slug>`, `<ecosystem>`, `NNNN`) appear only inside the artifact **template** (Task 3) and schema frontmatter block (Task 6) — these are the intended scaffold placeholders, exactly as in the `frontend-architecture` sibling template, not plan placeholders. No "TBD/TODO/handle errors"-style gaps; every file's full content is inline. ✓

**3. Type/identifier consistency:** `name: mobile-architecture` == directory == README title == schema backlink throughout. Section titles match across SKILL Process, template, and schema required-sections (e.g. "Offline & Synchronization Design", "Security & Privacy Callouts", "Release & Operations Callouts", "Failure Taxonomy"). Link depths consistent: `../<sibling>/SKILL.md` from the domain dir, `../../standards/...` and `../../implementations/...` from the domain dir, `../../../standards/...` from `references/`. Schema entry ordered after `frontend-architecture.md` and before `platform-architecture.md` (Task 6 Step 3 `order-ok`). ✓
