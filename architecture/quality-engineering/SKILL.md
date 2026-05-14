---
name: quality-engineering
description: Use when a service needs a production-grade testing strategy before
  merging or promoting a feature. Produces a contract-driven test plan,
  acceptance criteria from product success metrics, and an integration test
  harness plan that avoids fragile mocks of the system under test.
---

# Quality Engineering

## When to use

Invoke after the PRD, system design, API contract, and persistence model are defined, and before merging the first production-bound feature or promoting a service through CI. Use this skill to decide what must be tested, at which layer, and with which production-like dependencies. Do not use it for isolated unit-test implementation or one-off test debugging.

## Inputs

- Approved PRD with success metrics.
- Approved system design and backend architecture.
- OpenAPI spec or equivalent service contract.
- Persistence schema or migration plan.
- Existing test structure, CI constraints, and known risk areas.

## Output contract

`testing-strategy.md` and any generated test harness guidance MUST conform to:

- [api-standards](../../standards/api-standards/README.md): every endpoint in the published contract is tested; tests assert the standard error envelope shape and status-code conventions; idempotency tests for non-idempotent endpoints use the contract's idempotency mechanism.
- [prd-schema Success Metrics](../../standards/prd-schema/README.md): acceptance criteria derive from the PRD's success metrics.
- [security-standards](../../standards/security-standards/README.md): auth tests cover unauthenticated, authenticated-but-forbidden, and scope-insufficient cases where applicable.
- [observability-standards](../../standards/observability-standards/README.md): test runs emit structured signals; no test logs leak secrets or tokens.

Upstream inputs come from the approved PRD, `system-design.md`, backend architecture, `openapi.yaml` or equivalent contract, and active database schema migrations. Do not invent endpoints, states, scopes, or success metrics.

## Process

1. Trace PRD success metrics and backend contract behavior into acceptance criteria.
2. Classify risks by test layer: unit, integration, contract, end-to-end, migration, security, and observability checks.
3. For each endpoint, workflow, or externally visible behavior, define at least one happy-path test and the required negative cases.
4. Select production-like dependencies for integration tests. Prefer real infrastructure in disposable containers for databases, queues, caches, and contract-critical middleware.
5. Define test data setup and teardown. Reset state deterministically between tests; do not rely on transactional rollback when testing behavior that spans transactions.
6. Define what may be mocked. Do not mock components under test such as repositories, persistence adapters, or domain services; mock only external systems outside the service boundary.
7. Specify CI gates: which suites run on every PR, which run before release, time budgets, flake handling, and required artifacts.
8. Emit `testing-strategy.md` and any ecosystem-specific harness notes or file-level implementation guidance.

## Outputs

- `testing-strategy.md`.
- Acceptance criteria mapped to PRD success metrics.
- Contract and integration test matrix by endpoint or workflow.
- Harness guidance for production-like dependencies, test data, and CI gates.

## Quality checks

- [ ] Every PRD success metric maps to at least one acceptance criterion or documented non-testable metric.
- [ ] Every endpoint or externally visible workflow has at least one happy-path and one negative test.
- [ ] Non-idempotent operations have an idempotency test using the contract's idempotency mechanism.
- [ ] Auth tests cover 401 (unauthenticated) and 403 (authenticated but forbidden), per [security-standards](../../standards/security-standards/README.md).
- [ ] Error responses are asserted against the [api-standards](../../standards/api-standards/README.md) error envelope shape.
- [ ] No mocks replace components inside the system under test.
- [ ] Test data setup and cleanup are deterministic.
- [ ] CI gates declare which suites are required before merge and before release.

## References

(None in v0.1.)
