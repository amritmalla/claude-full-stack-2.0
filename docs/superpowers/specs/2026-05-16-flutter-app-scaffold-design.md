# Flutter App Scaffold — Implementation Skill Design

**Date:** 2026-05-16
**Topic:** `implementations/mobile/flutter/flutter-app-scaffold-and-runtime`
**Tier:** Mature-sibling (SKILL.md + assets + references; no skill-level README)
**Ecosystem:** Flutter (first mobile implementation skill)

---

## Context

`architecture/mobile-architecture` is fully implemented (mature-sibling tier, 6 commits). It references `implementations/mobile/<ecosystem>` as its downstream but that namespace does not yet exist. This spec defines the first skill in that namespace: `flutter-app-scaffold-and-runtime`.

The Flutter scaffold is the baseline all other Flutter archetypes extend. It must be authored before routing, state/data-fetching, design-system, or performance-and-battery skills can be written.

---

## File Structure

```
implementations/
  mobile/
    README.md                          ← mobile implementations tier README
    flutter/
      README.md                        ← Flutter ecosystem README (archetype table + skill status)
      flutter-app-scaffold-and-runtime/
        SKILL.md                       ← imperative recipe (~150–200 lines)
        assets/
          flutter-app-scaffold.template.md   ← directory-tree + pubspec scaffold
        references/
          flutter-scaffold-playbook.md       ← per-area guidance + anti-patterns
          flutter-scaffold-quality-rubric.md ← grouped binary checklists
```

No skill-level README inside `flutter-app-scaffold-and-runtime/`. The `flutter/README.md` carries all skill tracking (Purpose, Owns, Produces, archetype table, status). This is intentional — future archetype skills follow the same convention, and the ecosystem README becomes the single tracking document for the Flutter tier.

---

## Ownership Boundary

### Owned by this skill

| Area | What the skill produces |
|---|---|
| Project layout | `pubspec.yaml` (pinned deps, no `^`), features-first or clean-arch directory structure per `mobile-architecture.md`, flavor entry points (`main_dev.dart`, `main_staging.dart`, `main_prod.dart`) |
| Flavor/environment handling | dart-define flavor constants, flavor-specific config stubs, documented secret approach (never committed) |
| Error-handling baseline | `runZonedGuarded` → `PlatformDispatcher.instance.onError` → `FlutterError.onError` → `ErrorWidget.builder` override with safe fallback widget |
| Observability baseline | Crash reporting init (vendor from `mobile-architecture.md`), structured logging client (level- and flavor-aware), performance tracing seam wired in `main.dart` |
| DI / session provider baseline | ProviderScope root, GetIt registration stub, or the container named in `mobile-architecture.md`; auth session provider shell with documented seams |
| CI / signing scaffolding | Fastlane Appfile/Fastfile or Codemagic yaml structure, flavor-aware build commands, signing config referencing environment variables (no real secrets), `.gitignore` for keystores/certs |

### Deferred (seams only, not implementations)

| Concern | Deferred to |
|---|---|
| Observability vendor choice | `architecture/mobile-architecture` → `mobile-architecture.md` |
| DI container / state library choice | `architecture/mobile-architecture` → `mobile-architecture.md` |
| Auth token storage, refresh, protected routes | `flutter-state-and-data-fetching` (future archetype) |
| Release channel, staged rollout, store signing depth | `architecture/operations` / `architecture/infrastructure-platform` |

---

## Operating Rules

- Never generate tutorial-grade scaffolding. Assume multiple environments, observability, store or enterprise deployment, code-signing discipline, and operational ownership.
- Consume `mobile-architecture.md`; do not invent decisions. Platform target, DI container, state management approach, observability vendor, and auth provider belong to `mobile-architecture.md` and `architecture/security`. If either is silent on a needed decision, pause and raise an ADR candidate.
- Owns the DI / session provider baseline only — the shell, not the flow. Token storage, refresh, and protected-route gates belong to the state-and-data-fetching archetype.
- Secure by default: no secrets in `pubspec.yaml`, no hardcoded API keys, no flavor-specific `.env` committed, signing config references paths or environment variables rather than embedding credentials.
- Observability is mandatory in the baseline: crash reporting seam, structured logging client, performance tracing seam — all wired in `main.dart`.
- Error handling is layered in a specific order: `runZonedGuarded` (outermost, catches async errors) → `PlatformDispatcher.instance.onError` (platform channel errors) → `FlutterError.onError` (framework errors) → `ErrorWidget.builder` (fallback widget for failed builds).
- Flavors are not optional: dev/staging/prod distinction from day one.
- A scaffold that does not build is not done. Run `flutter analyze` and a flavor build before declaring completion; fix and re-run on failure.

---

## SKILL.md Process (10 steps)

1. **Gather context** — load `mobile-architecture.md`: platform target, DI container, state approach, observability vendor, auth provider from `architecture/security`, supported platforms, minimum OS versions. If a needed decision is missing, pause and raise an ADR candidate against `mobile-architecture` or `architecture/security`.
2. **Confirm target directory** — recommend `apps/<app-name>/`; refuse to write into the skill repo without explicit user override.
3. **Generate project layout** — `pubspec.yaml` (pinned deps, no `^`), features-first or clean-arch directory structure per `mobile-architecture.md`, flavor entry points (`main_dev.dart`, `main_staging.dart`, `main_prod.dart`).
4. **Generate flavor/environment handling** — dart-define flavor constants, flavor-specific config stubs (e.g. `firebase_options_dev.dart` pattern), documented approach for secrets (never committed, reference env vars or CI secrets).
5. **Generate layered error-handling baseline** — `runZonedGuarded`, `PlatformDispatcher.instance.onError`, `FlutterError.onError`, `ErrorWidget.builder` override with a safe fallback widget that does not expose internal state.
6. **Generate observability baseline** — crash reporting init (vendor from `mobile-architecture.md`), structured logging client (level- and flavor-aware), performance tracing seam wired in `main.dart`.
7. **Generate DI/session provider baseline** — ProviderScope root, GetIt registration stub, or the container named in `mobile-architecture.md`; auth session provider shell with documented seams explicitly left for `flutter-state-and-data-fetching`.
8. **Generate CI/packaging scaffolding** — Fastlane Appfile/Fastfile or Codemagic yaml structure, flavor-aware build commands, signing config referencing environment variables (no real secrets), `.gitignore` covering keystores and signing certificates.
9. **Build verification (mandatory)** — run `flutter analyze` and `flutter build apk --flavor dev` / `flutter build ios --no-codesign --flavor dev` (simulator). Fix and re-run on failure; do not declare done on a broken build.
10. **Validate against standards** — security-standards (no secrets in bundle), observability-standards (crash + logging + tracing seam wired), deployment-standards (env-agnostic build, signing via env vars). Explicitly document any unresolved gap.

---

## Assets

### `assets/flutter-app-scaffold.template.md`

Content: a directory-tree scaffold showing the features-first layout, flavor entry points, and placeholder comments for each seam the skill installs. Includes a commented `pubspec.yaml` stub with pinned version sections, the flutter/dart SDK constraint, and the key dependency groups (core, platform, observability, dev). Placeholder tokens use `<kebab-case>` style matching the architecture template convention.

---

## References

### `references/flutter-scaffold-playbook.md`

Sections:
- **Why this workflow exists** — what this skill prevents (tutorial scaffolding in prod, flavor chaos, missing error layers, secrets in bundles)
- **Behavioral rules in depth** — one subsection per operating rule with rationale
- **Step detail** — expanded guidance per process step
- **Anti-patterns to detect** — explicit list: hardcoded API keys, single `main.dart` with no flavors, `^` everywhere in pubspec, missing `ErrorWidget.builder`, observability wired only in happy-path flows, signing credentials committed, auth flow in the scaffold instead of the seam

### `references/flutter-scaffold-quality-rubric.md`

Grouped binary checklists:
- **Project layout & flavors** — pubspec pinned, entry points exist, directory structure named
- **Error handling** — all four layers wired, safe fallback widget present
- **Observability** — crash, logging, tracing seam wired in `main.dart`
- **DI / session seam** — named after `mobile-architecture.md` decision, token logic explicitly absent
- **CI / signing** — no secrets committed, signing via env vars, `.gitignore` covers certs
- **Build verification** — `flutter analyze` clean, flavor build passes
- **Standards conformance** — security, observability, deployment standards pass or gap documented
- **Failure handling** section — three steps: identify missing decision → raise ADR candidate or ask user → revise and re-verify

---

## Standards Conformance

Every generated scaffold conforms to:

- `standards/security-standards` — no secrets in bundle, signing via env vars
- `standards/observability-standards` — crash reporting, structured logging, performance tracing seam wired
- `standards/deployment-standards` — env-agnostic build, flavor-aware artifact, runtime config not build-time-baked

---

## Upstream / Downstream

- **Upstream:** `architecture/mobile-architecture` (platform target, DI, state, observability vendor, auth provider decision from `architecture/security`)
- **Downstream:** future Flutter archetypes extend this baseline — `flutter-navigation-and-routing`, `flutter-state-and-data-fetching`, `flutter-design-system-and-accessibility`, `flutter-performance-and-battery`

---

## Out of Scope

- No other Flutter archetypes in this session (scaffold only)
- No `implementations/mobile/react-native/` or other ecosystems
- No `standards/` modifications (this skill conforms to existing standards, does not define new ones)
- No owned auth flow, token storage, or protected-route gates
- No owned security design or release/signing depth (callout seams only)
