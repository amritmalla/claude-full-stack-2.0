# AWS Network and Identity Foundation Playbook

Load this when designing any owned area of `aws-network-and-identity-foundation` or checking the anti-pattern list. It expands the operating rules and process steps in `SKILL.md` with the detail needed to produce a production-grade in-account network and identity foundation.

## Why this workflow exists

Network and identity defects in AWS are the breaches that make the news. A flat VPC with the database in a public subnet is one security-group mistake from internet exposure. A role with `Action: "*"` and no permission boundary turns one leaked task credential into account takeover. Long-lived IAM access keys committed to a repo are the single most common AWS incident root cause. Blanket VPC peering "to ship faster" gives a compromised dev workload a route to prod data. None of this fails a functional test — the app connects fine.

The goal is a tiered, least-route, federated, bounded, customer-encrypted foundation where every route and every grant is justified — consuming the security architecture instead of inventing it.

## Behavioral rules in depth

### 1. Consume security and platform; do not invent it

Trust zones, the IAM model, and encryption posture come from `architecture/security`; network shape and connectivity intent from `infrastructure-platform.md`. The CIDR plan and the rotation cadence implement decisions; they are not chosen here. If a needed decision is missing, raise an ADR candidate.

### 2. Stay in-account — org topology is upstream

`aws-account-and-organization-topology` created the accounts, OUs, and SCPs. This skill builds *inside* them: VPCs, IAM roles, KMS keys, secrets, DNS. Creating an account or writing an SCP here splits ownership of the org boundary across two skills.

### 3. The VPC is tiered, never flat

| Tier | Reachability |
|---|---|
| Public | Load balancers / NAT only — never application or data |
| Private-app | Application compute; egress via NAT; no inbound from internet |
| Private-data | Databases/stateful; reachable only from private-app; no internet route |

Across at least the multi-AZ count the reliability tier requires. A data resource in a public subnet is a finding, not a shortcut.

### 4. Connectivity is explicit and least-route

Inter-account/inter-VPC reachability is Transit Gateway (hub) or peering with **scoped route tables** — only the routes the trust zones justify. PrivateLink exposes a single service without opening the network. Blanket peering with a default route is rejected: it is lateral movement waiting to happen.

### 5. Humans federate; nobody gets a long-lived key

IAM Identity Center federated to the IdP, permission sets mapped to the account/OU layout, session-duration bounded. No IAM users for humans. No long-lived access keys anywhere — workloads use instance/IRSA/task roles. A long-lived key is an ADR-justified exception with a rotation and scoping story.

### 6. Every role is least-privilege under a permission boundary

The policy grants exactly the operational need; the permission boundary caps the maximum so an over-broad policy (or a future edit) still cannot escalate. Wildcard `Action`/`Resource` is an ADR-justified exception, not the starting point. This is the in-account complement to the org SCPs (which are guardrails, not IAM).

### 7. Encryption is customer-managed where the posture requires it

KMS CMKs per-env, and per-tenant where the tenancy model requires, with key policies scoped to the using roles (not `kms:*` to the account root). In-transit (TLS) and at-rest encryption are defaults. AWS-managed keys only where `architecture/security` explicitly permits.

### 8. Secrets live in Secrets Manager, rotated

No secrets in launch-template/task-def env vars, SSM SecureString-treated-as-plaintext, or AMIs. Secrets Manager with rotation at the security-defined cadence; the consuming role gets `secretsmanager:GetSecretValue` on exactly that secret, nothing broader.

### 9. DNS is a designed zone strategy

Route 53 private hosted zones per env, split-horizon where public and private names diverge, delegation aligned to the account/env boundary. Ad-hoc records in a single shared zone is not a strategy.

### 10. An unvalidated foundation is unverified

Produce a reachability matrix and confirm it matches the trust zones (a path that should not exist must not resolve). Run IAM Access Analyzer / a policy review and confirm no unintended external access and no excess privilege. Untested network/identity is unverified.

## Step detail

**Step 1 — Gather context.** Load `architecture/security` (trust zones, IAM model, encryption) and `infrastructure-platform.md` (network shape, connectivity). Resolve tier from `architecture-schema`. Confirm the account/OU layout. Raise an ADR candidate for any missing decision.

**Step 2 — VPC topology.** Per-env VPCs; public / private-app / private-data tiers across the reliability AZ count; CIDR/IPAM; NAT/egress posture.

**Step 3 — Connectivity.** TGW/peering with scoped route tables; PrivateLink for service-to-service; DX/VPN if on-prem.

**Step 4 — Human identity.** IAM Identity Center federation; permission sets per role/account; no IAM users for humans.

**Step 5 — Workload identity.** IAM roles (instance/IRSA/task), least-privilege, each under a permission boundary.

**Step 6 — KMS.** Per-env (per-tenant where required) CMKs; key policies scoped to using roles; encryption defaults.

**Step 7 — Secrets.** Secrets Manager hierarchy; rotation at the security cadence; least-privilege consumption.

**Step 8 — DNS.** Route 53 private zones per env; split-horizon where required; delegation per the account/env boundary.

**Step 9 — Validate.** Reachability matrix vs trust zones; IAM access review (Access Analyzer). Document any check that cannot run.

**Step 10 — Emit & validate.** `network-identity-foundation.md` (VPC/subnet plan, connectivity matrix, role/boundary map, CMK strategy, secret/rotation policy, DNS strategy), gap list with ADR candidates, handoff list. Validate against security-, deployment-, observability-standards, naming-conventions, architecture-schema.

## Anti-patterns to detect

Call these out explicitly when found:

- Account/OU/SCP design done here (belongs to `aws-account-and-organization-topology`)
- Flat VPC, or a data resource in a public subnet
- Fewer AZs than the reliability tier requires
- Blanket VPC peering / default-route reachability instead of scoped routes
- IAM users for humans; any long-lived access key without an ADR
- Role with wildcard `Action`/`Resource` or no permission boundary
- `kms:*` key policy to the account root instead of scoped to using roles
- AWS-managed keys where the security posture requires customer-managed
- Secrets in env vars / launch templates / AMIs / plaintext SSM
- Ad-hoc Route 53 records instead of a per-env zone strategy
- Foundation declared done with no reachability matrix or IAM access review
- Terraform module/state mechanics authored here (belongs to Family H)
