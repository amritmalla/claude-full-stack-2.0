# implementations/infrastructure

Technology-specific execution skills for infrastructure.

## Philosophy

Each infrastructure implementation skill speaks as a **senior platform / DevOps / SRE engineer** in a specific tool or platform. It implements, hardens, or reviews — it does not invent architectural decisions. Architecture artifacts produced by `architecture/infrastructure-platform`, `architecture/reliability`, `architecture/security`, `architecture/operations`, and `architecture/performance` are the source of truth; the implementation skill consumes them and emits IaC modules, deployment manifests, pipeline definitions, network and identity policies, observability and cost wiring, and DR procedures.

If an artifact is silent on a needed decision (compute primitive per workload, trust zone boundaries, env-promotion ladder, RPO/RTO target), the implementation skill **pauses and raises an ADR candidate** against the upstream domain rather than guessing.

Skills are scoped, not monolithic. Each `SKILL.md`:

- declares its upstream architecture domain(s) and the standards it conforms to,
- requires the upstream artifact when scaffolding new accounts, networks, clusters, modules, or pipelines, and runs standalone for review or hardening when the artifact does not yet exist,
- maps to exactly one archetype from its **tool family** (below),
- emits concrete IaC code, manifests, workflow YAML, policies, and runbook inputs — not prose-only deliverables.

## Tool families

Unlike the backend and frontend layers (one archetype set per layer), the infrastructure layer defines **four tool families** by role. Each family has its own archetype set tuned to the tools' responsibilities. Stacks belong to exactly one family.

| Family | Role | Stacks |
|---|---|---|
| F | Cloud platforms | [aws](aws/), [gcp](gcp/), [azure](azure/) |
| G | Runtime / orchestration / packaging | [kubernetes](kubernetes/) *(includes container packaging — Docker folded in as a sub-skill)* |
| H | Infrastructure-as-code | [terraform](terraform/) |
| I | CI/CD | [github-actions](github-actions/) |

### Family F — Cloud platforms

For AWS, GCP, Azure. Owns account topology, identity foundation, workload runtime primitives, observability/cost, and DR.

| # | Archetype | What the skill produces | Primary upstream |
|---|---|---|---|
| 1 | **account-and-organization-topology** | Org/account/project/subscription structure, environment isolation, baseline guardrails (SCPs / org policies / management groups), billing topology. | `infrastructure-platform` + `security` |
| 2 | **network-and-identity-foundation** | VPC/VNet topology, trust zones, identity provider integration, IAM model, secrets manager, KMS/HSM, encryption posture, peering and private connectivity. | `security` + `infrastructure-platform` |
| 3 | **workload-runtime-and-deployment** | Compute primitive selection (VM / managed container / serverless / managed runtime), load balancing, autoscaling, deployment mechanics per workload class. | `infrastructure-platform` + `reliability` |
| 4 | **observability-and-cost-readiness** | Provider-native logs/metrics/traces wiring, dashboards, SLO alerting, cost monitoring with budgets and anomaly detection, FinOps tagging discipline. | `operations` + `performance` |
| 5 | **dr-and-multi-region-readiness** | Multi-AZ/region posture, RPO/RTO validation, backup/restore for provider-managed services, failover drills, traffic-shifting mechanics. | `reliability` + `operations` |

### Family G — Runtime / orchestration / packaging

For Kubernetes. Container packaging (Docker) is folded in as a sub-skill of archetype 1, not a separate stack.

| # | Archetype | What the skill produces | Primary upstream |
|---|---|---|---|
| 1 | **workload-packaging-and-manifest** | Container images (Dockerfile, base-image strategy, runtime tuning) **and** Kubernetes workload manifests (Deployment, StatefulSet, Job, CronJob, Service, Ingress, HPA, PDB) with probes, resource requests/limits, and rollout strategy. | `infrastructure-platform` + `backend-architecture` |
| 2 | **network-and-identity-policy** | NetworkPolicy, ServiceAccount and RBAC, ingress/gateway posture, mTLS or service-mesh wiring (where adopted), image-pull secrets, registry auth, Pod Security Standards. | `security` + `infrastructure-platform` |
| 3 | **scaling-and-resilience-topology** | HPA / VPA / KEDA, PDB, pod anti-affinity, topology spread constraints, multi-zone placement, graceful shutdown, rolling-update strategy, surge/unavailable budgets. | `reliability` + `performance` |
| 4 | **observability-and-operations-readiness** | Cluster and pod metrics (kube-state-metrics, cAdvisor), log shipping, distributed tracing wiring, ServiceMonitor/PodMonitor, audit-log posture, runbook inputs. | `operations` + `reliability` |
| 5 | **supply-chain-and-image-hardening** | Minimal base images, non-root, read-only root FS, dropped capabilities, image signing (cosign), SBOM, vulnerability scanning, admission control (Kyverno / Gatekeeper). | `security` + `operations` |

### Family H — Infrastructure-as-code

For Terraform.

| # | Archetype | What the skill produces | Primary upstream |
|---|---|---|---|
| 1 | **module-and-repository-scaffold** | Terraform module layout (root, modules, env-per-workspace or env-per-directory), provider versioning, conventions for inputs/outputs, code-owner and review posture. | `infrastructure-platform` + `operations` |
| 2 | **state-and-secret-management** | Remote state backend (S3 + DynamoDB / GCS / Azure Storage), state encryption, state locking, workspace strategy, secret handling (no plaintext secrets in state, sensitive variables, references to secret managers). | `security` + `infrastructure-platform` |
| 3 | **plan-gate-and-policy-as-code** | Pre-merge gates: `terraform validate`, `terraform plan` diff review, policy-as-code (OPA / Sentinel / Checkov / tfsec), drift detection, required reviewers per blast-radius tier. | `operations` + `security` |
| 4 | **apply-and-promotion-mechanics** | Apply orchestration across env ladder, manual vs auto-apply policy per env, blast-radius gating (targeted apply, refresh-only), rollback procedure, drift remediation playbook. | `infrastructure-platform` + `reliability` |
| 5 | **module-reuse-and-supply-chain** | Versioned module registry, semantic versioning of modules, dependency pinning, provenance for community modules, SBOM-equivalent for the module dependency tree. | `security` + `operations` |

### Family I — CI/CD

For GitHub Actions.

| # | Archetype | What the skill produces | Primary upstream |
|---|---|---|---|
| 1 | **workflow-scaffold-and-runner-topology** | Workflow layout, reusable workflows, composite actions, runner topology (hosted vs self-hosted, runner labels, isolation), repo-vs-org-level workflow organization. | `infrastructure-platform` + `operations` |
| 2 | **identity-and-oidc-federation** | OIDC federation to AWS/GCP/Azure (no long-lived cloud keys), repository and environment secrets, signing keys, environment protection rules, least-privilege `permissions` per job. | `security` + `infrastructure-platform` |
| 3 | **gate-and-environment-policy** | Required status checks per branch, environment approvals, deployment branches, concurrency control, change-window enforcement, manual-approval gates for tier-0. | `operations` + `security` |
| 4 | **release-mechanics-and-promotion** | Build → test → scan → sign → push → deploy orchestration, env-promotion ladder, canary/blue-green/rolling deployment hooks, rollback workflow, release-notes automation. | `infrastructure-platform` + `reliability` |
| 5 | **supply-chain-and-artifact-integrity** | Pinned action SHAs, SBOM generation, dependency scanning (SCA), container/artifact signing (cosign/Sigstore), provenance attestations (SLSA), secret scanning. | `security` + `operations` |

## Stacks

### Implemented

| Stack | Family | Authored skills |
|---|---|---|
| [kubernetes](kubernetes/) | G — Runtime/orchestration | all 5 archetypes authored at **mature tier** (`k8s-workload-packaging-and-manifest`, `k8s-network-and-identity-policy`, `k8s-scaling-and-resilience-topology`, `k8s-observability-and-operations-readiness`, `k8s-supply-chain-and-image-hardening`) + [`k8s-deploy-manifest-review`](kubernetes/k8s-deploy-manifest-review/SKILL.md) *(omnibus, lean)* + [`dockerfile-and-jvm-tuning`](kubernetes/dockerfile-and-jvm-tuning/SKILL.md) *(JVM sub-skill, lean)* |
| [github-actions](github-actions/) | I — CI/CD | [`github-actions-pipeline-hardened`](github-actions/github-actions-pipeline-hardened/SKILL.md) *(omnibus)* |
| [terraform](terraform/) | H — IaC | all 5 archetypes authored (`module-and-repository-scaffold`, `state-and-secret-management`, `plan-gate-and-policy-as-code`, `apply-and-promotion-mechanics`, `module-reuse-and-supply-chain`) |
| [aws](aws/) | F — Cloud platforms | all 5 archetypes authored — `aws-account-and-organization-topology` *(lean)* + archetypes 2–5 at **mature tier** (`aws-network-and-identity-foundation`, `aws-workload-runtime-and-deployment`, `aws-observability-and-cost-readiness`, `aws-dr-and-multi-region-readiness`) |

### Planned (future scope)

| Stack | Family | Status |
|---|---|---|
| [gcp](gcp/) | F — Cloud | 0/5 |
| [azure](azure/) | F — Cloud | 0/5 |
| [kubernetes](kubernetes/) | G — Runtime | 5/5 archetype-scoped authored; non-JVM packaging sub-skills still planned |
| [github-actions](github-actions/) | I — CI/CD | 1 authored, archetype-aligned splits planned |

## Omnibus skills and the split plan

Two existing skills predate the archetype model and span four archetypes each. They are kept as **production-readiness review** entry points — useful when reviewing a workload or pipeline holistically before promotion — and will be supplemented (not replaced immediately) by archetype-scoped successors.

- **[`k8s-deploy-manifest-review`](kubernetes/k8s-deploy-manifest-review/SKILL.md)** — touches archetypes G.1 (Deployment/Service/HPA/PDB), G.2 (NetworkPolicy/ServiceAccount), G.3 (HPA/PDB/rolling-update), and G.5 (security context). The archetype-scoped successors (`k8s-workload-packaging-and-manifest`, `k8s-network-and-identity-policy`, `k8s-scaling-and-resilience-topology`, `k8s-supply-chain-and-image-hardening`) now own the *authoring* of each slice; this skill remains the holistic cross-archetype review pass.
- **[`github-actions-pipeline-hardened`](github-actions/github-actions-pipeline-hardened/SKILL.md)** — touches archetypes I.1 (workflow scaffold), I.2 (OIDC + minimal permissions), I.3 (CI gates), and I.5 (SBOM + cosign + pinned SHAs). Future archetype-scoped GHA skills will own each slice; this skill remains the holistic review pass.

This is a **planned exception** to the one-skill-per-archetype rule, documented so it does not propagate.

## Docker → Kubernetes consolidation

The former `implementations/infrastructure/docker/` stack has been retired. Container packaging is part of Family G (runtime/orchestration) and lives under `implementations/infrastructure/kubernetes/` as a sub-skill of archetype 1 (`workload-packaging-and-manifest`). The existing `dockerfile-and-jvm-tuning` skill has moved accordingly. Future authored skills will cover non-JVM packaging variants (Python, Node, Go, .NET, static binaries) under the same archetype slot.

## Decided design constraints

These constraints are locked for all current and future infrastructure implementation skills:

- **Tool-family archetypes are normative.** A skill that belongs to a family but does not fit any of its five archetypes is a signal that the family taxonomy is wrong — escalate before authoring outside the model.
- **One skill per archetype per stack, omnibus exceptions documented.** The two existing omnibus skills are explicitly enumerated; no new omnibus skills are authored.
- **Per-skill upstream linkage.** Every `SKILL.md` names its upstream architecture domain(s) and conformance standards directly.
- **OIDC over long-lived credentials.** CI and workload-to-cloud authentication uses OIDC federation. Long-lived access keys are an ADR-justified exception.
- **Supply-chain integrity is a first-class concern.** SBOMs, signatures, pinned versions, and provenance are required outputs of the relevant archetypes — never an afterthought.
- **DR is rehearsed, not aspirational.** Family F archetype 5 and equivalent backup-and-restore archetypes in the data layer require documented and exercised failover drills, not paper plans.

## Standards every infrastructure implementation skill conforms to

- [deployment-standards](../../standards/deployment-standards/README.md)
- [security-standards](../../standards/security-standards/README.md)
- [observability-standards](../../standards/observability-standards/README.md)
- [naming-conventions](../../standards/naming-conventions/README.md)
- [architecture-schema](../../standards/architecture-schema/README.md) — tier classification drives DR posture, replica counts, and gate strictness.
