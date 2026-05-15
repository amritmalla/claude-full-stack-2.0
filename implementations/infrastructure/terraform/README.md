# terraform

> Status: scaffold.

## Purpose

Implements `architecture/infrastructure-platform`, `architecture/security`, `architecture/reliability`, and `architecture/operations` as Terraform code: module and repository structure, state and secret management, plan-gate and policy-as-code, apply and promotion mechanics, module reuse and supply chain.

Architecture decisions (env ladder, blast-radius tiers, module boundaries, secrets handling, promotion gates) come from upstream and are taken as inputs here.

## Tool family

Terraform is the sole member of **Family H — Infrastructure-as-code** in the infrastructure layer model. See [`implementations/infrastructure/README.md`](../README.md) for the full archetype set and philosophy.

## Ecosystem (target)

- Terraform 1.7+ or OpenTofu equivalent
- Remote state backend: S3 + DynamoDB lock / GCS / Azure Storage
- Workspace strategy: env-per-directory (default) or env-per-workspace where justified
- Policy-as-code: OPA / Conftest / Checkov / tfsec / Terraform Cloud Sentinel
- Module registry: Terraform Registry, internal Git module sources, or Terraform Cloud private registry
- Drift detection: `terraform plan -refresh-only` on a schedule

## Skills

### Authored

_None._

### Archetype coverage

| # | Archetype | Skill | Status |
|---|---|---|---|
| 1 | module-and-repository-scaffold | `terraform-module-and-repository-scaffold` | planned |
| 2 | state-and-secret-management | `terraform-state-and-secret-management` | planned |
| 3 | plan-gate-and-policy-as-code | `terraform-plan-gate-and-policy-as-code` | planned |
| 4 | apply-and-promotion-mechanics | `terraform-apply-and-promotion-mechanics` | planned |
| 5 | module-reuse-and-supply-chain | `terraform-module-reuse-and-supply-chain` | planned |

### Planned skill scope (future work)

- **`terraform-module-and-repository-scaffold`** — repo layout (root + `modules/` + `environments/<env>/`), provider version constraints, `required_version` discipline, input/output conventions, `README.md` per module, `examples/` directory for module consumers, code-owner and review rules tied to env and blast-radius tier.
- **`terraform-state-and-secret-management`** — remote state backend selection (S3 + DynamoDB / GCS / Azure Storage / Terraform Cloud), state encryption at rest, state locking, workspace strategy (env-per-directory vs `terraform workspace`), `sensitive = true` on outputs containing secrets, secret references to AWS Secrets Manager / GCP Secret Manager / Azure Key Vault rather than plaintext, no secrets in `.tfvars` committed to source.
- **`terraform-plan-gate-and-policy-as-code`** — pre-merge gates (`terraform fmt`, `terraform validate`, `terraform plan` diff posted to PR), policy-as-code (OPA/Conftest / Checkov / tfsec / Sentinel) with blast-radius-tiered policy strictness, drift detection on a schedule, required-reviewer rules per env, prohibited resources or providers per env.
- **`terraform-apply-and-promotion-mechanics`** — apply orchestration across env ladder (dev → staging → prod), manual approval gates for prod, targeted apply discipline for blast-radius control, `terraform refresh` and drift remediation playbook, rollback procedure (revert + apply, or restore prior state version), runbook inputs for partial-apply failures and lock-recovery.
- **`terraform-module-reuse-and-supply-chain`** — versioned module registry (private Terraform Cloud registry or Git tags), semantic versioning of modules (`MAJOR.MINOR.PATCH`), dependency pinning of providers and modules in consumers, provenance review for community modules, SBOM-equivalent for the module dependency tree, deprecation policy for breaking-change releases.

## Architecture domains implemented

| Architecture domain | How |
|---|---|
| [infrastructure-platform](../../../architecture/infrastructure-platform/README.md) | Module boundaries, env ladder, deployment mechanics. |
| [security](../../../architecture/security/README.md) | State secret discipline, policy-as-code, no plaintext credentials. |
| [reliability](../../../architecture/reliability/README.md) | Drift detection, rollback procedure, lock management. |
| [operations](../../../architecture/operations/README.md) | Promotion gates, runbook inputs for apply failures. |

## Standards this implementation conforms to

- [deployment-standards](../../../standards/deployment-standards/README.md) — env ladder, promotion gates, rollback artifacts.
- [security-standards](../../../standards/security-standards/README.md) — secret handling, policy-as-code, least-privilege provider credentials via OIDC.
- [naming-conventions](../../../standards/naming-conventions/README.md) — resource and module names follow project conventions.
- [architecture-schema](../../../standards/architecture-schema/README.md) — tier classification drives policy strictness and promotion-gate count.

## Upstream inputs

- Approved `infrastructure-platform.md` declaring env ladder, module boundaries, blast-radius tiers, and target cloud(s).
- Approved `architecture/security` decisions on state secret handling, provider authentication, and policy-as-code requirements.
- Approved `architecture/operations` decisions on promotion gates and rollback expectations.
