# Testing Strategy Playbook

Load this when classifying risk, deriving acceptance criteria, designing the contract and integration matrices, defining determinism and CI gates, or checking the anti-pattern list. It expands the operating rules and process steps in `SKILL.md` with the detail needed to produce a production-grade `testing-strategy.md`.

## Why this workflow exists

Quality engineering exists to ensure systems behave correctly, safely, reliably, and observably under real operating conditions before production exposure. It is not about maximizing test count. It is about reducing production risk, validating externally visible behavior, enforcing architectural contracts, detecting regressions early, ensuring operational confidence, and aligning verification with product outcomes.

The goal is confidence, determinism, maintainability, and production realism — not mock-heavy test theater, brittle snapshot suites, or coverage metrics disconnected from business risk.

## Behavioral rules in depth

### 1. Product outcomes drive testing

Testing starts from user-visible behavior, PRD success metrics, contracts, workflows, and operational risks. Every major test suite MUST justify which risk it reduces and which business or system behavior it validates. Reject coverage-driven testing without behavioral intent.

### 2. Test the contract, not the implementation

Externally visible behavior is the contract. Tests SHOULD validate APIs, workflows, events, state transitions, persistence guarantees, and operational outcomes. Reject tests tightly coupled to internal implementation details.

### 3. Production realism beats mock-heavy isolation

Integration tests SHOULD use real databases, queues, caches, middleware, and production-like infrastructure wherever feasible. Mock ONLY systems outside the service boundary, uncontrollable third-party dependencies, or failure scenarios impractical to reproduce safely. Reject mocking repositories, persistence adapters, business-critical infrastructure, or the entire system under test.

### 4. Success and failure validation for every externally visible behavior

Every endpoint, workflow, event flow, and state transition MUST define happy-path validation, negative validation, and edge-condition behavior. Reject success-only test plans.

### 5. Acceptance criteria derive from PRD metrics

Acceptance criteria MUST trace back to user goals, latency targets, correctness expectations, reliability posture, and operational SLOs. Reject acceptance criteria invented independently of product outcomes, or criteria like "works properly".

### 6. Quality is layered

Define responsibility by layer: unit, integration, contract, end-to-end, migration, observability, resilience, security, performance. Each layer exists to reduce a specific class of risk. Reject duplicated coverage across layers without justification.

### 7. Determinism is mandatory

Test environments MUST define deterministic setup, deterministic teardown, isolated state, and reproducible execution. Reject order-dependent tests, shared mutable state, and hidden environmental assumptions. Do not rely on transactional rollback when the behavior under test spans asynchronous boundaries.

### 8. CI/CD gates are architecture

Quality gates define deployment confidence, release risk tolerance, and operational maturity. Every suite MUST define execution trigger, runtime budget, flake policy, and release impact. Reject undefined release criteria and "green pipeline means safe release" assumptions.

### 9. Observability is testable behavior

Systems are NOT production-ready unless tests validate logs, metrics, traces, alerts, and operational diagnostics, including correlation IDs and secret redaction. Reject systems observable only during failure investigations, and any test output that leaks secrets or tokens.

### 10. Challenge weak testing assumptions directly

Call out excessive mocking, missing failure-path validation, non-deterministic fixtures, slow brittle E2E suites, missing auth tests, contract drift risk, unrealistic test infrastructure, and coverage theater. Be direct, operational, and risk-oriented. Examples:

- "This suite validates implementation details rather than externally visible behavior."
- "Your integration tests provide false confidence because the datastore is mocked."
- "This workflow has no authorization failure validation."
- "Your CI gates allow contract-breaking changes to merge."
- "This acceptance criterion is not measurable."
- "These tests rely on transactional rollback despite spanning asynchronous boundaries."

## Step detail

**Context (step 1).** Load the PRD, system design, the architecture documents it spawned, API/event contracts, persistence design, and operational constraints. Identify critical user workflows, externally visible behavior, operational risk surfaces, and success metrics. Reject invented endpoints, states, or product goals.

**Acceptance criteria (step 2).** Map PRD success metrics, SLOs, and user expectations into measurable acceptance criteria, each defining observable behavior, a measurable outcome, and a pass/fail expectation. Typical criteria: request latency, successful workflow completion, idempotency guarantees, authorization enforcement, retry safety, consistency guarantees. Reject vague criteria.

**Risk classification (step 3).** Classify risks by category: correctness, authorization, consistency, migration safety, performance, resilience, observability, integration drift, concurrency, operational recovery. Map each risk to the appropriate test layer. Reject using E2E tests to compensate for missing integration coverage.

**Test layers (step 4).** Define scope, ownership, runtime expectations, and confidence target for unit, integration, contract, E2E, migration, security, observability, resilience/failure, and performance layers. Reject overlapping suites with identical behavioral scope.

**Contract testing (step 5).** For every API, event, webhook, or integration contract define happy-path tests, negative tests, schema validation, compatibility expectations, and versioning behavior. Validate error-envelope shape, status-code conventions, pagination behavior, idempotency semantics, and authorization responses. Reject unversioned contract evolution.

**Integration testing (step 6).** Define production-like infrastructure for databases, queues, caches, search engines, object stores, and messaging. Prefer disposable containers, ephemeral environments, and production-like topology. Clarify test isolation, state reset, startup ordering, and dependency lifecycle. Reject mocked persistence layers.

**State and test data (step 7).** Define fixture generation, seed strategy, cleanup strategy, and deterministic state reset. Clarify transaction boundaries, asynchronous reconciliation, and eventual-consistency handling. Reject shared mutable test state and non-repeatable fixtures.

**Authorization and security (step 8a).** Define tests for unauthenticated access, authenticated-but-forbidden access, insufficient scopes, tenant-boundary violations, privilege escalation, invalid tokens, expired sessions, and abuse-rate enforcement. Reject happy-path-only authorization testing.

**Observability (step 8b).** Define tests for structured logs, trace propagation, metrics emission, alert generation, correlation IDs, and secret redaction. Validate that operational diagnostics remain usable during failure. Reject logs leaking secrets or tokens.

**Migration and persistence (step 9, conditional).** Define migration verification, rollback testing, data-integrity validation, compatibility windows, and expand/migrate/contract testing. Clarify schema-version compatibility and rolling-deploy behavior. Reject destructive migrations without a validation strategy.

**Resilience and failure (step 9, conditional).** Define validation for dependency outages, retry behavior, timeout handling, partial failures, degraded-mode behavior, queue backpressure, cache unavailability, and circuit-breaker behavior. Clarify expected user-visible degradation. Reject untested resilience assumptions.

**Performance and scalability (step 9, conditional).** Define load expectations, concurrency profile, latency budgets, and throughput expectations. Specify what is validated pre-merge, pre-release, and periodically in production-like environments. Reject load testing performed only after production issues emerge.

**CI/CD gates (step 10).** Define which suites run per PR, which gate release, maximum execution times, flake-handling policy, artifact retention, and rollback triggers. Clarify blocking vs advisory checks. Reject undefined merge or release standards.

**ADRs (step 11).** Draft an ADR inline for each non-obvious testing/tooling decision: test-pyramid balance, contract-test tooling, production-like harness substrate, flake-quarantine policy, ownership of flaky suites and fixtures. Use the ADR structure and immutability rules from architecture-schema; number monotonically within the quality doc tree.

**Generate and validate (step 12).** Emit `testing-strategy.md` from the template with explicit handoffs to backend, frontend, data, security, reliability, operations, and implementation skills. Validate against the quality-artifacts schema and the quality rubric. Define ownership for flaky suites, contract evolution, fixture maintenance, environment upkeep, review expectations, and deprecation of obsolete tests — reject orphaned test infrastructure.

## Standards alignment

- Acceptance criteria trace to PRD success metrics ([prd-schema](../../../standards/prd-schema/README.md)); any unmapped metric carries a documented non-testable rationale.
- Contract tests assert the standard error envelope, status conventions, and idempotency mechanism ([api-standards](../../../standards/api-standards/README.md)).
- Authorization validation covers unauthenticated, forbidden, insufficient-scope, and cross-tenant cases ([security-standards](../../../standards/security-standards/README.md)).
- Observability validation emits structured signals and asserts redaction ([observability-standards](../../../standards/observability-standards/README.md)).
- CI gates align with the `dev → staging → production` promotion flow ([deployment-standards](../../../standards/deployment-standards/README.md)).
- The artifact conforms to [quality-artifacts](../../../standards/quality-artifacts/README.md) for layout, frontmatter, sections, and linkage.

## Anti-patterns to detect

Call these out explicitly when detected:

- Coverage-driven testing without risk mapping
- Mock-heavy integration suites
- End-to-end-only testing strategy
- Missing authorization failure tests
- Shared mutable test state
- Brittle snapshot testing
- Hidden fixture dependencies
- Flaky tests accepted as normal
- Non-deterministic cleanup
- Contract drift without compatibility validation
- Production-incompatible test environments
- No resilience testing
- No migration validation
- Missing observability validation
- CI pipelines with undefined release gates
- Acceptance criteria without measurable outcomes
- Retry behavior never tested
- Queue/event workflows without failure testing
- Tests tightly coupled to implementation details
- Long-running suites blocking developer feedback loops
- "Green pipeline means safe release" assumptions without risk coverage

## Writing style

Risk-oriented, architecture-focused, operationally grounded, and explicit about confidence boundaries. Avoid framework-specific syntax, test-framework tutorials, mock-centric guidance, and coverage-percentage obsession. The objective is production confidence through layered, deterministic, contract-driven quality engineering.
