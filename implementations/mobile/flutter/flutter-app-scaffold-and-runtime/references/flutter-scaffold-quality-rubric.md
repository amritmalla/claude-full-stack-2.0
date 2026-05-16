# Flutter App Scaffold Quality Rubric

Load this before declaring the scaffold complete. Revise until each check passes or the unresolved gap is explicitly documented in the local-run README.

## Project layout and flavors

- [ ] `pubspec.yaml` has all dependencies pinned — no `^` constraints anywhere.
- [ ] `pubspec.lock` is committed.
- [ ] `analysis_options.yaml` is present with strict lints.
- [ ] Flavor entry points exist: `main_dev.dart`, `main_staging.dart`, `main_prod.dart`.
- [ ] `app_config.dart` defines a `Flavor` enum and flavor-specific constants (app name, bundle ID suffix, API base URL slot).
- [ ] Android `build.gradle` has a `productFlavors` block for dev/staging/prod.
- [ ] iOS has scheme targets or equivalent flavor separation (Dev/Staging/Prod).
- [ ] `.gitignore` covers `.env`, signing artifacts (`*.jks`, `*.p12`, `*.mobileprovision`), `key.properties`, `google-services.json` with real credentials, `build/`, `.dart_tool/`.
- [ ] `.env.example` documents all required environment variables with placeholder values only.

## Error handling

- [ ] `runZonedGuarded` wraps `runApp` in each `main_*.dart` and routes unhandled async errors to `CrashReporter.recordError`.
- [ ] `PlatformDispatcher.instance.onError` is assigned a handler that logs and reports.
- [ ] `FlutterError.onError` is overridden to log and report (non-fatal in non-dev flavors).
- [ ] `ErrorWidget.builder` is overridden to render a safe fallback widget.
- [ ] The fallback widget does not expose stack traces or internal state in staging or prod flavors.
- [ ] All four layers are called from `setupErrorHandlers()` before `runApp`.

## Observability

- [ ] Crash reporting is initialized in each `main_*.dart` before `runApp`, with flavor-aware configuration (dev and prod streams are separate).
- [ ] Structured logging client is level-aware and flavor-aware (debug logs suppressed in prod).
- [ ] Performance tracing seam is initialized and exposes `startTrace`/`stopTrace` for downstream archetypes to instrument.
- [ ] No PII field names (`email`, `token`, `password`, `userId`) appear in default log output.
- [ ] If the observability vendor is deferred, a no-op stub implementing the same interface is in place.

## DI and session seam

- [ ] DI container matches the one named in `mobile-architecture.md`, or is documented as deferred with a pending ADR candidate.
- [ ] Auth session provider shell is registered and typed.
- [ ] Token storage, refresh, and protected-route gates are explicitly marked with TODO comments naming `flutter-state-and-data-fetching` and `flutter-navigation-and-routing` as owners.
- [ ] No token or auth implementation logic exists in the scaffold (seam only).

## CI and signing

- [ ] Signing configuration references environment variables only — no credentials committed anywhere in the repository.
- [ ] Fastlane or CI yaml has flavor-aware build lanes.
- [ ] `fastlane/README.md` (or equivalent) lists every required environment variable, its purpose, and where to source it in CI.
- [ ] `fastlane/Gemfile` pins the `fastlane` gem version.

## Build verification

- [ ] `flutter analyze` reports zero issues (warnings included).
- [ ] `flutter build apk --flavor dev` succeeds, or the skip is documented with reason.
- [ ] `flutter build ios --no-codesign --flavor dev` succeeds, or the skip is documented with reason.

## Standards conformance

- [ ] [security-standards](../../../../../standards/security-standards/README.md): no secrets in bundle or committed config; signing via env vars.
- [ ] [observability-standards](../../../../../standards/observability-standards/README.md): crash reporting, structured logging, and performance tracing seam wired with flavor tags.
- [ ] [deployment-standards](../../../../../standards/deployment-standards/README.md): env-agnostic build via Flutter flavor mechanism; no per-environment source branches; no build-time-baked credentials.

## Failure handling

If a check fails:

1. Identify the missing or incorrect implementation.
2. Ask the user for clarification if the decision cannot be inferred from `mobile-architecture.md` or `architecture/security`.
3. Revise the scaffold file, re-run `flutter analyze`, and re-run the flavor build.
4. Keep any unresolved gap explicit in the local-run README — do not hide it as an assumption.
