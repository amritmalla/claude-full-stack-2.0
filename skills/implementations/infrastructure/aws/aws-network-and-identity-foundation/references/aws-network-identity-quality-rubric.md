# AWS Network and Identity Foundation Quality Rubric

Load this before declaring the foundation complete. Revise until each check passes or the unresolved gap is explicitly documented in `network-identity-foundation.md`.

## Context & boundary

- [ ] Trust zones, IAM model, and encryption posture are sourced from `architecture/security`; network shape from `infrastructure-platform.md` (or an ADR candidate is raised).
- [ ] The workload tier from `architecture-schema` informed subnet isolation, CMK granularity, and rotation cadence.
- [ ] No org/account/OU/SCP design is done here — the foundation is built inside the existing account layout.

## VPC & connectivity

- [ ] VPCs are per-env and tiered: public / private-app / private-data.
- [ ] Subnets span at least the multi-AZ count the reliability tier requires.
- [ ] No data resource is in a public subnet; no flat single-subnet VPC.
- [ ] Inter-account/inter-VPC connectivity uses TGW/peering with scoped route tables — no blanket peering or default-route reachability.
- [ ] PrivateLink is used for service-to-service exposure where it avoids opening the network.

## Identity

- [ ] Human access is IAM Identity Center federated to the IdP with permission sets; no IAM users for humans.
- [ ] No long-lived access keys exist for humans or workloads (or each is an ADR-justified exception with rotation/scoping).
- [ ] Workload identity uses IAM roles (instance/IRSA/task).
- [ ] Every role is least-privilege and under a permission boundary; wildcard `Action`/`Resource` is ADR-justified.

## Encryption & secrets

- [ ] KMS CMKs are per-env (per-tenant where the tenancy model requires).
- [ ] Key policies are scoped to the using roles, not `kms:*` to the account root.
- [ ] Encryption in transit and at rest is the default.
- [ ] Secrets are in Secrets Manager with rotation at the security-defined cadence.
- [ ] No secrets in launch-template/task-def env vars, AMIs, or plaintext SSM; consumption is least-privilege.

## DNS & validation

- [ ] Route 53 is a designed per-env zone strategy aligned to the account/env boundary (split-horizon where required).
- [ ] A reachability matrix is produced and matches the trust zones, or the gap is documented.
- [ ] An IAM access review (Access Analyzer or equivalent) shows no unintended external access and no excess privilege, or the gap is documented.

## Standards conformance & handoffs

- [ ] [security-standards](../../../../../../standards/security-standards/README.md): least-privilege bounded IAM, no IAM users/long-lived keys, customer-managed encryption where required, private connectivity, rotated secrets.
- [ ] [deployment-standards](../../../../../../standards/deployment-standards/README.md): foundation reproducible via IaC-ready definitions; no click-ops-only.
- [ ] [observability-standards](../../../../../../standards/observability-standards/README.md): VPC Flow Logs and CloudTrail data-event seam present (full wiring deferred).
- [ ] [naming-conventions](../../../../../../standards/naming-conventions/README.md): VPC, subnet, role, CMK alias, hosted-zone naming.
- [ ] [architecture-schema](../../../../../../standards/architecture-schema/README.md): tier classification drove isolation, CMK granularity, rotation cadence.
- [ ] Org topology, workload runtime, observability/cost, DR, and Terraform module/state mechanics are named handoffs — none implemented here.

## Failure handling

If a check fails:

1. Identify the over-broad route, grant, or unencrypted/plaintext element.
2. Ask the user for clarification if the decision cannot be inferred from `architecture/security` or `infrastructure-platform.md`.
3. Revise the definition, re-run the reachability matrix and IAM access review.
4. Keep any unresolved gap explicit in `network-identity-foundation.md` — do not hide it as an assumption.
