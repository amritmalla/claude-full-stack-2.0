# Node.js Auth and Security Review Playbook

Load this when implementing any owned area of `nodejs-auth-and-security-review` or running the OWASP-style review. It expands the operating rules and process steps in `SKILL.md` with the detail needed to ship a defensible auth layer.

## Why this workflow exists

Auth done wrong is the most expensive class of production bug: a missing authorization check is a data breach, not a 500; authentication mistaken for authorization lets any logged-in user act as any other; a leaked signing key invalidates every token ever issued; and a permissive CSP turns one XSS into account takeover. These failures are not caught by typecheck or happy-path tests — only by default-deny design and negative tests.

The goal is an auth layer where identity and permission are distinct, every protected route is explicitly authorized, secrets never touch source, and the failure mode of every check is denial.

## Behavioral rules in depth

### 1. Consume the security architecture; do not invent it

`architecture/security` decides the provider, session-vs-token model, token lifetime, and secret handling. These are risk decisions, not implementation defaults. If a needed decision is missing, raise an ADR candidate. The skill implements the decided model; it does not pick between sessions and JWTs on its own.

### 2. Extend the scaffold seam — never duplicate it

`nodejs-service-scaffold` installed a typed principal-provider shell, validated config, structured logging, and error tiers. Authentication fills the principal shell; auth config extends the existing zod schema; redaction extends the existing logger. Re-implementing any of these forks the baseline and the two copies drift.

### 3. Authentication is not authorization

Authentication answers "who is this". Authorization answers "may they do this". A valid token means the first, never the second. Every protected route resolves an explicit authorization decision against the model in `architecture/security` (RBAC role, ABAC attribute, or OAuth scope). The default is deny: a route with no decision is unreachable, not open.

### 4. Never authorize on client-supplied identifiers alone (IDOR)

`GET /orders/:id` must check that the authenticated principal owns or may read order `:id` — not merely that a token is valid. Authorizing on a path/body id without binding it to the principal is Insecure Direct Object Reference, the most common real-world breach. Bind every resource access to the principal.

### 5. Secrets flow through the validated config seam only

Signing keys, client secrets, session secrets, and JWKS URIs are added to the scaffold's zod schema so a missing one aborts boot, not a request. They are never hardcoded, never logged, never committed. `.env.example` carries placeholder names only. Log serializers redact `authorization`, `cookie`, token, and password fields.

### 6. Secure headers and abuse controls are baseline, not optional

| Control | Why | Where |
|---|---|---|
| helmet + deny-by-default CSP | Contains XSS; blocks inline-script account takeover | Scaffold app factory, after context middleware |
| HSTS | Prevents protocol downgrade | helmet config |
| Remove `x-powered-by` | Reduces version fingerprinting | helmet / framework option |
| CSRF token | Blocks cross-site state change on cookie sessions | State-changing routes when session is cookie-based |
| Rate limiting | Slows credential stuffing and brute force | Authentication endpoints |

CSRF is required only for cookie-session state changes — pure bearer-token APIs are not CSRF-prone but still need the other controls.

### 7. Fail closed

Every auth and authz code path treats an error as denial. Never `try/catch` an authorization failure into a fallthrough that allows the request. A verification library throwing is a 401/403, never a 200.

### 8. A review without negative tests is theater

The security suite must assert *denial*: unauthenticated request → 401; authenticated but wrong role/scope → 403; expired token → 401; tampered signature → 401; IDOR attempt → 403/404. Positive cases per role prove the matrix is not deny-all. The matrix lives as a table in the test file so reviewers see coverage at a glance.

## Step detail

**Step 1 — Context.** Load `architecture/security` and `backend-architecture.md`. Extract provider, session-vs-token, token lifetime, secret handling, route boundaries. Confirm the scaffold baseline. Missing decision → ADR candidate.

**Step 2 — Config.** Add `AUTH_ISSUER`, `AUTH_AUDIENCE`, `AUTH_JWKS_URI`, `OAUTH_CLIENT_ID`, `OAUTH_CLIENT_SECRET`, `SESSION_SECRET`, or the subset the chosen model needs, to the scaffold zod schema and `.env.example` (placeholders only).

**Step 3 — Authentication.** Implement the chosen strategy in `src/auth/`: Passport strategy, `jose`/JWKS JWT verification, or OAuth2/OIDC authorization-code flow. Populate the scaffold principal seam with a typed `Principal { sub, roles/scopes, ... }`. Reject expired, malformed, wrong-issuer, wrong-audience tokens.

**Step 4 — Authorization.** Implement a default-deny guard. Per route, declare the required role/scope/attribute. Resolve the decision against `Principal`; bind resource access to the principal (anti-IDOR). No route is reachable without an explicit decision.

**Step 5 — Hardening.** Add helmet with deny-by-default CSP + HSTS, strip `x-powered-by`, CSRF on cookie-session state-changing routes, rate limiter on auth endpoints. Wire in the scaffold app factory after the request-context middleware so logs and errors still correlate.

**Step 6 — Secrets.** Confirm every credential resolves via config; extend logger redaction; document rotation (key rollover, JWKS cache TTL, secret store) in the README security section.

**Step 7 — Review.** Walk the rubric: authn, authz/IDOR, injection, secrets, headers, rate limiting, error leakage, `npm audit`. Record findings + resolutions in the README.

**Step 8 — Tests.** Negative suite + positive-per-role + authorization matrix table. Wire into the existing test command.

**Step 9 — Verify.** `tsc --noEmit`, lint, full tests incl. security suite, boot smoke. Then standards check (security-standards, api-standards). Document any unresolved gap explicitly.

## Anti-patterns to detect

Call these out explicitly when found:

- A valid token treated as permission (no separate authorization decision)
- A protected route with no explicit authorization check (implicit allow)
- Authorization on a path/body id without binding it to the principal (IDOR)
- Signing keys, client secrets, or session secrets hardcoded, logged, or committed
- `authorization`/`cookie`/token fields unredacted in logs
- Auth config read from `process.env` directly instead of the scaffold config schema
- Missing helmet/CSP, `x-powered-by` still present, or a wide-open `unsafe-inline` CSP
- No rate limiting on login/token endpoints
- Authorization error caught into an allow (fails open)
- Security suite with only positive cases (no denial tests)
- Re-implementing config, logging, or error tiers instead of extending the scaffold
- `npm audit` not run, or high-severity advisories neither fixed nor explicitly accepted
