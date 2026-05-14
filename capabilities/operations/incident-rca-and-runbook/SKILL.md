---
name: incident-rca-and-runbook
description: Use when an incident has occurred and a postmortem is required, or
  when a recurring alert needs a reusable runbook. Produces a blameless
  postmortem with factual timeline, root cause distinct from trigger, and
  five-whys; plus a runbook with detection criteria, diagnostics, mitigation,
  and rollback for the alert's symptom.
---

# Incident RCA and Runbook

## When to use

Invoke immediately after an incident is mitigated, or when an alert that has fired ≥ 2 times in 90 days has no runbook. Do not invoke for unconfirmed user reports — gather facts first.

## Inputs

- Incident description: when it started, when it was detected, when it was mitigated, who responded.
- Timeline raw material: chat transcript, alert log, metrics screenshots, deploy log.
- (For runbook) the alert name and a description of the symptom.

## Output contract

Postmortems and runbooks MUST conform to:

- [observability-standards](../../../standards/observability-standards/README.md) — runbooks are referenced by name from alerts; every paging alert MUST have a runbook authored here, or the alert is deleted.
- [security-standards](../../../standards/security-standards/README.md) — security incidents follow the security-standards incident clauses; postmortem is mandatory and public-to-org.
- [deployment-standards](../../../standards/deployment-standards/README.md) — postmortems for deploy-related incidents reference the deployment-event metric and the rolled-back artifact.

Postmortems are blameless. Findings name systems, not individuals.

## Process

1. Build a factual timeline. Each event has a UTC timestamp, an actor (system or person), and a source (log file, dashboard, chat link). Mark times of: detection, page, mitigation start, mitigation end.
2. State the **trigger** in one sentence — the event that directly caused the incident.
3. State the **root cause** in one sentence — the underlying condition that allowed the trigger to cause harm. Trigger and root cause must be distinct.
4. Apply five-whys from the root cause; stop when an answer is actionable.
5. List **contributing factors** that worsened the impact (alert was wrong, runbook was missing, dashboard was broken).
6. Write the postmortem in blameless format: describe systems and processes, not individuals.
7. Define action items, each with an owner, a due date (ISO 8601), and a tracking link.
8. Extract a reusable runbook for the alert/symptom: detection criteria, diagnostic commands, mitigation steps in order, and rollback. Link from the postmortem.
9. Emit `postmortem.md` and `runbooks/<symptom>.md`.

## Outputs

- `postmortem.md`.
- `runbooks/<symptom>.md`.

## Quality checks

- [ ] Every timeline event has a UTC timestamp and a source.
- [ ] Trigger and root cause are distinct one-sentence statements.
- [ ] Postmortem is blameless: no individual is named as a cause.
- [ ] Every action item has an owner and an ISO 8601 due date.
- [ ] Runbook lists detection, diagnostics, mitigation, and rollback in that order.

## References

(None in v0.1.)
