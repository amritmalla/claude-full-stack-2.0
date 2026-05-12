# API Contract Quality Rubric

Load this before finalizing. Revise until each check passes or explicitly document the unresolved gap.

## Required checks

- [ ] Every endpoint defines success and error responses.
- [ ] Every error response references the shared error schema.
- [ ] Error codes are stable and machine-readable.
- [ ] Pagination is cursor-based on all collection endpoints unless offset pagination is explicitly justified.
- [ ] No endpoint exposes unbounded collections.
- [ ] Filtering and sorting rules are documented and bounded.
- [ ] Unsafe operations define idempotency semantics.
- [ ] `Idempotency-Key` is documented where required.
- [ ] Validation rules are explicit for all fields.
- [ ] Nullability is unambiguous.
- [ ] Versioning strategy is globally consistent.
- [ ] Compatibility, deprecation, and breaking-change policy are documented.
- [ ] Security schemes are documented in OpenAPI.
- [ ] Authorization or scope expectations are documented per protected operation.
- [ ] Example payloads are realistic and valid.
- [ ] Resource naming is consistent throughout.
- [ ] No endpoint leaks database or framework implementation details.
- [ ] PATCH, PUT, and delete semantics are explicit.
- [ ] Long-running or async operations define status and retry behavior.
- [ ] The contract could realistically generate server and client code safely.
- [ ] The contract supports long-term API evolution.
- [ ] Every operation declares an explicit `operationId` in camelCase, globally unique.
- [ ] Every operation has at least one tag, and tags follow plural resource names.
- [ ] PATCH semantics are explicit (RFC 7396 or RFC 6902) and documented in `api-conventions.md`.
- [ ] Error codes used in the spec are listed in the conventions error code registry, and the registry references the standard set unless a domain code is justified.
- [ ] Endpoints subject to rate limits include `X-RateLimit-*` headers and a documented `429` response with `Retry-After`.
- [ ] OpenAPI lint (`spectral` or `redocly`) was run and passed, **or** the skip is documented under deferred decisions in `api-conventions.md`.

## Failure handling

If a check fails:

1. Identify the missing convention, endpoint behavior, schema rule, or unresolved decision.
2. Fix it if the expected behavior is clear.
3. Ask the user for confirmation when the decision changes public compatibility, security, idempotency, or lifecycle semantics.
4. Document intentionally deferred decisions in `api-conventions.md`.
