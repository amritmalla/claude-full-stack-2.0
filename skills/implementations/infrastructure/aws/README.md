# aws

> Status: active — all 5 archetypes authored.

## Purpose

Implements `architecture/infrastructure-platform`, `architecture/security`, `architecture/reliability`, and `architecture/operations` on Amazon Web Services: organization and account topology, network and identity foundation, workload runtime selection, observability and cost, and DR posture.

Architecture decisions (org structure, environment ladder, trust zones, compute primitive per workload, RPO/RTO targets) come from upstream and are taken as inputs here.

## Tool family

AWS belongs to **Family F — Cloud platforms** in the infrastructure layer model. See [`implementations/infrastructure/README.md`](../README.md) for the full archetype set and philosophy.

## Ecosystem (target)

- AWS Organizations + Control Tower (or equivalent landing-zone pattern)
- AWS SSO / IAM Identity Center + IAM roles
- VPC, Transit Gateway, PrivateLink, Route 53
- KMS + Secrets Manager + Parameter Store
- ECS / EKS / Lambda / Fargate / EC2 — chosen per workload class
- CloudWatch + AWS Distro for OpenTelemetry + Cost Explorer + AWS Budgets
- Backup, RDS PITR, S3 versioning + replication

## Skills

### Skill tier

The four archetype-scoped skills (2–5) are authored at **mature tier** — each is a directory of `SKILL.md` + `references/<name>-playbook.md` + `references/<name>-quality-rubric.md` + `assets/<name>.template.md`, following the `implementations/mobile/flutter` mature-tier exemplar. This is a **deliberate divergence** from the lean single-file convention used elsewhere in the infrastructure tier (terraform, archetype 1). The aws stack is therefore mixed-tier by design: the network/runtime/observability/DR successors are mature; `aws-account-and-organization-topology` remains lean.

### Authored

- [aws-account-and-organization-topology](aws-account-and-organization-topology/SKILL.md) — *archetype 1, lean*. AWS Organizations OU structure, landing-zone approach, SCP guardrails mapped to security rationale, environment-isolated account layout, centralized audit, and mandatory tagging/cost-allocation policy.
- [aws-network-and-identity-foundation](aws-network-and-identity-foundation/SKILL.md) — *archetype 2, mature*. Per-env tiered multi-AZ VPC, TGW/peering/PrivateLink, IAM Identity Center federation, bounded least-privilege roles, KMS CMK strategy, rotated Secrets Manager, Route 53.
- [aws-workload-runtime-and-deployment](aws-workload-runtime-and-deployment/SKILL.md) — *archetype 3, mature*. Compute-primitive selection by workload class, ALB/NLB, autoscaling, blue-green/canary/rolling deploy with automated rollback (EKS in-cluster manifests handed to Family G).
- [aws-observability-and-cost-readiness](aws-observability-and-cost-readiness/SKILL.md) — *archetype 4, mature*. CloudWatch/ADOT/X-Ray, SLO dashboards and alarms, AWS Budgets/Cost Anomaly Detection, FinOps discipline consuming the org tag policy, Savings Plans/RI posture.
- [aws-dr-and-multi-region-readiness](aws-dr-and-multi-region-readiness/SKILL.md) — *archetype 5, mature*. Multi-AZ baseline, tier-driven multi-region topology, cross-region replication, Route 53 failover with fail-back, AWS Backup, and a **rehearsed** drill with measured RPO/RTO.

### Archetype coverage

| # | Archetype | Skill | Status |
|---|---|---|---|
| 1 | account-and-organization-topology | [`aws-account-and-organization-topology`](aws-account-and-organization-topology/SKILL.md) *(lean)* | ✓ authored |
| 2 | network-and-identity-foundation | [`aws-network-and-identity-foundation`](aws-network-and-identity-foundation/SKILL.md) *(mature)* | ✓ authored |
| 3 | workload-runtime-and-deployment | [`aws-workload-runtime-and-deployment`](aws-workload-runtime-and-deployment/SKILL.md) *(mature)* | ✓ authored |
| 4 | observability-and-cost-readiness | [`aws-observability-and-cost-readiness`](aws-observability-and-cost-readiness/SKILL.md) *(mature)* | ✓ authored |
| 5 | dr-and-multi-region-readiness | [`aws-dr-and-multi-region-readiness`](aws-dr-and-multi-region-readiness/SKILL.md) *(mature)* | ✓ authored |

All five Family F archetypes are authored. Cross-archetype handoffs are named in each skill; IaC module/state mechanics remain the `terraform` Family H skills' ownership.

## Architecture domains implemented

| Architecture domain | How |
|---|---|
| [infrastructure-platform](../../../architecture/infrastructure-platform/SKILL.md) | Account topology, network, compute primitives, deployment. |
| [security](../../../architecture/security/SKILL.md) | IAM model, KMS, Secrets Manager, SCPs, trust zones. |
| [reliability](../../../architecture/reliability/SKILL.md) | Multi-AZ/region posture, backups, failover. |
| [operations](../../../architecture/operations/SKILL.md) | CloudWatch alarms, runbook inputs, audit. |
| [performance](../../../architecture/performance/SKILL.md) | Compute right-sizing, cost monitoring, anomaly detection. |

## Standards this implementation conforms to

- [deployment-standards](../../../../standards/deployment-standards/README.md)
- [security-standards](../../../../standards/security-standards/README.md)
- [observability-standards](../../../../standards/observability-standards/README.md)
- [naming-conventions](../../../../standards/naming-conventions/README.md)
- [architecture-schema](../../../../standards/architecture-schema/README.md) — tier classification drives DR posture, replica counts, alarm strictness.

## Upstream inputs

- Approved `infrastructure-platform.md` declaring org topology, environment ladder, network shape, identity model, and workload-runtime selections.
- Approved `architecture/security` decisions on IAM model, secret handling, encryption posture.
- Approved `architecture/reliability` decisions on SLOs and RPO/RTO targets per workload tier.
