# AWS Workload Runtime and Deployment Quality Rubric

Load this before declaring the runtime complete. Revise until each check passes or the unresolved gap is explicitly documented in `workload-runtime-deployment.md`.

## Context & boundary

- [ ] Runtime substrate and release strategy are sourced from `infrastructure-platform.md`; SLOs/scaling shape from `architecture/reliability` (or an ADR candidate is raised).
- [ ] The workload tier (architecture-schema) and class (Workload Inventory) are resolved and drive the design.
- [ ] Compute is placed into the existing `aws-network-and-identity-foundation` subnets/roles/CMKs — no new VPC, IAM role, or KMS key.

## Compute primitive

- [ ] The primitive matches the workload class with a stated rationale and rejected alternatives.
- [ ] No "everything on X" choice without a workload-class reason.
- [ ] For EKS: the skill stops at cluster + node-group/Fargate-profile provisioning; in-cluster manifests are a named `kubernetes` Family G handoff.

## Load balancing & autoscaling

- [ ] Load balancing matches the protocol (ALB for HTTP/HTTPS host/path; NLB for TCP/UDP/throughput/static IP).
- [ ] Health checks gate traffic into the target group and are distinct from the liveness probe.
- [ ] An autoscaling policy exists appropriate to the primitive.
- [ ] The scaling floor comes from the reliability tier (non-zero for tier-0/1); the ceiling from the capacity/cost envelope.

## Deployment & availability

- [ ] Deployment is blue/green or canary for tier-0; canary or rolling-with-bounded-surge for tier-1; rolling otherwise.
- [ ] An automated rollback trigger (alarm/health/error-rate) and procedure are declared.
- [ ] No tier-0/1 deployment relies on manual-only rollback.
- [ ] Multi-AZ is the posture for tier-0/1 compute and data; single-AZ is ADR-justified.
- [ ] Cross-region failover is named as an `aws-dr-and-multi-region-readiness` handoff, not designed here.

## Identity & validation

- [ ] The workload assumes the foundation's least-privilege role; no embedded credentials, no new IAM user.
- [ ] A triggered deployment confirmed the rollback path fires on its defined trigger, or the gap is documented.
- [ ] A triggered scale event confirmed the policy reacts within the reliability envelope, or the gap is documented.

## Standards conformance & handoffs

- [ ] [deployment-standards](../../../../../standards/deployment-standards/README.md): tier-correct strategy; automated rollback declared; env-agnostic, IaC-ready.
- [ ] [security-standards](../../../../../standards/security-standards/README.md): foundation least-privilege role; no embedded credentials; foundation-CMK encryption.
- [ ] [observability-standards](../../../../../standards/observability-standards/README.md): health-check and deployment-event signal seam present (dashboards/alarms deferred).
- [ ] [naming-conventions](../../../../../standards/naming-conventions/README.md): service, target-group, ASG, deployment-group naming.
- [ ] [architecture-schema](../../../../../standards/architecture-schema/README.md): tier drove deployment strategy, autoscaling floor, multi-AZ requirement.
- [ ] Org topology, network/identity, observability/cost, DR, in-cluster manifests, and Terraform mechanics are named handoffs — none implemented here.

## Failure handling

If a check fails:

1. Identify the mismatched primitive, missing rollback, or under-scaled policy.
2. Ask the user for clarification if the decision cannot be inferred from `infrastructure-platform.md` or `architecture/reliability`.
3. Revise the design, re-run the triggered-rollback and scale-event validations.
4. Keep any unresolved gap explicit in `workload-runtime-deployment.md` — do not hide it as an assumption.
