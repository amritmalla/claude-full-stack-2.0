---
symptom: <kebab-case slug>
alert: <alert name, or null if symptom-only>
service: <service slug>
owner: <team or role>
severity: sev2                         # sev1 | sev2 | sev3
last_reviewed: YYYY-MM-DD
---

# Runbook: [Symptom]

## Detection

- Fires when: [condition / alert]
- Alert / SLO defended: [name]
- Customer impact: [what users experience when this is active]

## Diagnostics

- Confirm: [command / query]
- Scope: [dashboard link, metric to read]
- Likely causes: [ordered by probability, with the signal that distinguishes each]

## Mitigation

- Required privileges: [role/scope]
- Steps:
  1. [safe stop-the-bleeding step]
  2. [step]
- If steps fail or privileges are insufficient: see Escalation.

## Escalation

| Level | Owner | When |
|---|---|---|
| Primary | [owner] | [on detection] |
| Secondary | [owner] | [no progress in N min] |
| Business-impact | [role] | [impact threshold crossed] |

## Rollback

- Mechanism: [how]
- Trigger conditions: [when to roll back rather than mitigate forward]
- Owner: [who]
- Verification: [how to confirm rollback succeeded]

## Verification

- Recovery confirmed when: [signal/metric returns to range]
- Customer impact ended when: [signal]
- Post-recovery: [follow-up, e.g. open postmortem if sev1/sev2]
