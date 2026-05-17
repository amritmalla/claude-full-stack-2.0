# quality-engineering

> Status: draft

## Purpose

Turns an approved system design and its contracts into a production-grade, risk-based testing strategy before merge approval, release, or production promotion: acceptance criteria from PRD success metrics, a contract and integration test plan that avoids mocking the system under test, layered coverage by risk, observability and resilience validation, and CI/CD quality gates.

Technology-agnostic. Owns *what* must be tested, *at which layer*, and *with which production-like dependencies and gates* — not the framework that runs the tests. Runner wiring, fixtures, and container libraries live under [implementations/*](../../implementations/).

## Owns

- Risk-based test layering (unit / integration / contract / E2E and beyond)
- Acceptance criteria derived from PRD success metrics
- Contract testing strategy and the mock boundary
- Production-like integration harness expectations
- Test determinism, data, and state-reset policy
- Authorization, observability, resilience, and migration validation posture
- CI/CD merge and release gate contract; flake-quarantine policy

## Produces

| Artifact | Conforms to |
|---|---|
| `testing-strategy.md` | [quality-artifacts](../../../standards/quality-artifacts/README.md), [documentation-standards](../../../standards/documentation-standards/README.md) |
| Acceptance criteria matrix | [prd-schema](../../../standards/prd-schema/README.md) (Success Metrics) |
| Contract test matrix | [api-standards](../../../standards/api-standards/README.md) (published contract) |
| Testing/tooling ADRs | [quality-artifacts](../../../standards/quality-artifacts/README.md) (ADR rules, per [architecture-schema](../../../standards/architecture-schema/README.md#adrs)) |

## Skills

- [quality-engineering](SKILL.md) — turns an approved system design and contracts into a risk-based testing strategy: acceptance criteria, contract and integration test plans, CI/CD quality gates, and implementation handoff notes.

## Standards this architecture domain conforms to

- [quality-artifacts](../../../standards/quality-artifacts/README.md) — `testing-strategy.md` layout, frontmatter, sections, ADR linkage.
- [prd-schema](../../../standards/prd-schema/README.md) — Success Metrics become acceptance criteria.
- [api-standards](../../../standards/api-standards/README.md) — contract tests verify the published spec and error envelope.
- [security-standards](../../../standards/security-standards/README.md) — 401/403/scope/cross-tenant coverage.
- [observability-standards](../../../standards/observability-standards/README.md) — test runs emit structured signals; redaction asserted.
- [deployment-standards](../../../standards/deployment-standards/README.md) — gates align with `dev → staging → production`.
- [documentation-standards](../../../standards/documentation-standards/README.md) — skill structure.

## Upstream inputs

Triggered by an approaching merge, release, or production-promotion decision. Requires an approved `system-design.md` (and the backend/frontend/data architecture documents it spawned), the published `openapi.yaml` / event contracts, the PRD success metrics, and the persistence or migration plan. Component boundaries shape test boundaries; contracts are the source of truth for endpoint and event tests. The strategy consumes these documents and does not redefine them.

## Downstream consumers

- [implementations/*](../../implementations/) — each ecosystem wires the strategy into its own runner, fixtures, and harness; CI pipelines invoke the suites and enforce the gates declared here.
- [architecture/operations](../operations/README.md) — observability and alert validation feeds runbook and on-call readiness.
- [architecture/reliability](../reliability/SKILL.md) — resilience validation feeds SLO and error-budget work.
