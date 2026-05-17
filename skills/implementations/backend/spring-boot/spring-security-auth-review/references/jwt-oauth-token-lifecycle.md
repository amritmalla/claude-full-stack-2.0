# JWT, OAuth, and Token Lifecycle

Use this reference for token validation, refresh/session strategy, secrets, and key rotation.

## JWT validation

Required checks:

- algorithm pinned explicitly,
- issuer validated,
- audience validated explicitly,
- expiry enforced,
- `nbf` enforced,
- clock skew bounded,
- JWKS refresh behavior defined,
- key-fetch failure behavior defined.

Spring resource servers validate issuer and time claims when configured correctly, but audience often needs explicit validation.

Recommended clock skew: 30 seconds for most deployments. Nimbus defaults may be wider; verify configuration.

Reject:

- accepting `none`,
- dynamic algorithm negotiation from token header,
- issuer-only validation,
- missing audience validation,
- symmetric keys shared across service boundaries,
- trusting claims from unvalidated tokens.

## Signing algorithms

Prefer asymmetric signing such as RS256, ES256, or EdDSA. The issuer keeps the private key; resource servers fetch public keys via JWKS.

Use HS256 only when issuer and resource server are the same trust domain. Do not distribute symmetric signing keys across services.

## Opaque tokens and introspection

Some OAuth2 resource servers use opaque tokens validated via the issuer's introspection endpoint (`/oauth2/introspect`) instead of self-validating JWTs. The validation surface is different:

- No algorithm pinning (no signature on the wire).
- No JWKS cache; instead, an **introspection response cache**.
- Each token validation is a network call by default — cache aggressively but bound by `expires_in` or a shorter TTL.
- Define introspection-endpoint failure behavior: cache hit only, fail closed, or limited grace window. Fail-open is rarely acceptable.
- Rate-limit and circuit-break the introspection client — the issuer is now a hot dependency.
- Introspection credentials (client_id/client_secret) are first-class secrets and rotate with the same discipline as signing keys.

Reject: unbounded introspection-response caching, fail-open introspection without justification, introspection client credentials in committed config.

## Refresh tokens and sessions

Refresh token requirements:

- rotation on each use,
- old token invalidated immediately,
- replay detection,
- token family invalidation on replay,
- bounded absolute lifetime,
- rate-limited refresh endpoint.

Recommended lifetimes:

- access token: 5-15 minutes,
- refresh token: bounded absolute expiry based on risk.

Reject indefinitely reusable refresh tokens, stateless refresh without replay controls, and long-lived bearer access tokens over 15 minutes without justification.

## Token storage

Browser SPA:

- access token in memory,
- refresh token in Secure, HttpOnly, SameSite cookie with `__Host-` prefix when possible.

Mobile:

- access token in memory,
- refresh token in platform secure storage.

Machine-to-machine:

- client credentials flow,
- no refresh token.

BFF pattern:

- browser never receives tokens,
- server manages OAuth tokens,
- browser receives secure session cookie.

Reject access or refresh tokens in localStorage or sessionStorage.

## Secrets and key management

Acceptable sources:

- KMS,
- HashiCorp Vault,
- AWS Secrets Manager,
- GCP Secret Manager,
- Azure Key Vault,
- JWKS endpoints with caching.

Rotation requirements:

- signing keys rotate with overlap,
- client secrets rotate with overlap,
- both old and new secrets valid during rotation window,
- JWKS cache TTL must be **shorter than the planned rotation overlap window**. 5–15 minutes is the recommended ceiling — chosen for revocation responsiveness, not as a target. Long caches (hours) defeat fast key revocation; rotation "overlap" alone does not save you when caches are stale.
- failure behavior uses retry/backoff and cached keys until expiry.

Reject hardcoded secrets, checked-in PEM files, unmanaged environment secrets, keys committed to git history, and fail-open key-fetch behavior unless explicitly justified.
