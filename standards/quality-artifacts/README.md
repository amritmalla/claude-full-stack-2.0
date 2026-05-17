# quality-artifacts

Canonical structure for the quality artifacts produced by `skills/architecture/quality-engineering`: the risk-based testing strategy and its optional supporting matrices. Consumed by every `skills/implementations/*` skill that wires the strategy into a concrete test runner, and by CI/CD pipelines that enforce its gates.

`testing-strategy.md` is a quality/process artifact, not a `*-architecture.md`. It does not live under `docs/architecture/` and is not governed by [architecture-schema](../architecture-schema/README.md). It consumes the architecture documents; it does not redefine them.

## File layout

```
docs/quality/<product-or-service-slug>/
├── testing-strategy.md         # primary artifact, always present
├── matrices/                   # OPTIONAL — generated supporting matrices
│   ├── acceptance-criteria.md  #   PRD success metric → measurable acceptance behavior
│   ├── contract-test-matrix.md #   endpoint/event → success, negative, error, auth, idempotency
│   └── workflow-coverage.md    #   workflow → layer that validates it
└── adrs/
    └── NNNN-<slug>.md          # one per non-obvious testing/tooling decision, monotonic numbering
```

## `testing-strategy.md`

Primary artifact. One file per system or service under test.

### Frontmatter (required)

```yaml
---
product: <kebab-case slug>             # matches the system-design / PRD slug
status: draft | review | approved | superseded
owner: <name or role>
system_design: <relative path to source system-design.md>
prd: <relative path to source PRD, or null>
version: <semver, starts at 0.1.0>
last_reviewed: YYYY-MM-DD
---
```

### Required sections

| Section | Purpose | Gate |
|---|---|---|
| `## Overview` | System under test, critical workflows, what the strategy optimizes for and intentionally does not. | Names the system under test and its highest-risk workflows |
| `## Acceptance Criteria` | Table: each PRD success metric → observable behavior, measurable threshold, pass/fail expectation — or a documented non-testable rationale. | Every success metric mapped or explicitly waived |
| `## Risk Classification` | Table: risk, category (correctness, authorization, consistency, migration, performance, resilience, observability, integration drift, concurrency, recovery), severity, owning test layer. | Each risk maps to exactly one owning layer |
| `## Test Layers` | Per layer (unit, integration, contract, E2E, plus any conditional layers): scope, ownership, runtime budget, confidence target. | No two layers claim identical behavioral scope without justification |
| `## Contract Test Matrix` | Per externally visible contract (API, event, webhook): happy path, negative cases, error-envelope assertion, auth posture, idempotency, compatibility/versioning. | Every published contract row has success and failure validation |
| `## Integration Test Plan` | Production-like dependencies, topology, what may be mocked (only outside the service boundary), isolation, state reset, startup ordering. | No mock replaces a component inside the system boundary |
| `## Test Data & State Management` | Fixture generation, seed strategy, cleanup, deterministic reset, transaction boundaries, eventual-consistency handling. | Setup and cleanup are deterministic and reproducible |
| `## Authorization & Security Validation` | Tests for unauthenticated (401), authenticated-but-forbidden (403), insufficient scope, and cross-tenant denial where applicable. | 401 and 403 covered for protected surfaces |
| `## Observability Validation` | Validation of logs, metrics, traces, alerts, correlation IDs, and secret/token redaction. | Redaction is asserted; no test output leaks secrets |
| `## CI/CD Quality Gates` | Per suite: trigger, runtime budget, flake policy, blocking vs advisory, merge-gating vs release-gating, artifact retention. | Merge and release requirements are explicit |
| `## Implementation Handoffs` | Explicit handoffs to `skills/implementations/*`, `backend-architecture`, `frontend-architecture`, `data-architecture`, `security`, `reliability`, `operations`. | Each handoff is concrete and addressed to a named consumer |
| `## ADR Index` | Table: ADR number, Title, Status, Summary. Links to `adrs/NNNN-<slug>.md`. | Every testing/tooling ADR referenced |

### Conditional sections

Include if material; otherwise omit and add a one-line rationale under `## Omitted sections`.

| Section | When to include |
|---|---|
| `## Migration & Persistence Validation` | The system has schema changes or data migrations in scope. Must define migration verification, rollback, data-integrity checks, and expand/migrate/contract compatibility windows. |
| `## Resilience & Failure Validation` | The system has external dependencies, async workflows, or degraded-mode behavior. Must define dependency-outage, retry, timeout, partial-failure, and backpressure validation with expected user-visible degradation. |
| `## Performance & Scalability Validation` | The PRD or SLOs define latency, throughput, or concurrency targets. Must state measurable thresholds and where each is validated (pre-merge, pre-release, periodic). |

`testing-strategy.md` consumes `system-design.md`, the backend/frontend/data architecture documents, and the published contracts. It MUST NOT redefine bounded contexts, components, data flow, or API contracts — those remain owned by their source documents.

## ADRs

Testing and tooling decisions that are non-obvious (test-pyramid balance, contract-test tooling, production-like harness substrate, flake-quarantine policy) are recorded as ADRs under `adrs/NNNN-<slug>.md`, using the ADR markdown structure and immutability rules defined in [architecture-schema](../architecture-schema/README.md#adrs). Numbering is monotonic within the quality doc tree and independent of the system's architecture ADR numbering. ADRs are drafted inline as decisions are made, not retrofitted.

## Versioning

- Bump **patch** for typo / clarification edits.
- Bump **minor** for added suites, layers, gates, or ADRs.
- Bump **major** when the layering model or merge/release gate contract changes — requires re-approval and a superseding ADR.
- `testing-strategy.md` is immutable in spirit once `status: approved`; material changes go through a new version and, where they change the gate contract, a superseding ADR.

## Linkage contract

- `testing-strategy.md` MUST link to its source `system-design.md` and (when present) the PRD in frontmatter.
- Acceptance criteria MUST trace to PRD success metrics per [prd-schema](../prd-schema/README.md); a metric with no acceptance criterion MUST carry a documented non-testable rationale.
- Contract tests MUST assert the published contract per [api-standards](../api-standards/README.md): the standard error-envelope shape, status-code conventions, and the contract's idempotency mechanism for non-idempotent operations.
- Authorization validation MUST conform to [security-standards](../security-standards/README.md): unauthenticated, forbidden, and insufficient-scope cases where applicable.
- Observability validation MUST conform to [observability-standards](../observability-standards/README.md): structured signals emitted, secrets redacted.
- CI/CD gates MUST align with the promotion flow in [deployment-standards](../deployment-standards/README.md): the strategy declares which suites gate `dev → staging → production`.
- Once `testing-strategy.md` is `approved`, it is the upstream input to the test-implementation work in `skills/implementations/*`; those skills wire it into a runner but do not redefine its layering or gate contract.

## Anti-patterns

- Coverage targets stated without mapping each suite to a risk it reduces.
- Mocks replacing repositories, persistence adapters, or the system under test inside the service boundary.
- An end-to-end-only strategy compensating for absent integration or contract layers.
- Success-only test plans — no negative or edge-condition validation.
- Acceptance criteria invented independently of PRD success metrics, or stated as "works properly".
- Non-deterministic setup/cleanup, order-dependent tests, shared mutable fixtures.
- Contract evolution with no compatibility or versioning validation.
- CI pipelines with undefined merge or release gates ("green pipeline means safe release").
- Flaky tests normalized instead of quarantined with an owner.
- Redefining bounded contexts, components, or API contracts instead of consuming the architecture documents.
