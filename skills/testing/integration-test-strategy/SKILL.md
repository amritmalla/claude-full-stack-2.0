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
- [ ] Every endpoint has at least one happy-path and one negative test.
- [ ] Non-idempotent endpoints have an idempotency test.
- [ ] No `@MockBean` of the repository under test.
- [ ] DB state is reset between tests.

## References

(None in v0.1.)
