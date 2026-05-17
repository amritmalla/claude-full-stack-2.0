---
service: <service slug>
owner: <team or role>
support_hours: <e.g. 24x7 | business-hours>
last_reviewed: YYYY-MM-DD
---

# On-Call Handoff: [Service Name]

## Service Ownership

| Role | Owner | Notes |
|---|---|---|
| Primary owner | [owner] | [paging expectation] |
| Secondary owner | [owner] | [backup] |
| Support hours | [hours] | [after-hours behavior] |

## Escalation Path

| Level | Owner | Threshold | Escalation SLA |
|---|---|---|---|
| L1 | [owner] | [on page] | [ack time] |
| L2 | [owner] | [no progress in N min] | [time] |
| Business-impact | [role] | [impact threshold] | [time] |

## Dashboards

| Dashboard | Link | Customer Impact Shown |
|---|---|---|
| [name] | [link] | [what user-facing signal it shows] |

## Alerts

| Alert | Severity | Runbook | Responder Action |
|---|---|---|---|
| [alert] | [sev] | [runbooks/<symptom>.md] | [action] |

## Rollback

- Mechanism: [how]
- Trigger conditions: [when]
- Owner: [who]
- Verification: [how]

## Deployment Expectations

- Release mechanism: [rolling / blue-green / canary / progressive]
- Gating signals: [signals]
- Deployment-event correlation: [how deploys map to incident timelines]

## Operational Caveats

- [Known sharp edge, dependency ownership, after-hours limit]
