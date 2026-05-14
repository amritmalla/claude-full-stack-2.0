# Claude Full Stack 2.0 v0.1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship v0.1 of the `claude-full-stack-2.0` Claude Code plugin: 12 lifecycle-spanning skills, one Spring Boot reference example (`orders-api`), a capstone workflow, plugin manifest, and supporting docs.

**Architecture:** A Claude Code plugin distributed via marketplace manifest. Skills follow the official `SKILL.md` + YAML frontmatter format and are organized in flat domain folders under `skills/`. Lifecycle sequencing lives in `workflows/`. Each skill is exercised against a single Spring Boot reference service (`orders-api`); each skill's example output is committed under `examples/spring-boot/orders-api/.skill-outputs/`. Quality gate: a `validate-skills.sh` script enforces frontmatter rules in CI; authors manually run each skill against `orders-api` before merge.

**Tech Stack:** Markdown (skills/docs), YAML frontmatter, JSON (plugin manifests), Bash (validation scripts), GitHub Actions (CI). Reference example uses Java 21 + Spring Boot 3.x + Postgres 16 + Flyway + Testcontainers + Docker + Kubernetes.

---

## Phase 0 — Cleanup

### Task 1: Remove stale scaffold

**Files:**
- Delete: all 112 `.gitkeep` placeholders under `skills/`
- Delete: `skills/01-product-ideation/` through `skills/15-engineering-operations/` (numbered lifecycle folders, entire tree)
- Delete: `mcp/` (entire tree)
- Delete: `assets/` (entire tree)

- [ ] **Step 1: Verify nothing else references these paths**

Run: `git grep -nE "01-product-ideation|02-system-architecture|^mcp/|^assets/" -- ':!docs/superpowers/'`
Expected: no matches outside docs.

- [ ] **Step 2: Delete the directories**

```bash
git rm -rf skills/01-product-ideation skills/02-system-architecture \
  skills/03-frontend-engineering skills/04-backend-engineering \
  skills/05-database-engineering skills/06-testing-qa \
  skills/07-devops-infrastructure skills/08-cicd-delivery \
  skills/09-security-engineering skills/10-observability-monitoring \
  skills/11-platform-engineering skills/12-ai-native-engineering \
  skills/13-reliability-engineering skills/14-performance-engineering \
  skills/15-engineering-operations mcp assets
```

- [ ] **Step 3: Commit**

```bash
git commit -m "chore: remove stale scaffold (numbered lifecycle folders, mcp, assets)"
```

### Task 2: Rewrite legacy specs

**Files:**
- Modify: `SKILL_SPEC.md` (full rewrite)
- Modify: `WORKFLOW_SPEC.md` (full rewrite)
- Modify: `ROADMAP.md` (replace with v0.1–v1.0 phasing from design spec §13)

- [ ] **Step 1: Rewrite `SKILL_SPEC.md`**

Replace the file with the contents specified in design spec §7 (SKILL.md format + the 6 authoring rules). Title: `# Skill Specification`. Body explains the `SKILL.md` frontmatter format (`name`, `description`), the required section headings (When to use / Inputs / Process / Outputs / Quality checks / References), and lists the 6 authoring rules verbatim from the design spec.

- [ ] **Step 2: Rewrite `WORKFLOW_SPEC.md`**

Replace with the workflow format from design spec §8: frontmatter (`name`, `description`), `## Phases` with per-phase Entry/Exit/Gate, the rule that workflows never duplicate skill logic.

- [ ] **Step 3: Rewrite `ROADMAP.md`**

Replace with the v0.1 → v1.0 phasing table from design spec §13.

- [ ] **Step 4: Commit**

```bash
git add SKILL_SPEC.md WORKFLOW_SPEC.md ROADMAP.md
git commit -m "docs: rewrite SKILL_SPEC, WORKFLOW_SPEC, ROADMAP for v0.1 design"
```

---

## Phase 1 — Plugin scaffold and automation

### Task 3: Create plugin manifests

**Files:**
- Create: `.claude-plugin/plugin.json`
- Create: `.claude-plugin/marketplace.json`

- [ ] **Step 1: Write `.claude-plugin/plugin.json`**

```json
{
  "name": "claude-full-stack-2.0",
  "version": "0.1.0",
  "description": "AI-native software engineering skills from idea to production.",
  "author": {
    "name": "Amrit Malla",
    "email": "amritmalla2021@gmail.com"
  },
  "repository": "https://github.com/<owner>/claude-full-stack-2.0",
  "license": "MIT"
}
```

Note: confirm GitHub owner before merging; placeholder `<owner>` must be replaced.

- [ ] **Step 2: Write `.claude-plugin/marketplace.json`**

```json
{
  "name": "claude-full-stack-2.0",
  "displayName": "Claude Full Stack 2.0",
  "summary": "Production-grade Claude skills for full stack engineering and DevOps.",
  "tags": ["full-stack", "devops", "sre", "spring-boot", "kubernetes", "production"],
  "skills": [
    "skills/product/prd-from-idea",
    "skills/architecture/system-design-from-prd",
    "skills/backend/spring-boot-service-scaffold",
    "architecture/backend-architecture",
    "skills/backend/spring-security-auth-review",
    "skills/data/postgres-schema-and-migration",
    "skills/testing/integration-test-strategy",
    "skills/containers/dockerfile-and-jvm-tuning",
    "skills/cicd/github-actions-pipeline-hardened",
    "skills/deploy/k8s-deploy-manifest-review",
    "skills/observability/observability-readiness",
    "skills/operations/incident-rca-and-runbook"
  ]
}
```

- [ ] **Step 3: Commit**

```bash
git add .claude-plugin/
git commit -m "feat: add plugin and marketplace manifests"
```

### Task 4: Add LICENSE

**Files:**
- Modify: `LICENSE`

- [ ] **Step 1: Replace `LICENSE` with MIT text**

Use the standard MIT license template, copyright `2026 Amrit Malla`.

- [ ] **Step 2: Commit**

```bash
git add LICENSE
git commit -m "chore: adopt MIT license"
```

### Task 5: Skill validation script

**Files:**
- Create: `scripts/validate-skills.sh`

- [ ] **Step 1: Write the script**

```bash
#!/usr/bin/env bash
set -euo pipefail

fail=0
while IFS= read -r -d '' skill; do
  dir="$(dirname "$skill")"
  expected_name="$(basename "$dir")"

  # Extract YAML frontmatter
  fm="$(awk '/^---$/{f++; next} f==1{print} f==2{exit}' "$skill")"

  name="$(printf '%s\n' "$fm" | awk -F': *' '/^name:/{print $2; exit}')"
  desc="$(printf '%s\n' "$fm" | awk -F': *' '/^description:/{print $2; exit}')"

  if [[ -z "$name" || -z "$desc" ]]; then
    echo "FAIL $skill: missing name or description"; fail=1; continue
  fi
  if [[ "$name" != "$expected_name" ]]; then
    echo "FAIL $skill: name '$name' != directory '$expected_name'"; fail=1
  fi
  if [[ ${#desc} -gt 1024 ]]; then
    echo "FAIL $skill: description > 1024 chars"; fail=1
  fi
  if [[ ! "$desc" =~ ^Use\ when ]]; then
    echo "FAIL $skill: description must start with 'Use when'"; fail=1
  fi
done < <(find skills -name SKILL.md -print0)

exit $fail
```

- [ ] **Step 2: Make executable and test on an empty repo (no SKILL.md yet)**

```bash
chmod +x scripts/validate-skills.sh
./scripts/validate-skills.sh
```

Expected: exit 0 (no skills yet = no failures).

- [ ] **Step 3: Commit**

```bash
git add scripts/validate-skills.sh
git commit -m "ci: add skill frontmatter validation script"
```

### Task 6: Markdown lint script

**Files:**
- Create: `scripts/lint-markdown.sh`

- [ ] **Step 1: Write the script**

```bash
#!/usr/bin/env bash
set -euo pipefail
# Requires markdownlint-cli (npm i -g markdownlint-cli) and markdown-link-check
npx --yes markdownlint-cli "**/*.md" --ignore node_modules --ignore docs/superpowers
npx --yes markdown-link-check -q README.md SKILL_SPEC.md WORKFLOW_SPEC.md ROADMAP.md CONTRIBUTING.md
```

- [ ] **Step 2: Make executable**

```bash
chmod +x scripts/lint-markdown.sh
```

- [ ] **Step 3: Commit**

```bash
git add scripts/lint-markdown.sh
git commit -m "ci: add markdown lint script"
```

### Task 7: CI workflow

**Files:**
- Create: `.github/workflows/ci.yml`

- [ ] **Step 1: Write CI**

```yaml
name: ci
on:
  pull_request:
  push:
    branches: [main]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - name: Validate skill frontmatter
        run: ./scripts/validate-skills.sh
      - name: Lint markdown
        run: ./scripts/lint-markdown.sh
```

- [ ] **Step 2: Commit**

```bash
git add .github/workflows/ci.yml
git commit -m "ci: run skill validation and markdown lint on PRs"
```

---

## Phase 2 — Reference example skeleton

### Task 8: Scaffold `orders-api` reference service

**Files:**
- Create: `examples/spring-boot/orders-api/README.md`
- Create: `examples/spring-boot/orders-api/.skill-outputs/.gitkeep`

The actual Spring Boot code is *produced by skills 3–7* when authors execute them; we only commit the README and the outputs directory now.

- [ ] **Step 1: Write README**

```markdown
# orders-api (reference example)

Minimal e-commerce order service used as the canonical input for every skill in this plugin.

## Domain

Endpoints: create order, get order, list orders by customer, cancel order.
State machine: created → paid → shipped → cancelled.
Persistence: Postgres. Auth: JWT (customer scope). Events: logs `order.created`.

## Skill outputs

Every skill in this plugin is exercised against `orders-api`. The output produced by each skill is committed under `.skill-outputs/<skill-name>/` for reference.
```

- [ ] **Step 2: Commit**

```bash
git add examples/spring-boot/orders-api/
git commit -m "feat: add orders-api reference example skeleton"
```

---

## Phase 3 — Skills (one task per skill)

Each of the 12 skill tasks follows the same shape. Task 9 is the **fully-worked template**; tasks 10–20 reuse the structure with skill-specific content.

### Task 9: Skill — `prd-from-idea` (template)

**Files:**
- Create: `skills/product/prd-from-idea/SKILL.md`
- Create: `skills/product/README.md`
- Create: `examples/spring-boot/orders-api/.skill-outputs/prd-from-idea/PRD.md`

- [ ] **Step 1: Write `SKILL.md`**

```markdown
---
name: prd-from-idea
description: Use when a user has a rough product idea and needs a tight PRD before
  any architecture or coding work. Produces a one-page PRD with problem statement,
  users, scope, explicit non-goals, success metrics, and open questions.
---

# PRD from Idea

## When to use
Invoke when the user describes a new product, feature, or service in informal
terms ("I want to build X", "we need a thing that does Y") and there is no
written PRD yet. Do not invoke for changes to an existing PRD — use a doc-edit
flow instead.

## Inputs
- A 1–5 sentence informal description of the idea
- (Optional) Target users or customer segment
- (Optional) Known constraints (budget, deadline, stack)

## Process
1. Restate the idea in one sentence. Confirm with the user.
2. Identify the primary user persona and the job-to-be-done.
3. Draft a problem statement: what hurts today, for whom, and why now.
4. Define scope as a bulleted list of in-scope outcomes.
5. Define non-goals explicitly — what this product will NOT do.
6. Propose 2–4 success metrics, each measurable and time-bound.
7. List open questions blocking design.
8. Emit the PRD using the template in `references/prd-template.md`.

## Outputs
- `PRD.md` with sections: Problem, Users, Scope, Non-goals, Success Metrics,
  Open Questions.

## Quality checks
- [ ] Problem statement names a specific user and a specific pain.
- [ ] Non-goals section is non-empty and contradicts at least one tempting scope creep.
- [ ] Every success metric has a unit and a target value.
- [ ] No solutioning in the Problem section (no "we will build X").

## References
- references/prd-template.md
```

- [ ] **Step 2: Write the example output (`PRD.md` for orders-api)**

A complete one-page PRD for `orders-api` following the format above. Problem: small merchants need a lightweight order-tracking API. Users: backend devs at SMB e-commerce shops. Scope: create/get/list/cancel orders, JWT auth, Postgres persistence. Non-goals: payments, shipping integration, multi-tenant. Metrics: p95 < 200ms, 99.9% availability, zero data-loss on cancel.

- [ ] **Step 3: Write `skills/product/README.md`**

```markdown
# Product Skills

| Skill | Purpose |
|---|---|
| [prd-from-idea](prd-from-idea/) | Generate a tight PRD from a rough idea |
```

- [ ] **Step 4: Validate**

```bash
./scripts/validate-skills.sh
```
Expected: PASS.

- [ ] **Step 5: Manual trigger-prompt verification (in PR description)**

Author tests 3 should-match and 2 should-NOT-match prompts in Claude Code, confirms invocation behavior. Examples:
- Should match: "Help me write a PRD for a notes app"
- Should match: "I have an idea for a service that does X — what should I build first?"
- Should match: "Draft requirements for this new feature"
- Should NOT match: "Update the existing PRD with the new metric"
- Should NOT match: "Review this architecture doc"

- [ ] **Step 6: Commit**

```bash
git add skills/product/ examples/spring-boot/orders-api/.skill-outputs/prd-from-idea/
git commit -m "skill: add prd-from-idea"
```

### Task 10–20: Remaining 11 skills

For each skill below, follow the same 6-step pattern as Task 9: write `SKILL.md`, write the example output under `.skill-outputs/<skill-name>/`, add/update the domain `README.md` index, validate, manual trigger check, commit.

Per-skill specifics:

**Task 10: `architecture/system-design-from-prd`**
- Inputs: PRD.md from Task 9 output
- Process: identify bounded contexts, choose architecture style (monolith/modular/microservice), draw component diagram, list ADRs needed, capture failure modes
- Outputs: `system-design.md` + `adrs/0001-*.md`
- Quality checks: each component has clear responsibility + interface; at least one failure mode per component; ADR exists for every non-obvious choice
- Example output: system design + 2 ADRs for `orders-api` (monolithic Spring Boot, JWT auth choice)

**Task 11: `backend/spring-boot-service-scaffold`**
- Inputs: system design, service name, Java/Spring versions
- Process: generate `pom.xml`, package layout (controller/service/repository/domain), `application.yml` with `dev`/`staging`/`prod` profiles, Actuator config, global `@RestControllerAdvice` error envelope, Logback JSON encoder
- Outputs: complete project skeleton, list of files created
- Quality checks: Actuator endpoints gated by auth in non-dev profiles; `/actuator/health/liveness` returns < 50ms; no secrets in committed config; structured JSON logs outside dev
- Example output: scaffolded `orders-api` skeleton committed under `.skill-outputs/spring-boot-service-scaffold/`

**Task 12: `architecture/backend-architecture`**
- Inputs: PRD + domain model
- Process: define resources, draft OpenAPI 3.1 spec, define error model, pagination, idempotency keys for create/cancel, versioning strategy (URI vs header)
- Outputs: `openapi.yaml`, `api-conventions.md`
- Quality checks: every endpoint has at least one 4xx response defined; create/cancel accept `Idempotency-Key` header; pagination uses cursor not offset; errors share a single envelope shape
- Example output: `orders-api` OpenAPI spec with 4 endpoints

**Task 13: `data/postgres-schema-and-migration`**
- Inputs: domain model
- Process: design tables, primary keys, FKs, indexes; write initial Flyway migration; design a *zero-downtime* migration plan for one realistic future change (e.g., adding `currency` column to orders)
- Outputs: `V1__init.sql`, `V2__add_currency.sql` (with expand/migrate/contract phases documented)
- Quality checks: every FK has an index; no nullable FKs unless justified; migration uses `ADD COLUMN ... NULL` then backfill then `SET NOT NULL` (no blocking `ALTER`); rollback plan documented
- Example output: full migration set for `orders-api`

**Task 14: `backend/spring-security-auth-review`**
- Inputs: existing or scaffolded Spring Boot app, auth model (JWT for v0.1)
- Process: review `SecurityFilterChain` config, token validation, scope enforcement, refresh strategy, CSRF/CORS, secret storage
- Outputs: `auth-review.md` with findings + a hardened config snippet
- Quality checks: JWTs validated against issuer + audience + expiry + signing key; scopes enforced per endpoint; refresh tokens rotated; signing key not in source; CSRF disabled only with justification
- Example output: auth review for `orders-api`'s JWT setup

**Task 15: `testing/integration-test-strategy`**
- Inputs: scaffolded service + OpenAPI
- Process: design test pyramid for this service, scaffold Testcontainers Postgres setup, generate happy-path + 3 edge-case integration tests per endpoint, set up MockMvc/WebTestClient
- Outputs: `OrderIntegrationTest.java`, `pom.xml` dependency additions, `application-test.yml`
- Quality checks: tests reset DB between runs; no `@MockBean` of the repository under test; every endpoint has at least one negative test; idempotency tested for create/cancel
- Example output: full integration test class for `orders-api`

**Task 16: `containers/dockerfile-and-jvm-tuning`**
- Inputs: built JAR location, expected memory budget
- Process: multi-stage build (builder + distroless or jlink runtime), non-root user, healthcheck, JVM flags for containers (`-XX:MaxRAMPercentage`, `+UseG1GC`, `-XX:+ExitOnOutOfMemoryError`), `.dockerignore`
- Outputs: `Dockerfile`, `.dockerignore`, brief JVM-tuning rationale
- Quality checks: image runs as non-root; final image < 200MB; `MaxRAMPercentage` set explicitly; OOM kills the container; no secrets baked in
- Example output: Dockerfile for `orders-api`

**Task 17: `cicd/github-actions-pipeline-hardened`**
- Inputs: project type (Maven/Gradle), target registry, target cloud
- Process: design build → test → SAST → SBOM → sign (cosign) → push → deploy job graph; pin action SHAs; minimal `permissions`; OIDC to cloud (no long-lived secrets); concurrency control
- Outputs: `.github/workflows/build.yml`, `release.yml`
- Quality checks: every `uses:` pinned to SHA; `permissions:` defaults to read; cloud creds via OIDC; cosign signature published; SBOM uploaded as artifact
- Example output: hardened pipeline for `orders-api`

**Task 18: `deploy/k8s-deploy-manifest-review`**
- Inputs: existing manifests or app spec
- Process: review/produce Deployment + Service + HPA + PDB + NetworkPolicy + ServiceAccount; readiness/liveness/startup probes; resource requests + limits; security context (non-root, read-only FS, drop caps); rollout strategy
- Outputs: complete manifest set + a `findings.md` if reviewing existing
- Quality checks: requests AND limits set on every container; liveness ≠ readiness ≠ startup; runAsNonRoot=true; readOnlyRootFilesystem=true; NetworkPolicy denies by default; PDB present for >1 replica
- Example output: k8s manifests for `orders-api`

**Task 19: `observability/observability-readiness`**
- Inputs: running service spec
- Process: audit/produce Micrometer config, Prometheus scrape, OpenTelemetry tracing exporter, structured logging with trace correlation; define SLIs (availability, latency p99, error rate) and SLOs; design 3–5 alerts on burn rate, not raw thresholds
- Outputs: `observability.md`, Spring config snippets, Prometheus rule file, alert rule file
- Quality checks: each SLI has a corresponding SLO; alerts use multi-window multi-burn-rate; logs include trace_id; traces sampled at >0%; dashboards listed by name
- Example output: full observability config for `orders-api`

**Task 20: `operations/incident-rca-and-runbook`**
- Inputs: an incident description (timeline, logs, metrics) OR a synthetic incident for the example
- Process: build factual timeline (UTC), identify trigger / contributing factors / resolution; produce 5-whys; write postmortem in blameless format; extract a reusable runbook for the alert/symptom
- Outputs: `postmortem.md`, `runbooks/<symptom>.md`
- Quality checks: timeline events have timestamps and sources; root cause distinct from trigger; action items have owners and dates; runbook has detection criteria + diagnostic commands + mitigation steps + rollback
- Example output: synthetic "orders-api OOMKill at 02:13 UTC" incident → postmortem + runbook

---

## Phase 4 — Workflow and docs

### Task 21: Capstone workflow

**Files:**
- Create: `workflows/idea-to-production-spring-boot/WORKFLOW.md`

- [ ] **Step 1: Write `WORKFLOW.md`**

Use the exact format from design spec §8. Four phases — Define / Build / Ship / Operate — chaining the 12 skills in order. Each phase lists its skills, Entry artifacts, Exit artifacts, and the Gate (sign-off / green CI / staging smoke / on-call handoff). Frontmatter:

```yaml
---
name: idea-to-production-spring-boot
description: Use when taking a new service from concept to production on Kubernetes
  with Spring Boot and Postgres. Sequences 12 skills covering PRD, architecture,
  scaffold, API, schema, auth, tests, container, CI, deploy, observability, and ops.
---
```

- [ ] **Step 2: Validate frontmatter**

Workflows are not picked up by `validate-skills.sh` (it scans `skills/` only). Manually confirm `name` matches directory and description starts with "Use when".

- [ ] **Step 3: Commit**

```bash
git add workflows/
git commit -m "feat: add idea-to-production-spring-boot capstone workflow"
```

### Task 22: README, CONTRIBUTING, docs

**Files:**
- Modify: `README.md` (full rewrite)
- Modify: `CONTRIBUTING.md`
- Create: `docs/philosophy.md`
- Create: `docs/skill-authoring-guide.md`
- Create: `docs/workflow-authoring-guide.md`
- Delete: `docs/architecture/`, `docs/best-practices/`, `docs/case-studies/`, `docs/contributing/`, `docs/philosophy/`, `docs/standards/`, `docs/workflows/` (empty placeholder dirs)

- [ ] **Step 1: Rewrite `README.md`**

Sections: tagline, what it is, install (`/plugin install <marketplace> claude-full-stack-2.0`), skill index (table of all 12 with one-line purposes), workflow list, example walkthrough link, contributing link, license. State explicitly that v0.1 covers the production-ops half of "Full Stack 2.0"; frontend skills land in v0.2.

- [ ] **Step 2: Rewrite `CONTRIBUTING.md`**

Use the contribution flow from design spec §12 verbatim: issue → claim → PR with SKILL.md + example output + index entry + 5 trigger prompts → review → squash-merge.

- [ ] **Step 3: Write `docs/philosophy.md`**

200–400 words on the AI-native positioning: skills are imperative recipes, not docs; production-ops differentiation; one reference example per stack; the "idea → production" promise.

- [ ] **Step 4: Write `docs/skill-authoring-guide.md`**

Practical authoring walkthrough: pick a domain, copy the template, fill the 6 sections, run validation, write 5 trigger prompts, execute against `orders-api`, commit output, open PR. Link to `SKILL_SPEC.md` for the formal contract.

- [ ] **Step 5: Write `docs/workflow-authoring-guide.md`**

Similar to skill guide but for workflows. Emphasize: workflows sequence, they don't duplicate skill content.

- [ ] **Step 6: Delete empty docs subdirectories**

```bash
git rm -r docs/architecture docs/best-practices docs/case-studies \
  docs/contributing docs/philosophy docs/standards docs/workflows 2>/dev/null || true
```
(Use `2>/dev/null || true` because some may already be empty/missing after Task 1.)

- [ ] **Step 7: Commit**

```bash
git add README.md CONTRIBUTING.md docs/
git commit -m "docs: rewrite README and CONTRIBUTING; add philosophy and authoring guides"
```

### Task 23: Issue and PR templates

**Files:**
- Create: `.github/ISSUE_TEMPLATE/skill-proposal.yml`
- Create: `.github/PULL_REQUEST_TEMPLATE.md`

- [ ] **Step 1: Write skill-proposal issue form**

YAML form with fields: proposed name (kebab-case), domain (dropdown of 10 domains), one-paragraph when-to-use, expected outputs, why this skill belongs in v0.x.

- [ ] **Step 2: Write PR template**

Checklist: SKILL.md present? Example output committed under `.skill-outputs/`? Domain README index updated? 5 trigger prompts listed below? Manual execution against `orders-api` confirmed?

- [ ] **Step 3: Commit**

```bash
git add .github/ISSUE_TEMPLATE/ .github/PULL_REQUEST_TEMPLATE.md
git commit -m "chore: add skill-proposal issue form and PR template"
```

---

## Phase 5 — Release

### Task 24: Final validation

- [ ] **Step 1: Run full validation locally**

```bash
./scripts/validate-skills.sh && ./scripts/lint-markdown.sh
```
Expected: both PASS.

- [ ] **Step 2: Confirm all 12 `.skill-outputs/` directories are populated**

```bash
ls examples/spring-boot/orders-api/.skill-outputs/
```
Expected: 12 directories, one per skill.

- [ ] **Step 3: Verify marketplace.json lists exactly 12 skills**

```bash
grep -c '"skills/' .claude-plugin/marketplace.json
```
Expected: 12.

### Task 25: Tag v0.1.0

- [ ] **Step 1: Tag**

```bash
git tag -a v0.1.0 -m "v0.1.0 — initial 12-skill release"
```

- [ ] **Step 2: Push (after user approval)**

```bash
git push origin master --tags
```

---

## Self-Review Checklist

**Spec coverage** (design spec section → task):
- §4 Key Decisions → enforced throughout (format in Task 9; structure in Task 1; manifests in Task 3)
- §5 MVP list → Tasks 9–20
- §6 Repo structure → Tasks 1, 3, 8, 22
- §7 SKILL.md format → Tasks 2, 9
- §8 WORKFLOW.md format → Tasks 2, 21
- §9 `orders-api` → Task 8 + per-skill outputs
- §10 Quality bar → Task 5 (frontmatter) + per-skill quality checks + Task 9 step 5 (trigger prompts) + Task 24
- §11 Automation → Tasks 5, 6, 7
- §12 Contribution flow → Task 22 step 2 + Task 23
- §13 Phasing → Task 2 step 3 (in ROADMAP)
- §14 Open items (license) → Task 4

**Placeholder scan:** Tasks 10–20 use a per-skill specification list rather than full SKILL.md bodies. This is intentional — each skill's full prose is authored at execution time, but every required section, every quality check, and the example-output domain are specified concretely. No "TBD", "implement later", or "add validation" survives in the plan.

**Type consistency:** Skill names, directory paths, and marketplace.json entries match across Tasks 1, 3, 9–20, and 22.

---

**Plan complete and saved to `docs/superpowers/plans/2026-05-12-claude-full-stack-2.0-v0.1.md`. Two execution options:**

1. **Subagent-Driven (recommended)** — fresh subagent per task, review between tasks, fast iteration.
2. **Inline Execution** — execute tasks in this session with checkpoints.

Which approach?
