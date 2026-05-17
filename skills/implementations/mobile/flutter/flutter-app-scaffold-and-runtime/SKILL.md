---
name: flutter-app-scaffold-and-runtime
description: Use when creating, modernizing, or production-hardening a Flutter mobile application after mobile architecture is approved or intentionally deferred. Produces a production-ready app shell with flavor-separated entry points, environment and profile handling, layered error handling (runZonedGuarded, PlatformDispatcher, FlutterError, ErrorWidget), a structured logging client, crash reporting and performance tracing seams, the DI and session provider baseline downstream archetypes extend, and CI signing scaffolding without committing credentials. Do not use for navigation topology or deep-link wiring, state or data-fetching implementation, design-system or accessibility integration, or performance budget enforcement; use the other Flutter archetype skills instead.
---

# Flutter App Scaffold and Runtime

## When to use

Invoke when starting a new Flutter application, standardizing an existing Flutter app baseline, modernizing a project that lacks flavor separation or observability, or preparing a Flutter app for store or enterprise distribution.

Do not use for: navigation topology and deep-link wiring (use `flutter-navigation-and-routing`), state management and data-fetching implementation (use `flutter-state-and-data-fetching`), design-system and accessibility integration (use `flutter-design-system-and-accessibility`), or performance budget enforcement (use `flutter-performance-and-reliability`).

## Inputs

Required:

- App name and the business capability it serves.
- Approved `mobile-architecture.md`, or explicit confirmation that mobile architecture is intentionally deferred.

Optional:

- Approved `architecture/security` decisions on auth provider, session model, and token strategy.
- Supported platforms (iOS, Android, or both).
- DI container preference if `mobile-architecture.md` is silent (GetIt default; ProviderScope if state is Riverpod-first).
- Observability vendor (Firebase Crashlytics, Sentry, or none — deferred no-op stub).
- CI system (Fastlane, Codemagic, or none).
- Minimum OS versions.
- Monorepo vs single-app repo placement.

## Operating rules

- Never generate tutorial-grade scaffolding. Assume multiple environments, observability, store or enterprise deployment, code-signing discipline, and operational ownership.
- Consume `mobile-architecture.md`; do not invent decisions. Platform target, DI container, state management approach, observability vendor, and auth provider belong to `mobile-architecture.md` and `architecture/security`. If either is silent on a decision this scaffold needs, pause and raise an ADR candidate rather than guessing.
- Owns the DI and session provider baseline only — the shell, not the flow. Token storage, refresh, and protected-route gates belong to `flutter-state-and-data-fetching`. Scaffold the seam; do not implement the flow.
- Secure by default: no secrets in `pubspec.yaml` or committed config, no hardcoded API keys, no flavor-specific `.env` committed, signing config references environment variables or CI secret store rather than embedding credentials.
- Observability is mandatory in the baseline: crash reporting init, structured logging client, and performance tracing seam — all wired in each flavor `main_*.dart` before `runApp`.
- Error handling is layered in a specific order: `runZonedGuarded` (outermost; catches unhandled async errors) → `PlatformDispatcher.instance.onError` (platform channel and native plugin errors) → `FlutterError.onError` (framework widget errors) → `ErrorWidget.builder` (safe fallback UI for failed widget builds). All four layers are required.
- Flavors are not optional: dev/staging/prod separation from day one. The same codebase runs in every environment via flavor constants; no per-environment source branches.
- A scaffold that does not build is not done. Run `flutter analyze` and a flavor build before declaring completion; fix and re-run on failure.
- Confirm the target directory before writing files. Recommend `apps/<app-name>/` in a monorepo or repo root for a single-app repo. Refuse to write into a plugin or skill repository without explicit user override.

## Output contract

The generated app shell MUST conform to:

- [security-standards](../../../../../standards/security-standards/README.md) — no secrets in bundle or committed config, signing via environment variables or CI secret store.
- [observability-standards](../../../../../standards/observability-standards/README.md) — crash reporting, structured logging, and performance tracing seam wired with environment and flavor tags.
- [deployment-standards](../../../../../standards/deployment-standards/README.md) — env-agnostic build via Flutter flavor mechanism; runtime config not baked at build time; no per-environment source branches.

Upstream contract: `mobile-architecture.md` is the source of truth for platform target, DI container, state approach, and observability vendor; `architecture/security` is the source of truth for auth provider, session model, and token strategy. If either is silent on a decision this scaffold needs, pause and raise an ADR candidate rather than guessing.

## Progressive references

- Read `references/flutter-scaffold-playbook.md` when implementing any owned area or checking the anti-pattern list.
- Read `references/flutter-scaffold-quality-rubric.md` before declaring the scaffold complete.
- Use `assets/flutter-app-scaffold.template.md` as the directory-layout and entry-point reference.

## Process

1. Gather context: app name, business capability, **target directory**, supported platforms, observability vendor, CI system, and the auth provider decision from `architecture/security`. Load `mobile-architecture.md` and extract platform target, DI container, and state approach. If a needed decision is missing, raise an ADR candidate before proceeding. Confirm the target directory is not a plugin or skill repository.
2. Generate the project layout: `pubspec.yaml` (all dependencies pinned, no `^`), `analysis_options.yaml` with strict lints, directory structure (features-first or clean-arch per `mobile-architecture.md`), flavor entry points (`main_dev.dart`, `main_staging.dart`, `main_prod.dart`), and the root app widget. Reference `assets/flutter-app-scaffold.template.md` for the canonical layout.
3. Generate flavor and environment handling: dart-define flavor constants (`Flavor` enum, app name, bundle ID suffix, API base URL slot) in `app/app_config.dart`, flavor-specific config stubs (e.g. `firebase_options_dev.dart` pattern or equivalent), `.env.example` documenting all env vars with placeholder values only, `.gitignore` covering `.env`, signing artifacts, `key.properties`, and `build/`.
4. Generate the layered error-handling baseline: `runZonedGuarded` wrapping `runApp` in each `main_*.dart` routing unhandled async errors to crash reporting; `PlatformDispatcher.instance.onError` assigning a handler that logs and reports; `FlutterError.onError` overriding to log and report (non-fatal in non-dev flavors); `ErrorWidget.builder` override producing a safe fallback widget that does not expose stack traces in non-dev flavors.
5. Generate the observability baseline: crash reporting init in `core/observability/crash_reporter.dart` (vendor from `mobile-architecture.md`, or a no-op stub if deferred); structured logging client in `core/logging/app_logger.dart` (level-aware, flavor-aware, PII-free by default); performance tracing seam in `core/observability/perf_tracer.dart`. Wire all three in each `main_*.dart` before `runApp`.
6. Generate the DI and session provider baseline: ProviderScope root, GetIt registration file, or the container named in `mobile-architecture.md`, implemented in `core/di/injection.dart`. Install the auth session provider as a named typed shell. Leave explicit TODO comments in the seam file identifying `flutter-state-and-data-fetching` as the owner of token storage, refresh, and session persistence.
7. Generate CI and signing scaffolding: Fastlane `Appfile` (referencing `ENV['APP_IDENTIFIER']` and `ENV['TEAM_ID']`) and `Fastfile` with flavor-aware build lanes and signing configuration referencing environment variables only, or an equivalent Codemagic yaml. Create `Gemfile` pinning the `fastlane` gem. Create `fastlane/README.md` listing all required environment variables and their purpose.
8. Generate local-run documentation: how to run each flavor, all required environment variables, the runtime-config contract, and the explicit table of seams downstream archetypes will fill (navigation, state/data, design-system, performance).
9. Build verification (mandatory): run `flutter analyze` and `flutter build apk --flavor dev` (Android) and `flutter build ios --no-codesign --flavor dev` (iOS simulator). If a platform toolchain is unavailable, document the skipped check in the README rather than declaring success silently. Fix and re-run on failure.
10. Validate against [security-standards](../../../../../standards/security-standards/README.md), [observability-standards](../../../../../standards/observability-standards/README.md), and [deployment-standards](../../../../../standards/deployment-standards/README.md). Revise until all pass or explicitly document any unresolved gap.

## Outputs

Required:

- Flutter project source tree with `pubspec.yaml` (pinned deps) and `analysis_options.yaml`.
- Flavor entry points (`main_dev.dart`, `main_staging.dart`, `main_prod.dart`) and `app_config.dart` flavor constants.
- Layered error-handling baseline (all four layers wired; safe fallback widget).
- Observability baseline: crash reporting init, structured logging client, performance tracing seam.
- DI and session provider baseline (seam only; token logic and route gates explicitly deferred).
- CI and signing scaffolding (env-var-referenced credentials only; no committed secrets).
- `.env.example` and local-run README listing all seams downstream archetypes fill.

Output rules:

- Generated files are functional and buildable, not placeholder-heavy.
- No secrets in `pubspec.yaml`, `.env.example`, committed config, or the build artifact.
- The auth baseline is a seam, not a flow — token logic and protected-route gates are explicitly deferred to `flutter-state-and-data-fetching` and `flutter-navigation-and-routing`.
- The same build artifact runs in every environment via the Flutter flavor mechanism.

## Quality checks

- [ ] `flutter analyze` reports zero issues.
- [ ] A flavor build (`--flavor dev`) succeeds on at least one platform, or the skipped platform is documented with reason.
- [ ] No secrets appear in `pubspec.yaml`, committed config, or the build artifact.
- [ ] All four error-handling layers are wired: `runZonedGuarded`, `PlatformDispatcher.instance.onError`, `FlutterError.onError`, `ErrorWidget.builder`.
- [ ] The `ErrorWidget.builder` fallback does not expose stack traces or internal state in non-dev flavors.
- [ ] Crash reporting, structured logging, and performance tracing seam are initialized in each `main_*.dart` before `runApp`.
- [ ] The DI/session provider shell is named and tied to a `mobile-architecture.md` or `architecture/security` decision; token logic and route gates are explicitly deferred with TODO comments.
- [ ] Signing configuration references environment variables only — no credentials committed.
- [ ] The local-run README lists all seams downstream archetypes are expected to fill.

## References

- Upstream: [`architecture/mobile-architecture`](../../../../architecture/mobile-architecture/SKILL.md), [`architecture/security`](../../../../architecture/security/SKILL.md).
- Related Flutter archetype skills (extend this baseline): `flutter-navigation-and-routing`, `flutter-state-and-data-fetching`, `flutter-design-system-and-accessibility`, `flutter-performance-and-reliability`.
- Standards: [`security-standards`](../../../../../standards/security-standards/README.md), [`observability-standards`](../../../../../standards/observability-standards/README.md), [`deployment-standards`](../../../../../standards/deployment-standards/README.md).
