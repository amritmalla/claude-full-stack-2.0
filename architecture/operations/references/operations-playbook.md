# Operations Playbook

Load this when collecting incident context, building a timeline, or producing any operational artifact. It expands the operating rules and process steps in `SKILL.md` with the detail needed to produce postmortems, runbooks, and on-call handoffs.

## Why this workflow exists

Design operational clarity after incidents and before production ownership transitions. It prevents repeated incidents with no learning loop, undocumented operational knowledge, pager fatigue from low-quality alerts, escalation ambiguity, rollback confusion during outages, and operational dependency on tribal knowledge.

The goal is not "writing a postmortem" — it is operational resilience, reusable operational knowledge, faster recovery, safer deployments, sustainable on-call, and system-level learning.

## Behavioral rules in depth

### 1. Incidents are analyzed blamelessly

Never blame individuals. Failures emerge from systems, processes, tooling, communication, operational gaps, and organizational incentives. Postmortems discuss systems, workflows, missing safeguards, and process failures. Reject "human error" as root cause and naming individuals. People may trigger failures; systems allow failures to become incidents.

### 2. Trigger and root cause are different

Trigger = the event that immediately caused impact. Root cause = the underlying condition that allowed the trigger to cause harm. Example — Trigger: "A malformed deployment exhausted DB connections." Root cause: "The deployment pipeline lacked connection-pool regression validation." Reject postmortems where trigger and root cause are identical.

### 3. Operational artifacts must be reusable

Every runbook defines, in order: Detection, Diagnostics, Mitigation, Escalation, Rollback, Verification. Reject narrative-only runbooks and undocumented recovery assumptions.

### 4. Alerts without actionability are operational debt

Every paging alert maps to a service owner, has a documented runbook, defines customer impact, and defines the required responder action. Reject alerts with no operational response and alerts that only say "investigate."

### 5. Timelines are factual and source-backed

Every timeline entry includes a UTC timestamp, actor, event, and evidence source (logs, metrics, dashboards, deploy records, audit trails, incident chat links). Reject reconstructed timelines without evidence and relative-time narratives.

### 6. Action items reduce future risk

Action items reduce recurrence probability, reduce blast radius, improve detection, improve mitigation speed, or improve operational clarity. Each has owner, due date, severity, and tracking reference. Reject vague items and "be more careful" remediation.

### 7. Rollback is a first-class capability

Every deployable system defines rollback mechanism, owner, trigger conditions, and verification. Reject "redeploy previous version manually" without procedural clarity.

### 8. Escalation paths are explicit

Every operational artifact defines primary owner, secondary owner, escalation order, and business-impact escalation thresholds. Reject escalation through tribal knowledge.

### 9. Operational readiness is part of delivery

A service is not production-ready unless alerts, dashboards, runbooks, ownership, rollback, and on-call responsibilities exist and are documented. Reject "we'll operationalize later."

### 10. Challenge weak operational practices directly

Be operationally concrete and recovery-focused. Examples of the kind of feedback to give:

- "This alert pages but defines no responder action."
- "Your rollback path depends on tribal knowledge."
- "The system has no operational owner after hours."
- "This dashboard lacks customer-impact visibility."
- "The mitigation procedure assumes cluster-admin privileges without escalation guidance."

## Step detail

**Context collection (step 1).** Collect incident description, operational symptom, affected services, customer impact, and mitigation status. Gather alerts, logs, metrics, traces, deployment records, dashboards, and incident chat transcripts. Clarify severity, impact duration, and current operational state. Refuse analysis without evidence.

**Timeline (step 2).** Construct a factual UTC timeline. Mark explicitly: first symptom, alert firing, detection, acknowledgment, mitigation start, mitigation completion, rollback, recovery verification, and customer-impact windows. Reject approximate timelines without evidence references.

**Trigger and root cause (step 3).** State the trigger in one sentence and the root cause in one sentence. Ensure they are distinct, operationally meaningful, and actionable.

**Five whys (step 4).** Apply five-whys from the root cause. Stop only when the result is actionable, systemic, and operationally meaningful. Categories: deployment process, observability gap, ownership ambiguity, scaling assumption, architectural weakness, testing gap, operational tooling failure. Avoid infinite philosophical chains and shallow one-step explanations.

**Contributing factors (step 5).** List factors that worsened impact: missing alerts, unclear ownership, noisy alerts, poor dashboards, lack of rollback, unsafe deploy strategy, missing rate limits, weak runbooks, insufficient redundancy, stale documentation. Distinguish root cause, trigger, and contributing factors.

**Postmortem (step 6).** Generate incident summary, impact summary, timeline, trigger, root cause, contributing factors, mitigation summary, lessons learned, and remediation actions. Tone is factual, blameless, operational, improvement-oriented. Reject emotionally defensive language and blame narratives.

**Action items (step 7).** Categories: alerting, observability, rollback safety, deployment gating, automation, redundancy, documentation, rate limiting, testing, ownership clarification. Each item has title, owner, severity, due date (ISO 8601), tracking reference, expected operational improvement. Reject non-trackable items.

**Runbooks (step 8).** Generate reusable runbooks for alerts, symptoms, or operational scenarios. Each contains the six sections in order, with commands, dashboards, metrics, dependencies, and escalation triggers. Reject runbooks requiring tribal knowledge.

**On-call handoff (step 9).** Produce service ownership model, escalation paths, dashboard inventory, alert inventory, rollback procedure, deployment expectations, and operational caveats. Clarify support hours, paging expectations, escalation SLAs, and dependency ownership. Reject unsupported production services.

## Operational standards alignment

- Every paging alert references a runbook ([observability-standards](../../../standards/observability-standards/README.md)); alerts without runbooks are deleted.
- Security incidents require a mandatory, org-visible postmortem ([security-standards](../../../standards/security-standards/README.md)).
- Deploy-related incidents reference the deployment-event metric and rolled-back artifact ([deployment-standards](../../../standards/deployment-standards/README.md)).

## Anti-patterns to detect

Call these out explicitly when detected:

- "Human error" as root cause
- Alerts with no responder action
- Missing rollback path
- No operational owner
- Shared pager ownership ambiguity
- Dashboard without customer-impact visibility
- Tribal-knowledge mitigation
- Postmortems without action items
- Action items without owners
- Noisy paging alerts
- Runbooks written as narratives
- Production deploys without rollback verification
- Incident timelines without evidence
- Escalation paths hidden in chat history
- Alert fatigue normalization
- Unsupported after-hours systems
- Security incidents without mandatory review
- Deployments lacking deployment-event correlation
- Manual mitigation requiring undocumented credentials

## Writing style

Operationally rigorous, factual, blameless, systems-oriented. Avoid emotional framing, blame language, vague remediation, and narrative storytelling without operational value. The objective is operational resilience and organizational learning — not merely documenting outages.
