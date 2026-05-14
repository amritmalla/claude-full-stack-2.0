# Auth Review Quality Rubric

Load this before finalizing. Revise until each check passes or explicitly document the unresolved gap.

## Required checks

- [ ] Trust boundaries are mapped and gaps are identified.
- [ ] Spring Security version is identified.
- [ ] Servlet vs reactive stack is identified and configuration matches.
- [ ] JWT algorithm validation is pinned explicitly.
- [ ] Issuer, audience, expiry, and time validation are enforced.
- [ ] JWKS cache and key-fetch failure behavior are documented.
- [ ] Endpoint-level authorization exists, not only gateway-level enforcement.
- [ ] Scopes and roles are least-privilege and endpoint-specific.
- [ ] Tenant isolation is addressed where relevant.
- [ ] Refresh token replay protection exists where refresh tokens are used.
- [ ] Signing keys and client secrets are externally managed with documented rotation.
- [ ] CSRF posture is explicitly justified.
- [ ] CORS uses explicit allow-lists per environment.
- [ ] Auth errors avoid user enumeration, privilege enumeration, and token probing.
- [ ] Security-relevant events are observable and logged.
- [ ] No sensitive credentials or tokens are logged.
- [ ] Security tests exist or gaps are documented.
- [ ] Every finding has severity, confidence, component, evidence, impact, and remediation.
- [ ] The configuration could realistically survive production exposure.
- [ ] Spring Security 5.x APIs (`WebSecurityConfigurerAdapter`, `authorizeRequests`) trigger a Blocker finding and the review is adapted to the actual API surface, not Security 6 lambda DSL.
- [ ] Pre-flight gate was applied — review did not proceed against a service with no security config; if it did, the verdict is "incomplete — preconditions not met."
- [ ] Secrets scan over `application*.yml`, `bootstrap*.yml`, `.env*`, and `src/main/resources/**` was performed. Findings, if any, are Blocker severity.
- [ ] Static analysis (CVE scan + semgrep `p/spring-security` `p/jwt`) was run, **or** a Medium finding documents the skip with the missing tool named.
- [ ] Rate limiting on auth-adjacent endpoints (login, refresh, password reset, 2FA) is verified or flagged as a finding.
- [ ] Opaque-token services are not reviewed with JWT-only criteria; the introspection failure mode and cache policy are addressed.
- [ ] Actuator review covers the full sensitive endpoint set (env, configprops, beans, mappings, loggers, heapdump, threaddump, httpexchanges, caches, auditevents, metrics, scheduledtasks, flyway, shutdown), not just env/configprops/heapdump.

## Failure handling

If a check fails:

1. Record a finding with severity and evidence.
2. Provide concrete remediation.
3. Ask the user for clarification only when the missing decision cannot be inferred.
4. Keep unresolved questions explicit; do not bury them in assumptions.
