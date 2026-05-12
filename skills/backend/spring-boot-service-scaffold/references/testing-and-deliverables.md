# Testing and Deliverables

Use this reference when generating the scaffold and checking file completeness.

## Required deliverables

- `pom.xml` or `build.gradle.kts`
- package structure
- `application.yml`
- at least two non-default profiles (typically `application-dev.yml` and `application-prod.yml`) that differ meaningfully
- `logback-spring.xml`
- `GlobalExceptionHandler.java`
- health probe configuration
- actuator configuration
- security baseline
- `Dockerfile`
- `.dockerignore`
- `.gitignore`
- `README.md`
- `Makefile` or task runner commands
- baseline integration test example

## Optional deliverables

Include when appropriate:

- `application-staging.yml` (only when staging is a real environment, not a copy of prod),
- `application-local.yml` (only when local diverges from dev),
- `docker-compose.yml` for local dev dependencies,
- OpenAPI starter config,
- OpenTelemetry starter config,
- Kubernetes probe examples,
- Flyway migration placeholder (empty `V1__init.sql` with a header comment) when a database is confirmed — leave content for the `postgres-schema-and-migration` skill,
- `.editorconfig` for consistent indentation across editors,
- formatter configuration (Spotless or Checkstyle) when team standardization matters,
- `.gitattributes` for line-ending normalization in mixed-OS teams.

## Testing foundation

Generate:

- unit testing setup,
- integration testing baseline,
- Testcontainers for real database dependencies,
- profile-aware test configuration,
- minimal mocking of infrastructure,
- repository tests against real databases where persistence exists.

Avoid brittle over-mocked architectures. Mock external HTTP/event sinks, not the repository or database behavior under test.

## No-placeholder rule

Generated deliverables must be functional. Avoid TODO comments or placeholder files standing in for real configuration.

Acceptable placeholders:

- environment variable examples with safe dummy values,
- package-level extension points,
- empty migration only if the service has no confirmed schema yet and the README explains why.

Unacceptable placeholders:

- fake secrets,
- disabled security,
- empty exception handlers,
- actuator config without secured non-dev behavior,
- tests that compile but assert nothing meaningful.
