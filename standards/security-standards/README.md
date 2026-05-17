# security-standards

Cross-cutting security contract. Every architecture domain and implementation MUST conform.

## Authentication

- Human users: OAuth2 / OIDC via an identity provider. No homegrown password storage unless explicitly justified in an ADR.
- Service-to-service: short-lived (≤1h) signed tokens (JWT, SPIFFE, or cloud-native workload identity). No long-lived shared secrets between services.
- API keys: allowed only for external partner integrations. Must be rotatable, scoped, and revocable individually.
- MFA required for any human access to production data.

## Authorization

- Default: role-based access control (RBAC) at the API gateway / service boundary.
- Resource-level checks (ABAC) live in the service that owns the resource — never trust the caller's claim of ownership.
- Every endpoint declares its required scope/role in the OpenAPI spec.
- "Authenticated" ≠ "authorized". A 401 vs 403 distinction is mandatory.

## Secrets management

- No secrets in source control. Ever. Pre-commit hook + CI scan (gitleaks or equivalent) is a required gate.
- Secrets live in a managed store (Vault, AWS Secrets Manager, GCP Secret Manager, Azure Key Vault).
- Application loads secrets at startup or via sidecar — never bakes them into images.
- Rotation cadence:
  - Service-to-service tokens: automatic, ≤1h lifetime.
  - Database credentials: ≤90 days.
  - API keys: ≤180 days or on personnel change.
  - Signing keys: ≤1 year with overlap window.

## Data protection

- TLS 1.3 in transit, no exceptions for internal traffic. mTLS for service mesh where available.
- At-rest encryption mandatory for all persistent stores. Cloud-managed keys acceptable; customer-managed keys (CMK) required for regulated workloads.
- PII MUST be tagged at schema level (see `prd-schema` and `architecture-schema` data ownership).
- Logs MUST NOT contain raw PII, tokens, or secrets. Mask at the logging layer, not in code-review.

## Threat modeling

Required before any `tier: 0` or `tier: 1` component (see `architecture-schema`) goes to production. Use STRIDE or equivalent. Output lives at `docs/architecture/<product>/threat-models/<component>.md`.

## Vulnerability management

- Dependency scanning (SCA): required in CI; high-severity vulns block merge.
- Container scanning: required for every image build.
- SAST (Semgrep or equivalent): required for backend services in CI.
- DAST: required quarterly for externally exposed services.
- CVE response SLO: critical = 7 days, high = 30 days, medium = 90 days.

## Compliance posture

When a product handles regulated data, the PRD MUST name the regime (`SOC 2`, `HIPAA`, `PCI-DSS`, `GDPR`, etc.). Implementation skills check the regime tag and enforce regime-specific controls.

## Incident response

- Every production service has a named on-call owner (see `architecture-schema` component frontmatter).
- Security incidents follow the playbook at `skills/architecture/operations` / `workflows/incident-response`.
- Post-incident review is mandatory; output is a public-to-org write-up.

## Anti-patterns

- Long-lived service tokens cached in env vars.
- "Internal-only" endpoints with no auth ("we'll add it later").
- Role checks performed only at the gateway, with services trusting forwarded user identity unconditionally.
- Logging full request bodies "for debugging".
- Disabling SAST/SCA gates "because the finding is a false positive" without filing the suppression in the registry.
