# Operations Quality Rubric

Load this before emitting any operational artifact. Revise until each check passes or the unresolved gap is explicitly documented.

## Evidence and timeline

- [ ] Analysis is backed by evidence; no speculative incident analysis.
- [ ] Every timeline event has a UTC timestamp, actor, event, and evidence source.
- [ ] Timeline marks detection, page, mitigation start/end, rollback, recovery verification, and customer-impact windows.
- [ ] No reconstructed or relative-time narrative without evidence references.

## Root cause analysis

- [ ] Trigger is one sentence; root cause is one sentence; they are distinct.
- [ ] Root cause is systemic and actionable; it is not "human error".
- [ ] Five-whys stops at an actionable, systemic conclusion — neither shallow nor an infinite chain.
- [ ] Contributing factors are listed and separated from the root cause and trigger.

## Postmortem quality

- [ ] Postmortem is fully blameless: no individual named as a cause.
- [ ] Summary, impact, timeline, trigger, root cause, contributing factors, mitigation, and lessons learned are present.
- [ ] Impact is quantified (duration, scope, error budget), not "some users".
- [ ] Tone is factual and improvement-oriented; no defensive or blame language.
- [ ] No "TBD" remains in a `final` postmortem.

## Action items

- [ ] Every action item has title, owner, severity, ISO 8601 due date, tracking reference, and expected operational improvement.
- [ ] Items reduce recurrence, blast radius, detection time, mitigation speed, or operational clarity.
- [ ] No "be more careful" remediation; no non-trackable items.

## Runbooks

- [ ] Each runbook contains Detection, Diagnostics, Mitigation, Escalation, Rollback, Verification — in that exact order.
- [ ] Diagnostics and mitigation include concrete commands, dashboards, and metrics; no tribal knowledge required.
- [ ] Mitigation states required privileges and escalation guidance.
- [ ] Every paging alert references a runbook authored to this structure.

## On-call readiness

- [ ] Handoff names service owner, secondary owner, support hours, and paging expectations.
- [ ] Escalation path is explicit with business-impact thresholds and escalation SLAs.
- [ ] Dashboards inventory shows customer impact; alert inventory maps each alert to a responder action.
- [ ] Rollback mechanism, trigger, owner, and verification are documented; no unsupported after-hours systems.

## Linkage and conformance

- [ ] Artifacts conform to [operational-artifacts](../../../../standards/operational-artifacts/README.md): file layout, frontmatter, required sections, ordering, immutability.
- [ ] Security incidents produced a `final` postmortem per security-standards.
- [ ] Deploy-related postmortems reference the deployment-event metric and rolled-back artifact.
- [ ] At least one weak operational practice was surfaced, or the operational health of the system was explicitly affirmed.

## Failure handling

If a check fails:

1. Identify the missing or weak operational decision.
2. Ask the incident owner for clarification if it cannot be inferred from evidence.
3. Revise the postmortem, runbook, or handoff.
4. Keep unresolved questions explicit as tracked action items; do not hide them as assumptions.
