# HTTP Semantics and Operational Rules

Use this reference when defining endpoint behavior, pagination, idempotency, retries, and errors.

## Method semantics

Define:

- create semantics,
- update semantics,
- PATCH vs PUT behavior,
- delete semantics,
- partial update rules,
- immutable fields,
- optimistic concurrency,
- eventual consistency assumptions.

Defaults:

- Use `POST` for creation and state transitions.
- Use `GET` for safe reads.
- Use `PATCH` for partial mutation, defaulting to **RFC 7396 JSON Merge Patch** with `Content-Type: application/merge-patch+json`. Use **RFC 6902 JSON Patch** with `Content-Type: application/json-patch+json` only when granular array/operation semantics are required. Document the chosen RFC explicitly in `api-conventions.md`.
- Use `PUT` only for full replacement with clear semantics.
- Avoid hard delete unless retention and audit requirements allow it.

## Async and long-running operations

Use async behavior when operations are expensive, integration-heavy, or not guaranteed to finish inside a normal request timeout.

Define:

- accepted response shape,
- operation resource or status endpoint,
- retry behavior,
- idempotency,
- timeout expectations,
- partial failure behavior.

## Pagination, filtering, and sorting

Use cursor pagination by default:

```http
GET /orders?cursor=abc123&limit=50
```

```json
{
  "items": [],
  "nextCursor": "xyz456"
}
```

Rules:

- reject offset pagination unless explicitly justified,
- enforce bounded `limit`,
- use stable cursors,
- define deterministic ordering,
- avoid unbounded list responses,
- document filter and sort fields explicitly,
- avoid arbitrary filter explosion.

## Idempotency and retries

Every unsafe operation must define:

- whether `Idempotency-Key` is required,
- key format,
- TTL,
- duplicate request behavior,
- replay behavior,
- mutation guarantees,
- retry-safe status codes,
- failure semantics.

Recommended default:

```http
Idempotency-Key: <uuid>
```

Use a 24-hour TTL unless the business workflow requires a different window.

## Error contract

Use one shared error envelope:

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Order not found",
    "traceId": "abc123",
    "details": []
  }
}
```

Rules:

- stable machine-readable codes,
- client-safe messages,
- trace correlation,
- validation detail support,
- consistent structure everywhere,
- relevant 4xx and 5xx responses for every endpoint.

Reject raw framework exceptions, inconsistent validation payloads, and persistence-layer leakage.

## Standard error codes

Use this canonical set as the default registry. Add domain-specific codes only when the standard set does not express the failure clearly.

| Code | HTTP status | Meaning |
|---|---:|---|
| `VALIDATION_FAILED` | 400 | Request body or parameters failed schema validation. Include per-field detail in `details`. |
| `UNAUTHENTICATED` | 401 | Missing, malformed, or expired credentials. |
| `FORBIDDEN` | 403 | Authenticated principal lacks permission for the operation or resource. |
| `RESOURCE_NOT_FOUND` | 404 | Resource does not exist, or principal is not allowed to know it exists. |
| `METHOD_NOT_ALLOWED` | 405 | HTTP method is not supported on this resource. |
| `CONFLICT` | 409 | Request conflicts with current resource state (e.g., illegal state transition, version mismatch). |
| `IDEMPOTENCY_CONFLICT` | 409 | Same `Idempotency-Key` reused with a different request body. |
| `PAYLOAD_TOO_LARGE` | 413 | Request body exceeds the documented size limit. |
| `RATE_LIMITED` | 429 | Caller exceeded the rate limit. Response MUST include `Retry-After`. |
| `INTERNAL` | 500 | Unhandled server error. `traceId` is required for correlation. |
| `UPSTREAM_UNAVAILABLE` | 502 / 503 | A required dependency is down or timed out. |

Domain-specific codes follow `SCREAMING_SNAKE_CASE`, are stable across versions, and are listed in `api-conventions.md`'s error code registry.

## Rate limiting

For any endpoint subject to a rate limit, the response contract MUST include:

- Standard headers on every response (success or failure):
  - `X-RateLimit-Limit` — requests permitted in the current window.
  - `X-RateLimit-Remaining` — requests remaining in the current window.
  - `X-RateLimit-Reset` — Unix timestamp (seconds) when the window resets.
- `429 Too Many Requests` response with the `RATE_LIMITED` error code and a `Retry-After` header (seconds or HTTP-date).

Document the windowing strategy (fixed, sliding, token bucket) in `api-conventions.md`.
