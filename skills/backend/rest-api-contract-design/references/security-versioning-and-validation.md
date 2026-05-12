# Security, Versioning, and Validation

Use this reference for exposure rules, compatibility, field constraints, and examples.

## Security and exposure

Clarify:

- public vs internal API,
- authentication model,
- authorization scopes,
- RBAC needs,
- tenant isolation,
- service-to-service auth,
- rate limiting,
- abuse prevention,
- sensitive data exposure.

Define OpenAPI `components/securitySchemes` and apply security requirements consistently at the global or operation level.

Defaults:

- OAuth2/JWT for external APIs,
- service auth for internal APIs,
- explicit tenant boundaries,
- rate-limit expectations for public or high-risk endpoints.

## Versioning

Choose one strategy and apply it globally.

URI versioning is the recommended default for operational simplicity:

```http
/v1/orders
```

Header versioning is acceptable only when platform governance requires it:

```http
Accept: application/vnd.api.v1+json
```

Document:

- compatibility guarantees,
- additive-change rules,
- breaking-change policy,
- deprecation process,
- sunset policy.

This skill defaults to versioned URIs over hypermedia for evolution. HATEOAS is out of scope unless the user explicitly accepts the implementation, documentation, and client-tooling cost.

## Validation

Define for every schema:

- required fields,
- nullable semantics,
- enum constraints,
- length limits,
- numeric bounds,
- timestamp format,
- identifier format,
- immutable fields,
- default values when they exist.

Rules:

- timestamps use ISO-8601 UTC,
- validation must be explicit,
- nullability must be unambiguous,
- examples must satisfy the schema.

## Examples

Every request and response body should include realistic examples.

Avoid:

- toy values that hide constraints,
- missing required fields,
- examples that violate enum or timestamp rules,
- ambiguous IDs that do not match documented formats.
