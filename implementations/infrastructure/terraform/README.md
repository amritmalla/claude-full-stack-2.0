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

- [terraform-module-and-repository-scaffold](terraform-module-and-repository-scaffold/SKILL.md) — repo layout (root + `modules/` + `environments/<env>/`), provider and `required_version` pinning, typed input/output conventions, per-module `README` + `examples/`, and blast-radius-tiered CODEOWNERS/review rules.
- [terraform-state-and-secret-management](terraform-state-and-secret-management/SKILL.md) — remote backend selection (S3+DynamoDB / GCS / Azure / TFC), state encryption at rest, locking, per-environment state isolation, secret-manager references, `sensitive` discipline, and backend-migration procedure.
- [terraform-plan-gate-and-policy-as-code](terraform-plan-gate-and-policy-as-code/SKILL.md) — blocking pre-merge gate (`fmt`/`validate`/`plan` diff to PR), policy-as-code (OPA/Conftest, Checkov, tfsec, Sentinel) with tier-scaled strictness, secret scan, and scheduled drift detection.
- [terraform-apply-and-promotion-mechanics](terraform-apply-and-promotion-mechanics/SKILL.md) — apply orchestration across the env ladder, manual-vs-auto-apply per tier, reviewed-plan apply, blast-radius control, rollback procedure, drift-remediation playbook, and apply-failure/lock-recovery runbook inputs.
- [terraform-module-reuse-and-supply-chain](terraform-module-reuse-and-supply-chain/SKILL.md) — versioned module registry strategy, semantic versioning, consumer pinning + committed lockfile, provenance review for community modules/providers, SBOM-equivalent of the dependency tree, and breaking-change deprecation policy.

### Archetype coverage

| # | Archetype | Skill | Status |
|---|---|---|---|
| 1 | module-and-repository-scaffold | [`terraform-module-and-repository-scaffold`](terraform-module-and-repository-scaffold/SKILL.md) | authored |
| 2 | state-and-secret-management | [`terraform-state-and-secret-management`](terraform-state-and-secret-management/SKILL.md) | authored |
| 3 | plan-gate-and-policy-as-code | [`terraform-plan-gate-and-policy-as-code`](terraform-plan-gate-and-policy-as-code/SKILL.md) | authored |
| 4 | apply-and-promotion-mechanics | [`terraform-apply-and-promotion-mechanics`](terraform-apply-and-promotion-mechanics/SKILL.md) | authored |
| 5 | module-reuse-and-supply-chain | [`terraform-module-reuse-and-supply-chain`](terraform-module-reuse-and-supply-chain/SKILL.md) | authored |

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
