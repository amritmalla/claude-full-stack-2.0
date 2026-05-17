# Flutter Performance and Reliability Quality Rubric

Load this before declaring the performance and reliability layer complete. Revise until each check passes or the unresolved gap is explicitly documented.

## Budgets

- [ ] Every budget (cold/warm start, transition latency, memory, background execution, battery, network, storage) is traceable to `mobile-architecture.md` / `architecture/performance` — none invented.
- [ ] Crash-free-rate and ANR/watchdog targets come from the architecture documents.
- [ ] Each budget is paired with its degradation behavior from the Failure Taxonomy / degraded-mode rows.
- [ ] A missing budget or vendor is recorded as a pending ADR candidate, not silently defaulted.

## Instrumentation

- [ ] Startup (cold/warm) and frame timing (jank/dropped frames) are instrumented through the scaffold `perf_tracer.dart` seam.
- [ ] Memory-pressure and battery/power telemetry route through the existing telemetry seam, tagged by flavor and device class.
- [ ] There is no second tracer or competing crash handler — the scaffold seams are consumed.
- [ ] No error-handling code (`runZonedGuarded`, `*.onError`, `ErrorWidget.builder`) is added or modified here.

## Reliability metrics

- [ ] Crash-free-rate and ANR/watchdog metrics come from the architecture-named release-monitoring vendor through the scaffold crash seam.
- [ ] Crash-free/ANR are treated as gated metrics, not as a handler concern.
- [ ] The observability vendor matches `mobile-architecture.md`, or a pending ADR candidate is documented.

## Graceful degradation

- [ ] Behavior under low memory matches the declared degraded-mode row.
- [ ] Behavior under poor connectivity matches the declared degraded-mode row.
- [ ] Behavior under battery saver matches the declared degraded-mode row.

## CI gates

- [ ] A build-failing CI gate enforces the startup-time budget.
- [ ] A build-failing CI gate enforces frame performance.
- [ ] A build-failing CI gate enforces the app-size budget.
- [ ] A build-failing CI gate enforces the crash-free-rate / ANR threshold (or the release-gating mechanism the vendor supports).
- [ ] Gates are attached to the existing Fastlane/Codemagic pipeline, not a separate unmonitored job.

## Verification

- [ ] All budget measurements were taken in profile/release mode (never debug).
- [ ] All budget measurements were taken on the lowest-end supported device, or the gap is documented.
- [ ] `flutter analyze` reports zero issues (warnings included), or the skip is documented with reason.

## Standards conformance

- [ ] [observability-standards](../../../../../../standards/observability-standards/README.md): startup, frame, memory, battery, crash-free, and ANR telemetry through the scaffold seams with environment and flavor tags.
- [ ] [deployment-standards](../../../../../../standards/deployment-standards/README.md): performance-regression and crash-free/ANR gates wired into CI as build-failing checks.
- [ ] [naming-conventions](../../../../../../standards/naming-conventions/README.md): trace, metric, and CI-gate naming.

## Failure handling

If a check fails:

1. Identify the missing budget, instrumentation, or gate.
2. Ask the user for clarification if a budget or the vendor cannot be inferred from `mobile-architecture.md` or `architecture/performance`.
3. Revise the instrumentation or gate, re-measure in profile/release on the floor device, and re-run `flutter analyze`.
4. Keep any unresolved gap explicit — do not hide it as an assumption.
