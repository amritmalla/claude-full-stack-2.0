# Claude Full Stack 2.0

> **AI-native software engineering skills from idea to production.**

A Claude Code plugin: a curated set of production-grade Claude Skills that take a software project from idea to production. Positioned as AI-native software engineering — not a prompt collection — with primary differentiation in DevOps, SRE, and production operations.

## Install

```bash
/plugin install https://github.com/amritmalla/claude-full-stack-2.0
```

Once installed, the skills below become invocable by Claude Code's `Skill` tool whenever their `description` matches your request.

## Skills (v0.1)

Twelve lifecycle-spanning skills, organized by domain:

| Stage | Skill | What it produces |
|---|---|---|
| Idea | [`prd-from-idea`](skills/product/prd-from-idea/) | One-page PRD: problem, users, scope, non-goals, metrics |
| Architecture | [`system-design-from-prd`](skills/architecture/system-design-from-prd/) | System design + ADRs |
| Backend scaffold | [`spring-boot-service-scaffold`](skills/backend/spring-boot-service-scaffold/) | Production-ready Spring Boot layout |
| API | [`rest-api-contract-design`](skills/backend/rest-api-contract-design/) | OpenAPI 3.1 with idempotency, cursor pagination, error envelope |
| Data | [`postgres-schema-and-migration`](skills/data/postgres-schema-and-migration/) | Schema + zero-downtime migration plan |
| Security | [`spring-security-auth-review`](skills/backend/spring-security-auth-review/) | JWT/OAuth2 review and hardening |
| Testing | [`integration-test-strategy`](skills/testing/integration-test-strategy/) | Testcontainers-based integration suite |
| Containers | [`dockerfile-and-jvm-tuning`](skills/containers/dockerfile-and-jvm-tuning/) | Multi-stage Dockerfile + container-aware JVM flags |
| CI/CD | [`github-actions-pipeline-hardened`](skills/cicd/github-actions-pipeline-hardened/) | OIDC, pinned SHAs, SBOM, cosign |
| Deploy | [`k8s-deploy-manifest-review`](skills/deploy/k8s-deploy-manifest-review/) | Hardened Kubernetes manifests |
| Observability | [`observability-readiness`](skills/observability/observability-readiness/) | SLIs/SLOs + multi-burn-rate alerts |
| Operations | [`incident-rca-and-runbook`](skills/operations/incident-rca-and-runbook/) | Blameless postmortem + reusable runbook |

## Workflow

[`idea-to-production-spring-boot`](workflows/idea-to-production-spring-boot/) chains all 12 skills with explicit Entry/Exit/Gate checkpoints across four phases: Define → Build → Ship → Operate.

## Reference example

Every skill is exercised against [`orders-api`](examples/spring-boot/orders-api/) — a minimal e-commerce order service. Skill outputs land under `examples/spring-boot/orders-api/.skill-outputs/<skill-name>/`.

## What's in v0.1, what's not

**In:** the production-ops half of "Full Stack 2.0" — DevOps, SRE, security, observability, plus the architecture and backend depth needed to make those skills land on real systems. Spring Boot as the single reference stack.

**Out:** frontend skills (Next.js production readiness lands in v0.2), a second reference stack (v0.3), and an MCP server (v0.4 if a real need emerges).

See [`ROADMAP.md`](ROADMAP.md) for the full release plan.

## Contributing

Read [`CONTRIBUTING.md`](CONTRIBUTING.md). New skills follow [`SKILL_SPEC.md`](SKILL_SPEC.md). New workflows follow [`WORKFLOW_SPEC.md`](WORKFLOW_SPEC.md).

## License

MIT. See [`LICENSE`](LICENSE).
