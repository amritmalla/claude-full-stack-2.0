# Claude Full Stack 2.0 — Design Spec

**Date:** 2026-05-12
**Status:** Approved (brainstorming phase)
**Author:** Amrit Malla

## 1. Purpose

Claude Full Stack 2.0 is a Claude Code plugin distributing a curated set of production-grade Claude Skills that take a software project from idea to production. It is positioned as **AI-native software engineering** — not a prompt collection — with primary differentiation in DevOps, SRE, and production operations.

Tagline: *"AI-native software engineering skills from idea to production."*

## 2. Goals

- Ship a usable, installable Claude Code plugin in v0.1 with 12 skills covering the full lifecycle.
- Anchor every skill to a single reference example (`orders-api`, Spring Boot) so users can see input → output.
- Establish authoring conventions that scale to hundreds of skills without quality decay.
- Differentiate from existing AI coding repos by emphasizing maintainability, scalability, and operational excellence.

## 3. Non-Goals (v0.1)

- Multi-stack examples (Spring Boot only; Next.js parallel deferred to v0.3).
- MCP servers (deferred to v0.4 if a concrete need emerges).
- Automated skill execution tests in CI (manual author execution is the gate).
- The 112 empty scaffold directories from the prior structure.

## 4. Key Decisions

| # | Decision | Choice |
|---|---|---|
| 1 | Primary consumer | AI agents (Claude Code), via the `Skill` tool |
| 2 | Skill format | Official Anthropic format: `SKILL.md` + YAML frontmatter |
| 3 | Distribution | Claude Code plugin via `marketplace.json` / `plugin.json` |
| 4 | Organization | Flat domain folders in `skills/`; lifecycle sequencing in `workflows/` |
| 5 | MVP scope | 12 skills covering idea → ops, all exercised against one reference example |
| 6 | Reference stack | Spring Boot + Postgres + Kubernetes |
| 7 | Reference domain | `orders-api` — minimal e-commerce order service |

## 5. MVP Skill List (v0.1)

Twelve skills, one per lifecycle stage:

| # | Stage | Skill (directory under `skills/`) |
|---|---|---|
| 1 | Idea | `product/prd-from-idea` |
| 2 | Architecture | `architecture/system-design` |
| 3 | Backend scaffold | `backend/spring-boot-service-scaffold` |
| 4 | API | `architecture/backend-architecture` |
| 5 | Data | `data/postgres-schema-and-migration` |
| 6 | Security | `backend/spring-security-auth-review` |
| 7 | Quality | `architecture/quality-engineering` |
| 8 | Containerization | `containers/dockerfile-and-jvm-tuning` |
| 9 | CI/CD | `cicd/github-actions-pipeline-hardened` |
| 10 | Deploy | `deploy/k8s-deploy-manifest-review` |
| 11 | Observability | `observability/observability-readiness` |
| 12 | Operations | `architecture/operations` |

Skill selection methodology: weighted mix scoring on (D) differentiation 40% + (B) production risk 30% + (C) AI-leverage 20% + (A) pain/frequency 10%, then biased to ensure full-lifecycle coverage to honor the "Full Stack 2.0" brand promise.

## 6. Repository Structure

```
claude-full-stack-2.0/
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── skills/
│   ├── product/prd-from-idea/
│   ├── architecture/system-design/
│   ├── backend/
│   │   ├── spring-boot-service-scaffold/
│   │   ├── backend-architecture/
│   │   └── spring-security-auth-review/
│   ├── data/postgres-schema-and-migration/
│   ├── architecture/quality-engineering/
│   ├── containers/dockerfile-and-jvm-tuning/
│   ├── cicd/github-actions-pipeline-hardened/
│   ├── deploy/k8s-deploy-manifest-review/
│   ├── observability/observability-readiness/
│   └── architecture/operations/
├── workflows/
│   └── idea-to-production-spring-boot/
│       └── WORKFLOW.md
├── examples/
│   └── spring-boot/orders-api/
│       └── .skill-outputs/<skill-name>/   # committed example outputs
├── templates/
│   ├── adr/
│   ├── runbook/
│   ├── dockerfile/
│   ├── github-actions/
│   └── k8s/
├── docs/
│   ├── philosophy.md
│   ├── skill-authoring-guide.md
│   ├── workflow-authoring-guide.md
│   └── contributing.md
├── scripts/
│   ├── validate-skills.sh
│   └── lint-markdown.sh
├── .github/workflows/ci.yml
├── SKILL_SPEC.md
├── WORKFLOW_SPEC.md
├── ROADMAP.md
├── CONTRIBUTING.md
├── README.md
└── LICENSE
```

Each skill folder contains:
- `SKILL.md` (required)
- `references/` (optional, on-demand deep dives)
- `examples/` (optional, sample inputs/outputs)

Folders dropped from the prior scaffold: the 15 numbered lifecycle folders, 112 empty skill placeholders, the `mcp/` tree, and `assets/` (until a real asset exists).

## 7. SKILL.md Format

```markdown
---
name: <kebab-case, matches directory name>
description: Use when <trigger>. <One-sentence outcome.>
---

# <Title Case Name>

## When to use
## Inputs
## Process
## Outputs
## Quality checks
## References
```

### Authoring rules

1. **`description` is load-bearing.** It is the only text Claude reads to decide whether to invoke. Must start with "Use when", be ≤ 1024 characters, specific enough to match real triggers, generic enough to catch variants.
2. **`name` matches directory name exactly.** Lowercase, hyphen-separated.
3. **`SKILL.md` is the only file Claude reads by default.** All `references/*` are loaded on demand when the skill body instructs.
4. **Imperative recipes, not essays.** Every section answers "what does Claude do next?"
5. **Quality checks are binary-verifiable.** Never "ensure it's good." Always something a human or Claude can check pass/fail.
6. **One skill = one repeatable job.** Two outcomes = two skills.

## 8. WORKFLOW.md Format

Workflows sequence skills; they never duplicate skill logic.

```markdown
---
name: <kebab-case>
description: Use when <trigger>. Sequences <N> skills covering <stages>.
---

# <Title>

## Phases
### Phase N — <Name> (skills: a, b, c)
**Entry:** <required artifacts>
**Exit:** <produced artifacts>
**Gate:** <human or automated checkpoint>
```

The v0.1 workflow `idea-to-production-spring-boot` has four phases — Define, Build, Ship, Operate — chaining all 12 skills with gates between phases.

## 9. Reference Example: `orders-api`

A minimal e-commerce order service exercised by every skill.

- **Endpoints:** create order, get order, list by customer, cancel order
- **Persistence:** Postgres
- **Auth:** JWT (customer scope)
- **Events:** logs `order.created` (Kafka deferred)
- **State machine:** created → paid → shipped → cancelled

The repo ships the service unfinished. Each skill's example output is committed under `examples/spring-boot/orders-api/.skill-outputs/<skill-name>/`. Running the capstone workflow produces the production-ready version.

## 10. Quality Bar (v0.1, every skill)

1. Valid frontmatter (`name` matches directory; `description` starts with "Use when"; ≤ 1024 chars).
2. Skill invoked end-to-end against `orders-api` by author; output committed under `.skill-outputs/`.
3. Quality-checks section is concrete and binary-verifiable.
4. Author supplies 3 "should match" and 2 "should NOT match" trigger prompts in the PR description; manually verifies Claude's behavior on each.
5. `SKILL.md` ≤ ~400 lines; overflow moves to `references/`.

## 11. Automation

- `scripts/validate-skills.sh` — frontmatter schema check, name/dir match, description length cap.
- `scripts/lint-markdown.sh` — markdown lint + link check.
- `.github/workflows/ci.yml` — runs both on every PR.
- No skill execution tests in v0.1.

## 12. Contribution Flow

1. Open an issue using the skill-proposal template.
2. Maintainer assigns or claims.
3. PR includes: `SKILL.md`, example output under `.skill-outputs/`, an index entry in `skills/<domain>/README.md`, and the 5 trigger prompts in the PR description.
4. One maintainer reviews; author confirms manual execution in the PR.
5. Squash-merge with `skill: add <name>`.

Governance for v0.1: single maintainer. No formal RFC process. CODEOWNERS added in v0.2.

## 13. Release Phasing

| Version | Scope |
|---|---|
| **v0.1** | Cleanup, plugin manifest, 12 skills (SKILL.md only), `orders-api` example, capstone workflow, rewritten specs, docs. |
| **v0.2** | Add `references/` deep-dives to every skill. Add 3–5 honorable-mention skills (auth-review broadening, deployment-strategy-design, cost-optimization-audit, flaky-test-triage, nextjs-production-readiness). |
| **v0.3** | Second reference stack: Next.js + Node parallel example. Skills tested against both stacks. |
| **v0.4** | MCP server, if a concrete need emerges (e.g., live k8s state for diagnosis skills). |
| **v1.0** | Stability promise on `name`/`description`/output contracts; semver; published case studies. |

## 14. Open Items

- **License**: current `LICENSE` says "License to be determined." Pick before v0.1 ships. Recommendation: MIT (matches plugin ecosystem norms).
- **Plugin author metadata** in `plugin.json` (name, email, repo URL): fill in during implementation.
- **Marketplace listing copy**: drafted during v0.1 implementation.

## 15. Risks

- **Spring Boot lock-in.** Mitigation: skills are written stack-agnostic where possible; only examples are Spring Boot. v0.3 adds a second stack.
- **No frontend skill in v0.1.** May feel incomplete for a "Full Stack 2.0" brand. Mitigation: README is explicit that v0.1 covers the production-ops half; v0.2 adds `nextjs-production-readiness`.
- **Manual quality gate doesn't scale.** Acceptable for 12 skills; revisit when contributor volume grows in v0.2+.
