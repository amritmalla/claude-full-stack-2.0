# FastAPI Service Scaffold Playbook

Load this when implementing any owned area of `fastapi-service-scaffold` or checking the anti-pattern list. It expands the operating rules and process steps in `SKILL.md` with the detail needed to produce a production-grade service shell.

## Why this workflow exists

A FastAPI scaffold done wrong takes weeks to fix: unpinned dependencies cause irreproducible builds; settings read ad hoc from `os.environ` fail as a runtime `None` deep in a request instead of at boot; a missing top-level exception handler turns one unhandled error into a 500 with a full traceback leaked to the client; no ASGI-lifespan shutdown drops in-flight requests and leaks connection pools on every deploy; and observability bolted on later means the first production incident is diagnosed by guesswork.

The goal is a service that boots deterministically, fails fast on bad settings, logs with request correlation, handles every error tier, and shuts down cleanly through the ASGI lifespan — a baseline every downstream archetype extends safely, not a working feature, not a tutorial app.

## Behavioral rules in depth

### 1. Consume architecture; do not invent it

Read `backend-architecture.md` before writing a single file. Domain boundaries, data layer, and API/event contracts are architectural decisions — not scaffold defaults. Auth provider and secret handling come from `architecture/security`. If any needed decision is missing, surface an ADR candidate before proceeding. The scaffold implements what was decided; it does not decide.

### 2. Pin every dependency — no exceptions

Use exact version pins in `pyproject.toml` with a hashed lockfile (`uv.lock`, or `requirements.txt` with `--hash`). Unbounded or floating specifiers cause resolution divergence between developer machines and CI. The lockfile is committed and is the sole source of truth for reproducibility. Set `requires-python` so a wrong interpreter fails install, not production. Never add a dependency without a pin.

### 3. Settings are validated at boot — never read ad hoc

A single typed `Settings(BaseSettings)` instance is built once at startup. Required variables that are missing or malformed raise `ValidationError` and abort the process with a clear message naming the field — not a runtime `None` surfacing inside a request handler hours later. `os.environ` is never read outside `app/config.py`; the settings instance is imported everywhere.

### 4. All four error tiers — no fewer

Python/ASGI error propagation has four independent tiers, each catching failures the others miss:

| Tier | What it catches | Where to wire |
|---|---|---|
| `sys.excepthook` | Uncaught exceptions on the main thread | `app/server/process_handlers.py` |
| `loop.set_exception_handler` | Unhandled exceptions in asyncio tasks/callbacks | `app/server/process_handlers.py` |
| FastAPI/Starlette exception handlers | Errors raised in route/dependency handlers | `app.add_exception_handler(...)` |
| ASGI lifespan shutdown | In-flight work and resources during termination | `lifespan` async context manager |

The two process/loop handlers log fatal, flush logs, and exit non-zero — a process in an unknown state must not keep serving. The exception handlers return a structured body with no traceback or internals outside dev. The lifespan shutdown stops accepting connections, drains in-flight requests, and closes every registered resource within a bounded timeout. Missing any tier leaves a class of production failure unhandled or a traceback leaked.

### 5. Observability is a seam the scaffold installs, not a vendor it chooses

The structlog logger and `contextvars` request context are mandatory baseline infrastructure: every log line carries a request id so a production trace is a filter, not an archaeology dig. The tracer/metrics interface is a no-op stub implementing the same shape; `fastapi-observability-readiness` replaces the stub with OpenTelemetry and prometheus-client. Wire the context middleware first so it wraps every later handler. Reject PII keys (`email`, `token`, `password`, `authorization`) in the default structlog processors.

### 6. The DI seam owns the shell; auth owns the flow

Register the principal/auth-context provider as a typed FastAPI dependency (`async def get_principal(...) -> Principal`). Mark the deferred work explicitly with the owning archetype:

```python
# TODO(fastapi-auth-and-security-review): verify token and populate Principal
# TODO(fastapi-auth-and-security-review): wire protected-route dependency
```

The scaffold owns the dependency signature and the type. `fastapi-auth-and-security-review` owns the implementation. The SQLAlchemy session is registered the same way — a seam owned by the data implementation, not built here.

### 7. Liveness and readiness are different questions

`/healthz` answers "is the process up" — it returns 200 as soon as the event loop runs and must not check dependencies, or a slow database triggers a pointless pod restart. `/readyz` answers "should this instance receive traffic" — it iterates registered dependency-check callables and returns 503 until all pass, so a starting instance is kept out of the load balancer. Conflating them causes either restart storms or traffic to a not-ready instance.

### 8. The image references secrets — it never contains them

No `.env`, secret, key, or credential is copied into the image or committed. The container runs as a non-root user from a digest-pinned base image (`python:3.11.x-slim@sha256:...`), uses a multi-stage build so build tooling is absent from the runtime layer, and receives all configuration at runtime via environment variables. The repository holds only the reference pattern and `.env.example` with placeholders.

### 9. A scaffold that does not run is not done

Run `mypy` first — zero errors, no exceptions. Then `ruff check`, then `pytest`, then a boot smoke check: start the app, assert `httpx` `GET /healthz` returns 200, shut down cleanly through the lifespan. If a check cannot run in the environment, document it in the README — do not declare the scaffold done on an unverified build.

## Step detail

**Step 1 — Gather context.** Load `backend-architecture.md`. Extract domain boundaries, data layer, contracts, and the auth provider decision from `architecture/security`. Confirm the target directory. Missing decision → ADR candidate, do not guess.

**Step 2 — Project layout.** Generate `pyproject.toml` with pinned deps + hashed lockfile and `requires-python`; `ruff` and `mypy` config (strict); `.gitignore` per the template. Choose the package structure (domain-first) per `backend-architecture.md`.

**Step 3 — Settings.** Implement `app/config.py`: a `Settings(BaseSettings)` with typed fields and no defaults for required secrets; instantiate once at import; on `ValidationError` print the aggregated error and `raise SystemExit(1)`. Create `.env.example` with every variable and placeholder values.

**Step 4 — Logging and request context.** Implement `app/observability/logging.py` (structlog config, level from settings, PII-key redaction processor), `app/observability/context.py` (`contextvars.ContextVar` request context + `get_request_id()`), ASGI middleware that reads or generates `x-request-id` and binds the bound logger, and `app/observability/telemetry.py` (no-op `Tracer`/`Metrics` interface with TODOs naming `fastapi-observability-readiness`).

**Step 5 — Error handling.** Implement `app/server/process_handlers.py` (`sys.excepthook`, `loop.set_exception_handler` → log fatal, flush, `os._exit`/`SystemExit` non-zero), FastAPI/Starlette exception handlers (structured `{ "error", "request_id" }`; map known exception types to status; no traceback outside dev), and the `lifespan` context manager (startup: open registered resources; shutdown: stop accepting, await in-flight drain with timeout, close registered resource hooks).

**Step 6 — Health probes.** Implement `/healthz` (static 200) and `/readyz` (iterate a registry of `Callable[[], Awaitable[bool]]` dependency checks; 200 only when all pass, else 503 with failing check names). Register both before feature routers.

**Step 7 — DI/principal seam.** Implement `app/container.py` with FastAPI `Depends` providers. Register the principal provider shell and the SQLAlchemy session placeholder. Add explicit TODO comments naming `fastapi-auth-and-security-review` and the data implementation as owners.

**Step 8 — Container packaging.** Write a multi-stage `Dockerfile` (deps → build → slim runtime), non-root `USER`, digest-pinned base, `HEALTHCHECK` hitting `/healthz`, and a `.dockerignore` excluding caches, `.env`, tests as appropriate. Run under Gunicorn + `UvicornWorker` for prod.

**Step 9 — Local-run docs.** In the service README, document run commands per environment, every env var (mirrored from `.env.example`), the runtime-config contract, and the seam table from the template.

**Step 10 — Build verification and standards.** Run `mypy`, `ruff check`, `pytest`, boot smoke. Then check deployment-standards (env-agnostic image, non-root, runtime config), observability-standards (request-correlated structured logs, tracer seam), security-standards (no secrets, fail-fast settings), naming-conventions. Document any unresolved gap explicitly — do not hide it.

## Anti-patterns to detect

Call these out explicitly when found:

- Unbounded or floating dependency specifiers; lockfile not committed or not hashed
- `os.environ` / `os.getenv` read directly outside `app/config.py`
- Settings read lazily so a missing required variable fails mid-request instead of at boot
- Missing `sys.excepthook` or asyncio exception handler, or a handler that logs and continues instead of exiting
- No ASGI-lifespan shutdown — `SIGTERM` kills in-flight requests and leaks the connection pool
- Exception handler leaking a traceback or internal message in non-dev (default FastAPI 500 behavior left unchanged)
- `/healthz` checking the database (turns a slow dependency into a restart storm), or no separate `/readyz`
- Logging without request-id correlation; PII keys unredacted in structlog processors
- Auth token/session logic implemented in the scaffold instead of delegated to `fastapi-auth-and-security-review`
- Secrets, `.env`, or credentials copied into the image; container running as root; unpinned (`:latest`) base image
- Sync blocking calls on the async path in the shell (defer the discipline to `fastapi-performance-and-resilience`, but do not introduce the anti-pattern here)
- Build not verified (`mypy`/`ruff`/`pytest`/boot smoke) before declaring the scaffold complete
