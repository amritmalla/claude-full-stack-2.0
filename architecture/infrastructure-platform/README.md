# infrastructure-platform

> Status: draft

## Purpose

Defines platform and infrastructure architecture from an approved system design: cloud and account topology, environment model, runtime substrate selection, network and trust-boundary architecture, identity and secrets strategy, deployment and release substrate, IaC ownership boundaries, CI/CD posture, operational platform services, cost strategy, and disaster posture.

Technology-agnostic and platform-oriented. Owns *what platform contracts exist and how workloads are isolated, deployed, and operated*, not the Terraform/manifests that implement them. Vendor-specific IaC and pipeline code lives under [implementations/infrastructure](../../implementations/infrastructure/).

## Owns

- Cloud/account topology and environment model
- Runtime substrate selection per workload class
- Network architecture and named trust boundaries
- Workload/human/service identity and secrets lifecycle
- Packaging, deployment, and release substrate
- IaC ownership boundaries and CI/CD trust model
- Cross-cutting platform services posture
- Cost/FinOps posture and disaster/resilience posture

## Produces

| Artifact | Conforms to |
|---|---|
| `platform-architecture.md` | [architecture-schema](../../standards/architecture-schema/README.md), [documentation-standards](../../standards/documentation-standards/README.md) |
| ADR drafts (substrate, region topology, IaC tool, deployment mechanism) | [architecture-schema](../../standards/architecture-schema/README.md) |

## Skills

- [infrastructure-platform](SKILL.md) - turns an approved system design into platform architecture: topology, environments, runtime substrate, network/trust zones, identity, secrets, deployment, IaC, CI/CD, cost, disaster posture, and implementation handoffs.

## Standards this architecture domain conforms to

- [architecture-schema](../../standards/architecture-schema/README.md) - `platform-architecture.md` artifact structure and system-design traceability.
- [security-standards](../../standards/security-standards/README.md) - trust zones, identity, secrets, supply-chain posture.
- [observability-standards](../../standards/observability-standards/README.md) - platform telemetry substrate.
- [deployment-standards](../../standards/deployment-standards/README.md) - release substrate, gating, rollback.
- [documentation-standards](../../standards/documentation-standards/README.md) - skill structure.

## Upstream inputs

Requires an approved `system-design.md` per [architecture-schema](../../standards/architecture-schema/README.md) whose design needs dedicated platform/infrastructure architecture. Workload inventory, component boundaries, and ADRs shape the platform architecture produced here.

## Downstream consumers

Platform architecture produced here is the source of truth for:

- [implementations/infrastructure/*](../../implementations/infrastructure/) - AWS, GCP, Azure, Kubernetes, Terraform, and GitHub Actions skills follow topology, substrate, and trust-boundary decisions.
- [architecture/security](../security/SKILL.md) - trust zones, identity, secrets, and supply-chain boundaries.
- [architecture/reliability](../reliability/SKILL.md) - failover topology and RTO/RPO inputs.
- [architecture/operations](../operations/SKILL.md) - observability substrate and runbook hooks.
