---
name: flutter-performance-and-reliability
description: Use when enforcing startup, frame, memory, and battery budgets, instrumenting performance and reliability telemetry, or adding performance-regression and crash-free/ANR CI gates to a Flutter application after the app scaffold exists and mobile architecture is approved or intentionally deferred. Produces budget definitions from mobile-architecture.md, profiling and telemetry wired through the scaffold's tracing and crash seams, crash-free-rate and ANR/watchdog gated metrics, graceful-degradation posture verification, and CI gates that fail the build on regression. Does not own error-handling code (that stays in app-scaffold-and-runtime) or the observability vendor decision (that stays in mobile-architecture.md). Do not use for app scaffolding, navigation, state management, or design-system integration; use the other Flutter archetype skills instead.
---

# Flutter Performance and Reliability

## When to use

Invoke when defining and enforcing performance budgets for a scaffolded Flutter app, instrumenting startup/frame/memory/battery and crash-free/ANR telemetry, adding performance-regression CI gates, or verifying graceful-degradation behavior under low memory, poor network, and battery saver.

Do not use for: app scaffolding or the error-handling layers themselves (use `flutter-app-scaffold-and-runtime`); navigation, state, or design-system work (use the respective Flutter archetype skills). This skill gates those archetypes; it does not implement them.

## Inputs

Required:

- A scaffolded Flutter app with the performance-tracing seam (`perf_tracer.dart`) and crash-reporting seam (`crash_reporter.dart`) in place.
- Approved `mobile-architecture.md`, or explicit confirmation that mobile architecture is intentionally deferred.

Optional:

- Approved `architecture/performance` budgets and methodology where they extend or override the mobile-architecture budgets.
- Target device matrix, especially the lowest-end supported device (the budget is set there, not on a flagship).
- CI system already scaffolded (Fastlane/Codemagic) to attach gates to.
- Release-monitoring vendor capability for crash-free-rate and ANR (consumed, not chosen here).

## Operating rules

- Never generate vanity metrics. A budget that is not gated in CI and not measured on the lowest-end supported device is decoration, not a budget.
- Consume `mobile-architecture.md` and `architecture/performance`; do not invent budgets. Cold/warm start, transition latency, memory, background, battery, network, and storage budgets — and the crash-free/ANR targets — belong to those documents. If a needed budget is missing, pause and raise an ADR candidate rather than inventing a number.
- Consume the scaffold seams; do not re-implement them. Telemetry routes through the existing `perf_tracer.dart` and `crash_reporter.dart`. This skill does not add a second tracer or a competing crash handler.
- Error-handling code is out of scope. `runZonedGuarded`, `PlatformDispatcher.onError`, `FlutterError.onError`, and `ErrorWidget.builder` are owned by `flutter-app-scaffold-and-runtime`. This skill measures and gates crash-free-rate and ANR as metrics; it does not own the handlers.
- The observability vendor is consumed, not chosen. The crash-free/ANR/perf signal comes from the vendor named in `mobile-architecture.md`. A missing vendor is an ADR candidate, not a default.
- Budgets are measured on the lowest-end supported device. A 120Hz flagship hides the jank a 3-year-old Android shows. Profiling and gate thresholds reference the floor of the device matrix.
- Every budget has a defined degradation behavior. The budget is paired with what the app does when it is exceeded (per the Failure Taxonomy / degraded-mode rows) — not just a number that fails CI.
- Performance work is verified in profile/release mode, never debug. Debug-mode timings are meaningless; all measurements use `flutter run --profile` or release builds.
- A regression gate fails the build, not a dashboard. Startup, frame, bundle/size, and crash-free/ANR gates are wired into CI as build-failing checks with explicit thresholds.
- A budget without a CI gate and a lowest-end-device measurement is not done.

## Output contract

The generated performance and reliability layer MUST conform to:

- [observability-standards](../../../../standards/observability-standards/README.md) — startup, frame, memory, battery, crash-free-rate, and ANR telemetry routed through the scaffold seams with environment and flavor tags.
- [deployment-standards](../../../../standards/deployment-standards/README.md) — performance-regression and crash-free/ANR gates wired into the CI pipeline as build-failing checks.
- [naming-conventions](../../../../standards/naming-conventions/README.md) — trace, metric, and CI-gate naming.

Upstream contract: `mobile-architecture.md` and `architecture/performance` are the source of truth for all budgets and the crash-free/ANR targets; `mobile-architecture.md` is the source of truth for the observability vendor. If a needed budget or the vendor is missing, pause and raise an ADR candidate rather than inventing it.

## Progressive references

- Read `references/flutter-performance-playbook.md` when implementing any owned area or checking the anti-pattern list.
- Read `references/flutter-performance-quality-rubric.md` before declaring the performance layer complete.
- Use `assets/flutter-performance.template.md` as the budget, instrumentation, and CI-gate reference.

## Process

1. Gather context: load `mobile-architecture.md` and extract the Performance & Battery Budgets table, the degraded-mode/Failure Taxonomy rows, and the Observability & Analytics signals (startup & battery telemetry, performance telemetry, release monitoring, crash-free/ANR). Layer in `architecture/performance` where it extends those. Confirm the scaffold `perf_tracer.dart` and `crash_reporter.dart` seams and the device matrix floor. If a budget or the vendor is missing, raise an ADR candidate before proceeding.
2. Budget definition: encode each budget (cold/warm start, transition latency, memory, background execution, battery, network, storage) and the crash-free-rate and ANR/watchdog targets as explicit thresholds paired with their degradation behavior.
3. Startup & frame instrumentation: instrument cold/warm start and frame timings (jank / dropped frames) through the scaffold `perf_tracer.dart` seam — no second tracer.
4. Memory & battery telemetry: wire memory-pressure and battery/power signals through the existing telemetry seam, tagged by flavor and device class.
5. Reliability metrics: wire crash-free-rate and ANR/watchdog signals from the architecture-named release-monitoring vendor through the scaffold crash seam — measuring, not handling.
6. Graceful-degradation verification: verify the declared degraded-mode behavior under low memory, poor connectivity, and battery saver matches the Failure Taxonomy rows.
7. CI regression gates: add build-failing CI checks for startup time, frame performance, app-size, and crash-free/ANR thresholds, attached to the existing Fastlane/Codemagic pipeline.
8. Profiling verification: measure in profile/release mode on the lowest-end supported device; confirm each budget holds or document the gap. Run `flutter analyze` (zero issues).
9. Standards validation: check observability-standards (telemetry through seams), deployment-standards (gates in CI), naming-conventions. Document any unresolved gap explicitly.

## Outputs

Required:

- Encoded budgets and crash-free/ANR targets, each paired with a degradation behavior.
- Startup and frame instrumentation through the scaffold tracing seam.
- Memory and battery telemetry through the existing telemetry seam.
- Crash-free-rate and ANR/watchdog metrics from the architecture-named vendor (measured, not handled).
- Graceful-degradation verification under low memory, poor network, and battery saver.
- Build-failing CI gates for startup, frame, app-size, and crash-free/ANR thresholds.
- Profiling evidence from the lowest-end supported device.

Output rules:

- No second tracer or competing crash handler — the scaffold seams are consumed.
- No error-handling code — that ownership stays with `flutter-app-scaffold-and-runtime`.
- No invented budgets or vendor defaults — missing inputs are ADR candidates.
- All measurements are profile/release on the device-matrix floor, never debug on a flagship.

## Quality checks

- [ ] `flutter analyze` reports zero issues.
- [ ] Every budget (start, transition, memory, background, battery, network, storage) and the crash-free/ANR targets come from `mobile-architecture.md` / `architecture/performance` — none invented.
- [ ] Each budget is paired with its degradation behavior from the Failure Taxonomy / degraded-mode rows.
- [ ] Startup, frame, memory, and battery telemetry route through the scaffold `perf_tracer.dart` seam — no second tracer.
- [ ] Crash-free-rate and ANR/watchdog metrics come from the architecture-named vendor through the scaffold crash seam; no error-handling code is added here.
- [ ] Graceful degradation under low memory, poor connectivity, and battery saver matches the declared behavior.
- [ ] CI has build-failing gates for startup time, frame performance, app-size, and crash-free/ANR thresholds.
- [ ] All measurements were taken in profile/release mode on the lowest-end supported device, or the gap is documented.
- [ ] The observability vendor matches `mobile-architecture.md`, or a pending ADR candidate is documented.

## References

- Upstream: [`architecture/mobile-architecture`](../../../../architecture/mobile-architecture/SKILL.md), [`architecture/performance`](../../../../architecture/performance/SKILL.md).
- Baseline this skill consumes: `flutter-app-scaffold-and-runtime` (perf-tracing and crash-reporting seams; error-handling code owner).
- Gates (does not implement): `flutter-navigation-and-routing`, `flutter-state-and-data-fetching`, `flutter-design-system-and-accessibility`.
- Standards: [`observability-standards`](../../../../standards/observability-standards/README.md), [`deployment-standards`](../../../../standards/deployment-standards/README.md), [`naming-conventions`](../../../../standards/naming-conventions/README.md).
