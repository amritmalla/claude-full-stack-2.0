# Production Defaults

Use these defaults when generating configuration, package structure, persistence, Docker packaging, and local run documentation.

## Package structure

Prefer capability-oriented structure for larger services. Use the baseline layered structure only for small/simple services.

Baseline packages:

- `config`
- `controller`
- `service`
- `repository`
- `domain`
- `dto`
- `mapper`
- `exception`
- `validation`
- `security`
- `observability`
- `util`

Call out when a service may outgrow horizontal layers and should move to feature-sliced modules.

## Configuration

Required:

- `application.yml` (base, profile-agnostic settings),
- at least two non-default profile files that differ meaningfully — typically `application-dev.yml` and `application-prod.yml`.

Conditional:

- `application-staging.yml` — include only when the user confirms a staging environment exists. Do not ship a profile that is a copy of `prod`.
- `application-local.yml` — include when local development differs materially from CI/dev.

Defaults:

- externalize all secrets,
- UTC timezone,
- explicit UTF-8 charset,
- fail-fast startup on missing required config,
- environment overlays via Spring profiles,
- graceful shutdown enabled,
- container-friendly port and management port configuration.

Profiles must differ meaningfully. Do not create identical profile files.

## Persistence

Recommended defaults:

- Flyway migrations from the start,
- versioned migrations,
- HikariCP pool explicitly configured,
- explicit transaction boundaries,
- UTC timestamps,
- pagination limits for collection endpoints,
- optimistic locking where data contention is possible,
- no entities exposed through controllers.

Challenge giant aggregate roots, entity leakage, transactional RPC chains, shared database coupling, and implicit transaction sprawl.

## Docker and runtime

Generate:

- multi-stage `Dockerfile`,
- `.dockerignore`,
- non-root runtime user when practical,
- JVM/container-aware settings,
- health-compatible startup behavior,
- graceful shutdown support.

Keep runtime configuration externalized via environment variables.

## Local documentation

Generated `README.md` should include:

- purpose and service capability,
- prerequisites,
- how to run locally,
- how to run tests,
- environment variable reference,
- profile descriptions,
- actuator endpoints,
- available Make targets or task commands.
