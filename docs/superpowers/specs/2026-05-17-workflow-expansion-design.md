# Workflow Expansion — Design

**Date:** 2026-05-17
**Status:** Approved (design)
**Goal:** Demonstrate skill composition by adding 4 workflows that chain existing skills in different shapes, and retire the narrower `idea-to-production-spring-boot` workflow (superseded by the new full-stack one).

## Constraints

- Every workflow conforms to `WORKFLOW_SPEC.md`: frontmatter `name` (matches directory) + `description` (starts with "Use when"); each phase has Entry, Exit, Gate; skills referenced by exact name in `(skills: …)`.
- Skill-reference resolution is now CI-enforced by `scripts/validate_skills.py` — every referenced name must be a real skill directory.
- Workflows sequence only; they never duplicate skill procedural content.

## Workflows

### 1. `idea-to-production-full-stack` (replaces `idea-to-production-spring-boot`)

Backend (Spring Boot + Postgres) + web frontend (React), idea to production on Kubernetes.

- **P1 Define** — `idea-development`, `system-design`
  Entry: 1–5 sentence idea. Exit: `PRD.md`, `system-design.md`, `adrs/`. Gate: stakeholder sign-off on scope and architecture style.
- **P2 Build Backend** — `backend-architecture`, `spring-boot-service-scaffold`, `postgres-schema-and-migration`, `spring-security-auth-review`
  Entry: approved design. Exit: service compiles; `openapi.yaml` published; Flyway migrations applied; auth findings resolved. Gate: backend PR approved, CI green.
- **P3 Build Frontend** — `frontend-architecture`, `react-app-scaffold-and-runtime`, `react-routing-and-rendering-strategy`, `react-state-management-and-data-fetching`, `react-design-system-and-accessibility`
  Entry: `openapi.yaml` from P2. Exit: React app scaffolded; routes/state wired to the API contract; accessible design system applied. Gate: frontend PR approved, CI green, API contract consumed from `openapi.yaml`.
- **P4 Verify** — `quality-engineering`, `react-performance-and-delivery-optimization`
  Entry: backend + frontend integrated. Exit: risk-based contract + integration tests green; frontend performance budget met. Gate: full test suite green; perf budgets pass.
- **P5 Ship** — `dockerfile-and-jvm-tuning`, `github-actions-pipeline-hardened`, `k8s-deploy-manifest-review`
  Entry: P4 met. Exit: image built, signed (cosign), pushed; pipeline hardened; K8s manifests reviewed and applied to staging. Gate: staging smoke tests pass.
- **P6 Operate** — `spring-boot-observability-readiness`, `operations`
  Entry: running in staging/prod. Exit: SLIs/SLOs; multi-window burn-rate alerts; at least one runbook. Gate: on-call handoff checklist signed.

### 2. `idea-to-production-flutter` (mobile)

- **P1 Define** — `idea-development`, `system-design`
  Entry: 1–5 sentence idea. Exit: `PRD.md`, `system-design.md`, `adrs/`. Gate: stakeholder sign-off.
- **P2 Build** — `mobile-architecture`, `flutter-app-scaffold-and-runtime`, `flutter-navigation-and-routing`, `flutter-state-and-data-fetching`, `flutter-design-system-and-accessibility`
  Entry: approved design. Exit: app scaffolded; navigation + state wired; accessible design system applied. Gate: PR approved, CI green.
- **P3 Harden** — `quality-engineering`, `flutter-performance-and-reliability`
  Entry: feature-complete build. Exit: test strategy executed; startup/jank/memory budgets met; crash-free target defined. Gate: tests green; perf and reliability budgets pass.
- **P4 Release** — `github-actions-pipeline-hardened`, `operations`
  Entry: release candidate build. Exit: CI produces signed store artifacts (App Bundle / IPA); staged rollout plan; crash-triage runbook. Gate: store-readiness checklist + on-call handoff signed. (No Kubernetes phase — release means store distribution.)

### 3. `production-readiness-review` (harden an existing service — non-build composition)

Demonstrates a review/harden shape rather than idea→production.

- **P1 Reliability** — `reliability`
  Entry: a running service and its `system-design.md`. Exit: failure modes, SLO targets, resilience gaps documented. Gate: reliability findings triaged with owners.
- **P2 Security** — `security`
  Entry: P1 complete. Exit: threat model and prioritized security findings with remediations. Gate: no unresolved high/critical findings.
- **P3 Performance** — `performance`
  Entry: P2 complete. Exit: performance budgets, identified bottlenecks, load posture. Gate: budgets defined and met or explicitly waived.
- **P4 Operational readiness** — `operations`
  Entry: P1–P3 remediations merged. Exit: runbooks, escalation paths, on-call handoff. Gate: on-call handoff checklist signed.

### 4. `cloud-foundation-on-aws` (infra-only, no application code)

- **P1 Platform strategy** — `infrastructure-platform`
  Entry: organization and workload requirements. Exit: platform architecture and landing-zone decisions. Gate: architecture sign-off.
- **P2 Account & network foundation** — `aws-account-and-organization-topology`, `aws-network-and-identity-foundation`
  Entry: approved platform strategy. Exit: org/OU/account topology and network/identity baseline defined. Gate: security and network review.
- **P3 IaC mechanics** — `terraform-module-and-repository-scaffold`, `terraform-state-and-secret-management`, `terraform-module-reuse-and-supply-chain`, `terraform-plan-gate-and-policy-as-code`, `terraform-apply-and-promotion-mechanics`
  Entry: P2 baseline defined. Exit: Terraform repo scaffold; state/secret strategy; supply-chain controls; policy-as-code plan gate; promotion mechanics. Gate: plan gate enforced in CI.
- **P4 Workload & operations** — `aws-workload-runtime-and-deployment`, `aws-observability-and-cost-readiness`, `aws-dr-and-multi-region-readiness`
  Entry: IaC mechanics in place. Exit: workload runtime defined; observability and cost guardrails; DR / multi-region posture. Gate: DR test executed and cost guardrails reviewed.

## Retirement of `idea-to-production-spring-boot`

Delete `workflows/idea-to-production-spring-boot/`. Update the 3 live references:

- `README.md:57` — repoint to the new workflow set; describe `idea-to-production-full-stack` as the backend+web capstone and mention the other three workflows.
- `examples/spring-boot/orders-api/README.md:31` — repoint to `idea-to-production-full-stack` (its P2 Build Backend phase is what `orders-api` exercises).
- `docs/workflow-authoring-guide.md:24` — replace the `idea-to-production-spring-boot` Define→Build→Ship→Operate example with `idea-to-production-full-stack` and its phase list.

Frozen `docs/superpowers/` plans and specs that mention the old name are historical artifacts — left untouched.

## Non-Goals

- No new skills; workflows only sequence existing skills.
- No changes to skill bodies or the `WORKFLOW.md` format itself.
- No `workflows/README.md` index (was an offered option, not selected).

## Verification

- `python scripts/validate_skills.py` passes — confirms all 4 new workflows have valid frontmatter and every referenced skill resolves.
- `python -m pytest` passes.
- `node scripts/lint_markdown.mjs` passes — no broken links, including the 3 repointed references.
- `grep` confirms zero live references to `idea-to-production-spring-boot` outside frozen `docs/superpowers/`.
