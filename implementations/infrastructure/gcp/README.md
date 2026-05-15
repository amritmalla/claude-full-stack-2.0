# gcp

> Status: scaffold.

## Purpose

Implements `architecture/infrastructure-platform`, `architecture/security`, `architecture/reliability`, and `architecture/operations` on Google Cloud Platform: organization and folder/project topology, network and identity foundation, workload runtime selection, observability and cost, and DR posture.

Architecture decisions (org structure, environment ladder, trust zones, compute primitive per workload, RPO/RTO targets) come from upstream and are taken as inputs here.

## Tool family

GCP belongs to **Family F — Cloud platforms** in the infrastructure layer model. See [`implementations/infrastructure/README.md`](../README.md) for the full archetype set and philosophy.

## Ecosystem (target)

- GCP Organizations + folders + projects
- Cloud Identity / Workspace + IAM
- Shared VPC, VPC Service Controls, Private Service Connect
- Cloud KMS + Secret Manager
- GKE / Cloud Run / Cloud Functions / Compute Engine — chosen per workload class
- Cloud Monitoring + Cloud Logging + Cloud Trace + Billing
- Cloud SQL HA / Spanner / GCS multi-region

## Skills

### Authored

_None._

### Archetype coverage

| # | Archetype | Skill | Status |
|---|---|---|---|
| 1 | account-and-organization-topology | `gcp-account-and-organization-topology` | planned |
| 2 | network-and-identity-foundation | `gcp-network-and-identity-foundation` | planned |
| 3 | workload-runtime-and-deployment | `gcp-workload-runtime-and-deployment` | planned |
| 4 | observability-and-cost-readiness | `gcp-observability-and-cost-readiness` | planned |
| 5 | dr-and-multi-region-readiness | `gcp-dr-and-multi-region-readiness` | planned |

### Planned skill scope (future work)

- **`gcp-account-and-organization-topology`** — Organization → folders → projects topology, environment isolation via project boundary, org policies for guardrails (resource location, allowed services, public-access prevention), billing structure and cost-attribution labels, baseline Security Command Center posture.
- **`gcp-network-and-identity-foundation`** — Shared VPC host + service projects, VPC Service Controls perimeters, Private Service Connect for managed services, Cloud Identity federation, IAM with predefined-role discipline, custom roles where justified, service-account key minimization (Workload Identity over keys), KMS CMEK strategy, Secret Manager with rotation.
- **`gcp-workload-runtime-and-deployment`** — compute primitive selection per workload (Cloud Run for managed containers, GKE for orchestrated, Cloud Functions for event-driven, Compute Engine for legacy/specialty, Cloud SQL/Spanner for relational, Firestore for document), External and Internal Load Balancing, autoscaling, deployment mechanics (Cloud Deploy, rolling/blue-green).
- **`gcp-observability-and-cost-readiness`** — Cloud Monitoring metrics and alerting, Cloud Logging with structured logs and log-based metrics, Cloud Trace for distributed tracing, dashboards per SLO, Cloud Billing + Budgets + Recommender, FinOps labeling discipline, committed-use discount posture.
- **`gcp-dr-and-multi-region-readiness`** — regional vs multi-regional resource selection, Cloud SQL HA and cross-region replicas, Spanner multi-region instance posture, GCS multi-region buckets, GKE regional clusters, Cloud Load Balancing global posture, documented and rehearsed failover drills with RPO/RTO validation.

## Architecture domains implemented

| Architecture domain | How |
|---|---|
| [infrastructure-platform](../../../architecture/infrastructure-platform/README.md) | Org topology, network, compute primitives, deployment. |
| [security](../../../architecture/security/README.md) | IAM, VPC SC, KMS, Secret Manager, Workload Identity. |
| [reliability](../../../architecture/reliability/README.md) | Regional/multi-regional posture, backups, failover. |
| [operations](../../../architecture/operations/README.md) | Cloud Monitoring alerting, runbook inputs. |
| [performance](../../../architecture/performance/README.md) | Right-sizing via Recommender, cost monitoring. |

## Standards this implementation conforms to

- [deployment-standards](../../../standards/deployment-standards/README.md)
- [security-standards](../../../standards/security-standards/README.md)
- [observability-standards](../../../standards/observability-standards/README.md)
- [naming-conventions](../../../standards/naming-conventions/README.md)
- [architecture-schema](../../../standards/architecture-schema/README.md)

## Upstream inputs

- Approved `infrastructure-platform.md` declaring org topology, environment ladder, network shape, identity model, and workload-runtime selections.
- Approved `architecture/security` decisions on IAM model, secret handling, encryption posture.
- Approved `architecture/reliability` decisions on SLOs and RPO/RTO targets per workload tier.
