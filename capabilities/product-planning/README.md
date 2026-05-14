# product-planning

> Status: draft

## Purpose

Transforms raw ideas into validated, execution-ready product definitions.

Technology-agnostic. This capability owns *what* gets built and *why*, not *how*.

## Owns

- PRDs
- MVP scoping
- Roadmap planning
- Feature decomposition
- User journeys
- Success metrics
- Feasibility analysis

## Produces

| Artifact | Conforms to |
|---|---|
| `PRD.md` | [prd-schema](../../standards/prd-schema/README.md) |
| Roadmap | TBD |
| Feature matrix | TBD |
| Execution phases | TBD |
| Product constraints | embedded in PRD |

## Skills

- [prd-from-idea](prd-from-idea/SKILL.md) — turns an informal idea into a decision-oriented PRD conforming to `prd-schema`.

## Standards this capability conforms to

- [prd-schema](../../standards/prd-schema/README.md) — output contract.
- [documentation-standards](../../standards/documentation-standards/README.md) — skill structure.
- [naming-conventions](../../standards/naming-conventions/README.md) — slugs, file names.

## Downstream consumers

PRDs approved here are the sole upstream input to:

- [capabilities/system-design](../system-design/README.md)
- [capabilities/backend-systems](../backend-systems/README.md)
- [capabilities/frontend-architecture](../frontend-architecture/README.md)
- [capabilities/testing-quality](../testing-quality/README.md)

Downstream skills MUST NOT proceed if the PRD is `draft` or `review`.
