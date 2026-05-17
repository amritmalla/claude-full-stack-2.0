---
name: aws-workload-runtime-and-deployment
description: Use when selecting the AWS compute primitive for a workload and designing its load balancing, autoscaling, and deployment mechanics after the network/identity foundation exists and infrastructure-platform and reliability have decided the runtime substrate and SLOs. Produces the compute-primitive selection per workload class (Lambda / Fargate / EKS / EC2-ASG / RDS-Aurora / DynamoDB), ALB/NLB posture, autoscaling configuration, and deployment mechanics (CodeDeploy, blue/green for ALB, rolling for ECS) with rollback. Do not use for org/account topology, VPC/IAM/KMS foundation, observability/cost wiring, DR/multi-region, in-cluster Kubernetes manifests, or Terraform module/state mechanics; use the other aws (or Family G / Family H) skills.
---

# AWS Workload Runtime and Deployment

## When to use

Invoke when choosing how a workload runs on AWS, designing its load balancing and autoscaling, or defining its deployment and rollback mechanics — within the network/identity foundation an environment already has.

Do not use for: AWS Organizations/account/SCP topology (use `aws-account-and-organization-topology`); VPC/IAM/KMS/Secrets foundation (use `aws-network-and-identity-foundation`); CloudWatch/cost instrumentation (use `aws-observability-and-cost-readiness`); multi-region/DR (use `aws-dr-and-multi-region-readiness`); in-cluster Kubernetes workload manifests when EKS is the substrate (the `kubernetes` Family G skills own those — this skill provisions the cluster substrate, not its workloads); IaC module/state/plan/apply mechanics (the `terraform` Family H skills).

## Inputs

Required:

- A network/identity foundation from `aws-network-and-identity-foundation` (the VPC subnets, IAM roles, and CMKs the workload runs within).
- Approved `infrastructure-platform.md` Runtime Substrate Selection and Deployment & Release Architecture, or explicit confirmation they are intentionally deferred.

Optional:

- Approved `architecture/reliability` SLOs, scaling shape, and availability targets per workload tier.
- The workload tier from `architecture-schema` (drives deployment strategy and autoscaling floor).
- Workload class per the platform Workload Inventory (API / job / scheduled / queue / streaming / database).
- Traffic profile (steady / spiky / event-driven) and latency budget.
- Stateful requirements (relational, KV, ordered) driving the data-plane primitive.

## Operating rules

- Never generate tutorial-grade runtime. Assume real traffic shape, a deploy that must roll back cleanly, and a workload that must scale and survive an AZ loss.
- Consume `infrastructure-platform.md` and `architecture/reliability`; do not invent decisions. Runtime substrate, release strategy, SLOs, and scaling shape are architectural decisions. If a needed decision is missing, pause and raise an ADR candidate rather than guessing.
- Build within the foundation; do not re-create it. The VPC subnets, IAM roles, and CMKs come from `aws-network-and-identity-foundation`. This skill places compute into them; it does not author VPCs, roles, or keys.
- The compute primitive follows the workload class, not habit. Event-driven/ephemeral → Lambda; managed containers → Fargate; orchestrated containers needing cluster control → EKS; legacy/specialised → EC2/ASG; relational → RDS/Aurora; KV → DynamoDB. Justify the choice against the class and the platform substrate decision; "everything on EKS" or "everything on EC2" is rejected absent a reason.
- When EKS is the substrate, this skill stops at the cluster boundary. It provisions the cluster, node groups/Fargate profiles, and the cluster-level wiring; the in-cluster Deployment/Service/HPA manifests are the `kubernetes` Family G skills' ownership. Name the handoff.
- Load balancing matches the protocol. ALB for HTTP/HTTPS with path/host routing; NLB for TCP/UDP or extreme throughput/static IP. Health checks gate traffic and are distinct from liveness.
- Autoscaling is configured, not defaulted. A scaling policy (target-tracking / step / scheduled, or Lambda concurrency, or DynamoDB on-demand/auto) with a floor from the reliability tier and a ceiling from the capacity/cost envelope. A single fixed instance for a tier-0/1 workload is rejected.
- Deployment is safe and reversible. Blue/green (CodeDeploy + ALB) or canary for tier-0; rolling for ECS/EKS with surge bounded; every deployment declares its rollback trigger and procedure. A deploy with no automated rollback path is rejected for tier-0/1.
- Multi-AZ is the default for tier-0/1 compute and data. Single-AZ is an ADR-justified exception; cross-region is `aws-dr-and-multi-region-readiness`, named here, not designed here.
- Workload-to-AWS auth uses the roles from the foundation. No embedded credentials, no new IAM users; the task/instance/function role from `aws-network-and-identity-foundation` is assumed.
- This skill owns runtime selection + LB + autoscaling + deploy mechanics. Org topology, network/identity, observability/cost, DR, in-cluster manifests, and IaC mechanics are named handoffs.
- A runtime whose deployment rollback and autoscaling have not been validated (a triggered rollback, a scale event) is not done.

## Output contract

The workload runtime and deployment MUST conform to:

- [deployment-standards](../../../../../standards/deployment-standards/README.md) — blue/green or canary for tier-0, rolling with bounded surge otherwise; automated rollback trigger and procedure declared; env-agnostic, IaC-ready.
- [security-standards](../../../../../standards/security-standards/README.md) — workload assumes the foundation's least-privilege role; no embedded credentials; encryption via the foundation's CMKs.
- [observability-standards](../../../../../standards/observability-standards/README.md) — health checks and deployment events emit a signal seam (full dashboards/alarms deferred to `aws-observability-and-cost-readiness`).
- [naming-conventions](../../../../../standards/naming-conventions/README.md) — service, target-group, ASG, and deployment-group naming.
- [architecture-schema](../../../../../standards/architecture-schema/README.md) — tier classification drives deployment strategy, autoscaling floor, and multi-AZ requirement.

Upstream contract: `infrastructure-platform.md` is the source of truth for runtime substrate and release strategy; `architecture/reliability` is the source of truth for SLOs and scaling shape. If a needed decision is missing, pause and raise an ADR candidate. Org topology, network/identity, observability/cost, DR, in-cluster manifests, and IaC mechanics are named handoffs.

## Progressive references

- Read `references/aws-workload-runtime-playbook.md` when designing any owned area or checking the anti-pattern list.
- Read `references/aws-workload-runtime-quality-rubric.md` before declaring the runtime complete.
- Use `assets/aws-workload-runtime.template.md` as the compute/LB/autoscaling/deploy pattern reference.

## Process

1. Gather context: load `infrastructure-platform.md` (Runtime Substrate Selection, Deployment & Release Architecture) and `architecture/reliability` (SLOs, scaling shape). Resolve the workload tier from `architecture-schema` and the workload class from the platform Workload Inventory. Confirm the network/identity foundation exists. If a needed decision is missing, raise an ADR candidate before proceeding.
2. Select the compute primitive from the workload class and substrate decision; justify it and the rejected alternatives. For EKS, scope to cluster + node groups/Fargate profiles and name the in-cluster handoff.
3. Place compute into the foundation: the correct subnet tier, the foundation IAM role, the foundation CMK for encryption — no new VPC/role/key.
4. Design load balancing: ALB (HTTP/HTTPS, path/host) or NLB (TCP/UDP, throughput/static IP); health checks that gate traffic, distinct from liveness.
5. Configure autoscaling: the policy type appropriate to the primitive, floor from the reliability tier, ceiling from the capacity/cost envelope.
6. Design deployment mechanics: blue/green (CodeDeploy + ALB) or canary for tier-0, rolling with bounded surge otherwise; define the automated rollback trigger and procedure.
7. Set the multi-AZ posture: multi-AZ for tier-0/1 compute and data; single-AZ only with an ADR; name the cross-region handoff to DR.
8. Validate: trigger a deployment and confirm the rollback path fires correctly; trigger a scale event and confirm the policy reacts within the reliability envelope; document any check that cannot run.
9. Produce `workload-runtime-deployment.md` (primitive selection + rationale, LB design, autoscaling policy, deployment/rollback mechanics, multi-AZ posture) plus the gap list with ADR candidates and the named handoff list. Validate against deployment-, security-, observability-standards, naming-conventions, and architecture-schema. Revise until all pass or the gap is documented.

## Outputs

Required:

- Compute-primitive selection per workload with rationale and rejected alternatives.
- Compute placed into the foundation's subnets/roles/CMKs (no new VPC/role/key).
- Load-balancing design (ALB/NLB) with traffic-gating health checks.
- Autoscaling policy with reliability-tier floor and capacity/cost ceiling.
- Deployment mechanics (blue/green/canary/rolling) with an automated rollback trigger and procedure.
- Multi-AZ posture; cross-region named as a DR handoff.
- `workload-runtime-deployment.md`, the gap list with ADR candidates, and the named handoff list.

Output rules:

- IaC-ready definitions, not prose-only; not the Terraform module/state mechanics.
- The primitive matches the workload class; "all on X" without a reason is rejected.
- Tier-0/1 has automated rollback and multi-AZ; exceptions are ADR-justified.
- For EKS, in-cluster manifests are a named Family G handoff, not authored here.

## Quality checks

- [ ] Runtime substrate and release strategy are sourced from `infrastructure-platform.md`; SLOs/scaling from `architecture/reliability` (or an ADR candidate is raised).
- [ ] The compute primitive matches the workload class with a stated rationale and rejected alternatives.
- [ ] Compute runs in the foundation's subnet tier with the foundation IAM role and CMK — no new VPC/role/key.
- [ ] For EKS, the skill stops at cluster/node-group provisioning; in-cluster manifests are a named `kubernetes` Family G handoff.
- [ ] Load balancing matches the protocol (ALB vs NLB); health checks gate traffic and are distinct from liveness.
- [ ] An autoscaling policy exists with a reliability-tier floor and a capacity/cost ceiling; no fixed single instance for tier-0/1.
- [ ] Deployment is blue/green or canary for tier-0 (rolling with bounded surge otherwise) with an automated rollback trigger and procedure.
- [ ] Multi-AZ is the posture for tier-0/1 compute and data; single-AZ is ADR-justified; cross-region is a named DR handoff.
- [ ] A triggered rollback and a scale event were validated, or the gap is documented.
- [ ] Org topology, network/identity, observability/cost, DR, in-cluster manifests, and IaC mechanics are named handoffs.

## References

- Upstream: [`architecture/infrastructure-platform`](../../../../architecture/infrastructure-platform/SKILL.md), [`architecture/reliability`](../../../../architecture/reliability/SKILL.md).
- Builds on: [`aws-network-and-identity-foundation`](../aws-network-and-identity-foundation/SKILL.md) (subnets, roles, CMKs the workload runs within).
- Related aws archetype skills: [`aws-account-and-organization-topology`](../aws-account-and-organization-topology/SKILL.md), [`aws-observability-and-cost-readiness`](../aws-observability-and-cost-readiness/SKILL.md), [`aws-dr-and-multi-region-readiness`](../aws-dr-and-multi-region-readiness/SKILL.md).
- In-cluster handoff (EKS): the `kubernetes` Family G skills own Deployment/Service/HPA/PDB manifests.
- IaC mechanics handoff: the `terraform` Family H skills own module/state/plan/apply.
- Standards: [`deployment-standards`](../../../../../standards/deployment-standards/README.md), [`security-standards`](../../../../../standards/security-standards/README.md), [`observability-standards`](../../../../../standards/observability-standards/README.md), [`naming-conventions`](../../../../../standards/naming-conventions/README.md), [`architecture-schema`](../../../../../standards/architecture-schema/README.md).
