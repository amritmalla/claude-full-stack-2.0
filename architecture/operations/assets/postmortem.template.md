---
incident: <kebab-case slug>
status: draft                          # draft | review | final
severity: sev2                         # sev1 | sev2 | sev3
owner: <name or role>
services: [<service slug>]
detected_at: YYYY-MM-DDThh:mmZ         # UTC
resolved_at: YYYY-MM-DDThh:mmZ         # UTC
deployment_ref: <deploy id/artifact, or null>
last_reviewed: YYYY-MM-DD
---

# Postmortem: [Incident Title]

## Summary

[Two or three sentences: what happened, which services were affected, and the customer-visible effect.]

## Impact

| Dimension | Value |
|---|---|
| Customer impact | [what users experienced] |
| Duration | [start → end, UTC] |
| Scope | [% users / regions / tenants] |
| Error budget consumed | [amount] |

## Timeline

| Time (UTC) | Actor | Event | Source |
|---|---|---|---|
| YYYY-MM-DDThh:mmZ | [system/person] | [first symptom] | [log/dashboard/chat link] |
| YYYY-MM-DDThh:mmZ | [system] | [alert fired] | [alert link] |
| YYYY-MM-DDThh:mmZ | [person] | [detection / ack] | [chat link] |
| YYYY-MM-DDThh:mmZ | [person] | [mitigation start] | [source] |
| YYYY-MM-DDThh:mmZ | [person] | [mitigation complete / recovery verified] | [source] |

## Trigger

[One sentence: the event that directly caused impact.]

## Root Cause

[One sentence: the underlying condition that allowed the trigger to cause harm. Not "human error". Distinct from the trigger.]

## Contributing Factors

- [Factor that worsened impact or delayed recovery — distinct from root cause]

## Mitigation

[What stopped the bleeding. For deploy incidents, name the rollback artifact and deployment-event reference.]

## Lessons Learned

- What worked: [...]
- What did not: [...]
- What was luck: [...]

## Action Items

| Title | Owner | Severity | Due (ISO 8601) | Tracking Ref | Expected Improvement |
|---|---|---|---|---|---|
| [title] | [owner] | [sev] | [YYYY-MM-DD] | [issue link] | [recurrence / blast radius / detection / mitigation / clarity] |
