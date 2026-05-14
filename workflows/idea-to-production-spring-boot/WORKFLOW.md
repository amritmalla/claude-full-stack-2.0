---
name: idea-to-production-spring-boot
description: Use when taking a new service from concept to production on
  Kubernetes with Spring Boot and Postgres. Sequences 12 skills covering PRD,
  architecture, scaffold, API, schema, auth, tests, container, CI, deploy,
  observability, and operations.
---

# Idea to Production — Spring Boot

This workflow chains every v0.1 skill into a single end-to-end lifecycle path. Each phase has an explicit Entry artifact, Exit artifact, and Gate. Do not advance to the next phase until the Gate is satisfied.

## Phases

### Phase 1 — Define (skills: `prd-from-idea`, `system-design-from-prd`)

**Entry:** A 1–5 sentence informal idea.
**Exit:** `PRD.md` plus `system-design.md` and the initial `adrs/` directory committed.
**Gate:** Stakeholder sign-off on scope, non-goals, and chosen architecture style.

### Phase 2 — Build (skills: `spring-boot-service-scaffold`, `backend-architecture`, `postgres-schema-and-migration`, `spring-security-auth-review`, `testing-quality`)

**Entry:** Approved design from Phase 1.
**Exit:** Service compiles; `openapi.yaml` published; Flyway migrations applied locally; auth review findings resolved; integration test suite green against Testcontainers.
**Gate:** PR review approved and CI green.

### Phase 3 — Ship (skills: `dockerfile-and-jvm-tuning`, `github-actions-pipeline-hardened`, `k8s-deploy-manifest-review`)

**Entry:** Phase 2 exit met.
**Exit:** Container image built, signed with cosign, and pushed; Kubernetes manifests reviewed and applied to staging; staging deployment healthy.
**Gate:** Staging smoke tests pass and rollout completed without errors.

### Phase 4 — Operate (skills: `observability-readiness`, `operations`)

**Entry:** Service is running in staging or production.
**Exit:** SLIs and SLOs defined; multi-window multi-burn-rate alerts firing into the on-call channel; at least one runbook drafted from a real or synthetic incident.
**Gate:** On-call handoff checklist signed.

## Rules

- Workflows sequence; they do not duplicate skill logic. Procedural detail lives in the linked skills.
- A phase is not complete until its Gate is satisfied.
- If a skill's Quality Checks fail, return to that skill before advancing.
