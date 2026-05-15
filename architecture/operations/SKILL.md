---
name: operations
description: Use when a production incident occurs, a recurring operational issue needs a reusable runbook, or a service requires operational readiness and on-call handoff before production support. Produces blameless postmortems, actionable runbooks, operational ownership boundaries, escalation paths, mitigation procedures, rollback guidance, and operational readiness artifacts. Do not use for speculative incident analysis without evidence, infrastructure or platform architecture, application implementation, security threat modeling, or reliability engineering strategy; use infrastructure-platform, reliability, or the relevant implementation skill instead.
---

# Operations

## When to use

Invoke immediately after an incident is mitigated, when a recurring alert needs a reusable runbook, or when a service is entering production support and operational readiness needs a concrete on-call handoff artifact.

Do not invoke for unconfirmed user reports (gather facts first), infrastructure or platform architecture (use `infrastructure-platform`), system reliability engineering strategy (use `reliability`), application implementation, security threat modeling, or vendor-specific monitoring setup.

## Inputs

Required:

- Incident description or operational scenario, and current mitigation status.
- Timeline raw material: chat transcript, alert log, metrics screenshots, deploy log, audit trail.

Optional:

- Alert name, symptom, service owner, escalation path, and rollback mechanism.
- Severity, impact duration, and customer-impact assessment.
- SLOs, dashboards, and deployment records for the affected services.
- Prior postmortems or runbooks for the same service.

## Operating rules

- Incidents are analyzed blamelessly. Failures emerge from systems, processes, tooling, communication, and incentives. People may trigger failures; systems allow them to become incidents. Reject "human error" as a root cause and never name individuals as causes.
- Trigger and root cause are distinct. The trigger is the event that immediately caused impact; the root cause is the condition that allowed the trigger to cause harm. Reject postmortems where they are identical.
- Operational artifacts must be reusable. Every runbook defines Detection, Diagnostics, Mitigation, Escalation, Rollback, and Verification — in that order. Reject narrative-only runbooks and undocumented recovery assumptions.
- Alerts without actionability are operational debt. Every paging alert maps to a service owner, a runbook, a stated customer impact, and a required responder action. Reject alerts that only say "investigate."
- Timelines are factual and source-backed. Every entry has a UTC timestamp, an actor, an event, and an evidence source. Reject reconstructed timelines without evidence and relative-time narratives.
- Action items must reduce future risk and be trackable: each has an owner, due date (ISO 8601), severity, tracking reference, and a stated operational improvement. Reject "be more careful" remediation.
- Rollback is a first-class capability. Every deployable system defines rollback mechanism, owner, trigger conditions, and verification. Reject "redeploy previous version manually" without procedural clarity.
- Escalation paths are explicit: primary owner, secondary owner, escalation order, and business-impact thresholds. Reject escalation through tribal knowledge.
- Operational readiness is part of delivery. A service is not production-ready without alerts, dashboards, runbooks, ownership, rollback, and documented on-call responsibilities. Reject "we'll operationalize later."
- Challenge weak operational practices directly and concretely: noisy alerts, missing rollback, absent ownership, alert fatigue, dashboard gaps, operational coupling.

## Output contract

Postmortems, runbooks, and handoff notes MUST conform to [standards/operational-artifacts](../../standards/operational-artifacts/README.md), which is authoritative for their file layout, frontmatter, required sections, ordering, immutability, and linkage rules.

They additionally conform to [observability-standards](../../standards/observability-standards/README.md) (every paging alert has a runbook, or the alert is deleted), [security-standards](../../standards/security-standards/README.md) (security incidents require a mandatory, org-visible postmortem), and [deployment-standards](../../standards/deployment-standards/README.md) (deploy-related postmortems reference the deployment-event metric and rolled-back artifact). Skill structure conforms to [documentation-standards](../../standards/documentation-standards/README.md).

Use the `assets/*.template.md` scaffolds; they implement the schema. Postmortems are blameless: findings name systems and processes, not individuals.

## Progressive references

- Read `references/operations-playbook.md` when collecting incident context, building the timeline, separating trigger from root cause, running five-whys, identifying contributing factors, writing the postmortem, defining action items, extracting runbooks, or preparing on-call handoff, and to check the anti-pattern list.
- Read `references/operations-quality-rubric.md` before finalizing and use it as the validation checklist.
- Use `assets/postmortem.template.md`, `assets/runbook.template.md`, and `assets/on-call-handoff.template.md`.

## Process

Progress:

- [ ] Step 1: Collect incident or operational context: description, symptom, affected services, customer impact, mitigation status. Gather evidence (alerts, logs, metrics, traces, deploy records, dashboards, chat transcripts). Refuse analysis without evidence. See `references/operations-playbook.md`.
- [ ] Step 2: Build the incident timeline. Each event has a UTC timestamp, actor, event, and source. Mark first symptom, alert firing, detection, acknowledgment, mitigation start/end, rollback, recovery verification, and customer-impact windows.
- [ ] Step 3: State the trigger in one sentence and the root cause in one sentence. Ensure they are distinct, operationally meaningful, and actionable. Reject generic or blame-focused language.
- [ ] Step 4: Apply five-whys from the root cause. Stop when the result is actionable, systemic, and operationally meaningful. Avoid infinite chains and shallow one-step explanations.
- [ ] Step 5: Identify contributing factors that worsened impact or delayed recovery, kept distinct from the root cause and trigger.
- [ ] Step 6: Write the blameless postmortem: summary, impact, timeline, trigger, root cause, contributing factors, mitigation, lessons learned. Tone is factual, blameless, operational, improvement-oriented.
- [ ] Step 7: Define action items, each with title, owner, severity, due date (ISO 8601), tracking reference, and expected operational improvement. Reject non-trackable items.
- [ ] Step 8: Extract or create reusable runbooks for the alert, symptom, or scenario. Each contains Detection, Diagnostics, Mitigation, Escalation, Rollback, Verification in that order, with commands, dashboards, metrics, dependencies, and escalation triggers. Link from the postmortem.
- [ ] Step 9: When the service is entering support, produce the on-call handoff: ownership model, escalation paths, dashboard inventory, alert inventory, rollback procedure, deployment expectations, and operational caveats.
- [ ] Step 10: Emit `postmortems/YYYY-MM-DD-<incident-slug>.md`, `runbooks/<symptom-slug>.md`, and `on-call-handoff.md` (when applicable) from the templates. Validate against [standards/operational-artifacts](../../standards/operational-artifacts/README.md) and `references/operations-quality-rubric.md`; revise until both pass or explicitly note any unresolved gap.

## Outputs

Required:

- `postmortems/YYYY-MM-DD-<incident-slug>.md` and `runbooks/<symptom-slug>.md` at `docs/operations/<service-or-product-slug>/`, with frontmatter and sections per [standards/operational-artifacts](../../standards/operational-artifacts/README.md).

Optional, when applicable:

- `on-call-handoff.md`.
- Alert inventory, escalation matrix, dashboard inventory, mitigation checklist, rollback procedure reference.

Output rules:

- Keep artifacts factual, blameless, and operationally executable, not narrative storytelling.
- Every paging alert must reference a runbook authored to the six-section structure.
- Every action item must be trackable outside the document.
- Trigger, root cause, and contributing factors must remain distinct.

## Quality checks

- [ ] `references/operations-quality-rubric.md` was loaded before finalizing.
- [ ] Artifacts validate against [standards/operational-artifacts](../../standards/operational-artifacts/README.md): frontmatter complete; required sections present and, for runbooks, in the exact order.
- [ ] Every timeline event has a UTC timestamp and an evidence source.
- [ ] Trigger and root cause are distinct one-sentence statements; neither is "human error".
- [ ] Postmortem is blameless: no individual is named as a cause.
- [ ] Contributing factors are separated from the root cause.
- [ ] Every action item has an owner, severity, ISO 8601 due date, and tracking reference.
- [ ] Every paging alert references a runbook; runbooks list the six sections in order.
- [ ] Rollback procedures are operationally executable; escalation paths are explicit.
- [ ] On-call handoff names owner, escalation path, dashboards, alerts, rollback, and deployment expectations.

## References

- Output schema: [`standards/operational-artifacts`](../../standards/operational-artifacts/README.md).
- Related architecture skills: [`reliability`](../reliability/SKILL.md) (SLOs, error budgets, resilience strategy), [`infrastructure-platform`](../infrastructure-platform/SKILL.md) (deployment substrate, rollback mechanics), [`security`](../security/SKILL.md) (security-incident clauses).
- Downstream consumers: every `implementations/*` skill that emits a paging alert requires a runbook authored here.
