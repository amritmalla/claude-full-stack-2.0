# Domain Modeling and Boundaries

Backend architecture translates system design into behavior owned by a service, module, or bounded context.

## Start With Ownership

Identify:

- the decisions this backend boundary is allowed to make,
- the state it owns,
- the invariants it protects,
- the consumers it serves,
- the dependencies it must not absorb.

Weak boundary signals:

- the service mostly mirrors another system's data,
- every operation is CRUD with no owned policy,
- authorization rules live only in consumers,
- multiple teams can change the same state without coordination,
- failure behavior is "retry until it works" without ownership.

## Model Behavior Before Data

Use these terms consistently:

- Concept: business thing the backend must reason about.
- Aggregate: consistency boundary for related state and invariants.
- Command: intent to change state.
- Query: request to read state.
- Event: fact that something happened.
- Policy: rule that decides whether a command is allowed.

Avoid:

- tables as aggregates,
- DTOs as domain models,
- enum states without transition rules,
- one service per noun when the behavior is tightly coupled.

## Boundary Output

For each backend boundary, document:

- owned concepts,
- commands and queries,
- lifecycle states,
- invariants,
- external dependencies,
- integration events or APIs,
- assumptions inherited from system design.
