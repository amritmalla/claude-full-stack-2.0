# github-actions

> Status: draft

## Purpose

Implements CI/CD pipelines on GitHub Actions: workflow scaffold and runner topology, identity and OIDC federation, gate and environment policy, release mechanics and promotion, and supply-chain artifact integrity.

Architecture decisions (env ladder, required gates, runner posture, signing and SBOM requirements, promotion policy) come from upstream and are taken as inputs here.

## Tool family

GitHub Actions is the sole member of **Family I — CI/CD** in the infrastructure layer model. See [`implementations/infrastructure/README.md`](../README.md) for the full archetype set and philosophy.

## Ecosystem (target)

- GitHub Actions with hosted runners (default) or self-hosted runners where isolation/cost demands
- Reusable workflows (`workflow_call`) and composite actions for sharing
- OIDC federation to AWS / GCP / Azure (no long-lived cloud keys)
- Repository, environment, and organization secrets with environment protection rules
- Pinned action SHAs (never `@vN` floating tags) with Dependabot-managed updates
- SBOM via Syft; container/artifact signing via cosign/Sigstore; SLSA provenance attestations
- Required status checks tied to branch protection

## Skills

### Authored

- [github-actions-pipeline-hardened](github-actions-pipeline-hardened/SKILL.md) — *omnibus production-readiness pipeline* covering build/test/scan/sign/push with pinned action SHAs, OIDC, minimal permissions, SBOM, and cosign signature. Touches archetypes 1, 2, 3, and 5; kept as the holistic review and authoring entry point.

### Archetype coverage

| # | Archetype | Skill | Status |
|---|---|---|---|
| 1 | workflow-scaffold-and-runner-topology | covered partially by `github-actions-pipeline-hardened` *(omnibus)* | split planned |
| 2 | identity-and-oidc-federation | covered partially by `github-actions-pipeline-hardened` *(omnibus)* | split planned |
| 3 | gate-and-environment-policy | covered partially by `github-actions-pipeline-hardened` *(omnibus)* | split planned |
| 4 | release-mechanics-and-promotion | _none_ | planned |
| 5 | supply-chain-and-artifact-integrity | covered partially by `github-actions-pipeline-hardened` *(omnibus)* | split planned |

### Planned skill scope (future work)

- **`github-actions-workflow-scaffold-and-runner-topology`** *(archetype 1)* — workflow file layout (`build.yml`, `test.yml`, `release.yml`, `infra.yml`), reusable workflows for shared concerns (build-test-scan, container-sign-push), composite actions for repeated step sequences, hosted vs self-hosted runner selection per workload sensitivity, runner labels and isolation, repo-vs-org-level workflow organization.
- **`github-actions-identity-and-oidc-federation`** *(archetype 2)* — OIDC trust relationships per cloud (AWS IAM role + condition on `aud` and `sub`, GCP Workload Identity Federation, Azure federated credentials), removal of long-lived cloud access keys, repository and environment secret hygiene, signing-key handling (cosign keyless or KMS-backed), environment-protection rules, least-privilege `permissions:` per job.
- **`github-actions-gate-and-environment-policy`** *(archetype 3)* — required status checks per protected branch, environment approvers for prod, deployment branches and tag patterns, concurrency control (`concurrency.group`, `cancel-in-progress`), change-window enforcement via job conditionals, manual-approval gates for tier-0 deployments.
- **`github-actions-release-mechanics-and-promotion`** *(archetype 4)* — build → test → scan → sign → push → deploy orchestration as a reusable workflow, env-promotion ladder (CI builds + signs once; CD promotes the same artifact), canary / blue-green / rolling deployment hooks, rollback workflow, release-notes automation (changesets / release-please), version-tagging discipline.
- **`github-actions-supply-chain-and-artifact-integrity`** *(archetype 5)* — pinned action SHAs (no floating tags) maintained via Dependabot, SBOM generation (Syft) for every artifact, SCA via Dependabot/Snyk/OSV scanner, container/artifact signing via cosign (keyless or KMS), SLSA provenance attestations, secret scanning (gitleaks / GitHub native), required vulnerability-scan gates with tier-based thresholds.

## Omnibus skill posture

`github-actions-pipeline-hardened` is the **production-readiness** authoring entry point — useful when shipping a new pipeline holistically. It will not be deprecated when the archetype-scoped successors land; instead, it remains the cross-archetype "produce a complete hardened pipeline in one pass" skill, and the new skills own the *targeted* authoring or hardening of each slice. This is a documented exception to the one-skill-per-archetype rule.

## Architecture domains implemented

| Architecture domain | How |
|---|---|
| [infrastructure-platform](../../../architecture/infrastructure-platform/README.md) | CI/CD pipeline definitions, runner topology, env ladder. |
| [security](../../../architecture/security/README.md) | OIDC federation, signed artifacts, SAST/SCA/secret scanning, pinned actions. |
| [operations](../../../architecture/operations/README.md) | Promotion gates, environment protection, runbook inputs for failed releases. |
| [reliability](../../../architecture/reliability/README.md) | Rollback workflow, canary/blue-green deployment hooks. |

## Standards this implementation conforms to

- [deployment-standards](../../../standards/deployment-standards/README.md) — required CI gates (lint, test, build, scan, OpenAPI lint when relevant, migration plan review), env-ladder enforcement.
- [security-standards](../../../standards/security-standards/README.md) — pinned action SHAs, OIDC (no long-lived keys), signed artifacts (cosign/Sigstore), secret scanning.
- [naming-conventions](../../../standards/naming-conventions/README.md) — workflow filenames `kebab-case`, env vars `SCREAMING_SNAKE_CASE`.
- [architecture-schema](../../../standards/architecture-schema/README.md) — tier classification drives gate strictness, approver requirements, and signing posture.

## Upstream inputs

- Approved `infrastructure-platform.md` declaring env ladder, required gates, runner posture, and target cloud(s) for OIDC federation.
- Approved `architecture/security` decisions on OIDC trust shape, signing requirements, and SBOM/SCA gates.
- Approved `architecture/operations` decisions on promotion gates, environment approvers, and rollback expectations.
