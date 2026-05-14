# kubernetes

> Status: draft

## Purpose

Implements Kubernetes deployment topology for services: Deployment, Service, HPA, PDB, NetworkPolicy, ServiceAccount, and related resources.

## Skills

- [k8s-deploy-manifest-review](k8s-deploy-manifest-review/SKILL.md) — authors or reviews Kubernetes manifests for production workloads (Deployment, Service, HPA, PDB, NetworkPolicy, security context).

## Architecture domains implemented

| Architecture domain | How |
|---|---|
| [infrastructure-platform](../../../architecture/infrastructure-platform/README.md) | Workload topology, autoscaling, disruption budgets. |
| [reliability](../../../architecture/reliability/README.md) | Readiness/liveness probes, PDBs, multi-replica defaults. |
| [security](../../../architecture/security/README.md) | NetworkPolicy, non-root containers, read-only root FS, dropped capabilities. |

## Standards this implementation conforms to

- [deployment-standards](../../../standards/deployment-standards/README.md) — rolling update strategy, readiness probes mandatory, canary/blue-green for tier-0.
- [security-standards](../../../standards/security-standards/README.md) — non-root, drop ALL caps, NetworkPolicy by default, ServiceAccount scoping.
- [observability-standards](../../../standards/observability-standards/README.md) — Prometheus scrape annotations or ServiceMonitor.
- [naming-conventions](../../../standards/naming-conventions/README.md) — `kebab-case` resource names, suffixed by kind when ambiguous.
