---
name: github-actions-pipeline-hardened
description: Use when building or hardening a GitHub Actions pipeline for a
  production service. Produces a build/test/scan/sign/push workflow that pins
  action SHAs, uses OIDC for cloud authentication, sets minimal job permissions,
  and publishes an SBOM and a cosign signature for every artifact.
---

# GitHub Actions Pipeline (Hardened)

## When to use

Invoke when authoring CI/CD for a new service or when an existing pipeline lacks supply-chain controls (unpinned actions, long-lived cloud secrets, wide-open `permissions`). Use after the Dockerfile and tests exist.

## Inputs

- Project type: Maven/Gradle.
- Target container registry (e.g., GHCR, ECR, GAR).
- Target cloud account and the OIDC trust relationship name.

## Output contract

Generated workflows MUST conform to:

- [deployment-standards](../../../../standards/deployment-standards/README.md) — required CI gates: lint, unit, integration (Testcontainers), build artifact, SCA, container scan, SAST, OpenAPI lint (when relevant), migration plan review. CI does not push to environments; CD is a separate pipeline.
- [security-standards](../../../../standards/security-standards/README.md) — actions pinned by SHA, OIDC for cloud auth (no long-lived keys), signed artifacts (cosign/Sigstore), secret scanning in pre-commit + CI.
- [naming-conventions](../../../../standards/naming-conventions/README.md) — workflow filenames `kebab-case`, env vars `SCREAMING_SNAKE_CASE`.

## Process

1. Define the job graph: `build` → `test` → `sast` → `sbom` → `sign` → `push` → `deploy`. Each is a separate job with explicit `needs`.
2. Pin every `uses:` reference to a full commit SHA. Reject `@vN` floating tags.
3. Set top-level `permissions: read-all`; override per-job to add only what is required (e.g., `id-token: write` for OIDC, `packages: write` for GHCR push).
4. Use OIDC to authenticate to the cloud (`aws-actions/configure-aws-credentials` or equivalent). Remove any long-lived cloud secrets from repository settings.
5. Run SAST (e.g., `github/codeql-action`) and dependency scanning (e.g., `actions/dependency-review-action` on PRs).
6. Generate an SBOM with `anchore/sbom-action` and upload it as an artifact.
7. Sign the container image with cosign (keyless, using OIDC) and attach the signature.
8. Apply concurrency control: `concurrency: { group: ${{ github.ref }}, cancel-in-progress: true }` on PR builds.
9. Emit `.github/workflows/build.yml` and `.github/workflows/release.yml`, plus `pipeline.md` documenting the supply-chain controls.

## Outputs

- `.github/workflows/build.yml`.
- `.github/workflows/release.yml`.
- `pipeline.md`.

## Quality checks

- [ ] Every `uses:` is pinned to a full commit SHA.
- [ ] Top-level `permissions` defaults to read; jobs grant only what they need.
- [ ] Cloud authentication uses OIDC; no long-lived cloud credentials in secrets.
- [ ] SBOM is produced and uploaded as a workflow artifact.
- [ ] Container images are signed with cosign; signature is verifiable from the registry.
- [ ] PR workflows use `concurrency` with `cancel-in-progress`.

## References

(None in v0.1.)
