# Scaffold Quality Rubric

Load this before finalizing. Revise until each check passes or explicitly document the unresolved gap.

## Required checks

- [ ] Service starts with profile isolation.
- [ ] At least two non-default profile config files exist and differ meaningfully (typically dev + prod). Staging is included only when confirmed and only when it is materially different from prod.
- [ ] No secrets exist in committed configuration.
- [ ] Structured JSON logs are active in non-dev profiles.
- [ ] Logs include traceId and spanId fields.
- [ ] Actuator exposes health, info, metrics, and prometheus.
- [ ] Actuator endpoints are secured outside local/dev except health.
- [ ] Health probes expose liveness, readiness, and startup endpoints.
- [ ] Graceful shutdown is enabled.
- [ ] Every API error follows one envelope shape.
- [ ] Validation errors are mapped cleanly.
- [ ] Internal stack traces and persistence details are not exposed.
- [ ] Database migrations are versioned with Flyway when persistence exists.
- [ ] Testcontainers integration tests are configured when a database exists.
- [ ] Configuration supports containerized deployment.
- [ ] Dockerfile produces a runnable image.
- [ ] README explains local run, tests, environment variables, profiles, and task commands.
- [ ] Package structure reflects service capability and avoids flat dumping grounds.
- [ ] The scaffold could realistically pass a production-readiness review.

## Build verification

- [ ] `mvn -q -DskipTests verify` (or Gradle equivalent) completed successfully against the generated tree.
- [ ] `mvn -q test` completed successfully, **or** the test run was explicitly skipped (e.g., no Docker for Testcontainers) and the skip is documented in the README's Production Notes.
- [ ] No verification was claimed without evidence — the skill ran the build command and captured the result.

## Cross-file consistency

- [ ] Profile names in `application-*.yml` match those documented in `README.md` under "Profiles".
- [ ] Every environment variable consumed by `application*.yml` appears in the README's Environment Variables table, and vice versa.
- [ ] The package root declared in `Application.java` matches the directory structure under `src/main/java`.
- [ ] `<artifactId>` in `pom.xml` (or Gradle equivalent) matches the target directory name and the README title.
- [ ] Actuator endpoints exposed in configuration match those documented in the README.
- [ ] The Java package root contains no hyphens.

## Failure handling

If a check fails:

1. Identify the missing file, weak default, or unresolved decision.
2. Fix the scaffold when the decision is clear.
3. Ask the user for confirmation when the decision changes architecture, security, persistence, or runtime behavior.
4. Document intentionally deferred items in the README.
