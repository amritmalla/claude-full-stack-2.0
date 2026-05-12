# API Discovery and Resource Modeling

Use this reference to gather API context and shape resources before writing OpenAPI.

## API context

Gather:

- service and domain purpose,
- primary consumers,
- public vs internal exposure,
- auth expectations,
- implementation stack,
- operational constraints,
- compatibility expectations,
- lifecycle/state complexity.

Recommended default:

> I recommend designing this as an internal capability API first unless third-party integrations are already required because internal APIs can evolve faster with tighter consumer coordination. Confirm or redirect.

## Resource modeling

Resources are nouns that represent business concepts, workflows, or capabilities. They are not database tables, ORM entities, joins, or implementation classes.

Define:

- core resources,
- ownership boundaries,
- relationships,
- stable identifiers,
- lifecycle state transitions,
- collection vs single-resource behavior.

Good:

```http
POST /orders
GET /orders/{id}
POST /orders/{id}/cancel
```

Bad:

```http
POST /createOrder
GET /order_table_rows
POST /orders/{id}/doCancel
```

## State transitions

Use explicit action sub-resources for meaningful lifecycle transitions when the transition is not a normal field update.

Examples:

- `POST /orders/{id}/cancel`
- `POST /invoices/{id}/void`
- `POST /documents/{id}/submit-review`

Define allowed source states, resulting state, authorization, idempotency, and failure cases.

## Route shape

Use:

- plural nouns,
- lowercase kebab-case,
- shallow hierarchies,
- stable identifiers,
- verbs only through HTTP methods or explicit transition sub-resources.

Avoid:

- deep nesting,
- route names that expose database structure,
- endpoint explosions,
- chatty APIs requiring many round-trips,
- transport objects that mirror internal entities.

## Design critique

Call out:

- RPC disguised as REST,
- entity leakage through transport,
- database-shaped APIs,
- unclear ownership boundaries,
- nested routes that imply ownership that does not exist,
- giant payloads,
- workflows split across too many client calls.
