# Contract Deliverables

Use this reference when generating final artifacts.

## `openapi.yaml`

Must include:

- OpenAPI 3.1 declaration,
- `info` block with title, version, and description,
- server definitions per environment when known,
- security schemes in `components/securitySchemes`,
- all resources with full path definitions,
- request bodies with `$ref` schemas where reusable,
- field validation constraints,
- success responses,
- relevant 4xx responses,
- relevant 5xx responses,
- shared error schema,
- cursor pagination parameters and response shape for collection endpoints,
- `Idempotency-Key` header for unsafe operations,
- reusable schemas under `components/schemas`,
- realistic examples for request and response bodies.

## `api-conventions.md`

Must include:

- resource naming rules,
- route shape conventions,
- pagination standard with example,
- filtering and sorting conventions,
- idempotency requirements and TTL,
- error envelope definition,
- error code registry,
- versioning strategy,
- compatibility guarantees,
- deprecation and sunset policy,
- auth model summary.

## Optional artifacts

Include when appropriate:

- sequence diagrams for non-obvious flows,
- state transition tables for lifecycle resources,
- webhook contracts,
- SDK generation guidance,
- async workflow conventions.

## No-placeholder rule

Artifacts must be implementation-ready.

Avoid:

- placeholder schemas,
- TODO comments,
- undocumented endpoints,
- missing error responses,
- examples that do not validate,
- operation descriptions that only repeat the path name.
