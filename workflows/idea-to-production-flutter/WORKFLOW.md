---
name: idea-to-production-flutter
description: Use when taking a new mobile app from concept to store release
  with Flutter. Sequences 11 skills across four phases covering PRD, system
  design, mobile architecture, app scaffold, navigation, state, design
  system and accessibility, testing, performance and reliability, signed
  build pipeline, and operational readiness.
---

# Idea to Production — Flutter (Mobile)

This workflow is the mobile capstone: it chains the idea-to-production skill path for a Flutter app, ending in a signed store release rather than a Kubernetes deployment. Each phase has an explicit Entry artifact, Exit artifact, and Gate. Do not advance to the next phase until the Gate is satisfied.

## Phases

### Phase 1 — Define (skills: `idea-development`, `system-design`)

**Entry:** A 1–5 sentence informal idea.
**Exit:** `PRD.md` plus `system-design.md` and the initial `adrs/` directory committed.
**Gate:** Stakeholder sign-off on scope, non-goals, and chosen architecture style.

### Phase 2 — Build (skills: `mobile-architecture`, `flutter-app-scaffold-and-runtime`, `flutter-navigation-and-routing`, `flutter-state-and-data-fetching`, `flutter-design-system-and-accessibility`)

**Entry:** Approved design from Phase 1.
**Exit:** App scaffolded; navigation and state wired to data sources; accessible design system applied.
**Gate:** PR review approved and CI green.

### Phase 3 — Harden (skills: `quality-engineering`, `flutter-performance-and-reliability`)

**Entry:** Feature-complete build from Phase 2.
**Exit:** Risk-based test strategy executed; startup, jank, and memory budgets met; crash-free target defined.
**Gate:** Test suite green and performance and reliability budgets pass.

### Phase 4 — Release (skills: `github-actions-pipeline-hardened`, `operations`)

**Entry:** Release candidate build from Phase 3.
**Exit:** CI produces signed store artifacts (Android App Bundle / iOS IPA); staged rollout plan documented; crash-triage runbook drafted.
**Gate:** Store-readiness checklist and on-call handoff signed.

## Rules

- Workflows sequence; they do not duplicate skill logic. Procedural detail lives in the linked skills.
- A phase is not complete until its Gate is satisfied.
- If a skill's Quality Checks fail, return to that skill before advancing.
- Release means store distribution; there is no Kubernetes deployment phase.
