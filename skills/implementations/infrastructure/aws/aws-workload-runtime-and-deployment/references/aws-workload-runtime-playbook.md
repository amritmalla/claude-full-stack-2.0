# AWS Workload Runtime and Deployment Playbook

Load this when designing any owned area of `aws-workload-runtime-and-deployment` or checking the anti-pattern list. It expands the operating rules and process steps in `SKILL.md` with the detail needed to produce a production-grade runtime and deployment design.

## Why this workflow exists

Runtime and deployment defects are expensive to unwind. Choosing EC2/ASG for an event-driven workload pays for idle capacity 24/7; choosing Lambda for a long steady high-throughput service pays a latency and cost penalty forever. A deploy with no automated rollback turns a bad release into a manual 2 a.m. scramble. A single-AZ tier-0 database is one AZ event from a full outage. "Everything on EKS" inherits cluster operational cost for a workload that is one cron job. None of this fails a smoke test — it shows up in the bill and the incident review.

The goal is the right primitive for the workload class, scaled and load-balanced to the SLO, deployed reversibly, within the foundation that already exists — consuming the platform substrate decision instead of inventing it.

## Behavioral rules in depth

### 1. Consume the substrate decision; do not invent it

Runtime Substrate Selection and Deployment & Release Architecture in `infrastructure-platform.md`, plus SLOs and scaling shape in `architecture/reliability`, are the inputs. The primitive is chosen *to satisfy* those, not by preference. If a needed decision is missing, raise an ADR candidate.

### 2. Build within the foundation — do not re-create it

`aws-network-and-identity-foundation` produced the VPC subnets, IAM roles, and CMKs. This skill places compute into them. Authoring a new VPC, role, or key here forks the foundation and breaks the least-privilege and connectivity story that skill validated.

### 3. The primitive follows the workload class

| Class | Primitive | Signal |
|---|---|---|
| Event-driven / ephemeral / spiky | Lambda | Pay-per-invoke; no idle |
| Managed containers, no cluster control needed | Fargate | Containers without node ops |
| Orchestrated containers, cluster control needed | EKS | Mesh/operators/multi-workload |
| Legacy / specialised / licensing-bound | EC2 + ASG | Needs the instance |
| Relational | RDS / Aurora | ACID, SQL |
| Key-value / high-scale | DynamoDB | Predictable single-digit-ms KV |

"Everything on EKS" or "everything on EC2" without a workload-class reason is the canonical defect.

### 4. EKS: provision the cluster, hand off the workloads

When the substrate is EKS, this skill owns the cluster, node groups / Fargate profiles, add-ons, and cluster-level IAM (IRSA). The in-cluster Deployment/Service/HPA/PDB manifests belong to the `kubernetes` Family G skills. This is the mirror of Family G's "cluster provisioning is out of Family G" boundary — name it from this side too.

### 5. Load balancing matches the protocol

ALB for HTTP/HTTPS with host/path routing and TLS termination; NLB for TCP/UDP, ultra-high throughput, or a static IP requirement. The health check gates traffic into the target group and is distinct from a container liveness probe — conflating them removes a pod from service for a transient blip or keeps a dead one in rotation.

### 6. Autoscaling is configured, never defaulted

A target-tracking / step / scheduled policy (or Lambda reserved/provisioned concurrency, or DynamoDB on-demand/autoscaling) with a floor from the reliability tier (never zero for tier-0/1) and a ceiling from the capacity/cost envelope. A fixed single instance for an availability-critical workload is rejected.

### 7. Deployment is safe and reversible

| Tier | Strategy |
|---|---|
| tier-0 | Blue/green (CodeDeploy + ALB) or canary; instant shift-back |
| tier-1 | Canary or rolling with bounded surge |
| tier-2+ | Rolling with bounded surge |

Every deployment declares the automated rollback trigger (alarm, health, error rate) and the procedure. A deploy with no automated rollback path is rejected for tier-0/1 — manual rollback is not a plan.

### 8. Multi-AZ is the tier-0/1 default

Compute and data span AZs. Single-AZ is an ADR-justified exception. Cross-region is a different concern (`aws-dr-and-multi-region-readiness`) — name the handoff, do not design failover here.

### 9. Workload auth uses the foundation role

The task/instance/function assumes the least-privilege role `aws-network-and-identity-foundation` created. No embedded keys, no new IAM users, no inline broad policy "to get it working".

### 10. An unvalidated runtime is unverified

Trigger a deployment and confirm the rollback fires on the defined trigger. Trigger a scale event and confirm the policy reacts within the reliability envelope. A runtime declared done without these is unverified.

## Step detail

**Step 1 — Gather context.** Load `infrastructure-platform.md` (substrate, release) and `architecture/reliability` (SLOs, scaling). Resolve tier from `architecture-schema`, class from the Workload Inventory. Confirm the foundation exists. Raise an ADR candidate for any missing decision.

**Step 2 — Select the primitive.** Map class + substrate → primitive; justify, list rejected alternatives. For EKS, scope to cluster/node groups; name the in-cluster handoff.

**Step 3 — Place into the foundation.** Correct subnet tier, foundation IAM role, foundation CMK. No new VPC/role/key.

**Step 4 — Load balancing.** ALB vs NLB by protocol; traffic-gating health checks distinct from liveness.

**Step 5 — Autoscaling.** Policy per primitive; floor from reliability tier; ceiling from capacity/cost.

**Step 6 — Deployment mechanics.** Blue/green or canary for tier-0; rolling bounded otherwise; automated rollback trigger + procedure.

**Step 7 — Multi-AZ posture.** Multi-AZ for tier-0/1; single-AZ ADR-justified; name the cross-region DR handoff.

**Step 8 — Validate.** Triggered rollback + scale event. Document any check that cannot run.

**Step 9 — Emit & validate.** `workload-runtime-deployment.md` (selection + rationale, LB, autoscaling, deploy/rollback, multi-AZ), gap list with ADR candidates, handoff list. Validate against deployment-, security-, observability-standards, naming-conventions, architecture-schema.

## Anti-patterns to detect

Call these out explicitly when found:

- Primitive not matched to the workload class ("all on EKS/EC2/Lambda" with no reason)
- New VPC/IAM role/KMS key authored here instead of using the foundation
- EKS in-cluster Deployment/Service/HPA manifests authored here (belongs to Family G)
- ALB used for a raw TCP/UDP workload, or NLB where host/path routing is needed
- Health check conflated with the liveness probe
- No autoscaling policy, or a fixed single instance for a tier-0/1 workload
- Deploy with no automated rollback trigger for tier-0/1; manual-only rollback
- Single-AZ tier-0/1 compute or data without an ADR
- Embedded credentials / new IAM user instead of the foundation role
- Cross-region failover designed here instead of handed to the DR skill
- Runtime declared done with no triggered-rollback or scale-event validation
- Terraform module/state mechanics authored here (belongs to Family H)
