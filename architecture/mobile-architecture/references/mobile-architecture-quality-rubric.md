# Mobile Architecture Quality Rubric

Load this before emitting `mobile-architecture.md`. Revise until each check passes or the unresolved gap is explicitly documented.

## Platform & application

- [ ] Platform strategy (native / cross-platform-native / hybrid) has rationale, trade-offs, and rejected alternatives, recorded as an ADR.
- [ ] Minimum OS versions and device classes (phone/tablet/foldable) are explicit.
- [ ] Application layers, module boundaries, concurrency, and lifecycle handling are defined without over-abstraction.

## Navigation & state

- [ ] Navigation hierarchy, route ownership, deep-link handling, and state restoration after interruption are defined.
- [ ] Local, session, cached-remote, and persistent state each name ownership, sync rule, persistence, and invalidation.
- [ ] Optimistic updates, conflict resolution, and rollback behavior are defined.

## Offline & device

- [ ] Offline behavior is defined for every critical user journey (works / partially works / fails gracefully).
- [ ] Sync model names authoritative sources, queueing, retry, conflict resolution, and reconciliation.
- [ ] Every device capability names permission strategy, fallback, privacy posture, battery impact, and failure handling.

## Performance, accessibility, notifications

- [ ] Performance and battery budgets state measurable targets and degradation behavior under low memory, poor connectivity, thermal throttling, and battery saver.
- [ ] Accessibility posture names screen-reader support, dynamic text, reduced motion, contrast, RTL, and font scaling.
- [ ] Notification and interruption policies (types, delivery, priority, opt-in, rate-limiting, silent push) are documented where notifications exist.

## Resilience, observability, testing

- [ ] Error handling defines retry ceilings, crash recovery, interrupted-session handling, and degraded-mode UX.
- [ ] The failure taxonomy covers each named failure with detection, mitigation, recovery, observability, and user-facing behavior.
- [ ] Observability includes crash, latency, startup, and release telemetry with PII redaction and sampling.
- [ ] Testing covers offline, accessibility, and device-compatibility, with release gating and rollback validation.

## Callouts, linkage, decisions

- [ ] Security/privacy and release/operations appear only as callouts / ADR candidates - no owned security or release design.
- [ ] `mobile-architecture.md` conforms to [architecture-schema](../../../standards/architecture-schema/README.md): frontmatter complete, required sections present, conditional sections present or omitted with rationale.
- [ ] Every ADR candidate has Context, Decision, Consequences (including downsides), and Alternatives considered.
- [ ] No vendor SDK implementation detail leaked into the architecture unless it materially changes architecture behavior.
- [ ] At least one weak-architecture risk was surfaced, or the design's intentional simplicity was explained.

## Failure handling

If a check fails:

1. Identify the missing or weak decision.
2. Ask the user for clarification if it cannot be inferred from `system-design.md` or the PRD.
3. Revise `mobile-architecture.md` or the relevant ADR.
4. Keep unresolved questions explicit; do not hide them as assumptions.
