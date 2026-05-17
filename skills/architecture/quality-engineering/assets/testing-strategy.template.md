---
product: <kebab-case slug>             # matches the system-design / PRD slug
status: draft                          # draft | review | approved | superseded
owner: <name or role>
system_design: <relative path to source system-design.md>
prd: <relative path to source PRD, or null>
version: 0.1.0
last_reviewed: YYYY-MM-DD
---

# Testing Strategy: [System or Service Name]

## Overview

[System under test, critical workflows, what this strategy optimizes for and what it intentionally does not cover. Name the highest-risk workflows.]

## Acceptance Criteria

| PRD Success Metric | Observable Behavior | Measurable Threshold | Pass/Fail Expectation |
|---|---|---|---|
| [Metric] | [Behavior] | [Threshold] | [Expectation] |

Non-testable metrics:

- [Metric] — [why it cannot be tested and how it is otherwise assured]

## Risk Classification

| Risk | Category | Severity | Owning Test Layer |
|---|---|---|---|
| [Risk] | [correctness / authorization / consistency / migration / performance / resilience / observability / integration drift / concurrency / recovery] | [high/med/low] | [layer] |

## Test Layers

| Layer | Scope | Ownership | Runtime Budget | Confidence Target |
|---|---|---|---|---|
| Unit | [scope] | [owner] | [budget] | [target] |
| Integration | [scope] | [owner] | [budget] | [target] |
| Contract | [scope] | [owner] | [budget] | [target] |
| End-to-end | [scope] | [owner] | [budget] | [target] |

## Contract Test Matrix

| Contract | Happy Path | Negative Cases | Error Envelope | Auth Posture | Idempotency | Compatibility |
|---|---|---|---|---|---|---|
| [API/event/webhook] | [test] | [tests] | [assertion] | [401/403/scope] | [mechanism] | [versioning rule] |

## Integration Test Plan

- Production-like dependencies: [DB, queue, cache, middleware — how provisioned]
- Topology: [production-like shape]
- Mock boundary: [only external systems X, Y — nothing inside the service boundary]
- Isolation & state reset: [mechanism]
- Startup ordering & lifecycle: [order]

## Test Data & State Management

- Fixture generation: [strategy]
- Seed strategy: [strategy]
- Deterministic cleanup: [mechanism]
- Transaction boundaries: [behavior]
- Eventual-consistency handling: [reconciliation approach]

## Authorization & Security Validation

| Surface | Unauthenticated (401) | Forbidden (403) | Insufficient Scope | Cross-Tenant Denial |
|---|---|---|---|---|
| [Surface] | [test] | [test] | [test] | [test] |

## Observability Validation

- Logs: [structured-log assertions]
- Metrics: [emission assertions]
- Traces: [propagation assertions]
- Alerts: [generation assertions]
- Correlation IDs: [assertion]
- Redaction: [secret/token redaction assertion]

## Migration & Persistence Validation

> Conditional — include only when schema changes or data migrations are in scope; otherwise omit and record under `## Omitted sections`.

- Migration verification: [approach]
- Rollback testing: [approach]
- Data-integrity validation: [checks]
- Expand/migrate/contract compatibility windows: [windows]

## Resilience & Failure Validation

> Conditional — include only when the system has external dependencies, async workflows, or degraded-mode behavior; otherwise omit and record under `## Omitted sections`.

| Failure | Validation | Expected User-Visible Degradation |
|---|---|---|
| [dependency outage / timeout / partial failure / backpressure / cache loss] | [test] | [degradation] |

## Performance & Scalability Validation

> Conditional — include only when latency/throughput/concurrency SLOs exist; otherwise omit and record under `## Omitted sections`.

| Target | Threshold | Validated Where |
|---|---|---|
| [latency/throughput/concurrency] | [measurable threshold] | [pre-merge / pre-release / periodic] |

## CI/CD Quality Gates

| Suite | Trigger | Runtime Budget | Flake Policy | Blocking? | Gates | Artifacts |
|---|---|---|---|---|---|---|
| [suite] | [per-PR / pre-release / periodic] | [budget] | [policy] | [blocking/advisory] | [merge / release] | [retained artifacts] |

## Implementation Handoffs

- `implementations/*` (test runner & fixtures): [what to wire, which suites]
- `backend-architecture`: [contract/workflow validation expectations]
- `frontend-architecture`: [client-side validation expectations]
- `data-architecture`: [migration/consistency validation expectations]
- `security`: [auth/tenant validation expectations]
- `reliability`: [resilience/SLO validation expectations]
- `operations`: [observability/alert validation expectations]

## Omitted sections

- [Conditional section name] — [one-line rationale for omission]

## ADR Index

| ADR | Title | Status | Summary |
|---|---|---|---|
| [NNNN](adrs/NNNN-<slug>.md) | [Decision title] | [proposed/accepted/superseded] | [one-line summary] |

## Open Decisions

- [Decision requiring product or architecture owner, with owner and target date]
