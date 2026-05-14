# Claude Full Stack 2.0

> **AI-native software engineering skills from idea to production.**

A Claude Code plugin: a curated set of production-grade Claude Skills that take a software project from idea to production. Positioned as AI-native software engineering — not a prompt collection — with primary differentiation in DevOps, SRE, and production operations.

## Install

```bash
/plugin install https://github.com/amritmalla/claude-full-stack-2.0
```

Once installed, the skills below become invocable by Claude Code's `Skill` tool whenever their `description` matches your request.

## Repository layout

This repo is an AI-native engineering operating system. Skills are organized by what they own, not by topic:

- **[architecture/](architecture/)** — technology-agnostic decision domains (product, architecture, backend, security, etc.).
- **[implementations/](implementations/)** — ecosystem-specific execution (Spring Boot, Postgres, Kubernetes, GitHub Actions, ...).
- **[patterns/](patterns/)** — reusable architectural strategies (event-driven, hexagonal, modular-monolith, ...).
- **[standards/](standards/)** — shared interoperability contracts that everything above conforms to.
- **[workflows/](workflows/)** — end-to-end execution flows that chain architecture + implementations.

See the long-form rationale in [`docs/architecture/research.md`](docs/architecture/research.md).

## Skills (v0.1)

Twelve lifecycle-spanning skills:

| Stage | Skill | What it produces |
|---|---|---|
| Idea | [`idea-development`](architecture/idea-development/) | Discovery, refinement, validation, PRD specification, and execution readiness |
| Architecture | [`system-design`](architecture/system-design/) | System design + ADRs |
| Backend architecture | [`backend-architecture`](architecture/backend-architecture/) | Backend boundaries, domain behavior, contracts, transactions, handoff notes |
| Testing | [`integration-test-strategy`](architecture/testing-quality/integration-test-strategy/) | Testcontainers-based integration suite |
| Operations | [`incident-rca-and-runbook`](architecture/operations/incident-rca-and-runbook/) | Blameless postmortem + reusable runbook |
| Backend scaffold | [`spring-boot-service-scaffold`](implementations/backend/spring-boot/spring-boot-service-scaffold/) | Production-ready Spring Boot layout |
| Security | [`spring-security-auth-review`](implementations/backend/spring-boot/spring-security-auth-review/) | JWT/OAuth2 review and hardening |
| Observability | [`observability-readiness`](implementations/backend/spring-boot/observability-readiness/) | SLIs/SLOs + multi-burn-rate alerts |
| Data | [`postgres-schema-and-migration`](implementations/data/postgres/postgres-schema-and-migration/) | Schema + zero-downtime migration plan |
| Containers | [`dockerfile-and-jvm-tuning`](implementations/infrastructure/docker/dockerfile-and-jvm-tuning/) | Multi-stage Dockerfile + container-aware JVM flags |
| CI/CD | [`github-actions-pipeline-hardened`](implementations/infrastructure/github-actions/github-actions-pipeline-hardened/) | OIDC, pinned SHAs, SBOM, cosign |
| Deploy | [`k8s-deploy-manifest-review`](implementations/infrastructure/kubernetes/k8s-deploy-manifest-review/) | Hardened Kubernetes manifests |

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
