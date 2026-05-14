# Authorization, Browser Security, and Exposure

Use this reference for authorization coverage, tenant isolation, service-to-service auth, CSRF, CORS, cookies, and information leakage.

## Authorization enforcement

Review:

- path-based access rules,
- role and scope checks,
- method-level `@PreAuthorize` and `@PostAuthorize`,
- ownership checks,
- parameter-based authorization,
- reactive method security enablement,
- endpoint-specific permission boundaries.

Recommend centralized authority mapping and endpoint-specific scopes or roles.

Challenge coarse ADMIN/USER-only RBAC, admin-by-default scopes, role explosion, and "authenticated means allowed" assumptions.

## Service-to-service and tenant isolation

Verify services validate that callers are authorized, not merely authenticated.

Check confused deputy risk:

- end-user tokens passed to downstream services that require service identity,
- services accepting upstream context without validation,
- machine-to-machine calls using overly broad scopes.

Multi-tenant services must validate tenant claims against the requested resource. Authentication alone does not enforce tenant isolation.

## Rate limiting on auth endpoints

Authentication-adjacent endpoints are the most-attacked surface in any service. Verify rate limiting exists on:

- `/login` and any password verification path,
- `/oauth2/token` and refresh endpoints,
- password reset request and confirmation,
- 2FA challenge and verify,
- account lookup endpoints that reveal whether an identity exists.

Conventions (align with `rest-api-contract-design`):

- Return `429 RATE_LIMITED` with `Retry-After`.
- Emit `X-RateLimit-*` headers per the contract conventions.
- Track per-IP, per-account, and per-client limits independently — credential stuffing rotates IPs; an account-locked attacker should not be limited only per-IP.
- Combine rate limiting with progressive lockout (exponential backoff, captcha, MFA challenge) for repeated failures on the same account.

Missing rate limits on auth endpoints is High severity at minimum; without them, credential stuffing and refresh-token replay are trivial.

## CSRF and cookies

CSRF posture:

| Scenario | CSRF required | Rationale |
|---|---|---|
| Stateless bearer token API in Authorization header | No | No browser-managed credential |
| Cookie/session-authenticated MVC app | Yes | Browser auto-attaches cookies |
| BFF with cookie session | Yes | Browser auto-attaches cookies |
| SPA with refresh token in cookie | Yes on refresh endpoint | Cookie is browser-managed |

Cookie requirements:

- `Secure`,
- `HttpOnly`,
- `SameSite=Strict` or Lax when IdP redirect requires it,
- `__Host-` prefix when possible,
- narrowest practical path,
- server-side invalidation on logout.

Reject blanket CSRF disabling without justification, missing Secure flag in production, and `SameSite=None` without Secure.

## CORS

Rules:

- never use `allowedOrigins("*")` for authenticated APIs,
- use explicit allow-lists per environment,
- if `allowCredentials(true)`, origins must be explicit,
- validate `allowedOriginPatterns` carefully,
- use separate dev/staging/prod config,
- typical preflight `maxAge` is 1 hour.

Reject wildcard policies, origin reflection, broad credential sharing, and one shared CORS config for all environments.

## Error handling and information leakage

Rules:

- 401 response: generic "Authentication required",
- 403 response: generic "Access denied",
- login failure: same response for unknown user and bad password,
- token validation: same response for expired, invalid signature, wrong audience,
- no stack traces in production responses,
- no raw token logging.

Avoid privilege enumeration, username enumeration, and token structure probing through differentiated errors.
