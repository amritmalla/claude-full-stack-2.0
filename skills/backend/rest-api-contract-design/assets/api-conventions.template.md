# API Conventions

## Resource Naming

[Plural nouns, lowercase kebab-case, shallow hierarchies, stable identifiers, and state-transition route rules.]

## HTTP Semantics

[Create, update, PATCH vs PUT, delete, async operation, optimistic concurrency, and retry semantics.]

## Pagination

[Cursor pagination standard, limit bounds, deterministic ordering, request/response examples.]

## Filtering and Sorting

[Allowed filter fields, operators if any, sort fields, default order, and bounds.]

## Idempotency

[Unsafe operation requirements, `Idempotency-Key` format, TTL, duplicate request behavior, replay semantics.]

## Error Contract

[Shared error envelope, validation details, trace correlation.]

### Error Code Registry

| Code | HTTP status | Meaning | Notes |
|---|---:|---|---|
| `VALIDATION_FAILED` | 400 | Request validation failed | Per-field detail in `details` |
| `UNAUTHENTICATED` | 401 | Missing or invalid credentials | |
| `FORBIDDEN` | 403 | Authenticated but not permitted | |
| `RESOURCE_NOT_FOUND` | 404 | Resource does not exist | |
| `CONFLICT` | 409 | State conflict | Includes illegal transitions |
| `IDEMPOTENCY_CONFLICT` | 409 | Same key, different body | |
| `RATE_LIMITED` | 429 | Caller exceeded rate limit | Includes `Retry-After` |
| `INTERNAL` | 500 | Unhandled server error | `traceId` required |
| `UPSTREAM_UNAVAILABLE` | 502/503 | Dependency unavailable | |
| `<DOMAIN_CODE>` | nnn | [Domain-specific code] | Document why a standard code does not fit |

## Tags and Operation Naming

- Tags follow resource names in plural lowercase (`orders`, `payments`).
- Every operation declares an explicit `operationId` in camelCase: `createOrder`, `getOrder`, `listOrders`, `cancelOrder`.
- `operationId` values are globally unique within the spec and drive client SDK method names — keep them readable and stable across versions.

## Versioning and Compatibility

[Versioning strategy, additive-change rules, breaking-change policy, deprecation, sunset policy.]

## Security

[Auth model, authorization scopes, tenant boundaries, public/internal exposure.]

## Rate Limiting

[Windowing strategy (fixed/sliding/token bucket), per-caller limits, standard headers (`X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`), `429` response with `Retry-After`.]

## Examples

[Representative valid request/response examples or links to OpenAPI examples.]

## Deferred Decisions

[Only intentionally deferred API contract decisions.]
