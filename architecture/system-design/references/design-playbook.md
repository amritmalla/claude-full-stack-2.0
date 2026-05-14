# Design Playbook

Use this playbook to turn an approved PRD into logical system structure. Keep the design tied to product constraints and avoid deployment decisions until the logical boundaries are clear.

## Restate system goals

Extract from the PRD:

- core workflows,
- primary actors,
- business constraints,
- reliability or latency expectations,
- compliance or security needs,
- success metrics,
- and non-goals.

Identify what the system must optimize for and what it intentionally does not optimize for. Stop and ask for clarification if the PRD lacks a specific user, core workflow, non-goals, constraints, or success metrics.

## Bounded contexts

For each bounded context, define:

- Name,
- Responsibility,
- Owned data,
- External dependencies,
- Upstream interactions,
- Downstream interactions.

Use domain language. Good names include Identity and Access, Billing, Notification Delivery, Workflow Execution, Reporting, Audit Logging, and Payment Reconciliation.

Avoid names like SharedService, Utils, Core, API Service, Database Service, or Queue Worker.

Challenge suspicious decompositions:

- too many contexts for a small v1,
- artificial separation around technical layers,
- contexts with no owned business capability,
- or premature extraction into services.

## Components

For each component, define:

- Responsibility: concise, domain-oriented, and non-overlapping.
- Public interfaces: API, event, job, CLI, webhook, or internal module boundary.
- Dependencies: internal and external.
- Data inputs and outputs.
- Persistence requirements.
- Consistency requirements.
- Scalability expectations.

Name components by responsibility, not technology. Prefer Session Management, Document Processing, Notification Routing, Payment Reconciliation, or Audit Trail over RedisManager, APIWrapper, or DatabaseService.

## Data flow and ownership

Document:

- system entry points,
- request path,
- async boundaries,
- persistence boundaries,
- critical entities,
- source of truth,
- write owner,
- read models or replicated data,
- caching behavior,
- retention requirements,
- and consistency expectations.

Explicitly identify eventual consistency, retry behavior, idempotency requirements, and reconciliation needs.

Challenge shared mutable ownership, hidden coupling, distributed transactions, and unclear source-of-truth decisions.

## Persistence strategy

For each bounded context or major data group, document:

- storage technology,
- why it fits the access pattern,
- write ownership,
- read patterns,
- caching behavior if applicable,
- migration implications,
- and data retention requirements.

Do not choose storage because it is trendy. Tie storage choices to query shape, transaction needs, retention, scale, compliance, or operational simplicity.
