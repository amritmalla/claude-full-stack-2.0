---
name: rest-api-contract-design
description: Use when designing the REST contract for a new service or reviewing
  an existing one. Produces an OpenAPI 3.1 spec with consistent error model,
  cursor pagination, idempotency for unsafe operations, and an explicit versioning
  strategy.
---

# REST API Contract Design

## When to use

Invoke when starting a new service after architecture is approved, or when reviewing an existing API for consistency. Use before implementation so the contract drives controllers and integration tests. Do not invoke for GraphQL or RPC interfaces.

## Inputs

- Domain model (entities, relationships, state machines).
- Approved PRD or system design for scope.
- (Optional) Existing OpenAPI spec to review.

## Process

1. Identify resources from the domain model. Resources are nouns; verbs map to HTTP methods.
2. For each resource, define endpoints: list, get, create, update, delete, and any state-transition actions (e.g., `POST /orders/{id}/cancel`).
3. Define the error envelope shape ONCE and reference it from every error response: `{ "error": { "code", "message", "traceId", "details": [] } }`.
4. Define pagination: cursor-based, with `cursor` query param and `nextCursor` in response. Reject offset-based pagination.
5. Define idempotency for every non-idempotent endpoint: require an `Idempotency-Key` header; document semantics for retries within the key's TTL.
6. Choose a versioning strategy: URI (`/v1/orders`) or header (`Accept: application/vnd.api.v1+json`). Justify the choice.
7. Document required and optional fields, validation rules, and example payloads inline in the OpenAPI spec.
8. Emit `openapi.yaml` (OpenAPI 3.1) and `api-conventions.md` capturing the versioning, error, pagination, and idempotency rules.

## Outputs

- `openapi.yaml`.
- `api-conventions.md`.

## Quality checks

- [ ] Every endpoint has at least one 4xx response defined.
- [ ] Every error response references the shared error envelope component.
- [ ] Every non-idempotent endpoint accepts an `Idempotency-Key` header and documents its TTL.
- [ ] Pagination is cursor-based; no endpoint uses offset.
- [ ] Versioning strategy is explicit and consistent across all endpoints.

## References

(None in v0.1.)
