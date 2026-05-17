# Architecture And Implementation Rationale

This repository separates skills by ownership instead of by topic.

## Architecture Skills

Architecture skills are technology-agnostic. They define durable decisions, contracts, boundaries, quality gates, and handoff artifacts that implementation skills must obey.

Use `architecture/` when the output should remain true across frameworks, clouds, databases, and delivery tooling.

Examples:

- Product readiness and PRDs.
- System design and ADRs.
- Backend service behavior.
- Data, security, reliability, performance, and operations posture.

## Implementation Skills

Implementation skills are ecosystem-specific. They turn approved architecture decisions into concrete code, configuration, manifests, migrations, pipelines, or review artifacts.

Use `implementations/` when the answer depends on a framework, runtime, cloud, datastore, or delivery platform.

Examples:

- Spring Boot service scaffolding.
- PostgreSQL schema and migrations.
- Kubernetes workload manifests.
- GitHub Actions hardened pipelines.
- React application runtime and routing.

## Why This Boundary Matters

AI agents work better when each skill owns one repeatable job. Architecture skills prevent implementation skills from inventing product or system behavior. Implementation skills prevent architecture skills from drifting into framework-specific recipes too early.

The result is an idea-to-production chain where each stage can be reviewed, tested, and handed off without losing traceability.

