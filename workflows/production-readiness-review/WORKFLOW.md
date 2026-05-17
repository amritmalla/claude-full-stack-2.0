---
name: production-readiness-review
description: Use when an existing service needs a structured hardening pass
  before a production launch, a reliability milestone, or an ownership
  handoff. Sequences 4 review skills across reliability, security,
  performance, and operational readiness, producing prioritized findings
  and an on-call-ready service rather than new application code.
---

# Production Readiness Review

This workflow hardens a service that already exists. Unlike the idea-to-production capstones, it builds nothing new — it chains the cross-cutting review skills into a single readiness pass. Each phase has an explicit Entry artifact, Exit artifact, and Gate. Do not advance to the next phase until the Gate is satisfied.

## Phases

### Phase 1 — Reliability (skills: `reliability`)

**Entry:** A running service and its `system-design.md`.
**Exit:** Failure modes enumerated; SLO targets set; resilience gaps documented.
**Gate:** Reliability findings triaged and assigned owners.

### Phase 2 — Security (skills: `security`)

**Entry:** Phase 1 complete.
**Exit:** Threat model and prioritized security findings with concrete remediations.
**Gate:** No unresolved high or critical findings.

### Phase 3 — Performance (skills: `performance`)

**Entry:** Phase 2 complete.
**Exit:** Performance budgets defined; bottlenecks identified; load posture documented.
**Gate:** Budgets defined and met, or explicitly waived with rationale.

### Phase 4 — Operational readiness (skills: `operations`)

**Entry:** Phase 1–3 remediations merged.
**Exit:** Runbooks, escalation paths, and an on-call handoff package.
**Gate:** On-call handoff checklist signed.

## Rules

- Workflows sequence; they do not duplicate skill logic. Procedural detail lives in the linked skills.
- A phase is not complete until its Gate is satisfied.
- If a skill's Quality Checks fail, return to that skill before advancing.
- This workflow reviews and hardens an existing service; it does not scaffold or implement features.
