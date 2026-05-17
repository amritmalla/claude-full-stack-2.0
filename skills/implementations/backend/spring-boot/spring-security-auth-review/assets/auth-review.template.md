# Auth Review

## Executive Summary

[Verdict: production-ready / conditionally ready / not ready / incomplete — preconditions not met. Summarize top risks and confidence in the review's coverage.]

## Trust Boundary Map

[Actors, clients, gateway, issuer, service, downstream services, protected resources, tenant boundaries.]

## Findings

| Severity | Confidence | Component | Description | Evidence | Impact | Remediation |
|---|---|---|---|---|---|---|
| [Blocker/High/Medium/Low] | [Confirmed/Probable/Suspected] | [component] | [finding] | [file:line or tool output] | [impact] | [specific fix] |

## Spring Security Configuration

[Version, Servlet/reactive stack, filter chains, matcher scope, actuator rules, method security.]

## JWT and OAuth2 Validation

[Algorithm, issuer, audience, expiry, nbf, clock skew, JWKS cache, key-fetch behavior.]

## Authorization Coverage

[Endpoint rules, method-level checks, ownership checks, tenant isolation, service-to-service auth.]

## Token Lifecycle, Sessions, and Secrets

[Refresh tokens, sessions, token storage, secret source, rotation, key management.]

## Browser Security

[CSRF, CORS, cookies, SameSite, logout behavior.]

## Error Handling and Leakage

[401/403 behavior, login failures, token parsing errors, stack traces, token logging.]

## Observability and Auditability

[Auth logs, metrics, JWKS failures, refresh anomalies, sensitive-data redaction.]

## Security Testing

[Existing automated tests, missing tests, manual validation needs.]

## Remediation Priority

[Blockers first, ordered by risk.]

## Open Questions

[Only unresolved auth/security decisions.]
