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

### Authored

- [k8s-deploy-manifest-review](k8s-deploy-manifest-review/SKILL.md) — *omnibus production-readiness review* covering Deployment, Service, HPA, PDB, NetworkPolicy, ServiceAccount, security context, probes, resource bounds, and rollout strategy. Touches archetypes 1, 2, 3, and 5; kept as the holistic review entry point.
- [dockerfile-and-jvm-tuning](dockerfile-and-jvm-tuning/SKILL.md) — *sub-skill of archetype 1*, scoped to JVM containerization: multi-stage Dockerfile, distroless or jlink runtime, non-root user, container-aware JVM flags, healthcheck, `.dockerignore`. (Moved from the former `infrastructure/docker` stack, which has been retired.)

### Archetype coverage

| # | Archetype | Skill | Status |
|---|---|---|---|
| 1 | workload-packaging-and-manifest | [`dockerfile-and-jvm-tuning`](dockerfile-and-jvm-tuning/SKILL.md) *(JVM sub-skill)* + [`k8s-deploy-manifest-review`](k8s-deploy-manifest-review/SKILL.md) *(omnibus)* | partial (JVM-only image, omnibus manifests) |
| 2 | network-and-identity-policy | covered partially by `k8s-deploy-manifest-review` *(omnibus)* | split planned |
| 3 | scaling-and-resilience-topology | covered partially by `k8s-deploy-manifest-review` *(omnibus)* | split planned |
| 4 | observability-and-operations-readiness | _none_ | planned |
| 5 | supply-chain-and-image-hardening | covered partially by `k8s-deploy-manifest-review` *(omnibus)* + `dockerfile-and-jvm-tuning` | split planned |

### Planned skill scope (future work)

- **`k8s-workload-packaging-and-manifest`** *(archetype 1, archetype-scoped successor to the omnibus)* — Deployment / StatefulSet / Job / CronJob / Service / Ingress / HPA / PDB authoring, probe configuration, resource requests/limits, rolling-update parameters. Plus non-JVM container packaging variants (`python-image-and-runtime`, `node-image-and-runtime`, `go-image-and-runtime`, `dotnet-image-and-runtime`, `static-binary-image`) as sibling sub-skills of `dockerfile-and-jvm-tuning`.
- **`k8s-network-and-identity-policy`** *(archetype 2)* — NetworkPolicy authoring (default-deny, namespace-scoped, label-selected), ServiceAccount and RBAC (least-privilege Role/ClusterRole), Ingress/Gateway API posture, mTLS or service-mesh wiring (Istio/Linkerd) where adopted, image-pull secrets, registry auth, Pod Security Standards enforcement.
- **`k8s-scaling-and-resilience-topology`** *(archetype 3)* — HPA / VPA / KEDA selection, PDB sizing per tier, pod anti-affinity and topology-spread constraints, multi-zone placement, `terminationGracePeriodSeconds` and preStop hooks for graceful shutdown, surge and `maxUnavailable` budgets per workload tier.
- **`k8s-observability-and-operations-readiness`** *(archetype 4)* — kube-state-metrics, cAdvisor metrics, Prometheus scrape via ServiceMonitor/PodMonitor, log shipping (Fluent Bit / Vector / Loki / cloud-native), distributed tracing wiring (OTel collector), audit-log configuration, runbook inputs for pod-eviction storms, ImagePullBackOff sprees, and node-pressure incidents.
- **`k8s-supply-chain-and-image-hardening`** *(archetype 5, archetype-scoped successor to the security-context slice of the omnibus)* — minimal base images, non-root user, read-only root FS, dropped capabilities, image signing (cosign), SBOM (Syft), vulnerability scanning (Trivy/Grype) as a required gate, admission control via Kyverno/Gatekeeper for policy enforcement.

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
