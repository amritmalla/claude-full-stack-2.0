# FastAPI Service Scaffold Quality Rubric

Load this before declaring the scaffold complete. Revise until each check passes or the unresolved gap is explicitly documented in the service README.

## Project layout and dependencies

- [ ] `pyproject.toml` pins every dependency — no unbounded or floating specifiers.
- [ ] A hashed lockfile (`uv.lock` / `requirements.txt` with `--hash`) is committed.
- [ ] `requires-python` is set to the target version.
- [ ] `mypy` config is strict; `ruff` config is present.
- [ ] `.gitignore` covers `.env`, `.env.*` (except `.env.example`), `__pycache__`, `.venv`, build/dist, coverage.
- [ ] `.env.example` documents every required environment variable with placeholder values only.

## Settings

- [ ] A single `Settings(BaseSettings)` instance is built once at import.
- [ ] `os.environ`/`os.getenv` is not read anywhere outside `app/config.py`.
- [ ] Removing one required variable aborts boot with a clear message and a non-zero exit (verified).

## Error handling

- [ ] `sys.excepthook` logs fatal, flushes logs, and exits non-zero.
- [ ] `loop.set_exception_handler` logs fatal, flushes logs, and exits non-zero.
- [ ] FastAPI/Starlette exception handlers return a structured body.
- [ ] No traceback or internal detail appears in the error response outside dev.
- [ ] The ASGI `lifespan` shutdown stops accepting, drains in-flight, and closes registered resources within a bounded timeout.

## Observability seam

- [ ] A structlog structured logger is configured with level from settings and PII-key redaction (`email`, `token`, `password`, `authorization`).
- [ ] A `contextvars` request context binds a request id; every log line within a request carries it.
- [ ] The tracer/metrics interface is a no-op stub with TODO comments naming `fastapi-observability-readiness` as owner.

## Health probes

- [ ] `/healthz` returns 200 when the process is up and does not check dependencies.
- [ ] `/readyz` iterates registered dependency-check callables and returns 503 until all pass.
- [ ] Both probes are wired before any feature router.

## DI and principal seam

- [ ] The `Depends` providers match the structure named in `backend-architecture.md`, or deferral is documented with a pending ADR candidate.
- [ ] The principal/auth-context provider is a typed dependency shell.
- [ ] Token verification, session, and protected-route logic are explicitly marked with TODO comments naming `fastapi-auth-and-security-review` as owner.
- [ ] No auth or session implementation logic exists in the scaffold (seam only).

## Container packaging

- [ ] The `Dockerfile` is multi-stage (build tooling absent from the runtime layer).
- [ ] The container runs as a non-root user.
- [ ] The base image is digest-pinned (no `:latest`).
- [ ] A `HEALTHCHECK` hits `/healthz`; a `.dockerignore` excludes caches, `.env`, and tests.
- [ ] No secrets, `.env`, or credentials are copied into the image.

## Build verification

- [ ] `mypy` reports zero errors.
- [ ] `ruff check` passes.
- [ ] The test command runs (or the skip is documented with reason).
- [ ] The boot smoke check (`GET /healthz` → 200, clean lifespan shutdown) passes (or the skip is documented with reason).

## Standards conformance

- [ ] [deployment-standards](../../../../../../standards/deployment-standards/README.md): env-agnostic image, runtime config injected, non-root, one artifact per environment.
- [ ] [observability-standards](../../../../../../standards/observability-standards/README.md): structured logging with request-id correlation and environment tag; tracer/metrics seam present.
- [ ] [security-standards](../../../../../../standards/security-standards/README.md): no secrets in source, config, or image; settings fail fast on missing required secrets.
- [ ] [naming-conventions](../../../../../../standards/naming-conventions/README.md): service, module, and file naming.

## Failure handling

If a check fails:

1. Identify the missing or incorrect implementation.
2. Ask the user for clarification if the decision cannot be inferred from `backend-architecture.md` or `architecture/security`.
3. Revise the scaffold file, re-run `mypy`, `ruff check`, `pytest`, and the boot smoke check.
4. Keep any unresolved gap explicit in the service README — do not hide it as an assumption.
