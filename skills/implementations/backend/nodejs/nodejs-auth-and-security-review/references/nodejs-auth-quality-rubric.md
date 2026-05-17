# Node.js Auth and Security Review Quality Rubric

Load this before declaring the auth and hardening work complete. Revise until each check passes or the unresolved gap is explicitly documented in the service README security section.

## Authentication

- [ ] The verification strategy matches the model in `architecture/security` (Passport / JWT-JWKS / OAuth2-OIDC).
- [ ] The scaffold principal-provider seam is filled with a typed `Principal`; no auth shell TODO remains.
- [ ] Expired tokens are rejected (test-verified).
- [ ] Tampered or wrong-signature tokens are rejected (test-verified).
- [ ] Wrong-issuer / wrong-audience tokens are rejected.

## Authorization

- [ ] Every protected route resolves an explicit authorization decision; default is deny.
- [ ] Unauthenticated access to a protected route returns 401 (test-verified).
- [ ] Authenticated-but-wrong-role/scope access returns 403 (test-verified).
- [ ] Resource access is bound to the authenticated principal — IDOR attempt is denied (test-verified).
- [ ] An authorization error denies access (fails closed) — no catch-into-allow path.

## HTTP surface hardening

- [ ] helmet (or equivalent) is wired with a deny-by-default CSP and HSTS.
- [ ] `x-powered-by` is removed.
- [ ] CSRF protection is present on cookie-session state-changing routes (or N/A for pure bearer APIs, documented).
- [ ] Authentication endpoints are rate limited.
- [ ] Hardening middleware is wired after the scaffold request-context middleware (logs/errors still correlate).

## Secrets and input

- [ ] Every auth secret resolves through the scaffold validated config seam (missing one aborts boot).
- [ ] No secret is hardcoded, logged, or committed; `.env.example` has placeholders only.
- [ ] `authorization`, `cookie`, token, and password fields are redacted in log output.
- [ ] Every external input is validated at the boundary with a schema; unknown fields are rejected.

## Review and dependencies

- [ ] The OWASP-style review walked authn, authz/IDOR, injection, secrets, headers, rate limiting, error leakage.
- [ ] Error responses leak no stack trace or internal detail outside dev.
- [ ] `npm audit` (or equivalent) was run; high-severity advisories are fixed or explicitly accepted with rationale.
- [ ] Findings and resolutions are recorded in the service README security section.

## Tests

- [ ] A negative suite asserts denial for: unauthenticated, wrong-role/scope, expired token, tampered token, IDOR.
- [ ] Positive cases exist per role/scope (the matrix is not deny-all).
- [ ] An authorization matrix table is present in the test file.
- [ ] The security suite runs as part of the standard test command.

## Build verification

- [ ] `tsc --noEmit` reports zero errors.
- [ ] The lint command passes.
- [ ] The full test command (including the security suite) passes (or the skip is documented with reason).
- [ ] The boot smoke check still passes after the auth layer is added.

## Standards conformance

- [ ] [security-standards](../../../../../../standards/security-standards/README.md): default-deny authorization, secrets via config seam, secure headers, boundary validation, no secrets in source/image.
- [ ] [api-standards](../../../../../../standards/api-standards/README.md): consistent 401/403 semantics and error shape; documented public/protected route split.

## Failure handling

If a check fails:

1. Identify the missing or incorrect control.
2. Ask the user for clarification if the decision cannot be inferred from `architecture/security` or `backend-architecture.md`.
3. Revise, then re-run `tsc --noEmit`, lint, the full test suite, and the boot smoke check.
4. Keep any unresolved gap explicit in the service README security section — never hide it as an assumption, and never default a security decision silently.
