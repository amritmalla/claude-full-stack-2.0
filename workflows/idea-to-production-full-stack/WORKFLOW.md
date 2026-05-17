---
name: idea-to-production-full-stack
description: Use when taking a new product from concept to production as a
  full-stack system — a Spring Boot + Postgres backend and a React web
  frontend deployed on Kubernetes. Sequences 18 skills across six phases
  covering PRD, system design, backend architecture and scaffold, schema,
  auth, frontend architecture and build, testing, performance, container,
  CI, deploy, observability, and operations.
---

# Idea to Production — Full Stack (Spring Boot + React)

This workflow is the full-stack capstone: it chains the idea-to-production skill path for a Spring Boot + Postgres backend and a React web frontend deployed on Kubernetes. Each phase has an explicit Entry artifact, Exit artifact, and Gate. Do not advance to the next phase until the Gate is satisfied.

## Phases

### Phase 1 — Define (skills: `idea-development`, `system-design`)

**Entry:** A 1–5 sentence informal idea.
**Exit:** `PRD.md` plus `system-design.md` and the initial `adrs/` directory committed.
**Gate:** Stakeholder sign-off on scope, non-goals, and chosen architecture style.

### Phase 2 — Build Backend (skills: `backend-architecture`, `spring-boot-service-scaffold`, `postgres-schema-and-migration`, `spring-security-auth-review`)

**Entry:** Approved design from Phase 1.
**Exit:** Service compiles; `openapi.yaml` published; Flyway migrations applied locally; auth review findings resolved.
**Gate:** Backend PR review approved and CI green.

### Phase 3 — Build Frontend (skills: `frontend-architecture`, `react-app-scaffold-and-runtime`, `react-routing-and-rendering-strategy`, `react-state-management-and-data-fetching`, `react-design-system-and-accessibility`)

**Entry:** `openapi.yaml` published in Phase 2.
**Exit:** React app scaffolded; routing and state wired to the backend API contract; accessible design system applied.
**Gate:** Frontend PR review approved, CI green, and the API contract consumed from `openapi.yaml`.

### Phase 4 — Verify (skills: `quality-engineering`, `react-performance-and-delivery-optimization`)

**Entry:** Backend and frontend integrated.
**Exit:** Risk-based contract and integration test suite green against Testcontainers; frontend performance budget met.
**Gate:** Full test suite green and performance budgets pass.

### Phase 5 — Ship (skills: `dockerfile-and-jvm-tuning`, `github-actions-pipeline-hardened`, `k8s-deploy-manifest-review`)

**Entry:** Phase 4 exit met.
**Exit:** Container image built, signed with cosign, and pushed; pipeline hardened; Kubernetes manifests reviewed and applied to staging; staging deployment healthy.
**Gate:** Staging smoke tests pass and rollout completed without errors.

### Phase 6 — Operate (skills: `spring-boot-observability-readiness`, `operations`)

**Entry:** Service is running in staging or production.
**Exit:** SLIs and SLOs defined; multi-window multi-burn-rate alerts firing into the on-call channel; at least one runbook drafted from a real or synthetic incident.
**Gate:** On-call handoff checklist signed.

## Rules

- Workflows sequence; they do not duplicate skill logic. Procedural detail lives in the linked skills.
- A phase is not complete until its Gate is satisfied.
- If a skill's Quality Checks fail, return to that skill before advancing.
