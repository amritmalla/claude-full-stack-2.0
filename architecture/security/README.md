# security

> Status: draft

## Purpose

Defines security architecture from an approved system design: threat models, trust-boundary analysis, data classification, identity and authorization architecture, tenant-isolation strategy, secrets and key-management posture, abuse protections, supply-chain posture, audit requirements, and compliance mapping.

Technology-agnostic and threat-oriented. Owns *the security model* — trust boundaries, classification, identity, authorization, isolation — not the scanners, code fixes, or runtime hardening that enforce it. Tooling and remediation live in `implementations/*` and `operations`.

## Owns

- Data classification and handling rules
- Trust-boundary analysis and threat models
- Identity and authorization architecture
- Tenant-isolation strategy
- Secrets and key-management posture
- Input/output, abuse, and rate protections
- Audit posture and supply-chain trust
- Compliance control mapping

## Produces

| Artifact | Conforms to |
|---|---|
| `security-architecture.md` | [architecture-schema](../../standards/architecture-schema/README.md) (structure), [security-standards](../../standards/security-standards/README.md) (content), [documentation-standards](../../standards/documentation-standards/README.md) |
| ADR drafts (identity, isolation, encryption, supply-chain) | [architecture-schema](../../standards/architecture-schema/README.md) |

## Skills

- [security](SKILL.md) — turns an approved system design into security architecture: classification, trust boundaries, threat model, identity, authorization, isolation, secrets, audit, supply chain, compliance, and implementation handoffs.

## Standards this architecture domain conforms to

- [architecture-schema](../../standards/architecture-schema/README.md) — `security-architecture.md` artifact structure and system-design traceability.
- [security-standards](../../standards/security-standards/README.md) — auth schemes, scopes, secrets (security content).
- [observability-standards](../../standards/observability-standards/README.md) — security-event telemetry and audit signals.
- [deployment-standards](../../standards/deployment-standards/README.md) — supply-chain and artifact-promotion controls.
- [documentation-standards](../../standards/documentation-standards/README.md) — skill structure.

## Upstream inputs

Requires an approved `system-design.md` per [architecture-schema](../../standards/architecture-schema/README.md). Components, data flows, trust boundaries, and ADRs in the system design shape the security architecture produced here. Platform topology from `infrastructure-platform` informs trust zones when available.

## Downstream consumers

Security architecture produced here constrains:

- Security-relevant work across [implementations/*](../../implementations/) (e.g. `spring-security-auth-review`, `k8s-deploy-manifest-review`, `github-actions-pipeline-hardened`).
- [architecture/backend-architecture](../backend-architecture/README.md) and [architecture/data-architecture](../data-architecture/README.md) — authorization, classification, and data-protection decisions.
- [architecture/infrastructure-platform](../infrastructure-platform/README.md) — workload identity, secrets substrate, supply-chain controls.
- [architecture/operations](../operations/SKILL.md) — audit pipeline and security-incident clauses.
