---
name: backend-architecture
description: Use when an approved system design exists and the team needs backend service architecture before implementation. Produces backend boundaries, domain models, API and async contract decisions, transactional boundaries, idempotency and retry strategy, security touchpoints, operational concerns, and implementation handoff notes. Do not use for framework scaffolding, database schema implementation, UI architecture, or production deployment manifests.
---

# Backend Architecture

## When to use

Invoke after `system-design` has produced an approved system design and before implementation-specific skills generate code, schemas, tests, or deployment assets.

Use this skill to turn high-level system architecture into backend implementation direction: service responsibilities, domain boundaries, interface contracts, execution flows, consistency rules, security touchpoints, and operational expectations.

Do not use for framework scaffolding, database-specific schema design, frontend state/rendering architecture, Kubernetes manifests, CI/CD pipelines, or broad system topology decisions that still belong in `system-design`.

## Inputs

Required:

- Approved `system-design.md`.
- Relevant ADRs from the system design.
- Target backend component, service, bounded context, or module.
- Primary consumers and upstream/downstream dependencies.

Optional:

- Approved PRD sections for scope, non-goals, success metrics, and acceptance criteria.
- Existing API contracts, event contracts, domain models, or service code.
- Runtime constraints such as latency, throughput, cost, SLOs, deployment topology, or data residency.
- Security and compliance requirements.
- Implementation ecosystem preference, such as Spring Boot, Node.js, Go, Django, FastAPI, or .NET.

## Operating rules

- Preserve the system design. Do not silently change service boundaries, architecture style, consistency model, or deployment assumptions. If a backend concern reveals a system-design gap, raise it as an ADR candidate or open decision.
- Architect behavior before technology. Define responsibilities, contracts, transactions, workflows, and failure handling before naming frameworks or libraries.
- Keep domain concepts separate from persistence models, DTOs, queues, and framework classes.
- Design explicit boundaries: what the backend owns, what it consumes, what it emits, what it refuses to own, and which invariants it protects.
- Prefer boring, observable execution paths. Make retries, idempotency, timeouts, compensations, and partial failures explicit.
- Treat API contracts, event contracts, and background jobs as first-class architecture outputs. REST is common, not assumed.
- Ask for confirmation with recommended defaults when a decision changes service behavior, consistency, security exposure, or implementation scope. Use: "I recommend X because Y. Confirm or redirect."
- If REST contracts are in scope, use `assets/openapi-starter.template.yaml` and `assets/api-conventions.template.md`; lint the generated OpenAPI spec when tooling is available.

## Output contract

`backend-architecture.md` MUST describe the backend design clearly enough for implementation skills to proceed without inventing service behavior.

It MUST include:

- Backend scope and ownership boundary.
- Domain model, aggregates, commands, queries, and lifecycle states.
- Interface strategy: REST, GraphQL, gRPC, events, jobs, webhooks, or internal module APIs.
- Transactional boundaries and consistency model.
- Idempotency, retry, timeout, and concurrency strategy.
- Authorization and trust-boundary touchpoints.
- Failure modes, observability signals, and operational concerns.
- Handoff notes for implementation, data, testing, security, and reliability skills.

When REST is part of the interface strategy, `openapi.yaml` and `api-conventions.md` MUST conform to [standards/api-standards](../../../standards/api-standards/README.md). Security decisions MUST conform to [security-standards](../../../standards/security-standards/README.md). Naming for paths, identifiers, and event topics MUST conform to [naming-conventions](../../../standards/naming-conventions/README.md).

Use `assets/backend-architecture.template.md` for the main architecture handoff. Use the OpenAPI and API convention templates only when producing REST contract artifacts.

## Progressive references

- Read `references/backend-architecture-quality-rubric.md` before finalizing.
- Read `references/domain-modeling-and-boundaries.md` when translating system components into backend-owned domain concepts, aggregates, commands, queries, and lifecycle states.
- Read `references/transactions-consistency-and-workflows.md` when defining transactional boundaries, consistency, async workflows, retries, and compensations.
- Read `references/api-discovery-and-resource-modeling.md` when REST or resource-oriented contracts are in scope.
- Read `references/http-semantics-and-operational-rules.md` when generating REST method semantics, idempotency behavior, pagination, filtering, sorting, async HTTP operations, and errors.
- Read `references/security-versioning-and-validation.md` when defining auth schemes, authorization scopes, tenant boundaries, rate limits, versioning, compatibility, deprecation, validation rules, and examples.
- Read `references/contract-deliverables.md` when generating `openapi.yaml`, `api-conventions.md`, optional webhook/API artifacts, and no-placeholder contract output.

## Process

Progress:

- [ ] Step 1: Load the approved `system-design.md`, relevant ADRs, and any PRD sections that define scope, non-goals, users, success metrics, and acceptance criteria.
- [ ] Step 2: Identify the target backend boundary: service, module, bounded context, or component. Record owned responsibilities, explicitly excluded responsibilities, upstream dependencies, downstream consumers, and open system-design questions.
- [ ] Step 3: Model backend domain behavior: core entities, aggregates, commands, queries, lifecycle states, invariants, business rules, and decision points. Reject database-shaped or DTO-shaped domain models.
- [ ] Step 4: Define interface strategy. Choose which interactions are REST, GraphQL, gRPC, events, background jobs, webhooks, or internal module calls. Explain why each interface style fits the consumer, latency, coupling, and evolution needs.
- [ ] Step 5: Define synchronous request flows and asynchronous execution flows. Include sequence diagrams or numbered flow narratives for non-obvious paths.
- [ ] Step 6: Define transactional boundaries, consistency model, concurrency controls, idempotency rules, retry behavior, timeout budgets, duplicate handling, and compensation strategy.
- [ ] Step 7: Define data ownership expectations without implementing schema details: owned data, read models, external records of truth, retention needs, migration implications, and handoff notes for data implementation skills.
- [ ] Step 8: Define security touchpoints: authentication assumptions, authorization checks, tenant isolation, service-to-service trust, sensitive data handling, rate limits, and audit events.
- [ ] Step 9: Define operational concerns: logs, metrics, traces, health/readiness signals, SLO-sensitive paths, failure modes, alert-worthy symptoms, runbook hooks, and backpressure behavior.
- [ ] Step 10: Generate `backend-architecture.md` from `assets/backend-architecture.template.md`. Include clear implementation handoff notes for backend scaffold, database schema, security review, integration testing, observability, and deployment skills.
- [ ] Step 11: If REST contracts are required, generate or update `openapi.yaml` and `api-conventions.md` using the provided assets. Verify cross-file consistency and lint the spec with `npx @stoplight/spectral-cli lint openapi.yaml` or `npx @redocly/cli lint openapi.yaml` when available. If tooling is unavailable, document the skipped validation under deferred decisions.
- [ ] Step 12: Validate the result against `references/backend-architecture-quality-rubric.md`. If REST artifacts were produced, also validate them against [standards/api-standards](../../../standards/api-standards/README.md) and `references/api-contract-quality-rubric.md`.

## Outputs

Required:

- `backend-architecture.md`.

Optional, when applicable:

- `openapi.yaml` using OpenAPI 3.1.
- `api-conventions.md`.
- Event contract sketches.
- Background job definitions.
- Sequence diagrams or flow narratives.
- State transition tables.
- Implementation handoff checklist.

Output rules:

- The backend architecture must be implementation-ready, not placeholder-heavy.
- Every backend responsibility must map back to the system design or be marked as an open decision.
- Every externally visible behavior must identify its consumer, auth expectation, failure behavior, and compatibility expectation.
- Every unsafe operation or async workflow must define idempotency and retry behavior.
- Do not leak persistence schema, ORM classes, framework exceptions, or deployment mechanics into the architecture unless they materially affect behavior.

## Quality checks

- [ ] `references/backend-architecture-quality-rubric.md` was loaded before finalizing.
- [ ] `backend-architecture.md` identifies scope, non-scope, domain model, interfaces, transactions, consistency, security touchpoints, operational concerns, and implementation handoffs.
- [ ] Every interface decision names the consumer, interaction style, ownership boundary, compatibility expectation, and failure behavior.
- [ ] Transaction and consistency decisions are explicit for every state-changing workflow.
- [ ] Idempotency, retries, timeouts, and duplicate handling are explicit for unsafe operations and async workflows.
- [ ] Security touchpoints align with [security-standards](../../../standards/security-standards/README.md).
- [ ] REST artifacts, if produced, validate against [api-standards](../../../standards/api-standards/README.md) and can realistically drive server/client generation.

## References

- `assets/backend-architecture.template.md`
- `assets/api-conventions.template.md`
- `assets/openapi-starter.template.yaml`
- `references/backend-architecture-quality-rubric.md`
- `references/domain-modeling-and-boundaries.md`
- `references/transactions-consistency-and-workflows.md`
- `references/api-discovery-and-resource-modeling.md`
- `references/http-semantics-and-operational-rules.md`
- `references/security-versioning-and-validation.md`
- `references/contract-deliverables.md`
- `references/api-contract-quality-rubric.md`
