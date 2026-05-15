# operational-artifacts

Canonical structure for operational artifacts produced by `architecture/operations`: blameless postmortems, reusable runbooks, and on-call handoff notes. Consumed by on-call engineers, incident responders, and every implementation skill whose alerts require a runbook.

## File layout

```
docs/operations/<service-or-product-slug>/
├── postmortems/
│   └── YYYY-MM-DD-<incident-slug>.md   # one per incident
├── runbooks/
│   └── <symptom-slug>.md               # one per alert or operational symptom
└── on-call-handoff.md                  # OPTIONAL — when a service enters support
```

## `postmortem.md`

One file per incident. Blameless: findings name systems and processes, never individuals.

### Frontmatter (required)

```yaml
---
incident: <kebab-case slug>
status: draft | review | final
severity: sev1 | sev2 | sev3
owner: <name or role>
services: [<service slug>, ...]
detected_at: YYYY-MM-DDThh:mmZ          # UTC
resolved_at: YYYY-MM-DDThh:mmZ          # UTC
deployment_ref: <deploy id/artifact, or null>
last_reviewed: YYYY-MM-DD
---
```

### Required sections

| Section | Purpose | Gate |
|---|---|---|
| `## Summary` | What happened, in two or three sentences. | Names affected services and customer-visible effect |
| `## Impact` | Customer impact, duration, scope, error budget consumed. | Quantified, not "some users" |
| `## Timeline` | UTC-stamped events. Each row: timestamp, actor, event, evidence source. | Marks detection, page, mitigation start/end, recovery |
| `## Trigger` | One sentence: the event that directly caused impact. | Distinct from root cause |
| `## Root Cause` | One sentence: the condition that allowed the trigger to cause harm. | Distinct from trigger; not "human error" |
| `## Contributing Factors` | Conditions that worsened impact or delayed recovery. | Separated from root cause |
| `## Mitigation` | What was done to stop the bleeding, and the rollback if any. | References rollback artifact for deploy incidents |
| `## Lessons Learned` | What worked, what did not, what was lucky. | Systemic, blameless |
| `## Action Items` | Table: title, owner, severity, due date (ISO 8601), tracking ref, expected improvement. | Every row has owner + due date + tracking ref |

Security incidents additionally follow the incident clauses in [security-standards](../security-standards/README.md); a postmortem is mandatory and org-visible. Deploy-related incidents reference the deployment-event metric and rolled-back artifact per [deployment-standards](../deployment-standards/README.md).

## `runbook` (`runbooks/<symptom-slug>.md`)

One file per paging alert or operational symptom. Procedural, not narrative — executable without tribal knowledge.

### Frontmatter (required)

```yaml
---
symptom: <kebab-case slug>
alert: <alert name, or null if symptom-only>
service: <service slug>
owner: <team or role>
severity: sev1 | sev2 | sev3
last_reviewed: YYYY-MM-DD
---
```

### Required sections, in this exact order

1. `## Detection` — what fires this, the alert/SLO it defends, customer impact.
2. `## Diagnostics` — commands, dashboards, metrics, and queries to confirm and scope.
3. `## Mitigation` — the safe stop-the-bleeding steps, with required privileges.
4. `## Escalation` — primary owner, secondary owner, escalation order, business-impact thresholds.
5. `## Rollback` — mechanism, trigger conditions, owner, and verification.
6. `## Verification` — how to confirm recovery and customer impact has ended.

Every paging alert in [observability-standards](../observability-standards/README.md) MUST reference a runbook authored to this structure; an alert without a runbook is deleted.

## `on-call-handoff.md`

Optional. Produced when a service enters production support.

### Required sections

| Section | Purpose |
|---|---|
| `## Service Ownership` | Primary owner, secondary owner, support hours, paging expectations. |
| `## Escalation Path` | Ordered escalation with business-impact thresholds and escalation SLAs. |
| `## Dashboards` | Inventory with links; each names what customer impact it shows. |
| `## Alerts` | Inventory; each maps to a runbook and a responder action. |
| `## Rollback` | Mechanism, trigger conditions, owner, verification. |
| `## Deployment Expectations` | Release mechanism, gating signals, deploy-event correlation. |
| `## Operational Caveats` | Known sharp edges, dependency ownership, after-hours limits. |

## Versioning

- Postmortems are immutable once `status: final`; corrections append a dated addendum, never rewrite the timeline.
- Runbooks are living documents; bump `last_reviewed` on every change and after any incident that exercised them.

## Linkage contract

- Every paging alert MUST reference a runbook conforming to this schema, or the alert is deleted (enforced by [observability-standards](../observability-standards/README.md)).
- Every deploy-related postmortem MUST reference the deployment-event metric and rolled-back artifact per [deployment-standards](../deployment-standards/README.md).
- Every security incident MUST produce a `status: final` postmortem per [security-standards](../security-standards/README.md).
- Postmortem action items MUST be tracked outside the document (issue tracker); the document holds the reference, not the source of truth for status.

## Anti-patterns

- "Human error" as root cause — name the system or process that allowed it.
- Trigger and root cause stated identically.
- Timelines reconstructed from memory without evidence sources.
- Action items without an owner, due date, or tracking reference.
- "Be more careful" remediation instead of a systemic safeguard.
- Runbooks written as prose narratives instead of the six ordered sections.
- Alerts that page but document no responder action.
- "TBD" left in a `final` postmortem — convert to a tracked action item.
- Escalation paths that live only in chat history.
