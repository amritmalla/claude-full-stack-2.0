# deployment-standards

Contract for how artifacts are built, promoted, and released. Every `skills/implementations/infrastructure/*` and CI/CD-producing skill MUST conform.

## Build artifacts

- One artifact per service per commit, identified by immutable digest (image SHA, package hash).
- Artifacts are environment-agnostic. Configuration is injected at deploy time, never baked into the image.
- Reproducible: rebuilding the same commit produces a bit-identical artifact (modulo signing timestamps).
- Signed: artifacts MUST be signed (cosign, Sigstore, or platform-native) before promotion.

## Environments

Standard ladder:

```
local → ci → dev → staging → production
```

Promotion rules:

- An artifact reaches `production` only by promotion from `staging`, never by direct build.
- `staging` MUST mirror `production` topology (same managed services, same network policy shape). Data may be anonymized.
- No environment-specific code branches (`if env == 'prod'`). Behavior differences come from config.

## CI gates

Every PR to the default branch MUST pass:

1. Lint + format check.
2. Unit tests.
3. Integration tests against ephemeral dependencies (Testcontainers or equivalent).
4. Build artifact (proves it builds).
5. SCA + container scan (`security-standards`).
6. SAST (`security-standards`).
7. OpenAPI / schema lint where applicable (`api-standards`).
8. Migration plan generated and reviewed for any schema-changing PR.

CI MUST NOT push to environments. CD is a separate pipeline triggered by merge.

## CD gates

Per environment:

| Env | Gates before deploy | Rollback target |
|---|---|---|
| `dev` | CI green | Previous artifact |
| `staging` | CI green + deployed to `dev` for ≥10min with no error spike | Previous artifact |
| `production` | Passed in `staging` ≥1h + change approval (auto for tier-2/3, human for tier-0/1) | Previous artifact, ≤5min |

## Deployment strategies

- Default: rolling update with readiness probes.
- Tier-0 services: blue-green or canary required. Canary stage: 5% → 25% → 100% with automated rollback on SLO burn.
- Database migrations: backwards-compatible deploys mandatory (expand → migrate → contract). Never deploy a service version that requires a not-yet-run migration.

## Configuration

- 12-factor: config via environment variables or mounted config files.
- Per-environment config files live in the deployment repo, not the service repo.
- Feature flags for runtime toggles; do not redeploy to flip a flag.

## Rollback

- Every deploy declares a rollback artifact (typically the previous one).
- Rollback path MUST be tested in `staging` at least quarterly.
- Forward-fix preferred over rollback when data has been written in a non-backwards-compatible way; mark this in the deploy notes.

## Infrastructure as code

- All infrastructure managed via Terraform / Pulumi / CDK. No console clicks in `staging` or `production`.
- IaC changes follow the same CI/CD ladder as application code.
- State files: remote, locked, encrypted.

## Observability on deploy

Every deploy emits a deployment event into the metrics system:

```
deployment_event{service, version, environment, status, actor}
```

Dashboards correlate deploys with SLO burn (`observability-standards`).

## Anti-patterns

- Building artifacts in the deploy step instead of promoting an existing one.
- "Hot-fix in production" workflows that skip `staging`.
- Migrations coupled to deploys (must run together or app breaks).
- Long-lived feature branches that drift from the deploy ladder.
- Manual cloud-console changes that aren't reflected back into IaC.
