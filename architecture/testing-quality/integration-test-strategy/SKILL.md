---
name: integration-test-strategy
description: Use when designing the integration test suite for a Spring Boot
  service that depends on a real database. Produces a Testcontainers-based
  Postgres setup, a happy-path plus edge-case integration test per endpoint, and
  guidelines that prevent fragile mocks of components under test.
---

# Integration Test Strategy

## When to use

Invoke after the API contract and persistence layer are defined and before merging the first production-bound feature. Use to bootstrap an integration test harness, not to write unit tests for isolated logic.

## Inputs

- Scaffolded Spring Boot service with `application.yml` profiles.
- OpenAPI spec for the service (endpoint list + payloads).
- Database schema (Flyway migrations).

## Output contract

Generated tests and `testing-strategy.md` MUST conform to:

- [api-standards](../../../standards/api-standards/README.md) — every endpoint in the OpenAPI spec is tested; tests assert the standard error envelope shape and status-code conventions; idempotency tests for non-idempotent endpoints use `Idempotency-Key`.
- [prd-schema § Success Metrics](../../../standards/prd-schema/README.md) — acceptance criteria derive from the PRD's success metrics.
- [security-standards](../../../standards/security-standards/README.md) — auth tests cover unauthenticated (401), authenticated-but-forbidden (403), and (where applicable) scope-insufficient cases.
- [observability-standards](../../../standards/observability-standards/README.md) — test runs emit structured signals; no test logs leak secrets or tokens.

Upstream inputs come from approved `openapi.yaml` (the source of truth — do not invent endpoints) and the active database schema migrations.

> Note: this skill is currently Spring-Boot + Postgres flavored. Generalization to other ecosystems (Node, Django, FastAPI) is a follow-up; the *strategy* (Testcontainers + contract-driven + no-mock-on-SUT) is ecosystem-neutral.

## Process

1. Add Testcontainers (`org.testcontainers:postgresql`, `org.testcontainers:junit-jupiter`) to the test scope of `pom.xml`.
2. Create `application-test.yml` overriding datasource to point at the Testcontainers Postgres URL injected at runtime.
3. Add a base test class that starts a Postgres container once per suite and runs Flyway migrations on startup.
4. For each endpoint in the OpenAPI spec, write:
   - One happy-path test asserting status code, response shape, and persisted state.
   - At least one negative test (400, 401/403, or 404 as appropriate).
   - For non-idempotent endpoints, an idempotency test: same `Idempotency-Key` returns the same result.
5. Reset DB state between tests via `@Sql` cleanup scripts OR a `TRUNCATE` hook in `@AfterEach`. Do not rely on transactional rollback when testing controllers that span transactions.
6. Do NOT mock the repository under test. Mock only external HTTP/event sinks.
7. Emit the test class(es), `application-test.yml`, and a `testing-strategy.md` summarizing the rules.

## Outputs

- Test classes under `src/test/java/...`.
- `application-test.yml`.
- `testing-strategy.md`.

## Quality checks

- [ ] Postgres container is started once per suite, not per test.
- [ ] Every endpoint in the OpenAPI spec has at least one happy-path and one negative test.
- [ ] Non-idempotent endpoints have an idempotency test using `Idempotency-Key`.
- [ ] Auth tests cover 401 (unauthenticated) and 403 (authenticated but forbidden), per [security-standards](../../../standards/security-standards/README.md).
- [ ] Error responses asserted against the [api-standards](../../../standards/api-standards/README.md) error envelope shape.
- [ ] No `@MockBean` of the repository under test.
- [ ] DB state is reset between tests.

## References

(None in v0.1.)
