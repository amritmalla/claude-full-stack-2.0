---
name: dockerfile-and-jvm-tuning
description: Use when containerizing a JVM service for production. Produces a
  multi-stage Dockerfile with a minimal runtime image (distroless or jlink), a
  non-root user, container-aware JVM flags, a healthcheck, and a .dockerignore
  that excludes build artifacts and secrets.
---

# Dockerfile and JVM Tuning

## When to use

Invoke when packaging a Spring Boot service (or any JVM service) into a container image for deployment. Use before wiring CI image builds. Do not invoke for non-JVM services.

## Inputs

- Path to the built fat JAR (or build tool: Maven/Gradle).
- Target base image preference (distroless `gcr.io/distroless/java21-debian12:nonroot`, Eclipse Temurin, or jlink runtime).
- Expected memory budget (container memory limit).

## Output contract

Generated Dockerfile and runtime tuning MUST conform to:

- [deployment-standards](../../../../standards/deployment-standards/README.md) — env-agnostic image (no env-branched code, no baked secrets), config injected at deploy time, reproducible build, signed before promotion.
- [security-standards](../../../../standards/security-standards/README.md) — non-root user, minimal base (distroless or jlink), no secrets in layers, container scan as a required CI gate.
- [observability-standards](../../../../standards/observability-standards/README.md) — logs go to stdout (structured JSON), Prometheus scrape port exposed when applicable.
- [naming-conventions](../../../../standards/naming-conventions/README.md) — image names `kebab-case`, registry-prefixed.

## Process

1. Write a two-stage Dockerfile:
   - **Stage 1 (builder)**: `maven:3.9-eclipse-temurin-21` (or jlink builder); cache dependencies; build the JAR.
   - **Stage 2 (runtime)**: distroless or jlink runtime image; copy only the JAR; run as non-root (`USER nonroot:nonroot`).
2. Set container-aware JVM flags: `-XX:MaxRAMPercentage=75.0`, `-XX:+UseG1GC`, `-XX:+ExitOnOutOfMemoryError`, `-XshowSettings:vm` (dev only).
3. Add a `HEALTHCHECK` that hits `/actuator/health/liveness`.
4. Write `.dockerignore` excluding: `target/`, `.git/`, `.idea/`, `*.env`, `secrets/`, `node_modules/`.
5. Set explicit `EXPOSE` for the service port.
6. Document the resulting image size and the JVM flag rationale in `Dockerfile.md`.

## Outputs

- `Dockerfile` (multi-stage).
- `.dockerignore`.
- `Dockerfile.md` (rationale, expected size, tuning notes).

## Quality checks

- [ ] Final image runs as a non-root user.
- [ ] Final image size < 200 MB.
- [ ] `MaxRAMPercentage` is set explicitly; no implicit heap sizing.
- [ ] `ExitOnOutOfMemoryError` is set so OOM kills the container.
- [ ] `.dockerignore` excludes `target/`, secrets, and IDE files.
- [ ] No secrets, credentials, or `.env` files baked into any layer.

## References

(None in v0.1.)
