# Claude Full Stack 2.0

> **AI-augmented software engineering skills from idea to production.**

A Claude Code plugin: a curated set of production-grade Claude Skills that take a software project from idea to production. Positioned as AI-augmented software engineering — not a prompt collection — with primary differentiation in DevOps, SRE, and production operations.

## Install

Add the marketplace, then install the plugin from it:

```text
/plugin marketplace add amritmalla/claude-full-stack-2.0
/plugin install claude-full-stack-2-0@amritmalla-plugins
```

Once installed, the skills below become invocable by Claude Code's `Skill` tool whenever their `description` matches your request.

## Repository layout

This repo is an AI-augmented engineering operating system. Skills are organized by what they own, not by topic:

- **[skills/architecture/](skills/architecture/)** — technology-agnostic decision domains (product, architecture, backend, security, etc.).
- **[skills/implementations/](skills/implementations/)** — ecosystem-specific execution (Spring Boot, Postgres, Kubernetes, GitHub Actions, ...).
- **[architecture-patterns/](architecture-patterns/)** — reusable architectural strategies (event-driven, hexagonal, modular-monolith, ...).
- **[standards/](standards/)** — shared interoperability contracts that everything above conforms to.
- **[workflows/](workflows/)** — end-to-end execution flows that chain architecture + implementations.

See the long-form rationale in [`docs/architecture/research.md`](docs/architecture/research.md) and the guiding beliefs in [`docs/philosophy/`](docs/philosophy/README.md).

## Skills

The repository ships 80+ skills across the architecture decision domains and ecosystem implementations (Spring Boot, FastAPI, Node.js, React, Flutter, Postgres, MongoDB, Kubernetes, AWS, Terraform, GitHub Actions, OpenAI, Anthropic, LangChain, AutoGen, CrewAI, ...). Browse the full catalog under [`skills/architecture/`](skills/architecture/) and [`skills/implementations/`](skills/implementations/).

A representative end-to-end lifecycle path on the Spring Boot reference stack:

| Stage | Skill | What it produces |
|---|---|---|
| Idea | [`idea-development`](skills/architecture/idea-development/SKILL.md) | Discovery, refinement, validation, PRD specification, and execution readiness |
| Architecture | [`system-design`](skills/architecture/system-design/SKILL.md) | System design + ADRs |
| Backend architecture | [`backend-architecture`](skills/architecture/backend-architecture/SKILL.md) | Backend boundaries, domain behavior, contracts, transactions, handoff notes |
| Quality | [`quality-engineering`](skills/architecture/quality-engineering/SKILL.md) | Contract-driven test strategy, acceptance criteria, and integration test plan |
| Operations | [`operations`](skills/architecture/operations/SKILL.md) | Blameless postmortem, reusable runbook, and on-call handoff |
| Backend scaffold | [`spring-boot-service-scaffold`](skills/implementations/backend/spring-boot/spring-boot-service-scaffold/SKILL.md) | Production-ready Spring Boot layout |
| Security | [`spring-security-auth-review`](skills/implementations/backend/spring-boot/spring-security-auth-review/SKILL.md) | JWT/OAuth2 review and hardening |
| Observability | [`spring-boot-observability-readiness`](skills/implementations/backend/spring-boot/spring-boot-observability-readiness/SKILL.md) | SLIs/SLOs + multi-burn-rate alerts |
| Data | [`postgres-schema-and-migration`](skills/implementations/data/postgres/postgres-schema-and-migration/SKILL.md) | Schema + zero-downtime migration plan |
| Containers | [`dockerfile-and-jvm-tuning`](skills/implementations/infrastructure/kubernetes/dockerfile-and-jvm-tuning/SKILL.md) | Multi-stage Dockerfile + container-aware JVM flags |
| CI/CD | [`github-actions-pipeline-hardened`](skills/implementations/infrastructure/github-actions/github-actions-pipeline-hardened/SKILL.md) | OIDC, pinned SHAs, SBOM, cosign |
| Deploy | [`k8s-deploy-manifest-review`](skills/implementations/infrastructure/kubernetes/k8s-deploy-manifest-review/SKILL.md) | Hardened Kubernetes manifests |

## Workflows

Workflows sequence skills into lifecycle paths with explicit Entry/Exit/Gate checkpoints per phase:

- [`idea-to-production-full-stack`](workflows/idea-to-production-full-stack/) — Spring Boot + Postgres backend and React web frontend, idea to production on Kubernetes (the backend+web capstone).
- [`idea-to-production-flutter`](workflows/idea-to-production-flutter/) — a Flutter mobile app from idea to signed store release.
- [`production-readiness-review`](workflows/production-readiness-review/) — a non-build hardening pass (reliability → security → performance → operations) for an existing service.
- [`cloud-foundation-on-aws`](workflows/cloud-foundation-on-aws/) — an infrastructure-only AWS landing zone and Terraform delivery foundation.

## Claude Desktop

Claude Desktop doesn't load Claude Code plugins, but you can expose the 83
skills + 4 workflows as MCP tools via the companion package:

```bash
pip install claude-full-stack-skills
```

Then add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "claude-full-stack-skills": {
      "command": "claude-full-stack-skills"
    }
  }
}
```

Restart Claude Desktop. Skills become invocable by description match — same
routing logic as Claude Code's Skill tool. Full setup steps and reference-file
lookup are documented in [`INTEGRATION.md`](INTEGRATION.md).

## Memory

For durable cross-session memory and hierarchical retrieval over a repo's code, docs, and decisions, install [claude-repo-mem](https://github.com/amritmalla/claude-repo-mem) and follow [`INTEGRATION.md`](INTEGRATION.md). The [`memory-management`](skills/architecture/memory-management/SKILL.md) skill defines when each claude-repo-mem tool (`recall`, `trace`, `remember`, `plan_task`, `handoff`, `resume`, ...) is appropriate during architecture, implementation, and operations work.

## Scope

**In:** the full "Full Stack 2.0" surface — architecture decision domains plus ecosystem execution across backend (Spring Boot, FastAPI, Node.js), frontend (React), mobile (Flutter), data (Postgres, MongoDB), infrastructure (Kubernetes, AWS, Terraform, GitHub Actions), and AI (OpenAI, Anthropic, LangChain, AutoGen, CrewAI), composed by end-to-end workflows.

**Not yet:** several ecosystem directories are taxonomy placeholders awaiting skills (e.g. Go, Django, .NET, Vue, Azure, GCP), and an MCP server (only if a real need emerges).

## Contributing

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`CONVENTIONS.md`](CONVENTIONS.md). New skills follow [`SKILL_SPEC.md`](SKILL_SPEC.md). New workflows follow [`WORKFLOW_SPEC.md`](WORKFLOW_SPEC.md).

## License

MIT. See [`LICENSE`](LICENSE).
