# system-design

> Status: draft

## Purpose

Designs scalable system architecture and technical topology from an approved PRD. Defines the architectural envelope that downstream implementation domains fill in.

Technology-agnostic. Owns *shape* and *boundaries*, not vendor or framework choices (those land in `implementations/`).

## Owns

- Service boundaries
- Architecture patterns
- Distributed-systems decisions
- Scalability strategy
- Data flow topology
- Consistency models
- ADRs

## Produces

| Artifact | Conforms to |
|---|---|
| `system-design.md` | [architecture-schema](../../standards/architecture-schema/README.md) |
| `adrs/NNNN-<slug>.md` | [architecture-schema](../../standards/architecture-schema/README.md) |
| Optional `components/<name>.md` | [architecture-schema](../../standards/architecture-schema/README.md) |

## Skills

- [system-design-from-prd](system-design-from-prd/SKILL.md) — turns an approved PRD into a system design and inline ADRs.

## Standards this architecture domain conforms to

- [architecture-schema](../../standards/architecture-schema/README.md) — output contract.
- [security-standards](../../standards/security-standards/README.md) — informs Security and Compliance section.
- [observability-standards](../../standards/observability-standards/README.md) and [deployment-standards](../../standards/deployment-standards/README.md) — inform Operational Considerations section.
- [documentation-standards](../../standards/documentation-standards/README.md) — skill structure.

## Upstream inputs

Requires a PRD with `status: approved` per [prd-schema](../../standards/prd-schema/README.md). Do not invoke if PRD is `draft` or `review`.

## Downstream consumers

An approved `system-design.md` is the sole upstream input to scaffolding skills in:

- [implementations/backend/*](../../implementations/backend/)
- [implementations/frontend/*](../../implementations/frontend/)
- [implementations/data/*](../../implementations/data/)
- [implementations/infrastructure/*](../../implementations/infrastructure/)
- [architecture/backend-systems](../backend-systems/README.md) (API contracts)
- [architecture/data-systems](../data-systems/README.md) (schemas and migrations)
