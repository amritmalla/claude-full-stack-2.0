# Flutter Performance and Reliability Playbook

Load this when implementing any owned area of `flutter-performance-and-reliability` or checking the anti-pattern list. It expands the operating rules and process steps in `SKILL.md` with the detail needed to produce production-grade, gated performance and reliability work.

## Why this workflow exists

Performance and reliability regress silently. A feature merge adds 400ms to cold start; nobody notices on a flagship in debug mode; a month later the install-to-first-screen funnel has quietly collapsed. An unhandled jank source drops the scroll to 40fps only on the cheap Android that 60% of the user base actually owns. Crash-free rate slips from 99.8% to 99.1% and the only signal is a slow bleed of one-star reviews. None of this is caught by a developer running the app once on a fast device.

The goal is budgets that come from architecture, telemetry through the existing scaffold seams, and CI gates that fail the build the moment a regression lands — measured where users actually are, on the floor of the device matrix.

## Behavioral rules in depth

### 1. Consume budgets; do not invent them

The Performance & Battery Budgets table in `mobile-architecture.md` (extended by `architecture/performance`) is the source of truth for every threshold, including the crash-free-rate and ANR targets in Observability & Analytics. A number you made up is not a budget. If a budget is missing, raise an ADR candidate.

### 2. Consume the scaffold seams — never a second tracer

The scaffold installed `perf_tracer.dart` (with `startTrace`/`stopTrace`) and `crash_reporter.dart`. All instrumentation routes through them. A second tracing library or a competing crash handler splits the signal and produces two dashboards that disagree.

### 3. Error-handling code is not yours

`runZonedGuarded`, `PlatformDispatcher.onError`, `FlutterError.onError`, and `ErrorWidget.builder` are `flutter-app-scaffold-and-runtime`'s ownership. This skill consumes the crash *signal* those layers feed and turns crash-free-rate and ANR into gated metrics. It does not add, move, or rewrite a handler. Crossing this line duplicates the error pipeline.

### 4. The observability vendor is consumed, not chosen

Crash-free-rate, ANR, and release monitoring come from the vendor named in `mobile-architecture.md`. If the vendor is `none`/deferred, the metric path is a documented gap with a pending ADR candidate — not a default library this skill picks.

### 5. Measure on the floor of the device matrix

The budget is met on the lowest-end supported device or it is not met. A 120Hz flagship absorbs jank and masks memory pressure that a 3-year-old budget Android surfaces immediately. Profiling sessions and CI gate thresholds reference that floor device.

### 6. Every budget has a degradation behavior

A budget is `{threshold, what-the-app-does-when-exceeded}`. The "what it does" comes from the Failure Taxonomy and degraded-mode rows in `mobile-architecture.md` — drop image quality under memory pressure, defer non-critical sync under battery saver, show a lightweight skeleton when start exceeds budget. A bare number with no degradation path is half a budget.

### 7. Profile/release only — debug timings are noise

Debug mode disables compiler optimizations and adds assertion overhead; its timings are meaningless. Every measurement uses `flutter run --profile` or a release build. A budget "verified" in debug is unverified.

### 8. A gate fails the build, not a dashboard

Startup, frame, app-size, and crash-free/ANR gates are CI checks with explicit thresholds that fail the pipeline. A dashboard nobody is paged on is not a gate; a regression that merges green is not gated.

### 9. A budget without a gate and a floor-device measurement is not done

The two checks that make a budget real: it is enforced by a build-failing CI gate, and it has been measured in profile/release on the lowest-end supported device. Without both, it is aspirational.

## Step detail

**Step 1 — Gather context.** Load `mobile-architecture.md`; extract the Performance & Battery Budgets table, the degraded-mode/Failure Taxonomy rows, and the Observability & Analytics signals (startup/battery telemetry, performance telemetry, release monitoring, crash-free/ANR). Layer in `architecture/performance`. Confirm the scaffold `perf_tracer.dart`/`crash_reporter.dart` seams and the device-matrix floor. Raise an ADR candidate for any missing budget or vendor.

**Step 2 — Budget definition.** Encode each budget and the crash-free/ANR targets as explicit thresholds, each paired with its degradation behavior from the Failure Taxonomy rows.

**Step 3 — Startup & frame instrumentation.** Instrument cold/warm start spans and frame timing (jank/dropped frames) through `perf_tracer.dart`. No second tracer.

**Step 4 — Memory & battery telemetry.** Wire memory-pressure and battery/power signals through the existing telemetry seam, tagged by flavor and device class.

**Step 5 — Reliability metrics.** Wire crash-free-rate and ANR/watchdog from the architecture-named vendor through the scaffold crash seam — measuring only.

**Step 6 — Graceful-degradation verification.** Exercise low memory, poor connectivity, and battery saver; confirm behavior matches the declared degraded-mode rows.

**Step 7 — CI regression gates.** Add build-failing CI checks for startup, frame, app-size, and crash-free/ANR thresholds, attached to the existing Fastlane/Codemagic pipeline.

**Step 8 — Profiling verification.** Measure in profile/release on the lowest-end supported device; confirm each budget or document the gap. Run `flutter analyze`.

**Step 9 — Standards validation.** Check observability-standards (telemetry through seams), deployment-standards (gates in CI), naming-conventions. Keep gaps explicit.

## Anti-patterns to detect

Call these out explicitly when found:

- Invented budget numbers not traceable to `mobile-architecture.md` / `architecture/performance`
- A second tracing library or competing crash handler instead of the scaffold seams
- This skill adding/moving/rewriting error-handling layers owned by the scaffold
- Picking an observability vendor instead of consuming the architecture decision
- Budgets measured on a flagship and/or in debug mode
- A budget with a threshold but no degradation behavior
- "Gates" that are dashboards/alerts, not build-failing CI checks
- Regression that can merge green because no gate enforces the budget
- Crash-free/ANR treated as a handler concern rather than a gated metric
- Budget declared done with no floor-device, profile/release measurement
