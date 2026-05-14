# testing-quality

> Status: draft

## Purpose

Validates correctness, reliability, and production readiness. Owns testing strategy, QA automation, validation pipelines, regression prevention, and contract testing.

Architecture-domain level. The *strategy* and *coverage decisions* are ecosystem-neutral; the *wiring* (specific test runners, fixtures, container libraries) lives in implementation skills under each `implementations/*` ecosystem.

## Owns

- Testing pyramid balance (unit / integration / contract / E2E)
- Coverage targets per tier
- Contract testing strategy
- Regression prevention policy
- Test data strategy
- Flake budget and quarantine policy

## Produces

| Artifact | Conforms to |
|---|---|
| Test plan per service | TBD |
| Integration test suite outline | consumed from API contracts ([api-standards](../../standards/api-standards/README.md)) |
| Acceptance criteria | derived from PRD Success Metrics ([prd-schema](../../standards/prd-schema/README.md)) |

## Skills

- [integration-test-strategy](integration-test-strategy/SKILL.md) — designs Testcontainers-backed integration test suites driven by API contracts. Currently Spring-Boot-flavored; generalization to other ecosystems is a follow-up.

## Standards this architecture domain conforms to

- [api-standards](../../standards/api-standards/README.md) — contract tests verify the published spec.
- [prd-schema](../../standards/prd-schema/README.md) — Success Metrics become acceptance criteria.
- [observability-standards](../../standards/observability-standards/README.md) — test runs emit structured signals into CI dashboards.
- [deployment-standards](../../standards/deployment-standards/README.md) — tests gate promotion through `dev → staging → production`.

## Upstream inputs

- Approved `system-design.md` (component boundaries shape test boundaries).
- Approved `openapi.yaml` (contract is the source of truth for endpoint tests).
- Approved `PRD.md` Success Metrics (become acceptance criteria).

## Downstream consumers

- [implementations/backend/*](../../implementations/backend/) — each ecosystem wires the test strategy into its own runner and fixture library.
- [implementations/infrastructure/*](../../implementations/infrastructure/) — CI pipelines invoke the suites declared here.
