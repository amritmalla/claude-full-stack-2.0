# Testing Strategy Quality Rubric

Load this before emitting `testing-strategy.md`. Revise until each check passes or the unresolved gap is explicitly documented.

## Acceptance criteria

- [ ] Every PRD success metric maps to a measurable acceptance criterion, or carries a documented non-testable rationale.
- [ ] Each criterion states observable behavior, a measurable threshold, and a pass/fail expectation.
- [ ] No criterion is invented independently of product outcomes; none reads "works properly".

## Risk and layering

- [ ] Risks are classified by category and severity; each maps to exactly one owning test layer.
- [ ] Each layer states scope, ownership, runtime budget, and confidence target.
- [ ] No two layers claim identical behavioral scope without justification.
- [ ] E2E tests are not used to compensate for missing integration or contract coverage.

## Contract validation

- [ ] Every externally visible contract has happy-path, negative, and edge-condition validation.
- [ ] Error responses are asserted against the [api-standards](../../../../standards/api-standards/README.md) error envelope and status conventions.
- [ ] Non-idempotent operations validate retry and idempotency using the contract's mechanism.
- [ ] Contract evolution defines compatibility and versioning validation.

## Integration realism

- [ ] Integration tests use production-like dependencies (real DB, queue, cache, middleware) in disposable containers wherever feasible.
- [ ] No mock replaces a component inside the system boundary; the mock boundary is explicit.
- [ ] Topology, isolation, state reset, and startup ordering are defined.

## Determinism and test data

- [ ] Setup and cleanup are deterministic, isolated, and reproducible.
- [ ] No order-dependent tests or shared mutable fixtures.
- [ ] Transaction boundaries and eventual-consistency handling are explicit; no rollback reliance across async boundaries.

## Authorization and observability

- [ ] Authorization validation covers 401, 403, insufficient scope, and cross-tenant denial where applicable, per [security-standards](../../../../standards/security-standards/README.md).
- [ ] Observability validation covers logs, metrics, traces, alerts, and correlation IDs.
- [ ] Secret/token redaction is asserted; no test output leaks secrets.

## Conditional validation

- [ ] Migration/persistence validation is present for schema or migration changes, or omitted with rationale.
- [ ] Resilience/failure validation is present for external dependencies or async workflows, or omitted with rationale.
- [ ] Performance/scalability validation defines measurable thresholds when SLOs exist, or is omitted with rationale.

## CI/CD gates

- [ ] Every suite declares trigger, runtime budget, flake policy, and release impact.
- [ ] Merge-gating vs release-gating and blocking vs advisory checks are explicit.
- [ ] Gates align with the `dev → staging → production` promotion flow ([deployment-standards](../../../../standards/deployment-standards/README.md)).
- [ ] Ownership for flaky suites, fixtures, and environment upkeep is assigned; no orphaned test infrastructure.

## Linkage and conformance

- [ ] Artifact conforms to [quality-artifacts](../../../../standards/quality-artifacts/README.md): file layout, frontmatter, required sections, conditional omissions justified under `## Omitted sections`.
- [ ] Frontmatter links the source `system-design.md` and PRD; bounded contexts, components, data flow, and contracts are consumed, not redefined.
- [ ] Every non-obvious testing/tooling decision has an inline ADR referenced from the ADR Index.
- [ ] At least one weak testing assumption was surfaced, or the quality posture of the system was explicitly affirmed.

## Failure handling

If a check fails:

1. Identify the missing or weak quality decision and the risk it leaves uncovered.
2. Ask the architecture or product owner for clarification if it cannot be inferred from the upstream documents.
3. Revise `testing-strategy.md`, the matrices, or the ADRs.
4. Keep unresolved questions explicit as open decisions with owners; do not hide them as assumptions or silently drop coverage.
