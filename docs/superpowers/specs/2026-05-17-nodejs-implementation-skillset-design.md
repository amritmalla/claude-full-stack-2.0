# Node.js Implementation Skillset — Design

**Date:** 2026-05-17
**Topic:** `skills/implementations/backend/nodejs` (all 5 archetype skills)
**Tier:** Mature (per skill: `SKILL.md` + `references/<short>-playbook.md` + `references/<short>-quality-rubric.md` + `assets/<short>.template.md`)
**Ecosystem:** Node.js (first backend implementation skillset; all backend siblings are currently scaffold-only READMEs)
**Exemplar:** `skills/implementations/mobile/flutter` (mature-tier reference for structure, section model, and voice)

---

## Context

`skills/implementations/backend/nodejs/README.md` is a `> Status: scaffold` README that already declares 5 planned archetype skills, their owns/defers scope, the target ecosystem, conformed standards, and upstream inputs. No backend implementation skillset has been authored — `django`, `dotnet`, `fastapi`, `golang`, `spring-boot` are all scaffold READMEs with no lean single-file precedent. The `flutter` mobile skillset is the only built-out, mature-tier exemplar.

This spec defines all 5 nodejs archetype skills at mature tier and the upgrade of the stack README from scaffold to authored.

---

## File Structure

```
skills/implementations/backend/nodejs/
  README.md                                  ← upgraded scaffold → authored (flutter README format)
  nodejs-service-scaffold/
    SKILL.md
    references/nodejs-scaffold-playbook.md
    references/nodejs-scaffold-quality-rubric.md
    assets/nodejs-service-scaffold.template.md
  nodejs-auth-and-security-review/
    SKILL.md
    references/nodejs-auth-playbook.md
    references/nodejs-auth-quality-rubric.md
    assets/nodejs-auth-and-security-review.template.md
  nodejs-observability-readiness/
    SKILL.md
    references/nodejs-observability-playbook.md
    references/nodejs-observability-quality-rubric.md
    assets/nodejs-observability-readiness.template.md
  nodejs-queue-and-event-integration/
    SKILL.md
    references/nodejs-queue-playbook.md
    references/nodejs-queue-quality-rubric.md
    assets/nodejs-queue-and-event-integration.template.md
  nodejs-performance-and-resilience/
    SKILL.md
    references/nodejs-performance-playbook.md
    references/nodejs-performance-quality-rubric.md
    assets/nodejs-performance-and-resilience.template.md
```

Skill directory names and `name` frontmatter are taken verbatim from the README archetype table. No skill-level README inside each skill directory — the stack `README.md` is the single tracking document (flutter convention).

---

## Sequencing (pacesetter, then replicate)

1. Build `nodejs-service-scaffold` completely (all 4 files) — the canonical pattern and the baseline skills 2–5 extend.
2. **Pause for user review** of that one skill before proceeding.
3. Replicate the approved shape across `nodejs-auth-and-security-review`, `nodejs-observability-readiness`, `nodejs-queue-and-event-integration`, `nodejs-performance-and-resilience`.
4. Upgrade `skills/implementations/backend/nodejs/README.md` to authored, matching the flutter README format: Philosophy / Archetypes table (with links + ✓ authored status) / What each archetype owns+defers / Upstream / Standards.
5. Run `python scripts/validate_skills.py` and `python -m pytest`; fix until green. No git commit until the user asks.

---

## Per-skill SKILL.md content model (richer flutter variant)

Each `SKILL.md` follows the richer flutter variant, not just the SKILL_SPEC minimum. Sections in order:

`name`/`description` frontmatter (description starts with "Use when", ≤ 1024 chars) → `# Title Case` → `## When to use` (including explicit "do not use … use sibling X instead") → `## Inputs` (Required / Optional) → `## Operating rules` → `## Output contract` (links to applicable standards + upstream contract) → `## Progressive references` → `## Process` (numbered, verifiable steps; ends in mandatory build verification + standards validation) → `## Outputs` (Required + Output rules) → `## Quality checks` (binary checkboxes) → `## References` (upstream + sibling skills + standards).

Constraints: `SKILL.md` under 400 lines (target ~110–150). Repo-relative links only; all local links must resolve. Imperative voice of a **senior Node.js engineer**. Each skill consumes `backend-architecture.md` and the relevant `architecture/security|reliability|performance` decisions; it never invents architecture — if upstream is silent on a needed decision it pauses and raises an ADR candidate. Each skill is **additive** over the scaffold baseline. Framework-aware: behavior branches across Express / Fastify / NestJS per the framework declared in `backend-architecture.md`; no per-framework skill split.

- **`references/<short>-playbook.md`** (~90–120 lines): "Why this workflow exists", "Behavioral rules in depth" (one subsection per operating rule with rationale), "Step detail", "Anti-patterns to detect" (explicit list).
- **`references/<short>-quality-rubric.md`** (~60–80 lines): grouped binary checklists + a "Failure handling" section (identify missing decision → raise ADR candidate or ask user → revise and re-verify).
- **`assets/<short>.template.md`** (~150–200 lines): canonical directory tree + key file stubs, framework-aware (Express/Fastify/NestJS variants where relevant), pinned dependencies (no `^`), no committed secrets. A usable starting point, not TODO-stubs. Placeholder tokens use `<kebab-case>`/`<PascalCase>`.

---

## Ownership boundaries (owns / defers)

| Skill | Owns | Defers |
|---|---|---|
| **nodejs-service-scaffold** | Framework-aware project layout (express/fastify/nest), env/config handling, structured logging seam, health/readiness probes, layered error handling, request context, container packaging, DI shell | Auth flow → auth-and-security-review; observability vendor wiring → observability-readiness; queue wiring → queue-and-event-integration; perf/resilience gates → performance-and-resilience |
| **nodejs-auth-and-security-review** | Passport/JWT/OAuth flow, helmet, input validation, OWASP review, secret handling, security tests | App shell → service-scaffold; auth *provider* decision → `architecture/security` |
| **nodejs-observability-readiness** | pino + OpenTelemetry JS SDK + prom-client wiring, RED metrics, trace-correlated logs, SLI/SLO definitions, multi-burn-rate alert rules | SLO *targets* → `architecture/reliability`; error-handling code → service-scaffold |
| **nodejs-queue-and-event-integration** | BullMQ/KafkaJS/SQS wiring, delivery semantics, transactional outbox, idempotency keys, retry/DLQ, integration tests (Testcontainers) | Business domain logic; broker/contract choice → `backend-architecture.md` |
| **nodejs-performance-and-resilience** | Event-loop discipline, clustering/worker threads, backpressure, circuit breakers, timeout/retry budgets, load-test gates | SLO targets → `architecture/reliability`; observability vendor → observability-readiness |

---

## Standards conformance

Each skill's `## Output contract` links the applicable subset of the standards already named in the README (no new standard is created — implementation skills consume standards, they do not define artifact schemas; the architecture-schema workflow does not apply here). Each skill's `SKILL.md` computes its own repo-relative path (from `skills/implementations/backend/nodejs/<skill>/` that is `../../../../../standards/<name>/README.md`):

- `standards/api-standards`
- `standards/security-standards`
- `standards/observability-standards`
- `standards/deployment-standards`
- `standards/naming-conventions`

Mapping: service-scaffold → deployment + naming + observability (logging seam); auth-and-security-review → security + api; observability-readiness → observability; queue-and-event-integration → api (event contracts) + reliability posture; performance-and-resilience → deployment + observability.

Every skill's `## Process` ends with mandatory verification: TypeScript typecheck (`tsc --noEmit`) + test run (`vitest`/`jest`) + lint, plus a framework boot smoke check. "A build that does not pass is not done — fix and re-run."

---

## Upstream / Downstream

- **Upstream:** approved `backend-architecture.md` (framework choice, domain boundaries, API/event contracts, idempotency and retry strategy); `architecture/security` (auth provider, session model, secret handling); `architecture/reliability` (SLOs, degradation behavior); `architecture/performance` (budgets, load-test gates).
- **Downstream:** none — implementation skills emit code; they are the leaf of the chain. Skills 2–5 are additive over the scaffold baseline.

---

## Out of Scope

- No other backend ecosystems (`django`, `dotnet`, `fastapi`, `golang`, `spring-boot` stay scaffold-only).
- No `standards/` modifications — these skills conform to existing standards, they do not define new ones.
- No separate implementation-plan document — after spec approval, implement directly (user's settled preference).
- No git commit until the user explicitly asks.
- No invented architecture decisions — silent upstream → ADR candidate, not a guess.
