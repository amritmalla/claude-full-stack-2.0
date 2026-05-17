# Flutter App Scaffold Playbook

Load this when implementing any owned area of `flutter-app-scaffold-and-runtime` or checking the anti-pattern list. It expands the operating rules and process steps in `SKILL.md` with the detail needed to produce a production-grade scaffold.

## Why this workflow exists

A Flutter scaffold done wrong takes weeks to fix: floating deps with `^` cause irreproducible CI builds; missing error layers leave entire classes of production crashes unobserved; no flavor separation means dev API keys reach staging and staging config reaches prod; and absent observability means the first production incident is diagnosed by guesswork.

The goal is a buildable, observable, environment-separated, error-handled baseline that every downstream archetype can extend safely — not a working feature, not a tutorial app.

## Behavioral rules in depth

### 1. Consume architecture; do not invent it

Read `mobile-architecture.md` before writing a single file. The DI container, state approach, observability vendor, and auth provider are architectural decisions — not scaffold defaults. If any needed decision is missing, surface an ADR candidate before proceeding. The scaffold implements what was decided; it does not decide.

### 2. Pin every dependency — no exceptions

Use exact version pins in `pubspec.yaml` (e.g. `get_it: 7.6.7`, not `get_it: ^7.6.7`). Floating constraints cause version-resolution divergence between developer machines and CI. `pubspec.lock` is committed and is the sole source of truth for reproducibility. Never add a dependency without a pinned version.

### 3. All four error layers — no fewer

Flutter error propagation has four independent channels, each catching errors the others miss:

| Layer | What it catches | Where to wire |
|---|---|---|
| `runZonedGuarded` | Unhandled async errors outside the widget tree (e.g. isolate errors, unawaited futures) | Wraps `runApp` in each `main_*.dart` |
| `PlatformDispatcher.instance.onError` | Platform channel exceptions, native plugin errors, errors from `FlutterView` | Assigned before `runApp` in `error_handler.dart` |
| `FlutterError.onError` | Errors during widget build, layout, and paint phases | Overridden in `error_handler.dart` |
| `ErrorWidget.builder` | Failed widget subtree builds — renders a fallback in place of the broken widget | Overridden in `fallback_widget.dart` |

Missing any one layer leaves a class of production errors unobserved. All four are required.

### 4. Flavors from the first commit

Add dev/staging/prod flavor separation before writing any other code. Retrofitting flavors invalidates existing bundle IDs, breaks signing certificates already provisioned for a single app ID, and requires rewriting CI pipelines. Flavor constants live in `app_config.dart`; each `main_*.dart` sets the flavor before any initialization runs.

Android flavor configuration lives in `build.gradle` (`productFlavors` block). iOS flavor configuration uses separate scheme targets (Dev/Staging/Prod) with distinct bundle ID suffixes (e.g. `com.example.app.dev`, `com.example.app.staging`, `com.example.app`).

### 5. Observability is mandatory infrastructure

Wire crash reporting, structured logging, and performance tracing in `main_*.dart` before `runApp` — not inside feature code. An observability vendor that is not yet chosen gets a no-op stub implementing the same interface; the stub is replaced when the vendor decision lands. Flavor-aware initialization ensures dev and prod crash streams are separate and dev noise does not pollute prod dashboards.

### 6. The DI seam owns the shell; state owns the flow

Register the auth session provider as a typed shell (e.g. a `ValueNotifier<AuthSession?>` registered in GetIt, or a `StateNotifierProvider<AuthNotifier, AuthState>` in the ProviderScope root). Mark the token-storage and refresh TODOs explicitly with the owning archetype:

```dart
// TODO(flutter-state-and-data-fetching): implement token storage and refresh
// TODO(flutter-navigation-and-routing): wire protected-route redirect
```

The scaffold owns the registration point and the type. `flutter-state-and-data-fetching` owns the implementation.

### 7. Signing config references env vars — always

Never commit a `.p12`, `keystore.jks`, `key.properties`, `GoogleService-Info.plist` with real credentials, or hardcode signing values in `Fastfile`. Fastlane lanes reference `ENV['KEY_ALIAS']`, `ENV['STORE_PASSWORD']`, `ENV['TEAM_ID']`, etc. Document required vars in `fastlane/README.md` and `.env.example`. The CI secret store holds the values; the repository holds only the reference pattern.

### 8. A broken build is not a scaffold

Run `flutter analyze` first — zero issues, no exceptions. Then run a flavor build on at least one platform. If the iOS toolchain is unavailable (no macOS runner), document it in the README and run the Android build instead. Do not declare the scaffold done on a build that has not been verified.

## Step detail

**Step 1 — Gather context.** Load `mobile-architecture.md`. Extract: platform target (iOS/Android/both), DI container (GetIt/Riverpod/injectable/other), state approach, observability vendor (Crashlytics/Sentry/none), auth provider decision from `architecture/security`. Confirm the target directory. If `mobile-architecture.md` is missing a needed decision, raise an ADR candidate — do not guess.

**Step 2 — Project layout.** Generate `pubspec.yaml` with all deps pinned. Choose features-first (one directory per feature with data/domain/presentation) or clean-arch (layers-first with features as a subdirectory) per `mobile-architecture.md`. Create `analysis_options.yaml` extending `package:flutter_lints/flutter.yaml` with strict settings. Create `.gitignore` using the pattern in `assets/flutter-app-scaffold.template.md`.

**Step 3 — Flavor/environment handling.** Create `main_dev.dart`, `main_staging.dart`, `main_prod.dart` following the entry-point pattern in `assets/flutter-app-scaffold.template.md`. Create `app_config.dart` with a `Flavor` enum and `String.fromEnvironment` constants for API base URL and any other flavor-varying config. Add Android `productFlavors` block to `build.gradle`. Add iOS scheme targets. Create `.env.example` with placeholder values for every env var the app reads.

**Step 4 — Error handling.** In `core/error/error_handler.dart`, implement `setupErrorHandlers(Flavor flavor)` assigning `PlatformDispatcher.instance.onError` and overriding `FlutterError.onError`; both route to crash reporting (non-fatal) in non-dev flavors and print to console in dev. In `core/error/fallback_widget.dart`, implement `ErrorWidget.builder` returning a `Material`/`Scaffold` with a user-facing message — no stack trace in staging/prod. In each `main_*.dart`, wrap `runApp` in `runZonedGuarded` routing unhandled async errors to `CrashReporter.recordError`.

**Step 5 — Observability.** In `core/observability/crash_reporter.dart`, implement `CrashReporter.init(Flavor)` and `CrashReporter.recordError(Object, StackTrace, {bool fatal})` wrapping the vendor SDK (or a no-op if vendor is deferred). In `core/observability/perf_tracer.dart`, implement `PerfTracer.init(Flavor)`, `PerfTracer.startTrace(String name)`, and `PerfTracer.stopTrace(String name)` as thin wrappers or stubs. In `core/logging/app_logger.dart`, implement a level-aware logger suppressing debug-level output in prod and rejecting any field named `email`, `token`, `password`, or `userId` by default.

**Step 6 — DI/session seam.** In `core/di/injection.dart`, implement `setupDependencies()` registering singletons per `mobile-architecture.md`. Register the auth session provider shell as a named singleton or provider. Add explicit TODO comments identifying `flutter-state-and-data-fetching` as the owner of token storage and refresh, and `flutter-navigation-and-routing` as the owner of protected-route gates.

**Step 7 — CI/signing scaffolding.** Create `fastlane/Appfile` referencing `ENV['APP_IDENTIFIER']` and `ENV['TEAM_ID']`. Create `fastlane/Fastfile` with `build_dev`, `build_staging`, `build_prod` lanes; signing lanes referencing `ENV['KEYSTORE_PATH']`, `ENV['KEY_ALIAS']`, `ENV['STORE_PASSWORD']`, `ENV['KEY_PASSWORD']` (Android) and `ENV['MATCH_PASSWORD']` or equivalent (iOS). Create `fastlane/Gemfile` pinning `fastlane`. Create `fastlane/README.md` listing every required env var, its purpose, and where to source it in CI.

**Step 8 — Local-run docs.** In the project README, add: how to run each flavor, all required env vars (mirrored from `.env.example`), the runtime-config contract, and the seam table from `assets/flutter-app-scaffold.template.md`.

**Step 9 — Build verification.** Run `flutter analyze`. Fix every issue — warnings included. Run `flutter build apk --flavor dev` and, on macOS, `flutter build ios --no-codesign --flavor dev`. Document any skipped platform.

**Step 10 — Standards validation.** Check security-standards (no secrets), observability-standards (crash/logging/tracing wired with flavor tag), deployment-standards (env-agnostic, flavor mechanism, no per-environment branches). Document any unresolved gap explicitly — do not hide it.

## Anti-patterns to detect

Call these out explicitly when found:

- `^` version constraints anywhere in `pubspec.yaml`
- Single `main.dart` with no flavor separation
- Hardcoded API keys, bundle IDs, or environment URLs in source code
- `.env`, `key.properties`, `*.p12`, `*.jks`, or `GoogleService-Info.plist` with real credentials committed
- Missing any of the four error-handling layers
- `ErrorWidget.builder` displaying a raw stack trace in non-dev flavors
- Observability wired only inside feature code, not in `main_*.dart`
- DI seam implementing auth token logic instead of delegating to `flutter-state-and-data-fetching`
- Signing credentials embedded in `Fastfile` or CI yaml rather than referencing env vars
- Build not verified before declaring the scaffold complete
- `pubspec.lock` not committed
