# Flutter Performance and Reliability — Layout Reference

Use this as the canonical budget, instrumentation, and CI-gate reference. These files are **added to** the scaffold tree and consume the scaffold's tracing/crash seams; they do not replace them. Placeholder tokens use `<kebab-case>` or `<PascalCase>`.

## Directory tree (added to the scaffold)

```
<app-name>/
├── lib/
│   └── core/
│       └── performance/
│           ├── budgets.dart            # thresholds from mobile-architecture.md
│           ├── startup_trace.dart      # uses scaffold perf_tracer.dart seam
│           └── degradation.dart        # degraded-mode behavior per Failure Taxonomy
├── perf/
│   ├── startup_benchmark.dart          # `flutter run --profile` driven
│   └── thresholds.yaml                 # machine-readable gate thresholds
└── fastlane/ (or codemagic.yml)
    └── Fastfile                        # EXTEND with build-failing perf gates
```

## Budgets come from architecture — never invented

```dart
// core/performance/budgets.dart
// Every value below is copied from the Performance & Battery Budgets table
// in mobile-architecture.md / architecture/performance. No literals invented here.
abstract final class Budgets {
  static const coldStartMs       = 2200;   // <- mobile-architecture.md
  static const warmStartMs       = 900;
  static const transitionMs      = 300;
  static const memoryMb          = 180;
  static const crashFreeRatePct  = 99.5;   // <- Observability & Analytics
  static const anrRatePct        = 0.47;
}
```

## Instrument through the scaffold seam — no second tracer

```dart
// CORRECT: reuse the scaffold's perf_tracer.dart
PerfTracer.startTrace('cold_start');
// ... first frame ...
PerfTracer.stopTrace('cold_start');   // exported to the architecture-named vendor

// WRONG: adding a second tracing SDK / competing crash handler.
```

## Budget paired with degradation behavior

```dart
// core/performance/degradation.dart
// The threshold AND what the app does when exceeded (Failure Taxonomy rows).
void onMemoryPressure(MemoryLevel level) {
  if (level.usedMb > Budgets.memoryMb) {
    imageCache.clearLiveImages();        // declared degraded-mode behavior
    _disableNonCriticalAnimations();
  }
}
```

## Reliability as a gated metric — not a handler

```dart
// This skill consumes the crash signal the scaffold's error layers feed and
// turns it into a gated metric. It does NOT add runZonedGuarded / *.onError.
final crashFree = await ReleaseMonitor.crashFreeRate();   // architecture vendor
final anr       = await ReleaseMonitor.anrRate();
// -> compared against Budgets.* in the CI gate below.
```

## CI gate fails the build — not a dashboard

```ruby
# fastlane/Fastfile  (extend the scaffold's pipeline)
lane :perf_gate do
  cold = measure_cold_start(flavor: "prod")          # profile build, floor device
  UI.user_error!("cold start #{cold}ms > #{2200}ms") if cold > 2200

  size = apk_size_mb
  UI.user_error!("app size #{size}MB over budget") if size > APP_SIZE_BUDGET

  cf = release_monitor_crash_free_rate
  UI.user_error!("crash-free #{cf}% < 99.5%") if cf < 99.5
end
```

```yaml
# perf/thresholds.yaml — machine-readable, sourced from architecture budgets
cold_start_ms: 2200
warm_start_ms: 900
app_size_mb: 60
crash_free_rate_pct: 99.5
anr_rate_pct: 0.47
measured_on: "<lowest-end supported device>"   # never a flagship
build_mode: profile                            # never debug
```

## Seams this skill consumes and gates

| Seam | Source | Status |
|---|---|---|
| Performance tracing | scaffold `perf_tracer.dart` | consumed (no second tracer) |
| Crash/ANR signal | scaffold `crash_reporter.dart` + architecture vendor | consumed as a gated metric |
| Error-handling layers | scaffold `error_handler.dart` | NOT owned here |
| Observability vendor | `mobile-architecture.md` | consumed, not chosen |
| CI pipeline | scaffold Fastlane/Codemagic | extended with build-failing gates |
| Nav / state / design-system perf | other archetype skills | gated, not implemented |
