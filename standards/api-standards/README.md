# api-standards

Normative rules for REST APIs produced by `architecture/backend-architecture` and any `implementations/backend/*` skill. GraphQL and async messaging have their own sections.

## REST conventions

### Resource modeling
- Nouns, plural, `kebab-case`: `/user-profiles`, `/booking-requests`.
- Sub-resources reflect ownership: `/users/{id}/sessions`. Max nesting depth: 2.
- No verbs in paths. Actions use sub-resources: `POST /orders/{id}/cancellations` not `POST /orders/{id}/cancel`.

### HTTP verbs
| Verb | Use | Idempotent |
|---|---|---|
| `GET` | Read | Yes |
| `POST` | Create or non-idempotent action | No |
| `PUT` | Full replace | Yes |
| `PATCH` | Partial update (JSON Merge Patch, RFC 7396) | Yes |
| `DELETE` | Remove | Yes |

`PATCH` MUST appear in API design before `PUT` is added — most updates are partial. Document the merge semantics explicitly.

### Status codes
- `200` success with body; `201` created with `Location` header; `204` success no body.
- `400` validation error; `401` unauthenticated; `403` authenticated but forbidden; `404` not found; `409` conflict; `422` semantically invalid; `429` rate-limited.
- `500` unexpected server error; `503` dependency unavailable. Never return `500` for client-caused failures.

## Versioning

URL-based: `/v1/...`, `/v2/...`. Major version bump only for breaking changes. Two prior majors MUST remain supported for 6 months minimum after deprecation announcement.

Non-breaking additions (new fields, new endpoints, new optional query params) do NOT bump version.

## Pagination

Cursor-based by default:

```json
{
  "data": [...],
  "page": {
    "next_cursor": "opaque-string-or-null",
    "limit": 50
  }
}
```

Offset pagination only for admin / reporting endpoints. Document max page size explicitly; reject larger requests with `400`.

## Error envelope

Every non-2xx response MUST use this shape:

```json
{
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "Human-readable, safe for end users.",
    "details": { "...optional structured context..." },
    "request_id": "uuid-or-trace-id"
  }
}
```

`code` values live in a per-service **error code registry** (see `shared/schemas/error-codes.md` once authored). Codes are `SCREAMING_SNAKE_CASE`, namespaced when ambiguous (`BILLING_CARD_DECLINED`).

## Rate limiting

Every public endpoint declares a rate limit in its OpenAPI spec via `x-rate-limit` extension:

```yaml
x-rate-limit:
  requests: 100
  per: minute
  scope: user | api-key | ip
```

Responses include `RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset` headers (IETF draft).

## OpenAPI

- All REST APIs MUST publish an OpenAPI 3.1 spec.
- Spec location: `<service-root>/api/openapi.yaml` (co-located with the service) **or** `contracts/<service>/openapi.yaml` (centralized contracts repo). Pick one per organization and document the choice in each service's `api-conventions.md`.
- Spec is the source of truth — generate clients and server stubs from it, not the other way around.
- Spec lint (Spectral `spectral:oas` or Redocly CLI) is a required gate before merge. A spec that does not lint is not done.
- Each service additionally publishes an `api-conventions.md` alongside the spec, recording per-service choices (PATCH semantics, error-code registry, auth scopes, deprecation notes) that this standard intentionally leaves to the service.

## Authentication

- Default to OAuth2 / OIDC bearer tokens. API keys allowed only for server-to-server.
- Never accept credentials in query strings.
- See `security-standards` for token rotation and scope rules.

## GraphQL (when used)

- Schema-first; SDL is the contract.
- Single endpoint `/graphql`; persisted queries required in production.
- Pagination follows Relay cursor connection spec.
- Errors use the `errors` array; do not return partial `data` for fatal failures.

## Async / event APIs

- Topic naming per `naming-conventions` (`domain.entity.event`).
- Every event has a schema in `shared/schemas/events/` and a version field.
- Producers MUST guarantee at-least-once delivery; consumers MUST be idempotent.
- See `patterns/event-driven` once authored.

## Anti-patterns

- Verbs in REST paths.
- Returning HTTP 200 with `{"success": false}`.
- Leaking internal error messages or stack traces in `error.message`.
- Breaking change without version bump.
- Cursor pagination implemented as base64-encoded offset (defeats the purpose).
