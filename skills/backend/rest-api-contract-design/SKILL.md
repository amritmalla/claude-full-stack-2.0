---
name: rest-api-contract-design
description: Use when designing, reviewing, or standardizing a REST API contract before implementation begins. Produces a production-grade OpenAPI 3.1 specification with resource modeling, standardized errors, cursor pagination, idempotency semantics, validation rules, security expectations, versioning conventions, and API convention documentation. Do not use for GraphQL, gRPC, event schema design, database schema design, or internal method signatures. Pairs with spring-boot-service-scaffold (controllers), postgres-schema-and-migration (persistence), spring-security-auth-review (auth hardening), and integration-test-strategy (contract-driven tests).
---

# REST API Contract Design

## When to use

Invoke when designing a new REST API, reviewing an existing REST contract for consistency, defining contracts before implementation, standardizing API conventions, or preparing APIs for external consumers.

Do not use for GraphQL APIs, gRPC/RPC contracts, event schema design, frontend-only data modeling, database schema design, or internal method signatures.

## Inputs

Required:

- Service or domain purpose.
- Approved system boundary or architecture direction.
- Primary API consumers.

Optional:

- Existing domain model or state machine.
- Existing OpenAPI spec.
- Public vs internal exposure.
- Auth and authorization expectations.
- Compatibility, versioning, or deprecation constraints.
- Operational constraints such as rate limits, retries, long-running workflows, or SLOs.

## Operating rules

- Design contract-first. The API contract drives controllers, DTO boundaries, integration tests, and client generation.
- Model capabilities, not databases. Resources represent business concepts, workflows, and lifecycle states, not tables or ORM entities.
- Favor uniform conventions: naming, pagination, response shapes, idempotency, error semantics, validation, and versioning.
- Design for evolution: backward-compatible additive changes, explicit deprecation, and clear breaking-change policy.
- Challenge RPC disguised as REST, entity leakage, chatty APIs, giant payloads, deep nesting, database-shaped endpoints, and ambiguous PATCH semantics.
- Ask for confirmation with recommended defaults when a decision changes the contract. Use: "I recommend X because Y. Confirm or redirect."
- Confirm the target path for the spec before writing. Recommend `<service-root>/api/openapi.yaml` co-located with the service, or `contracts/<service>/openapi.yaml` in a contracts monorepo.
- Take a position on PATCH semantics. Default to RFC 7396 JSON Merge Patch (`Content-Type: application/merge-patch+json`). Use RFC 6902 JSON Patch only when granular array/operation semantics are required. Document the choice in `api-conventions.md`.
- A spec that does not lint is not done. Run `npx @stoplight/spectral-cli lint openapi.yaml` (or `npx @redocly/cli lint openapi.yaml`) before declaring completion. If neither tool is available, document the skipped validation in `api-conventions.md` under deferred decisions.

## Progressive references

- Read `references/api-discovery-and-resource-modeling.md` when gathering API context, modeling resources, relationships, ownership boundaries, and state transitions.
- Read `references/http-semantics-and-operational-rules.md` when defining methods, create/update/delete behavior, pagination, filtering, sorting, idempotency, retries, async behavior, and errors.
- Read `references/security-versioning-and-validation.md` when defining auth schemes, authorization scopes, tenant boundaries, rate limits, versioning, compatibility, deprecation, field validation, and examples.
- Read `references/contract-deliverables.md` when generating `openapi.yaml`, `api-conventions.md`, optional artifacts, and no-placeholder output.
- Read `references/api-contract-quality-rubric.md` before finalizing and use it as the validation checklist.
- Use `assets/api-conventions.template.md` for `api-conventions.md`.
- Use `assets/openapi-starter.template.yaml` as the starter structure for `openapi.yaml`.
- The canonical worked example for this skill lives at `examples/spring-boot/orders-api/.skill-outputs/rest-api-contract-design/` in the plugin repo. Consult it for cross-file conventions before generating.

## Process

Progress:

- [ ] Step 1: Gather API context and scope: service purpose, primary consumers, public/internal exposure, auth expectations, implementation stack, compatibility expectations, operational constraints, and **target path for the spec file** (default `<service-root>/api/openapi.yaml`).
- [ ] Step 2: Model resources and relationships using business nouns, ownership boundaries, and lifecycle state transitions. Reject database-shaped APIs and fake REST semantics.
- [ ] Step 3: Define API semantics: create/update/delete behavior, PATCH vs PUT, immutable fields, optimistic concurrency, synchronous vs async processing, long-running operations, and retry expectations.
- [ ] Step 4: Standardize pagination, filtering, sorting, and search. Use cursor pagination by default, bounded limits, stable cursors, and deterministic ordering.
- [ ] Step 5: Define idempotency and retry semantics for every unsafe operation, including `Idempotency-Key`, key TTL, duplicate request behavior, replay guarantees, and failure semantics.
- [ ] Step 6: Define one shared error envelope with stable codes, client-safe messages, trace correlation, validation details, and consistent 4xx/5xx behavior.
- [ ] Step 7: Define security and exposure rules: auth scheme, authorization scopes, tenant isolation, rate limiting, and public exposure expectations.
- [ ] Step 8: Choose versioning strategy and document compatibility, deprecation, and breaking-change policy.
- [ ] Step 9: Define validation rules and realistic examples for all request and response schemas.
- [ ] Step 10: Generate `openapi.yaml` and `api-conventions.md`; include optional artifacts only when they match the API's complexity. Verify cross-file consistency: every operation referenced in `api-conventions.md` exists in `openapi.yaml`; every error code in the conventions registry is used by at least one operation; every reusable schema is `$ref`'d, not inlined and duplicated.
- [ ] Step 11: **Spec lint (mandatory).** Run `npx @stoplight/spectral-cli lint openapi.yaml` with the `spectral:oas` ruleset, or fall back to `npx @redocly/cli lint openapi.yaml`. Fix all errors and re-run. If neither tool is available, document the skipped validation in `api-conventions.md` under deferred decisions — do not silently skip.
- [ ] Step 12: Validate the contract against `references/api-contract-quality-rubric.md`. Revise until checks pass or explicitly document any unresolved gap.

## Outputs

- `openapi.yaml` using OpenAPI 3.1.
- `api-conventions.md` covering resource naming, pagination, idempotency, errors, versioning, deprecation, and auth model.

Optional outputs when appropriate:

- Sequence diagrams for non-obvious flows.
- State transition tables for lifecycle resources.
- Webhook contracts.
- SDK generation guidance.
- Async workflow conventions.

Output rules:

- Generated contracts must be implementation-ready, not placeholder-heavy.
- Every endpoint must define success and error responses.
- Every reusable convention must be documented once and applied consistently.
- Examples must be realistic and valid.
- Avoid leaking persistence models or framework errors into the transport contract.

## Quality checks

- [ ] `references/api-contract-quality-rubric.md` was loaded before finalizing.
- [ ] `openapi.yaml` follows `assets/openapi-starter.template.yaml`.
- [ ] `api-conventions.md` follows `assets/api-conventions.template.md`.
- [ ] Every unsafe operation defines idempotency semantics.
- [ ] The contract could realistically generate server and client code safely.

## References

- `references/api-discovery-and-resource-modeling.md`
- `references/http-semantics-and-operational-rules.md`
- `references/security-versioning-and-validation.md`
- `references/contract-deliverables.md`
- `references/api-contract-quality-rubric.md`
- `assets/api-conventions.template.md`
- `assets/openapi-starter.template.yaml`
