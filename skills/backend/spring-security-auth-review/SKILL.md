---
name: spring-security-auth-review
description: Use when reviewing the authentication and authorization setup of a
  Spring Boot service that uses JWT or OAuth2. Produces a findings report and a
  hardened SecurityFilterChain config covering token validation, scope
  enforcement, refresh strategy, CSRF, CORS, and signing-key storage.
---

# Spring Security Auth Review

## When to use

Invoke before shipping any Spring Boot service that handles authenticated requests, or whenever the auth code is changed materially. Do not invoke for review of authorization business logic above the framework layer (use a domain-policy review for that).

## Inputs

- Spring Boot service source tree, including `SecurityFilterChain` configuration.
- Auth model: JWT issuer, audience, scopes, refresh strategy, token TTLs.
- Where signing keys / JWKS endpoints live.

## Process

1. Locate the `SecurityFilterChain` bean(s). List every matcher and the authentication required.
2. Verify JWT validation: signature algorithm pinned, issuer checked, audience checked, expiry enforced, clock skew bounded.
3. Verify scopes are enforced per endpoint (method security via `@PreAuthorize` or request matchers).
4. Verify the refresh token strategy: refresh tokens rotate on use; old refresh tokens are revoked; refresh endpoint is rate-limited.
5. Verify signing keys are NOT in source. Confirm key source (KMS, secret manager, JWKS URL with caching).
6. Verify CSRF posture: disabled only for stateless JSON APIs with no cookie auth; otherwise enabled.
7. Verify CORS: allow-list of origins, not `*`; explicit allowed methods and headers.
8. Verify error envelopes do not leak token contents, stack traces, or user-existence signals.
9. Emit `auth-review.md` with findings categorized as Blocker / High / Medium / Low, and a hardened `SecurityConfig.java` snippet implementing the recommendations.

## Outputs

- `auth-review.md`.
- Hardened `SecurityConfig.java` snippet.

## Quality checks

- [ ] JWT signature algorithm is pinned (no `alg: none`, no algorithm negotiation).
- [ ] Issuer, audience, and expiry are all validated.
- [ ] Scopes are enforced at the endpoint level, not only at the gateway.
- [ ] Refresh tokens rotate and are revoked on use.
- [ ] Signing key / JWKS source is not in source code.
- [ ] CSRF is enabled OR explicitly justified as disabled.
- [ ] CORS allow-list is finite and per-environment.

## References

(None in v0.1.)
