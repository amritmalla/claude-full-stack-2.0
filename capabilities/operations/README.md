# operations

> Status: draft

## Purpose

Standardizes engineering execution and organizational delivery: workflows, governance, release management, sprint execution, incident response, documentation standards.

Technology-agnostic. Owns *how the team operates*, not the tooling.

## Owns

- Team workflows and rituals
- Technical leadership patterns
- Delivery coordination
- Release governance
- Incident response process
- Runbook standards
- Postmortem rigor

## Produces

| Artifact | Conforms to |
|---|---|
| Incident postmortems | TBD |
| Runbooks | references alerts in [observability-standards](../../standards/observability-standards/README.md) |
| Release governance docs | references [deployment-standards](../../standards/deployment-standards/README.md) |
| Operational playbooks | — |

## Skills

- [incident-rca-and-runbook](incident-rca-and-runbook/SKILL.md) — produces blameless postmortems with root cause analysis and reusable runbooks for recurring alerts.

## Standards this capability conforms to

- [observability-standards](../../standards/observability-standards/README.md) — every alert has a runbook; runbooks live where this capability says they live.
- [deployment-standards](../../standards/deployment-standards/README.md) — release governance and rollback expectations.
- [documentation-standards](../../standards/documentation-standards/README.md) — skill structure.

## Downstream consumers

- All implementation skills generate alerts that require runbooks defined here.
- [workflows/incident-response](../../workflows/) (when authored) orchestrates this capability's incident process end-to-end.
