# aws

> Status: scaffold.

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

### Authored

- [aws-account-and-organization-topology](aws-account-and-organization-topology/SKILL.md) — AWS Organizations OU structure, landing-zone approach (Control Tower or custom), SCP guardrails mapped to security rationale, environment-isolated account layout, centralized audit (CloudTrail/Config/GuardDuty), and mandatory tagging/cost-allocation policy.

### Archetype coverage

| # | Archetype | Skill | Status |
|---|---|---|---|
| 1 | account-and-organization-topology | [`aws-account-and-organization-topology`](aws-account-and-organization-topology/SKILL.md) | authored |
| 2 | network-and-identity-foundation | `aws-network-and-identity-foundation` | planned |
| 3 | workload-runtime-and-deployment | `aws-workload-runtime-and-deployment` | planned |
| 4 | observability-and-cost-readiness | `aws-observability-and-cost-readiness` | planned |
| 5 | dr-and-multi-region-readiness | `aws-dr-and-multi-region-readiness` | planned |

### Planned skill scope (future work)

- **`aws-network-and-identity-foundation`** — VPC topology (per-env, per-tier subnets, multi-AZ), Transit Gateway or VPC peering for inter-account connectivity, PrivateLink for service-to-service, IAM Identity Center (SSO) federated to IdP, IAM role assumption patterns, permission boundaries, KMS CMK strategy (per-tenant, per-env), Secrets Manager with rotation, Route 53 zone strategy.
- **`aws-workload-runtime-and-deployment`** — compute primitive selection per workload (Lambda for ephemeral/event-driven, Fargate for managed containers, EKS for orchestrated containers, EC2/ASG for legacy, RDS/Aurora for relational, DynamoDB for KV), Application Load Balancer / Network Load Balancer posture, autoscaling configuration, deployment mechanics (CodeDeploy, blue/green for ALB, rolling for ECS).
- **`aws-observability-and-cost-readiness`** — CloudWatch Logs/Metrics/Alarms, AWS Distro for OpenTelemetry, X-Ray for tracing, dashboards per SLO, Cost Explorer + AWS Budgets + Cost Anomaly Detection, FinOps tagging discipline (`Environment`, `Workload`, `CostCenter`, `Owner`), savings-plan and RI posture.
- **`aws-dr-and-multi-region-readiness`** — multi-AZ default for tier-0 and tier-1, multi-region active-passive or active-active for tier-0 where architecture demands, RDS cross-region replicas, S3 cross-region replication, DynamoDB Global Tables, Route 53 health-check-based failover, AWS Backup posture, documented and rehearsed failover drills with RPO/RTO validation.

## Architecture domains implemented

| Architecture domain | How |
|---|---|
| [infrastructure-platform](../../../architecture/infrastructure-platform/README.md) | Account topology, network, compute primitives, deployment. |
| [security](../../../architecture/security/README.md) | IAM model, KMS, Secrets Manager, SCPs, trust zones. |
| [reliability](../../../architecture/reliability/README.md) | Multi-AZ/region posture, backups, failover. |
| [operations](../../../architecture/operations/README.md) | CloudWatch alarms, runbook inputs, audit. |
| [performance](../../../architecture/performance/README.md) | Compute right-sizing, cost monitoring, anomaly detection. |

## Standards this implementation conforms to

- [deployment-standards](../../../standards/deployment-standards/README.md)
- [security-standards](../../../standards/security-standards/README.md)
- [observability-standards](../../../standards/observability-standards/README.md)
- [naming-conventions](../../../standards/naming-conventions/README.md)
- [architecture-schema](../../../standards/architecture-schema/README.md) — tier classification drives DR posture, replica counts, alarm strictness.

## Upstream inputs

- Approved `infrastructure-platform.md` declaring org topology, environment ladder, network shape, identity model, and workload-runtime selections.
- Approved `architecture/security` decisions on IAM model, secret handling, encryption posture.
- Approved `architecture/reliability` decisions on SLOs and RPO/RTO targets per workload tier.
