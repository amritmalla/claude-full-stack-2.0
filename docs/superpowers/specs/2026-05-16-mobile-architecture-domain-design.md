# mobile-architecture domain — design

> Status: approved (revised 2026-05-16 to reconcile the user's rough-note draft)
> Date: 2026-05-16

## Context

The repository has no mobile layer: no `architecture/mobile-architecture/`
domain and no `implementations/mobile/` tree. Mobile mirrors the entire
frontend layer in size, so it is decomposed into independent sub-projects,
each with its own spec → plan → implementation cycle.

**This spec covers sub-project #1 only: the `architecture/mobile-architecture`
domain skill** (mature-sibling tier, peer to `frontend-/backend-/data-architecture`).
Implementation ecosystems (`implementations/mobile/*`) and any umbrella
mobile-layer roadmap are out of scope and will be separate efforts.

The user supplied a near-complete rough-note `SKILL.md` draft. This revision
folds that draft's richer structure and owned domains into the spec, after
reconciling four conflicts with the user (see Decisions). The mature-sibling
tier treatment still applies: SKILL.md stays a tight imperative recipe and the
rich per-area enumerations move into the playbook.

## Decisions

| Decision | Choice |
|---|---|
| Sub-project | `architecture/mobile-architecture` domain skill only |
| Tier | Mature-sibling tier (SKILL.md + README + `assets/` template + `references/` playbook + quality-rubric + a standard entry) |
| Domain shape | Standalone peer architecture domain, framework-agnostic, **self-contained** |
| Skill name | `mobile-architecture` (sibling-consistent) |
| Mobile security/privacy | **Deferred** — `security` domain owns it; mobile-architecture raises mobile callouts / ADR candidates only |
| Release & operations | **Deferred** — `operations` / `infrastructure-platform` own it; mobile-architecture raises callouts / ADR candidates only |
| State / performance / accessibility | **Owned, restated** as full sections (per rough note). Optional, non-binding cross-references to `frontend-architecture.md` where a web frontend exists |
| Platform scope | Native (iOS/Android) + cross-platform-native (React Native / Flutter / KMP). Mobile-web/PWA stays in `frontend-architecture` |
| Native-vs-cross-platform | Framed as an ADR the domain scopes but does **not** prescribe |
| Artifact strategy | Approach A: standalone, independently-valid `mobile-architecture.md`; cross-references to `frontend-architecture.md` are optional and non-binding (mobile-only products are valid) |
| Artifact schema | Extend `standards/architecture-schema` with a `mobile-architecture.md` entry (parallel to `frontend-architecture.md`) |
| Name normalization | Rough note's downstream/related names mapped to repo conventions: `frontend-mobile-{ios,android,cross-platform}` → `implementations/mobile/<ecosystem>`; `qa-testing` → `quality-engineering`; `frontend-web-architecture` → `frontend-architecture` |

## File layout

```
architecture/mobile-architecture/
├── SKILL.md
├── README.md
├── assets/
│   └── mobile-architecture.template.md
└── references/
    ├── mobile-architecture-playbook.md
    └── mobile-architecture-quality-rubric.md
```

Plus an edit to `standards/architecture-schema/README.md` defining the
`mobile-architecture.md` artifact.

## SKILL.md

### Frontmatter (load-bearing)

- `name: mobile-architecture` (equals the directory).
- `description:` starts with "Use when"; ≤ 1024 chars; no links/secrets.
  Adapted from the rough note: triggers on native, cross-platform-native, or
  hybrid mobile application architecture after an approved system design and
  before implementation. Negative-scoped away from: mobile-web/PWA (use
  `frontend-architecture`), backend service design (use `backend-architecture`),
  UI/visual design (use `frontend-design`), vendor-specific SDK
  implementation, deep mobile security (use `security`), and store-release /
  signing depth (use `operations` / `infrastructure-platform`).

### Body sections

Sibling section order and conventions (matches `frontend-architecture`):
`## When to use` / `## Inputs` / `## Operating rules` / `## Output contract`
/ `## Progressive references` / `## Process` (checkbox steps) / `## Outputs`
/ `## Quality checks` / `## References`. `##`-only headings, no `---` rules,
repo-relative links, ≤ ~200 lines (rich per-area enumerations move to the
playbook).

- **When to use** — invoke after `system-design` has approved a product that
  includes a native or cross-platform-native mobile app, and before
  `implementations/mobile/<ecosystem>` skills generate platform code. Covers
  iOS, Android, cross-platform, hybrid, tablet/foldable, and companion apps.
  Do not use when there is no mobile client, for pure backend architecture,
  for UI/visual design only, for vendor SDK implementation, or when
  architecture is already finalized and only implementation remains.
- **Inputs** — Required: approved `system-design.md` + ADRs; mobile product
  requirements; supported platforms and minimum OS versions; primary user
  journeys; performance expectations; offline expectations. Optional: backend/
  API contracts; design system / UX guidelines; accessibility requirements;
  analytics/notification/device-capability requirements; security/compliance
  constraints; release cadence; regional constraints; the product's
  `frontend-architecture.md` (optional cross-reference for shared concerns).
- **Operating rules** (condensed from the rough note's "Operating rules",
  "Architecture decision principles", "Platform strategy principles",
  "Non-goals"): treat the app as a constrained distributed system; assume
  unreliable networks and limited battery; design for termination, recovery,
  resumability; define device/backend state ownership; minimize background
  work; define degraded behavior explicitly; navigation/state/sync/caching are
  first-class; native conventions over framework convenience; accessibility
  and responsiveness are mandatory architectural qualities; prefer native
  conventions, simpler architecture, offline resilience, predictable state,
  battery efficiency, platform capabilities, accessibility, incremental
  rollout; evaluate native vs cross-platform vs hybrid vs PWA explicitly and
  never default to cross-platform without evaluating UX/startup/memory/
  animation/offline/native-API trade-offs; security/privacy and
  release/operations decisions are **callouts**, raised as ADR candidates
  against `system-design`, not owned here; no premature optimization for
  unsupported platforms; no device features without measurable user value.
- **Output contract** — `mobile-architecture.md` MUST conform to
  `standards/architecture-schema` (authoritative for frontmatter, required and
  conditional sections, conditional-omission rules, `system-design.md`
  traceability). Skill structure conforms to `documentation-standards`. Use
  `assets/mobile-architecture.template.md` as the scaffold. No
  framework-specific code or vendor SDK calls unless they materially change
  architecture behavior.
- **Progressive references** — read the playbook when defining any owned
  decision area or checking the anti-pattern list; read the quality-rubric
  before finalizing; use the template for the artifact.
- **Process** — checkbox steps mirroring the rough note's 1–17 flow, with
  security and release reframed as callouts:
  1. Platform & product assessment (load `system-design.md`; identify mobile
     journeys, platforms, capabilities, network/session/operational
     constraints; latency-sensitive and offline-sensitive flows).
  2. Platform strategy (native vs cross-platform vs hybrid; rationale,
     trade-offs, unsupported scenarios, min OS, device classes, tablet/
     foldable; recorded as an ADR).
  3. Application architecture (layers, module boundaries, state ownership,
     side effects, concurrency, lifecycle, DI; avoid over-abstraction).
  4. Navigation architecture (hierarchy, route ownership, deep links, modals,
     auth transitions, shell/tabs, restoration).
  5. State management strategy (local/session/cached/persistent state,
     sync ownership, optimistic updates, conflict resolution, invalidation).
  6. Offline & synchronization architecture (offline capabilities, sync
     model, queueing, retry, conflict resolution, authoritative sources,
     degraded-mode behavior; explicit works/partial/fails-gracefully).
  7. Device capability integration (per capability: permission strategy,
     fallback, privacy, battery impact, failure handling, platform limits).
  8. Performance & battery budgets (cold/warm start, transition latency,
     memory, background, battery, network, storage; degradation under low
     memory/poor connectivity/thermal/battery-saver).
  9. Security & privacy **callouts** (summarize mobile-specific auth/token/
     secure-storage/jailbreak/encryption concerns; draft ADR candidates;
     defer ownership to `security`).
  10. Accessibility & localization (screen reader, dynamic text, reduced
      motion, contrast, RTL, font scaling, i18n; accessibility failures are
      architectural failures).
  11. Notifications & background behavior (push types, delivery, priority,
      background refresh, routing, opt-in, rate-limiting, silent push;
      no background execution without measurable value).
  12. Error handling & recovery (global error strategy, retry ceilings,
      crash recovery, interrupted-session handling, degraded UX).
  13. Observability & analytics (crash, performance, network tracing,
      journey/screen analytics, startup, battery telemetry, release
      monitoring; logging policy, PII redaction, sampling, retention).
  14. Testing strategy (unit/integration/UI-automation/offline/device-
      compat/accessibility/perf-regression; emulator vs device; release
      gating; rollback validation).
  15. Release & operations **callouts** (summarize channels, staged rollout,
      store submission, forced-upgrade, deprecation as ADR candidates; defer
      ownership to `operations` / `infrastructure-platform`).
  16. Failure taxonomy (startup, network, sync conflict, rendering
      degradation, termination, permission denial, notification failure, API
      incompatibility, storage exhaustion, background failure; each with
      detection, mitigation, recovery, observability, user-facing behavior).
  17. Generate `mobile-architecture.md` from the template; validate against
      the schema and quality-rubric; consolidate ADR candidates.
- **Outputs** — Required: `mobile-architecture.md` at
  `docs/architecture/<product-slug>/mobile-architecture.md` per the schema.
  Optional: navigation diagrams, state-ownership maps, offline-sync diagrams,
  notification-routing diagrams, ADR drafts, performance-budget tables,
  failure-mode matrices.
- **Quality checks** — binary-verifiable, adapted from the rough note's
  checklist (rubric loaded before finalizing; schema-valid; platform strategy
  has rationale + trade-offs recorded as an ADR; navigation ownership and
  restoration defined; state ownership and sync rules explicit; offline
  behavior defined for all critical journeys; device capabilities include
  permission + privacy + fallback; performance and battery budgets are
  measurable; accessibility explicitly documented; notification and
  interruption policies documented; error handling and degraded behavior
  defined; observability includes crash/latency/release telemetry; testing
  includes offline/accessibility/device-compat; security/privacy and
  release/ops appear only as callout/ADR candidates, not owned designs; no
  vendor SDK detail unless it materially affects architecture).
- **References** — Upstream: `architecture/system-design`. Related:
  `backend-architecture`, `security` (mobile security callouts),
  `operations` / `infrastructure-platform` (release/signing callouts),
  `performance`, `quality-engineering`, `frontend-architecture` (optional
  shared cross-reference; mobile-web/PWA boundary). Downstream: future
  `implementations/mobile/<ecosystem>` (e.g. `ios`, `android`,
  `cross-platform`).

## `mobile-architecture.md` output structure (template + schema)

The `assets/mobile-architecture.template.md` and the architecture-schema entry
define this section structure (from the rough note's 18-section output, with
§9 and §15 reframed as callout sections):

1. Executive Summary
2. Platform Strategy
3. Application Architecture
4. Navigation Architecture
5. State Management Strategy
6. Offline & Synchronization Design
7. Device Capability Integration
8. Performance & Battery Budgets
9. Security & Privacy Callouts (deferred to `security`; ADR candidates)
10. Accessibility & Localization
11. Notifications & Background Behavior
12. Error Handling & Recovery
13. Observability & Analytics
14. Testing Strategy
15. Release & Operations Callouts (deferred to `operations`/`infrastructure-platform`; ADR candidates)
16. Failure Taxonomy
17. ADR Candidates
18. Implementation Handoffs (to `implementations/mobile/<ecosystem>`,
    `backend-architecture`, `security`, `operations`, `quality-engineering`)

## Playbook (references/mobile-architecture-playbook.md)

Deep enumerations + anti-pattern list for each owned area above (platform
strategy criteria, navigation patterns, state/sync models, offline matrices,
device-capability permission/fallback tables, performance/battery budget
guidance, accessibility/localization detail, notification/background patterns,
error/recovery taxonomy, observability signal catalog, testing matrix). The
security and release areas appear here only as callout checklists pointing to
`security` and `operations` / `infrastructure-platform`.

## standards/architecture-schema extension

Add a `mobile-architecture.md` entry parallel to `frontend-architecture.md`:
frontmatter requirements, the 18-section required/conditional structure above,
conditional-omission rules, `system-design.md` traceability, and the rule that
§9 and §15 are callout sections (summaries + ADR candidates, not owned
designs) and that cross-references to a product's `frontend-architecture.md`
are optional and non-binding. The artifact is independently valid without a
frontend artifact.

## README

`Purpose` / `Owns` / `Produces` / `Skills` / `Standards this domain conforms
to` / `Upstream inputs` / `Downstream consumers`, with `> Status: draft`.
`Owns` lists the self-contained domain set above; explicitly notes that mobile
security/privacy and release/operations are **not owned** (callouts to
`security` and `operations` / `infrastructure-platform`). Upstream = approved
`system-design.md` whose design includes a native or cross-platform-native
mobile surface. Downstream = future `implementations/mobile/<ecosystem>`, plus
`security` and `operations` / `infrastructure-platform` for the callout
boundaries.

## Out of scope

- `implementations/mobile/*` and any ecosystem (React Native, Flutter, iOS,
  Android, Expo, KMP).
- Mobile-web / PWA (owned by `frontend-architecture`).
- Deep mobile security/privacy design (owned by `security`; callouts only).
- Store-release / signing / mobile CI depth (owned by `operations` /
  `infrastructure-platform`; callouts only).
- Any umbrella mobile-layer roadmap document.
- ROADMAP.md / README.md registry edits.

## Quality bar (SKILL_SPEC.md + documentation-standards)

- Valid frontmatter: `name` equals directory (`mobile-architecture`);
  `description` starts "Use when", ≤ 1024 chars, no links/secrets.
- `SKILL.md` ≤ ~200 lines, `##`-only headings, no `---` rules, repo-relative
  links resolve.
- Quality-checks section is binary-verifiable.
- `standards/architecture-schema/README.md` cross-references resolve; the
  `mobile-architecture.md` entry is internally consistent with the template's
  18-section structure, including the §9/§15 callout framing.
- Playbook, quality-rubric, and template mirror the `frontend-architecture`
  sibling style; rich enumerations live in the playbook, not SKILL.md.
- No owned security/privacy or release/ops design content (callouts only) —
  verifiable against the quality-rubric.
- 3 "should match" and 2 "should NOT match" trigger prompts supplied at
  implementation time and verified.
