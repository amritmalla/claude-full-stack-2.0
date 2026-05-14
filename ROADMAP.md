# Roadmap

| Version | Scope |
|---|---|
| **v0.1** | Cleanup, plugin manifest, 12 lifecycle-spanning skills (`SKILL.md` only), the `orders-api` Spring Boot reference example, the `idea-to-production-spring-boot` capstone workflow, rewritten `SKILL_SPEC.md` and `WORKFLOW_SPEC.md`, README, CONTRIBUTING, and authoring guides. Goal: a usable, installable plugin a user can run end-to-end. |
| **v0.2** | Add `references/` deep-dives to every v0.1 skill. Add 3–5 honorable-mention skills (broader auth review, deployment-strategy-design, cost-optimization-audit, flaky-test-triage, `nextjs-production-readiness`). First frontend skill lands here. |
| **v0.3** | Second reference stack: parallel Next.js + Node example exercising the same skill set. Skills validated against both stacks. |
| **v0.4** | MCP server, if a concrete need emerges (e.g., a server that exposes live Kubernetes state to the diagnosis skills). |
| **v1.0** | Stability promise on `name`, `description`, and output contracts. Semantic versioning. Published case studies and contributor onboarding. |

## v0.1 Skill Set

| # | Stage | Skill |
|---|---|---|
| 1 | Idea | `product/prd-from-idea` |
| 2 | Architecture | `architecture/system-design-from-prd` |
| 3 | Backend scaffold | `backend/spring-boot-service-scaffold` |
| 4 | Backend architecture | `architecture/backend-architecture` |
| 5 | Data | `data/postgres-schema-and-migration` |
| 6 | Security | `backend/spring-security-auth-review` |
| 7 | Testing | `architecture/testing-quality` |
| 8 | Containerization | `containers/dockerfile-and-jvm-tuning` |
| 9 | CI/CD | `cicd/github-actions-pipeline-hardened` |
| 10 | Deploy | `deploy/k8s-deploy-manifest-review` |
| 11 | Observability | `observability/observability-readiness` |
| 12 | Operations | `architecture/operations` |

See [`docs/superpowers/specs/2026-05-12-claude-full-stack-2.0-design.md`](docs/superpowers/specs/2026-05-12-claude-full-stack-2.0-design.md) for the full v0.1 design and rationale.
