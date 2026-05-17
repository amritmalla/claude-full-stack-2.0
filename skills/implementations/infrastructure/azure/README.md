# azure

> Status: scaffold.

## Purpose

Implements `architecture/infrastructure-platform`, `architecture/security`, `architecture/reliability`, and `architecture/operations` on Microsoft Azure: tenant and management-group topology, network and identity foundation, workload runtime selection, observability and cost, and DR posture.

Architecture decisions (tenant structure, environment ladder, trust zones, compute primitive per workload, RPO/RTO targets) come from upstream and are taken as inputs here.

## Tool family

Azure belongs to **Family F — Cloud platforms** in the infrastructure layer model. See [`implementations/infrastructure/README.md`](../README.md) for the full archetype set and philosophy.

## Ecosystem (target)

- Microsoft Entra ID (formerly Azure AD) + management groups + subscriptions
- Azure Policy + Azure Blueprints (or Bicep/Terraform-driven landing zones)
- VNet, VNet peering, Private Endpoint, Azure Firewall
- Azure Key Vault
- AKS / Container Apps / App Service / Functions / VM Scale Sets — chosen per workload class
- Azure Monitor + Application Insights + Log Analytics + Cost Management
- Azure SQL HA / Cosmos DB multi-region / Storage GRS

## Skills

### Authored

_None._

### Archetype coverage

| # | Archetype | Skill | Status |
|---|---|---|---|
| 1 | account-and-organization-topology | `azure-account-and-organization-topology` | planned |
| 2 | network-and-identity-foundation | `azure-network-and-identity-foundation` | planned |
| 3 | workload-runtime-and-deployment | `azure-workload-runtime-and-deployment` | planned |
| 4 | observability-and-cost-readiness | `azure-observability-and-cost-readiness` | planned |
| 5 | dr-and-multi-region-readiness | `azure-dr-and-multi-region-readiness` | planned |

### Planned skill scope (future work)

- **`azure-account-and-organization-topology`** — tenant and management-group hierarchy aligned to Cloud Adoption Framework (CAF), subscription per environment per workload, Azure Policy assignments for guardrails, billing scopes and cost-allocation tags, Defender for Cloud baseline.
- **`azure-network-and-identity-foundation`** — hub-and-spoke VNet topology, VNet peering, Private Endpoint and Private Link for managed services, Azure Firewall or NVA selection, Entra ID with Conditional Access and PIM, managed identities for workloads, Key Vault with RBAC and rotation, custom role discipline.
- **`azure-workload-runtime-and-deployment`** — compute primitive selection per workload (App Service for managed web apps, Container Apps or AKS for containers, Functions for event-driven, VM Scale Sets for legacy, Azure SQL / Cosmos DB / Storage per data class), Application Gateway / Front Door / Load Balancer posture, autoscaling, deployment mechanics (deployment slots, rolling, blue/green via Front Door).
- **`azure-observability-and-cost-readiness`** — Azure Monitor metrics and alerts, Application Insights for app telemetry, Log Analytics workspace strategy, distributed tracing via OpenTelemetry exporters, dashboards per SLO, Cost Management + Budgets + Advisor, FinOps tagging discipline, reserved-instance posture.
- **`azure-dr-and-multi-region-readiness`** — Availability Zones default for tier-0/tier-1, region pairs for cross-region replication, Azure SQL geo-replication, Cosmos DB multi-region writes, Storage GRS/RA-GRS, Front Door / Traffic Manager for traffic shifting, Azure Backup and Site Recovery posture, documented and rehearsed failover drills with RPO/RTO validation.

## Architecture domains implemented

| Architecture domain | How |
|---|---|
| [infrastructure-platform](../../../architecture/infrastructure-platform/README.md) | Tenant topology, network, compute primitives, deployment. |
| [security](../../../architecture/security/README.md) | Entra ID, Key Vault, managed identities, Azure Policy. |
| [reliability](../../../architecture/reliability/README.md) | Availability Zones, region pairs, backups, failover. |
| [operations](../../../architecture/operations/README.md) | Azure Monitor alerting, runbook inputs. |
| [performance](../../../architecture/performance/README.md) | Right-sizing via Advisor, cost monitoring. |

## Standards this implementation conforms to

- [deployment-standards](../../../../standards/deployment-standards/README.md)
- [security-standards](../../../../standards/security-standards/README.md)
- [observability-standards](../../../../standards/observability-standards/README.md)
- [naming-conventions](../../../../standards/naming-conventions/README.md)
- [architecture-schema](../../../../standards/architecture-schema/README.md)

## Upstream inputs

- Approved `infrastructure-platform.md` declaring tenant topology, environment ladder, network shape, identity model, and workload-runtime selections.
- Approved `architecture/security` decisions on IAM model, secret handling, encryption posture.
- Approved `architecture/reliability` decisions on SLOs and RPO/RTO targets per workload tier.
