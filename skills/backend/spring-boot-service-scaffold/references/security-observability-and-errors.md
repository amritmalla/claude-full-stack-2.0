# Security, Observability, and Errors

Use this reference when generating operationally safe defaults.

## Security baseline

Clarify:

- public vs internal API,
- JWT/OAuth2/session auth,
- RBAC needs,
- service-to-service auth,
- actuator access policy,
- CORS expectations,
- CSRF posture,
- secret management strategy.

Defaults:

- stateless JWT for APIs,
- RBAC abstraction from the start,
- authenticated actuator endpoints outside dev,
- `/actuator/health` available for probes,
- externalized secrets,
- deny-by-default security posture.

Never scaffold hardcoded secrets, anonymous admin surfaces, open non-health actuator endpoints in non-dev, or permissive CORS without justification.

## Observability baseline

Generate:

- structured logs,
- JSON logs in non-dev profiles,
- traceId and spanId fields,
- MDC propagation where needed,
- Micrometer metrics,
- Prometheus exposure,
- readiness/liveness/startup probes,
- operational metadata,
- OpenTelemetry-compatible configuration hooks when appropriate.

Missing observability is a production defect.

## Actuator and health

Expose:

- `health`,
- `info`,
- `metrics`,
- `prometheus`.

Configure:

- liveness probe,
- readiness probe,
- startup probe,
- dependency-aware readiness,
- fast cold-start probe responses,
- secured non-dev actuator endpoints except health.

## Error handling

Generate one error envelope for every API error:

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Resource not found",
    "traceId": "abc123",
    "details": []
  }
}
```

Rules:

- never leak stack traces,
- never expose persistence internals,
- map validation errors cleanly,
- include correlation identifier,
- use consistent status-code mapping,
- keep domain exceptions separate from transport exceptions.
