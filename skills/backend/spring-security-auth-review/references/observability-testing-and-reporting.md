# Observability, Testing, and Reporting

Use this reference for auditability, tests, severity, and final artifacts.

## Security observability

Log:

- failed authentication attempts with correlation ID,
- successful authentications with principal identifier and timestamp,
- authorization failures with path and authority summary,
- token validation failures by type, not content,
- refresh token anomalies,
- JWKS fetch failures.

Metrics:

- auth failure rate by endpoint, client, or IP,
- token validation latency,
- refresh token usage patterns,
- JWKS fetch failures and latency,
- access denied rate.

Never log:

- raw access tokens,
- refresh tokens,
- ID tokens,
- passwords,
- client secrets,
- full JWT claims,
- Authorization headers,
- credential-containing cookies.

## Security testing

Automated CI/CD tests:

- 401 on protected endpoints without token,
- 401 on malformed token,
- 401 on expired token,
- 401 on wrong-audience token,
- 403 on insufficient scope or role,
- 403 on CSRF-protected endpoint without CSRF token where applicable,
- preflight rejection for disallowed origins,
- health/liveness accessible,
- sensitive actuator endpoints require auth.

Manual or periodic tests:

- refresh token replay detection,
- token rotation behavior,
- key rotation survivability on staging,
- session fixation resistance,
- cookie security flags.

Flag missing security tests as findings.

## Severity classification

| Level | Definition | Examples |
|---|---|---|
| Blocker | Enables direct compromise; must fix before production | Missing auth on sensitive endpoint, hardcoded secret, algorithm injection |
| High | Significant vulnerability or insecure default | Missing audience validation, replayable refresh tokens, wildcard CORS with credentials |
| Medium | Weakens security posture but not directly exploitable | Overly long token lifetimes, missing CSRF on non-sensitive cookie endpoints, unlogged auth failures |
| Low | Best practice deviation with minimal risk | Minor config improvement, documentation gap |

## Required report content

`auth-review.md` must include:

- executive summary and verdict,
- trust boundary map,
- findings table,
- severity classification,
- Spring Security version and stack type,
- JWT validation checklist,
- authorization coverage,
- refresh token/session strategy,
- secret and key management assessment,
- CSRF posture,
- CORS per environment,
- error handling leakage findings,
- observability gaps,
- security testing gaps,
- remediation priority list.

Verdicts:

- **production-ready** — no Blockers or Highs remain.
- **conditionally ready** — Highs remain with a documented remediation plan; Blockers absent.
- **not ready** — one or more Blockers present.
- **incomplete — preconditions not met** — the review halted before full coverage (e.g., no `SecurityFilterChain` exists, source tree inaccessible, required static-analysis tools unavailable). Document the precondition that failed.

## Findings columns

Every finding row must carry:

| Column | Required | Meaning |
|---|---|---|
| Severity | yes | Blocker / High / Medium / Low |
| Confidence | yes | Confirmed (read the file or saw the behavior), Probable (strong indirect signal), Suspected (pattern or grep hit, not verified) |
| Component | yes | The specific file, bean, filter chain, or boundary |
| Evidence | yes | `path/to/file.java:42` or the exact config line, or named tool output (e.g., `semgrep: spring-security.csrf-disabled-without-rationale`) |
| Impact | yes | What an attacker gains, or what posture is weakened |
| Remediation | yes | The specific change, not generic advice |

Mixing Confirmed and Suspected findings without marking them lets High-severity-Low-confidence findings dominate triage. Promote Suspected → Confirmed only after verification.
