# kubernetes

> Status: draft

## Purpose

Implements Kubernetes deployment topology for services: workload packaging (container images and manifests), network and identity policy, scaling and resilience, observability and operations, and supply-chain hardening. Container packaging (Docker) is folded in as a sub-skill of archetype 1 rather than a separate stack.

Architecture decisions (workload tier, runtime substrate, network shape, scaling targets, supply-chain posture) come from upstream and are taken as inputs here.

## Tool family

Kubernetes is the sole member of **Family G — Runtime / orchestration / packaging** in the infrastructure layer model. See [`implementations/infrastructure/README.md`](../README.md) for the full archetype set and philosophy.

## Ecosystem (target)

- Kubernetes 1.29+ on a managed control plane (EKS / GKE / AKS) or self-managed where architecture demands
- Container runtime: containerd
- Docker / BuildKit for image construction
- Distroless or jlink runtime images for JVM; minimal language-specific bases for others
- HPA + KEDA + VPA for scaling
- NetworkPolicy enforcement via the CNI (Calico / Cilium)
- Pod Security Standards (`restricted` baseline)
- Prometheus + Grafana + Loki + Tempo (or cloud-native equivalents) for observability
- cosign + SBOM (Syft) + Trivy/Grype for supply-chain
- Kyverno or Gatekeeper for admission control

## Skills

### Skill tier

The five archetype-scoped skills are authored at **mature tier** — each is a directory of `SKILL.md` + `references/<name>-playbook.md` + `references/<name>-quality-rubric.md` + `assets/<name>.template.md`, following the `implementations/mobile/flutter` mature-tier exemplar. This is a **deliberate divergence** from the lean single-file convention used elsewhere in the infrastructure tier (terraform, the omnibus, the JVM sub-skill). The kubernetes stack is therefore mixed-tier by design: the archetype-scoped successors are mature; the omnibus review pass and the language sub-skills remain lean.

### Authored

- [k8s-workload-packaging-and-manifest](k8s-workload-packaging-and-manifest/SKILL.md) — *archetype 1, mature tier*. Deployment/StatefulSet/DaemonSet/Job/CronJob, Service, Ingress, baseline HPA/PDB, probes, resource bounds, rollout parameters. Authoring successor to the omnibus manifest slice.
- [k8s-network-and-identity-policy](k8s-network-and-identity-policy/SKILL.md) — *archetype 2, mature tier*. Default-deny NetworkPolicy, least-privilege ServiceAccount/RBAC, ingress/Gateway posture, mTLS/mesh wiring, registry auth, PSS namespace floor.
- [k8s-scaling-and-resilience-topology](k8s-scaling-and-resilience-topology/SKILL.md) — *archetype 3, mature tier*. HPA/VPA/KEDA selection and tuning, tier-correct PDB sizing, anti-affinity, topology spread, graceful shutdown, rollout budgets.
- [k8s-observability-and-operations-readiness](k8s-observability-and-operations-readiness/SKILL.md) — *archetype 4, mature tier*. ServiceMonitor/PodMonitor, kube-state-metrics/cAdvisor coverage, log shipping, OTel tracing, SLO alerts, scoped audit collection, runbook inputs.
- [k8s-supply-chain-and-image-hardening](k8s-supply-chain-and-image-hardening/SKILL.md) — *archetype 5, mature tier*. Minimal non-root read-only-root-FS images, cosign signing, SBOM, scan-as-gate, Kyverno/Gatekeeper admission policy (extends the PSS floor).
- [k8s-deploy-manifest-review](k8s-deploy-manifest-review/SKILL.md) — *omnibus production-readiness review (lean)* covering Deployment, Service, HPA, PDB, NetworkPolicy, ServiceAccount, security context, probes, resource bounds, and rollout strategy. Touches archetypes 1, 2, 3, and 5; kept as the holistic cross-archetype review entry point.
- [dockerfile-and-jvm-tuning](dockerfile-and-jvm-tuning/SKILL.md) — *sub-skill of archetype 1 (lean)*, scoped to JVM containerization: multi-stage Dockerfile, distroless or jlink runtime, non-root user, container-aware JVM flags, healthcheck, `.dockerignore`. (Moved from the former `infrastructure/docker` stack, which has been retired.)

### Archetype coverage

| # | Archetype | Skill | Status |
|---|---|---|---|
| 1 | workload-packaging-and-manifest | [`k8s-workload-packaging-and-manifest`](k8s-workload-packaging-and-manifest/SKILL.md) *(mature)* + [`dockerfile-and-jvm-tuning`](dockerfile-and-jvm-tuning/SKILL.md) *(JVM sub-skill)* | ✓ authored (non-JVM packaging siblings still planned) |
| 2 | network-and-identity-policy | [`k8s-network-and-identity-policy`](k8s-network-and-identity-policy/SKILL.md) *(mature)* | ✓ authored |
| 3 | scaling-and-resilience-topology | [`k8s-scaling-and-resilience-topology`](k8s-scaling-and-resilience-topology/SKILL.md) *(mature)* | ✓ authored |
| 4 | observability-and-operations-readiness | [`k8s-observability-and-operations-readiness`](k8s-observability-and-operations-readiness/SKILL.md) *(mature)* | ✓ authored |
| 5 | supply-chain-and-image-hardening | [`k8s-supply-chain-and-image-hardening`](k8s-supply-chain-and-image-hardening/SKILL.md) *(mature)* | ✓ authored |

### Remaining planned scope

- Non-JVM container-packaging sub-skills of archetype 1 (`python-image-and-runtime`, `node-image-and-runtime`, `go-image-and-runtime`, `dotnet-image-and-runtime`, `static-binary-image`) as siblings of `dockerfile-and-jvm-tuning`.

## Omnibus skill posture

`k8s-deploy-manifest-review` is the **production-readiness review** entry point — useful when reviewing a workload holistically before promotion. It will not be deprecated when the archetype-scoped successors land; instead, it remains the cross-archetype review pass, and the new skills own the *authoring* of each slice. This is a documented exception to the one-skill-per-archetype rule.

## Architecture domains implemented

| Architecture domain | How |
|---|---|
| [infrastructure-platform](../../../architecture/infrastructure-platform/README.md) | Workload topology, autoscaling, disruption budgets, container packaging. |
| [reliability](../../../architecture/reliability/README.md) | Readiness/liveness probes, PDBs, multi-replica defaults, topology spread. |
| [security](../../../architecture/security/README.md) | NetworkPolicy, non-root, read-only root FS, dropped caps, image signing. |
| [operations](../../../architecture/operations/README.md) | Cluster and pod observability, runbook inputs, admission control. |
| [performance](../../../architecture/performance/README.md) | Resource requests/limits, HPA/VPA, JVM container-aware tuning. |

## Standards this implementation conforms to

- [deployment-standards](../../../standards/deployment-standards/README.md) — rolling update default; canary/blue-green for tier-0; readiness probes mandatory.
- [security-standards](../../../standards/security-standards/README.md) — non-root, drop ALL caps, NetworkPolicy by default, ServiceAccount scoping, signed images.
- [observability-standards](../../../standards/observability-standards/README.md) — Prometheus scrape annotations or ServiceMonitor.
- [naming-conventions](../../../standards/naming-conventions/README.md) — `kebab-case` resource and image names, suffixed by kind when ambiguous.
- [architecture-schema](../../../standards/architecture-schema/README.md) — tier classification drives PDB requirements and replica defaults.

## Upstream inputs

- Approved `infrastructure-platform.md` declaring runtime substrate, cluster topology, network shape, and supply-chain posture.
- Approved `architecture/security` decisions on network policy, identity, and image-trust requirements.
- Approved `architecture/reliability` decisions on SLOs, replica counts, and PDB requirements per tier.
- `backend-architecture.md` for workload tier, resource expectations, and operational contracts.
