# FastAPI Implementation Skillset — Design

**Date:** 2026-05-17
**Topic:** `skills/implementations/backend/fastapi` (all 5 archetype skills)
**Tier:** Mature (per skill: `SKILL.md` + `references/<short>-playbook.md` + `references/<short>-quality-rubric.md` + `assets/<short>.template.md`)
**Ecosystem:** FastAPI (Python); second backend implementation skillset
**Exemplars:** `skills/implementations/backend/nodejs` (just-authored sibling, same archetype set) and `skills/implementations/mobile/flutter` (mature-tier reference for structure, section model, voice)

---

## Context

`skills/implementations/backend/fastapi/README.md` is a `> Status: scaffold` README declaring the same 5 backend archetypes as nodejs, with FastAPI-specific names and scope. This spec replicates the approved, committed nodejs treatment (`267a2f9`) for FastAPI. The structure, tier, sequencing, and workflow are identical to nodejs; only the ecosystem idioms differ.

---

## File Structure

```
skills/implementations/backend/fastapi/
  README.md                                  ← upgraded scaffold → authored (flutter format)
  fastapi-service-scaffold/
    SKILL.md
    references/fastapi-scaffold-playbook.md
    references/fastapi-scaffold-quality-rubric.md
    assets/fastapi-service-scaffold.template.md
  fastapi-auth-and-security-review/
    SKILL.md
    references/fastapi-auth-playbook.md
    references/fastapi-auth-quality-rubric.md
    assets/fastapi-auth-and-security-review.template.md
  fastapi-observability-readiness/
    SKILL.md
    references/fastapi-observability-playbook.md
    references/fastapi-observability-quality-rubric.md
    assets/fastapi-observability-readiness.template.md
  fastapi-async-and-task-integration/
    SKILL.md
    references/fastapi-async-playbook.md
    references/fastapi-async-quality-rubric.md
    assets/fastapi-async-and-task-integration.template.md
  fastapi-performance-and-resilience/
    SKILL.md
    references/fastapi-performance-playbook.md
    references/fastapi-performance-quality-rubric.md
    assets/fastapi-performance-and-resilience.template.md
```

Skill directory names and `name` frontmatter taken verbatim from the README archetype table. No skill-level README — the stack `README.md` is the single tracking document (flutter convention).

---

## Sequencing (pacesetter, then replicate)

1. Build `fastapi-service-scaffold` completely (all 4 files) — the canonical pattern and the baseline skills 2–5 extend.
2. **Pause for user review** of that one skill before proceeding.
3. Replicate the approved shape across `fastapi-auth-and-security-review`, `fastapi-observability-readiness`, `fastapi-async-and-task-integration`, `fastapi-performance-and-resilience`.
4. Upgrade `skills/implementations/backend/fastapi/README.md` to authored, matching the flutter README format: Philosophy / Ecosystem / Compatible patterns / Archetypes table (links + ✓ authored) / What each archetype owns+defers / Upstream / Standards.
5. Run `python scripts/validate_skills.py`, `python -m pytest`, and markdown lint; fix until green. No git commit until the user asks.

---

## Per-skill SKILL.md content model (richer flutter variant)

Identical section model to nodejs: `name`/`description` frontmatter (description starts with "Use when", ≤ 1024 chars) → `# Title` → `## When to use` (incl. explicit "do not use … use sibling X") → `## Inputs` (Required/Optional) → `## Operating rules` → `## Output contract` (standards links + upstream contract) → `## Progressive references` → `## Process` (numbered, verifiable; ends in mandatory build verification + standards validation) → `## Outputs` (Required + Output rules) → `## Quality checks` (binary) → `## References`.

Constraints: `SKILL.md` under 400 lines (target ~100–150). Repo-relative links only; all must resolve. Voice of a **senior FastAPI/Python engineer**. Each skill consumes `backend-architecture.md` and the relevant `architecture/security|reliability|performance` decisions; never invents architecture — silent upstream → ADR candidate. Each skill is **additive** over the scaffold baseline. FastAPI is a single framework: no framework branching (the key structural difference from nodejs).

- **`references/<short>-playbook.md`** (~90–120 lines): "Why this workflow exists", "Behavioral rules in depth", "Step detail", "Anti-patterns to detect".
- **`references/<short>-quality-rubric.md`** (~60–80 lines): grouped binary checklists + "Failure handling" section.
- **`assets/<short>.template.md`** (~150–200 lines): canonical directory tree + key file stubs (Python/FastAPI idioms), pinned dependencies, no committed secrets. Usable starting point, not TODO-stubs.

---

## FastAPI-specific adaptations (vs nodejs)

| Concern | nodejs | fastapi |
|---|---|---|
| Framework | Express/Fastify/NestJS (branched) | FastAPI + Starlette only (no branching) |
| Config | zod, frozen object | Pydantic Settings (`BaseSettings`), fail-fast at boot |
| Logging | pino + AsyncLocalStorage | structlog + `contextvars` request context |
| Error tiers | `uncaughtException` + `unhandledRejection` + framework handler + graceful shutdown | `sys.excepthook` + asyncio loop exception handler + FastAPI/Starlette exception handlers + ASGI-lifespan graceful shutdown (uvicorn signal handling) |
| DI shell | awilix/tsyringe/Nest | FastAPI `Depends` + typed principal-provider dependency; SQLAlchemy 2.x + Alembic data-layer seam |
| Async (skill 4) | BullMQ/KafkaJS/SQS | Celery / RQ / arq (or Kafka per architecture); transactional outbox, idempotent tasks, retry/DLQ, Testcontainers |
| Perf (skill 5) | event-loop, clustering/worker threads | async-path discipline (no blocking calls → `run_in_threadpool`/async drivers), Uvicorn/Gunicorn worker model, connection-pool sizing, caching posture, circuit breakers, timeout/retry budgets, load-test gate |
| Verification | `tsc --noEmit` + eslint + vitest + boot smoke | `mypy` + `ruff` + `pytest` + boot smoke (`httpx` GET `/healthz`) |
| Deps | pinned `package.json` + lockfile | pinned `pyproject.toml`/requirements + lockfile (`uv.lock`/`requirements.txt` hashes); `python` pinned |

---

## Ownership boundaries (owns / defers) — same structure as nodejs

| Skill | Owns | Defers |
|---|---|---|
| **fastapi-service-scaffold** | Project layout, Pydantic Settings config, structlog seam + request context, liveness/readiness probes, layered error handling, ASGI lifespan, `Depends` DI shell + principal seam, non-root container | Auth flow → auth-and-security-review; observability vendor → observability-readiness; task wiring → async-and-task-integration; perf gates → performance-and-resilience; data client → data layer |
| **fastapi-auth-and-security-review** | OAuth2/OIDC + API-key flows, dependency-based default-deny authz, secure headers, input validation (Pydantic at boundary), secret handling, OWASP review, security tests | Service shell → service-scaffold; auth provider decision → `architecture/security` |
| **fastapi-observability-readiness** | OTel Python SDK tracing, prometheus-client RED metrics, trace-correlated structlog, SLI/SLO definitions, multi-burn-rate alerts | SLO targets → `architecture/reliability`; logger/error code → service-scaffold |
| **fastapi-async-and-task-integration** | Celery/RQ/arq or Kafka wiring, delivery semantics, transactional outbox, idempotent consumers, retry/DLQ, Testcontainers tests | Broker/contract choice → `backend-architecture.md`; business domain logic |
| **fastapi-performance-and-resilience** | Async-path discipline, worker model, connection-pool sizing, caching posture, circuit breakers, timeout/retry budgets, CI load-test gate | Budget/SLO numbers → `architecture/performance` & `architecture/reliability`; observability vendor → observability-readiness |

---

## Standards conformance

Same mapping as nodejs. Each skill's `## Output contract` links the applicable subset; each `SKILL.md` computes its own repo-relative path (`../../../../../standards/<name>/README.md`; references one level deeper: `../../../../../../standards/...`):

- `standards/api-standards`, `standards/security-standards`, `standards/observability-standards`, `standards/deployment-standards`, `standards/naming-conventions`

Mapping: service-scaffold → deployment + naming + observability (logging seam); auth-and-security-review → security + api; observability-readiness → observability; async-and-task-integration → api (event contracts) + observability; performance-and-resilience → observability + deployment.

No new standard is created — implementation skills consume standards, they do not define artifact schemas.

---

## Upstream / Downstream

- **Upstream:** approved `backend-architecture.md` (domain boundaries, API/event contracts, idempotency/retry strategy, data layer); `architecture/security` (auth provider, session model, secret handling); `architecture/reliability` (SLOs, degradation); `architecture/performance` (budgets, load-test gates). Skills 2–5 also consume the `fastapi-service-scaffold` baseline.
- **Downstream:** none — implementation skills emit code; they are the leaf of the chain.

---

## Out of Scope

- No other backend ecosystems (`django`, `dotnet`, `golang`, `spring-boot` stay scaffold-only).
- No `standards/` modifications.
- No separate implementation-plan document — implement directly after spec approval.
- No git commit until the user explicitly asks.
- No invented architecture decisions — silent upstream → ADR candidate, not a guess.
