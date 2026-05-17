# operations

> Status: draft

## Purpose

Produces operational clarity after incidents and before production ownership transitions: blameless postmortems, reusable runbooks, operational ownership boundaries, escalation paths, mitigation and rollback guidance, and on-call handoff artifacts.

Technology-agnostic. Owns *operational execution and operational learning* — how the team recovers, learns, and sustainably supports production — not the infrastructure or reliability strategy that shapes it.

## Owns

- Blameless postmortem rigor
- Reusable runbook standards (Detection → Verification)
- Incident timeline and root-cause discipline
- Action-item tracking quality
- Escalation paths and operational ownership
- Rollback as a first-class capability
- On-call readiness and handoff

## Produces

| Artifact | Conforms to |
|---|---|
| `postmortems/YYYY-MM-DD-<incident>.md` | [operational-artifacts](../../../standards/operational-artifacts/README.md), [security-standards](../../../standards/security-standards/README.md) (security incidents) |
| `runbooks/<symptom>.md` | [operational-artifacts](../../../standards/operational-artifacts/README.md), [observability-standards](../../../standards/observability-standards/README.md) (alert linkage) |
| `on-call-handoff.md` | [operational-artifacts](../../../standards/operational-artifacts/README.md) |

## Skills

- [operations](SKILL.md) — produces blameless postmortems, reusable runbooks, and operational handoff notes for services entering support.

## Standards this architecture domain conforms to

- [operational-artifacts](../../../standards/operational-artifacts/README.md) — postmortem, runbook, and on-call-handoff structure and linkage.
- [observability-standards](../../../standards/observability-standards/README.md) — every paging alert has a runbook; alerts without runbooks are deleted.
- [deployment-standards](../../../standards/deployment-standards/README.md) — deploy-related postmortems reference the deployment-event metric and rolled-back artifact.
- [security-standards](../../../standards/security-standards/README.md) — security incidents require a mandatory, org-visible postmortem.
- [documentation-standards](../../../standards/documentation-standards/README.md) — skill structure.

## Upstream triggers

Invoked by an event, not by an approved design: a mitigated incident, a recurring alert needing a runbook, or a service entering production support. Evidence (alerts, logs, metrics, deploy records, chat transcripts) is the required input.

## Downstream consumers

- Every [implementations/*](../../implementations/) skill that emits a paging alert requires a runbook authored here.
- [architecture/reliability](../reliability/SKILL.md) — postmortem action items feed resilience and SLO work.
- `workflows/incident-response` (when authored) orchestrates this domain's incident process end-to-end.
