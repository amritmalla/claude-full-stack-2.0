# Domain and Access Modeling

Use this reference to discover the data model before writing DDL.

## Domain discovery

Gather:

- entities,
- relationships,
- ownership rules,
- lifecycle and state transitions,
- query patterns,
- write frequency,
- reporting needs,
- retention expectations,
- scale assumptions,
- hot paths,
- lookup patterns,
- pagination requirements,
- transactional boundaries.

If a system design exists, use bounded contexts to determine table ownership. No table should receive writes from outside its owning context.

## Bounded context data ownership

Rules:

- Each bounded context owns its tables.
- Cross-context data access happens through APIs, events, read models, or explicit interfaces.
- A single PostgreSQL database can host multiple schemas when bounded contexts share deployment but not data ownership.
- If bounded contexts are in separate deployables, use separate databases or isolated schemas with no cross-schema FK dependencies.
- Cross-database references are by ID only, never by FK.

When no system design exists, default to a single database with logical schema boundaries unless requirements justify separation.

## Identity and primary keys

Choose intentionally:

- `bigserial` or identity `BIGINT`: good for internal high-write systems, compact indexes, and local debugging.
- UUID: good for externally visible IDs, distributed generation, and low coordination.
- ULID/KSUID-style IDs: useful when external IDs need approximate ordering.
- Composite natural keys: rare; justify explicitly.

Sequence safety:

- Use `BIGINT`, not `INTEGER`.
- Sequences can gap on rollback; never rely on gapless IDs.
- Tune sequence cache only when insert rate justifies it.
- For logical replication or active-active patterns, plan collision avoidance.

Call out tradeoffs: index bloat, random write amplification, debugging ergonomics, shardability, and public ID exposure.

## Tenant model

Decide early:

- database-per-tenant,
- schema-per-tenant,
- shared tables with `tenant_id`,
- shared tables with row-level security.

Document scaling limits, operational cost, backup/restore implications, tenant isolation strength, and query/index implications.

## Relationship modeling

Rules:

- every relationship gets explicit FK consideration,
- every FK column gets indexed unless covered by a suitable unique/composite index,
- nullable FKs require inline justification,
- many-to-many tables need ownership clarity and often represent real domain entities,
- polymorphic relationships require explicit justification and constraints.

Challenge soft relationships, missing integrity rules, ambiguous ownership, and tables that mix multiple aggregate boundaries.
