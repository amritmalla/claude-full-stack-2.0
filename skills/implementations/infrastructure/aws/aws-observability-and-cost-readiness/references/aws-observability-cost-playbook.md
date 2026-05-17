# AWS Observability and Cost Readiness Playbook

Load this when wiring any owned area of `aws-observability-and-cost-readiness` or checking the anti-pattern list. It expands the operating rules and process steps in `SKILL.md` with the detail needed to make an AWS workload genuinely observable and cost-governed.

## Why this workflow exists

Unobserved and ungoverned AWS is paid for twice. A workload with no SLO alarm is a black box until users complain; a log group with no retention policy quietly bills forever; a budget with no owner means the cost overrun is discovered in the monthly invoice, not the day it started; untagged resources make "what does this team spend" unanswerable. An alarm with no runbook wakes someone who does not know what to do. None of this fails a functional test — the app runs fine while the bill and the blind spots grow.

The goal is three signals with SLO-tied actionable alarms, and cost that is budgeted, owned, anomaly-detected, and tag-allocated — consuming the operations and performance posture instead of inventing it.

## Behavioral rules in depth

### 1. Consume operations and performance; do not invent it

The observability substrate, alert destinations, and runbook hooks come from `architecture/operations`; cost budgets and the commitment strategy from `architecture/performance`; SLOs from `architecture/reliability`. Thresholds are derived from those, not picked. If a needed decision is missing, raise an ADR candidate.

### 2. The tag policy is consumed, not authored

`aws-account-and-organization-topology` defined the mandatory tag keys (`Environment`, `Workload`, `CostCenter`, `Owner`) and enforces them via AWS tag policies. This skill *uses* those tags for cost allocation and reports coverage gaps. Re-declaring the mandatory keys or re-enforcing the policy here creates two owners for the tag contract.

### 3. Three signals, every workload

| Signal | Wiring | Failure if absent |
|---|---|---|
| Metrics | CloudWatch + ADOT where richer | No SLO evaluation |
| Logs | Structured → CloudWatch Logs, retained per tier | Not queryable; bills forever |
| Traces | X-Ray / ADOT export + propagation | Latency source invisible |

A workload missing one is not observability-ready.

### 4. Alarms are SLO-tied and actionable

Every CloudWatch alarm maps to an SLO (latency/availability/error-budget burn) or a concrete failure mode, carries a tier-derived severity, routes to the upstream destination, and names the runbook. An alarm with no SLO and no runbook trains on-call to ignore alarms and is rejected.

### 5. Logs are structured, retained per tier, redacted

Structured (JSON) so they are queryable in Logs Insights. Retention from the tier — not infinite by default (a silent cost). Secrets and PII are redacted in the pipeline; a token in a log group is an incident, and CloudWatch Logs is not a safe place for it.

### 6. Cost is governed, not just observed

| Control | Requirement |
|---|---|
| AWS Budgets | An owner and a defined breach action (not just a notification into the void) |
| Cost Anomaly Detection | Wired to a real destination |
| Cost Explorer | Views by the consumed tag dimensions |

A budget that emails an unmonitored alias is decoration.

### 7. FinOps discipline consumes the org tag keys

Cost allocation, showback/chargeback, and untagged-resource detection use the upstream-defined keys. The deliverable is a tag-coverage report and a gap list — not a new set of mandatory keys invented here.

### 8. Commitment posture is explicit and targeted

Savings Plans / RIs follow the `architecture/performance` strategy with a stated coverage target against the steady baseline load. "Buy later" with no target for a steady tier-0/1 baseline is rejected — it is a standing overspend.

### 9. Untested observability/cost is unverified

Test-fire each alarm and confirm it reaches its destination (an alarm that never fires, or fires into the void, is worse than none). Confirm the budget breach action is actually routable. Dashboards must reflect live signal. Unverified wiring is unverified.

## Step detail

**Step 1 — Gather context.** Load `architecture/operations` (substrate, destinations, runbook hooks) and `architecture/performance` (budgets, commitments); pull SLOs from `architecture/reliability`. Resolve tier from `architecture-schema`. Confirm the runtime and the upstream tag keys. Raise an ADR candidate for any missing decision.

**Step 2 — Metrics.** CloudWatch for the runtime primitives; ADOT where richer; namespaced/dimensioned for SLO evaluation.

**Step 3 — Logs.** Structured → CloudWatch Logs; tier retention; pipeline redaction.

**Step 4 — Traces.** X-Ray / ADOT export + propagation; verify trace↔log correlation.

**Step 5 — Dashboards & alarms.** SLO dashboards; each alarm → SLO/failure mode, tier severity, upstream destination, named runbook.

**Step 6 — Cost governance.** Budgets (owner + breach action); Cost Anomaly Detection → destination; Cost Explorer tag-dimension views.

**Step 7 — FinOps discipline.** Allocation by org tag keys; untagged-resource detection; tag-coverage gap list.

**Step 8 — Commitment posture.** Savings Plans / RI coverage target tied to steady baseline per `architecture/performance`.

**Step 9 — Validate.** Test-fire alarms to destinations; confirm budget breach action routable; dashboards reflect live signal. Document any check that cannot run.

**Step 10 — Emit & validate.** `observability-cost-readiness.md` (signal inventory, alarm→SLO→runbook map, retention, budget/anomaly config, tag-coverage, commitment posture), gap list with ADR candidates, handoff list. Validate against observability-, deployment-standards, naming-conventions, architecture-schema.

## Anti-patterns to detect

Call these out explicitly when found:

- Re-declaring or re-enforcing the mandatory tag policy (owned by `aws-account-and-organization-topology`)
- A workload missing metrics, logs, or traces
- Log groups with infinite/default retention; secrets or PII in a log group
- An alarm with no SLO/failure-mode mapping and no named runbook
- A budget with no owner or no defined breach action; anomaly detection into an unmonitored alias
- Cost Explorer / allocation not using the org-defined tag dimensions
- No untagged-resource / tag-coverage reporting
- No Savings Plans / RI coverage target for steady tier-0/1 baseline load
- Alarms never test-fired; budget breach action never confirmed routable
- Dashboards built click-ops with no IaC-ready definition
- Terraform module/state mechanics authored here (belongs to Family H)
