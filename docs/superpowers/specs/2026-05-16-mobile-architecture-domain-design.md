# mobile-architecture domain — design

> Status: approved
> Date: 2026-05-16

## Context

The repository has no mobile layer: no `architecture/mobile-architecture/`
domain and no `implementations/mobile/` tree. Mobile mirrors the entire
frontend layer in size, so it is decomposed into independent sub-projects,
each with its own spec → plan → implementation cycle.

**This spec covers sub-project #1 only: the `architecture/mobile-architecture`
domain skill** (mature-sibling tier, peer to `frontend-/backend-/data-architecture`).
Implementation ecosystems (`implementations/mobile/*`) and any umbrella
mobile-layer roadmap are explicitly out of scope and will be separate efforts.

## Decisions

| Decision | Choice |
|---|---|
| Sub-project | `architecture/mobile-architecture` domain skill only |
| Tier | Mature-sibling tier (SKILL.md + README + `assets/` template + `references/` playbook + quality-rubric + a standard entry) |
| Domain shape | Standalone peer architecture domain, framework-agnostic |
| Ownership | Owns the mobile-native core (below). Reuses `frontend-architecture` by reference for shared concerns |
| Store-release / signing | Out of scope here — defers to `operations` / `infrastructure-platform`; raised as mobile callouts only |
| Mobile security / privacy | Out of scope here — defers to the `security` domain; raised as mobile callouts only |
| Platform scope | Native (iOS/Android) + cross-platform-native (React Native / Flutter / KMP). Mobile-web/PWA stays in `frontend-architecture` |
| Native-vs-cross-platform | Framed as an ADR the domain scopes but does **not** prescribe (mirrors `frontend-architecture` deferring framework choice) |
| Artifact strategy | Approach A: standalone, independently-valid `mobile-architecture.md` with explicit cross-references to `frontend-architecture.md` where shared. No hard dependency on a frontend artifact (mobile-only products are valid) |
| Artifact schema | Extend `standards/architecture-schema` with a `mobile-architecture.md` entry (consistent with how `frontend-architecture.md` is defined there) |

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
  Triggers on production-grade mobile application architecture for a native or
  cross-platform-native app, after an approved system design and before
  mobile implementation. Negative-scoped away from: mobile-web/PWA (use
  `frontend-architecture`), framework scaffolding (use
  `implementations/mobile/<ecosystem>` once it exists), deep mobile security
  (use `security`), and store-release/signing (use `operations` /
  `infrastructure-platform`).

### Body sections

Sibling section order and conventions (matches `frontend-architecture`):
`## When to use` / `## Inputs` / `## Operating rules` / `## Output contract`
/ `## Progressive references` / `## Process` (checkbox steps) / `## Outputs`
/ `## Quality checks` / `## References`. `##`-only headings, no `---` rules,
repo-relative links, ≤ ~200 lines (overflow moves to the playbook).

- **When to use** — after `system-design` has approved a design that includes
  a native or cross-platform-native mobile surface, and before
  `implementations/mobile/<ecosystem>` skills generate the app. Not for
  mobile-web/PWA, not for framework scaffolding, not for backend APIs.
- **Inputs** — Required: approved `system-design.md` + relevant ADRs; the
  mobile surface(s) in scope; primary user tasks and the device/network/OS
  expectations they imply. Optional: the product's `frontend-architecture.md`
  (for shared decisions to reference), API contracts, identity model, store
  and compliance constraints, device matrix, offline expectations.
- **Operating rules** — architect before choosing native vs cross-platform;
  the platform-target decision is an ADR, not a prescription; offline and
  sync behavior are explicit decisions, not implementation detail; push,
  deep linking, background execution, and permissions each define failure and
  degraded-mode behavior; the native-module/bridge boundary is a named seam;
  shared client concerns are referenced from `frontend-architecture`, not
  restated; security/privacy and store-release decisions that cross a
  boundary are raised as ADR candidates against `system-design`, not owned
  here.
- **Output contract** — `mobile-architecture.md` MUST conform to
  `standards/architecture-schema` (authoritative for frontmatter, required and
  conditional sections, conditional-omission rules, and `system-design.md`
  traceability). Skill structure conforms to `documentation-standards`. Use
  `assets/mobile-architecture.template.md` as the scaffold. No
  framework-specific code or vendor SDK calls unless they materially change
  architecture behavior.
- **Progressive references** — read the playbook when defining any owned
  decision domain or checking the anti-pattern list; read the quality-rubric
  before finalizing; use the template for the artifact.
- **Process** — checkbox steps: load system-design + ADRs and identify mobile
  surfaces; decide platform target (ADR); define app shell & navigation;
  define offline-first/sync; define push/notifications; define deep
  linking; define app lifecycle & background execution; define device
  capabilities & permissions model; define the native-module/bridge boundary;
  reference shared concerns from `frontend-architecture` (or state the
  mobile-owned decision if absent); draft security/store callout ADR
  candidates; generate `mobile-architecture.md` from the template; validate
  against the schema and quality-rubric.
- **Outputs** — Required: `mobile-architecture.md` at
  `docs/architecture/<product-slug>/mobile-architecture.md` per the schema.
  Optional: navigation map, sync/offline diagrams, permission matrix, ADR
  drafts.
- **Quality checks** — binary-verifiable (rubric loaded before finalizing;
  schema-valid frontmatter and sections; platform-target decision recorded as
  an ADR; offline/sync names failure + degraded mode; push, deep linking,
  background, permissions each name a failure path; native-module boundary is
  explicit; every shared concern either references `frontend-architecture.md`
  or states the mobile-owned decision; security/store items appear as callout
  ADR candidates, not owned decisions; no framework code unless it changes
  architecture behavior).
- **References** — upstream `architecture/system-design`; downstream future
  `implementations/mobile/<ecosystem>`; related `frontend-architecture`
  (shared, by reference), `security` (mobile security callouts), `operations`
  / `infrastructure-platform` (release/signing callouts), `performance`,
  `quality-engineering`.

## Owned decision domains (playbook content)

The playbook carries deep enumerations + an anti-pattern list for:

1. Platform-target decision (native iOS+Android vs cross-platform-native
   RN/Flutter/KMP) — decision criteria, trade-offs, ADR framing.
2. App shell & navigation model (stack/tab/modal topology, deep-link routing,
   state restoration).
3. Offline-first / sync strategy (local store, conflict resolution, queueing,
   reconciliation, degraded mode).
4. Push & notifications architecture (token lifecycle, delivery semantics,
   foreground/background handling, opt-in UX).
5. Deep linking / universal links / app links (routing, deferred deep links,
   fallback).
6. App lifecycle & background execution (cold/warm start, suspension,
   background tasks, state restoration).
7. Device capabilities & permissions model (permission request UX, denial and
   revocation paths, degraded behavior).
8. Native-module / bridge boundary (when to drop to native, the interface
   contract, performance and threading implications).
9. Shared-by-reference concerns (state tiers, data fetching/caching,
   design-system seam, accessibility, performance budgets) — referenced from
   `frontend-architecture.md` by section when present; stated as the
   mobile-owned decision when absent.
10. Boundary callouts (not ownership): mobile security/privacy (token storage,
    biometric, pinning, encryption, privacy manifests) → `security`;
    release/signing/rollout → `operations` / `infrastructure-platform`.
    Surfaced as ADR candidates against `system-design`.

## standards/architecture-schema extension

Add a `mobile-architecture.md` entry parallel to the `frontend-architecture.md`
entry: frontmatter requirements, required sections, conditional sections and
their omission rules, `system-design.md` traceability, and the
cross-reference rule allowing shared sections to point at the product's
`frontend-architecture.md`. The artifact remains independently valid without a
frontend artifact.

## README

`Purpose` / `Owns` / `Produces` / `Skills` / `Standards this domain conforms
to` / `Upstream inputs` / `Downstream consumers`, with `> Status: draft`.
Upstream = approved `system-design.md` whose design includes a native or
cross-platform-native mobile surface. Downstream = future
`implementations/mobile/<ecosystem>`, plus `security` and `operations` /
`infrastructure-platform` for the callout boundaries.

## Out of scope

- `implementations/mobile/*` and any ecosystem (React Native, Flutter, iOS,
  Android, Expo, KMP).
- Mobile-web / PWA (owned by `frontend-architecture`).
- Deep mobile security/privacy content (owned by `security`).
- Store-release / signing / mobile CI depth (owned by `operations` /
  `infrastructure-platform`).
- Any umbrella mobile-layer roadmap document.
- ROADMAP.md / README.md registry edits.

## Quality bar (SKILL_SPEC.md + documentation-standards)

- Valid frontmatter: `name` equals directory; `description` starts "Use when",
  ≤ 1024 chars, no links/secrets.
- `SKILL.md` ≤ ~200 lines, `##`-only headings, no `---` rules, repo-relative
  links resolve.
- Quality-checks section is binary-verifiable.
- `standards/architecture-schema/README.md` cross-references resolve; the
  `mobile-architecture.md` entry is internally consistent with the template.
- Playbook, quality-rubric, and template mirror the `frontend-architecture`
  sibling style.
- 3 "should match" and 2 "should NOT match" trigger prompts supplied at
  implementation time and verified.
