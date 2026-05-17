# AWS Network and Identity Foundation — Layout Reference

Use this as the canonical VPC / IAM / KMS / Secrets / Route 53 pattern reference. These are **IaC-ready definitions** — the `terraform` Family H skills own module/state/plan/apply. Placeholder tokens use `<kebab-case>`. Values are illustrative — replace with the trust zones, CIDR plan, and tier from upstream.

## Definition set layout

```
network-identity-foundation.md     # VPC/subnet plan + connectivity matrix + role/boundary
                                    #   map + CMK strategy + secret/rotation + DNS strategy
definitions/
├── vpc.tf.json | vpc.yaml         # per-env tiered VPC (IaC-ready; not the module)
├── connectivity.<fmt>            # TGW/peering scoped routes + PrivateLink
├── iam-roles.<fmt>               # roles + permission boundaries (least-privilege)
├── kms.<fmt>                     # per-env/per-tenant CMKs + scoped key policies
├── secrets.<fmt>                 # Secrets Manager hierarchy + rotation
└── route53.<fmt>                 # per-env private hosted zones
```

## Tiered VPC — never flat, never public data

```
VPC <env> (10.<env>.0.0/16)         # per-env; CIDR/IPAM from upstream
├── public      AZ-a/b/c            # ALB / NAT ONLY — no app, no data
├── private-app AZ-a/b/c            # compute; egress via NAT; no inbound internet
└── private-data AZ-a/b/c           # DB/stateful; reachable only from private-app;
                                    #   NO internet route
# AZ count >= the reliability tier's multi-AZ requirement.
```

## Connectivity — scoped routes, not blanket peering

```hcl
# Transit Gateway hub with SCOPED route tables (only justified routes).
# PrivateLink for service-to-service without opening the network:
resource "aws_vpc_endpoint" "<service>" {
  vpc_id            = <consumer-vpc>
  service_name      = "<provider-endpoint-service>"
  vpc_endpoint_type = "Interface"
  # one service exposed — not a network-wide peering
}
# WRONG: aws_vpc_peering_connection with a 0.0.0.0/0 route "to keep it simple"
```

## Least-privilege role UNDER a permission boundary

```json
{
  "RoleName": "<service>-task-role",
  "PermissionsBoundary": "arn:aws:iam::<acct>:policy/<env>-boundary",
  "Policy": {
    "Effect": "Allow",
    "Action": ["s3:GetObject"],
    "Resource": "arn:aws:s3:::<bucket>/<prefix>/*"
  }
}
// Boundary caps the max even if the policy is later widened.
// Wildcard Action/Resource => ADR-justified exception only.
```

## Human access — federated, no IAM users

```
IAM Identity Center  ──federate──>  <IdP: Okta/Entra/Google>
  permission set: <Role>  ->  account(s) <env>   (session duration bounded)
# No IAM users for humans. No long-lived access keys anywhere.
```

## KMS CMK — scoped key policy, not kms:* to root

```json
{
  "Sid": "UseByWorkloadRoleOnly",
  "Effect": "Allow",
  "Principal": { "AWS": "arn:aws:iam::<acct>:role/<service>-task-role" },
  "Action": ["kms:Decrypt", "kms:GenerateDataKey"],
  "Resource": "*"
}
// Per-env (per-tenant where required). NOT kms:* to the account root.
```

## Secrets Manager — rotated, least-privilege consumption

```hcl
resource "aws_secretsmanager_secret_rotation" "<name>" {
  rotation_rules { automatically_after_days = <security-defined-cadence> }
}
# Consuming role gets secretsmanager:GetSecretValue on THIS secret only.
# No secrets in launch templates / task defs / AMIs / plaintext SSM.
```

## Handoffs this skill names (does not implement)

| Concern | Owner |
|---|---|
| AWS Organizations / OU / SCP / account vending | `aws-account-and-organization-topology` |
| Compute primitive selection, ALB/NLB, autoscaling, deploy mechanics | `aws-workload-runtime-and-deployment` |
| CloudWatch/ADOT/X-Ray, dashboards, Cost Explorer/Budgets, FinOps tags | `aws-observability-and-cost-readiness` |
| Multi-region, cross-region replicas, failover drills | `aws-dr-and-multi-region-readiness` |
| IaC module structure, state, plan gate, apply/promotion | `terraform` Family H skills |
