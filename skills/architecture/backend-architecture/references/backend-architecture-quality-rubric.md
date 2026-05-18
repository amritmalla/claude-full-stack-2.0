# Backend Architecture Quality Rubric

Use this before finalizing `backend-architecture.md`.

## Boundary Quality

- [ ] The backend scope is specific enough that implementation skills do not invent responsibilities.
- [ ] Non-scope is explicit, especially for adjacent services, frontend behavior, data ownership, and platform concerns.
- [ ] Every responsibility traces to the approved system design or is marked as an open decision.

## Domain Quality

- [ ] Domain concepts are business concepts, not database tables, DTOs, framework classes, or transport schemas.
- [ ] Aggregates, commands, queries, lifecycle states, and invariants are named where the backend owns meaningful behavior.
- [ ] State transitions reject impossible or unsafe transitions.

## Interface Quality

- [ ] Every interface names its consumer, ownership boundary, compatibility expectation, and failure behavior.
- [ ] REST, events, jobs, webhooks, GraphQL, gRPC, or internal calls are chosen based on coupling, latency, evolution, and operational needs.
- [ ] Public or cross-team contracts have enough detail for implementation and testing.

## Execution Quality

- [ ] State-changing workflows define transaction boundaries and consistency expectations.
- [ ] Async workflows define retries, deduplication, ordering assumptions, backpressure, and compensation where needed.
- [ ] Unsafe operations define idempotency behavior.
- [ ] Timeouts and partial failures are handled explicitly.

## Handoff Quality

- [ ] Backend scaffold, data, security, testing, observability, and deployment handoffs are concrete.
- [ ] Implementation notes avoid prescribing frameworks unless the ecosystem is already chosen.
- [ ] Open decisions have owners or escalation paths.
- [ ] Any diagram present is prose-consistent: no node references an element absent from this document; if this domain's primary topology diagram (per its authoring skill's Outputs) is omitted, the omission is stated with a rationale.
