# Node.js Service Scaffold Quality Rubric

Load this before declaring the scaffold complete. Revise until each check passes or the unresolved gap is explicitly documented in the service README.

## Project layout and dependencies

- [ ] `package.json` pins every dependency — no `^` or `~` ranges anywhere.
- [ ] The lockfile (`package-lock.json` / `pnpm-lock.yaml` / `yarn.lock`) is committed.
- [ ] `engines.node` is set to the target LTS.
- [ ] `tsconfig.json` enables `strict` (plus `noUncheckedIndexedAccess`).
- [ ] Lint config is present and the lint command passes.
- [ ] `.gitignore` covers `.env`, `.env.*` (except `.env.example`), `node_modules`, `dist`/`build`, coverage.
- [ ] `.env.example` documents every required environment variable with placeholder values only.

## Configuration

- [ ] A schema (zod or equivalent) parses `process.env` once at boot into a single frozen typed object.
- [ ] `process.env` is not read anywhere outside `src/config`.
- [ ] Removing one required variable aborts boot with a clear message and a non-zero exit (verified).

## Error handling

- [ ] `process.on('uncaughtException')` logs fatal, flushes logs, and exits non-zero.
- [ ] `process.on('unhandledRejection')` logs fatal, flushes logs, and exits non-zero.
- [ ] The framework error handler (Express middleware / Fastify `setErrorHandler` / Nest filter) returns a structured body.
- [ ] No stack trace or internal detail appears in the error response outside dev.
- [ ] Graceful shutdown on `SIGTERM`/`SIGINT` stops accepting, drains in-flight, closes registered resources within a bounded timeout, then exits.

## Observability seam

- [ ] A pino structured logger is configured with level from config and PII-field redaction (`email`, `token`, `password`, `authorization`).
- [ ] An AsyncLocalStorage request context binds a request id; every log line within a request carries it.
- [ ] The tracer/metrics interface is a no-op stub with TODO comments naming `nodejs-observability-readiness` as owner.

## Health probes

- [ ] `/healthz` returns 200 when the process is up and does not check dependencies.
- [ ] `/readyz` iterates registered dependency-check hooks and returns 503 until all pass.
- [ ] Both probes are wired before any feature route.

## DI and principal seam

- [ ] The DI container matches the one named in `backend-architecture.md`, or is documented as deferred with a pending ADR candidate.
- [ ] The principal/auth-context provider is registered as a typed shell.
- [ ] Token verification, session, and protected-route logic are explicitly marked with TODO comments naming `nodejs-auth-and-security-review` as owner.
- [ ] No auth or session implementation logic exists in the scaffold (seam only).

## Container packaging

- [ ] The `Dockerfile` is multi-stage (build tooling absent from the runtime layer).
- [ ] The container runs as a non-root user.
- [ ] The base image is digest-pinned (no `:latest`).
- [ ] A `HEALTHCHECK` hits `/healthz`; a `.dockerignore` excludes `node_modules`, `.env`, and tests.
- [ ] No secrets, `.env`, or credentials are copied into the image.

## Build verification

- [ ] `tsc --noEmit` reports zero errors.
- [ ] The lint command passes.
- [ ] The test command runs (or the skip is documented with reason).
- [ ] The boot smoke check (`GET /healthz` → 200, clean shutdown) passes (or the skip is documented with reason).

## Standards conformance

- [ ] [deployment-standards](../../../../../../standards/deployment-standards/README.md): env-agnostic image, runtime config injected, non-root, one artifact per environment.
- [ ] [observability-standards](../../../../../../standards/observability-standards/README.md): structured logging with request-id correlation and environment tag; tracer/metrics seam present.
- [ ] [security-standards](../../../../../../standards/security-standards/README.md): no secrets in source, config, or image; config fails fast on missing required secrets.
- [ ] [naming-conventions](../../../../../../standards/naming-conventions/README.md): service, module, and file naming.

## Failure handling

If a check fails:

1. Identify the missing or incorrect implementation.
2. Ask the user for clarification if the decision cannot be inferred from `backend-architecture.md` or `architecture/security`.
3. Revise the scaffold file, re-run `tsc --noEmit`, lint, tests, and the boot smoke check.
4. Keep any unresolved gap explicit in the service README — do not hide it as an assumption.
