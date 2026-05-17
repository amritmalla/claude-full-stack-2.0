# FastAPI Service Scaffold — Layout Reference

Use this as the canonical directory-layout, settings, and lifespan reference when generating a FastAPI service scaffold. Placeholder tokens use `<kebab-case>` or `<PascalCase>` style. FastAPI is a single framework — there is no framework branching. Versions are pinned examples — replace with the current stable release at scaffold time; never use unbounded specifiers.

## Directory tree

```
<service-name>/
├── pyproject.toml                        # all deps pinned; requires-python set
├── uv.lock                               # (or requirements.txt --hash) committed
├── ruff.toml                             # lint config
├── mypy.ini                              # strict type config
├── .gitignore                            # covers .env, __pycache__, .venv, dist
├── .dockerignore                         # excludes caches, .env, tests
├── .env.example                          # documents env vars; placeholder values only
├── Dockerfile                            # multi-stage, non-root, digest-pinned base
├── app/
│   ├── main.py                           # FastAPI app factory + lifespan + bootstrap
│   ├── config.py                         # Settings(BaseSettings); built once at import
│   ├── server/
│   │   ├── process_handlers.py           # sys.excepthook + loop exception handler
│   │   ├── exception_handlers.py         # FastAPI/Starlette handlers; no traceback in prod
│   │   └── lifespan.py                   # ASGI lifespan: startup/shutdown drain
│   ├── observability/
│   │   ├── logging.py                    # structlog; level from settings; PII redaction
│   │   ├── context.py                    # contextvars request context
│   │   └── telemetry.py                  # no-op Tracer/Metrics seam (TODO: observability skill)
│   ├── health/
│   │   └── probes.py                     # /healthz (liveness) + /readyz (readiness registry)
│   ├── container.py                      # Depends providers; principal + db session seams
│   └── modules/
│       └── <domain>/                     # one package per domain (per backend-architecture.md)
├── tests/
│   └── test_smoke.py                     # boot → GET /healthz 200 → clean lifespan shutdown
```

## pyproject.toml stub

```toml
[project]
name = "<service-name>"
version = "1.0.0"
requires-python = ">=3.11,<3.13"
dependencies = [
  "fastapi==0.115.0",
  "uvicorn[standard]==0.30.6",
  "gunicorn==23.0.0",
  "pydantic==2.9.2",
  "pydantic-settings==2.5.2",
  "structlog==24.4.0",
]

[dependency-groups]
dev = ["mypy==1.11.2", "ruff==0.6.8", "pytest==8.3.3", "httpx==0.27.2"]
```

All versions are pinned examples — replace with the exact current stable release at scaffold time. Commit the hashed lockfile.

## Settings pattern (app/config.py)

```python
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=None, frozen=True)
    env: str = Field(default="development")          # development|staging|production
    port: int = Field(default=8000, gt=0)
    log_level: str = Field(default="info")
    shutdown_timeout_s: float = Field(default=10.0, gt=0)
    # Required secrets/URLs: declare with NO default so a miss aborts boot.

try:
    settings = Settings()                            # built once at import
except Exception as exc:                             # pydantic ValidationError
    print(f"Invalid configuration: {exc}")
    raise SystemExit(1)
```

## Bootstrap + lifespan pattern (app/main.py)

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import settings
from app.observability.logging import logger
from app.server.process_handlers import register_process_handlers
from app.server.exception_handlers import register_exception_handlers
from app.health.probes import router as health_router

register_process_handlers(logger)  # sys.excepthook + loop handler → exit non-zero

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup: open registered resources
    yield
    # shutdown: stop accepting, drain in-flight, close hooks within settings.shutdown_timeout_s

app = FastAPI(lifespan=lifespan)
register_exception_handlers(app)              # structured body, no traceback in prod
# request-context middleware FIRST, then routers:
app.include_router(health_router)             # /healthz + /readyz before feature routers
```

Run prod via `gunicorn app.main:app -k uvicorn.workers.UvicornWorker`.

## Dockerfile stub

```dockerfile
# Build stage
FROM python:3.11.10-slim@sha256:<digest> AS build
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN pip install --no-cache-dir uv==0.4.18 && uv sync --frozen --no-dev
COPY . .

# Runtime stage
FROM python:3.11.10-slim@sha256:<digest> AS runtime
WORKDIR /app
ENV ENV=production PATH="/app/.venv/bin:$PATH"
COPY --from=build /app /app
RUN useradd -r appuser
USER appuser
HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import httpx,os;httpx.get(f'http://localhost:{os.getenv(\"PORT\",8000)}/healthz').raise_for_status()"
CMD ["gunicorn", "app.main:app", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000"]
```

No secrets baked. Runtime config arrives via environment. Replace `<digest>` with the pinned base-image digest.

## Seams for downstream archetypes

Document these explicitly in the service README:

| Seam | File | Filled by |
|---|---|---|
| Token verification, session, route guards | `app/container.py` (principal `Depends` shell + TODO) | `fastapi-auth-and-security-review` |
| OpenTelemetry tracing + prometheus-client metrics | `app/observability/telemetry.py` (no-op stub) | `fastapi-observability-readiness` |
| Celery/RQ/arq or Kafka producers and consumers | `app/container.py` (no client registered) | `fastapi-async-and-task-integration` |
| Pool sizing, circuit breakers, load-test gates | server + CI configuration | `fastapi-performance-and-resilience` |
| Data-layer client (SQLAlchemy session / Alembic) | `app/container.py` (placeholder) | data-layer implementation per `backend-architecture.md` |

## .gitignore additions (secrets and build)

```
# Secrets and environment
.env
.env.*
!.env.example

# Python build and caches
__pycache__/
*.pyc
.venv/
dist/
build/
.coverage
.mypy_cache/
.ruff_cache/
.pytest_cache/
```
