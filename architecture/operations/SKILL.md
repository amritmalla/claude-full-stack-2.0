---
name: operations
description: Use when an incident has occurred, a recurring alert needs a
  reusable runbook, or a service needs an on-call handoff before production.
  Produces a blameless postmortem, reusable runbook, and operational handoff
  notes with owners, escalation paths, diagnostics, mitigation, and rollback.
---

# Operations

## When to use

Invoke immediately after an incident is mitigated, when a recurring alert needs a reusable runbook, or when operational readiness needs a concrete on-call handoff artifact. Do not invoke for unconfirmed user reports; gather facts first.

## Inputs

- Incident description or operational scenario.
- Timeline raw material: chat transcript, alert log, metrics screenshots, deploy log.
- Alert name, symptom, service owner, escalation path, and rollback mechanism.

## Output contract

Postmortems, runbooks, and handoff notes MUST conform to:

- [observability-standards](../../standards/observability-standards/README.md): runbooks are referenced by name from alerts; every paging alert MUST have a runbook authored here, or the alert is deleted.
- [security-standards](../../standards/security-standards/README.md): security incidents follow the security-standards incident clauses; postmortem is mandatory and public-to-org.
- [deployment-standards](../../standards/deployment-standards/README.md): postmortems for deploy-related incidents reference the deployment-event metric and the rolled-back artifact.

Postmortems are blameless. Findings name systems and processes, not individuals.

## Process

1. Build a factual timeline. Each event has a UTC timestamp, an actor (system or person), and a source (log file, dashboard, chat link). Mark detection, page, mitigation start, mitigation end, and customer-impact windows.
2. State the trigger in one sentence: the event that directly caused the incident.
3. State the root cause in one sentence: the underlying condition that allowed the trigger to cause harm. Trigger and root cause must be distinct.
4. Apply five-whys from the root cause; stop when an answer is actionable.
5. List contributing factors that worsened impact, including missing alerts, unclear ownership, unsafe deploys, missing runbooks, or broken dashboards.
6. Write the postmortem in blameless format: describe systems and processes, not individuals.
7. Define action items, each with an owner, a due date (ISO 8601), severity, and a tracking link.
8. Extract a reusable runbook for the alert or symptom: detection criteria, diagnostics, mitigation, escalation, rollback, and verification. Link from the postmortem.
9. Emit `postmortem.md`, `runbooks/<symptom>.md`, and an on-call handoff note when the service is entering support.

## Outputs

- `postmortem.md`.
- `runbooks/<symptom>.md`.
- Optional `on-call-handoff.md`.

## Quality checks

- [ ] Every timeline event has a UTC timestamp and a source.
- [ ] Trigger and root cause are distinct one-sentence statements.
- [ ] Postmortem is blameless: no individual is named as a cause.
- [ ] Every action item has an owner, severity, tracking link, and ISO 8601 due date.
- [ ] Runbook lists detection, diagnostics, mitigation, escalation, rollback, and verification in that order.
- [ ] On-call handoff names service owner, escalation path, dashboards, alerts, and rollback command or procedure when applicable.

## References

(None in v0.1.)
