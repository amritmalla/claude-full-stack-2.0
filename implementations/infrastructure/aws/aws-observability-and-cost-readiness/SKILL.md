---
name: aws-observability-and-cost-readiness
description: Use when wiring AWS observability and cost readiness for a workload or account after the runtime exists and operations and performance have decided the observability substrate and cost posture. Produces CloudWatch Logs/Metrics/Alarms, AWS Distro for OpenTelemetry and X-Ray tracing, SLO dashboards, Cost Explorer + AWS Budgets + Cost Anomaly Detection, FinOps tagging discipline consuming the org tag policy, and savings-plan/RI posture. Do not use for org/account/tag-policy enforcement, network/identity, workload runtime, or DR/multi-region, or Terraform module/state mechanics; use the other aws (or Family H) skills.
---

# AWS Observability and Cost Readiness

## When to use

Invoke when making an AWS workload or account observable and cost-governed for production — metrics/logs/traces, SLO dashboards and alarms, budgets, anomaly detection, FinOps tagging, and commitment posture — or auditing an inherited account that is unmonitored or financially opaque.

Do not use for: AWS Organizations/account topology or the mandatory tag-policy *enforcement* (use `aws-account-and-organization-topology`); VPC/IAM/KMS foundation (use `aws-network-and-identity-foundation`); compute selection and deployment (use `aws-workload-runtime-and-deployment`); multi-region/DR (use `aws-dr-and-multi-region-readiness`); IaC module/state/plan/apply mechanics (the `terraform` Family H skills).

## Inputs

Required:

- A deployed runtime from `aws-workload-runtime-and-deployment` (the compute/LB/data this skill instruments) within the account topology.
- Approved `architecture/operations` decisions on the observability substrate, alert destinations, and runbook hooks, or explicit confirmation they are intentionally deferred.

Optional:

- Approved `architecture/performance` cost/performance budgets and the savings-plan/RI strategy.
- The workload tier from `architecture-schema` (drives alarm strictness, retention, budget thresholds).
- SLOs and error-budget policy from `architecture/reliability` (drive alarm thresholds).
- The mandatory tag keys defined by `aws-account-and-organization-topology` (consumed, not redefined).
- Existing CloudWatch/X-Ray/Cost Explorer state to audit.

## Operating rules

- Never generate vanity telemetry or a dashboard nobody is paged on. A metric with no alarm, a log nobody queries, and a budget with no owner or action are cost, not readiness.
- Consume `architecture/operations` and `architecture/performance`; do not invent decisions. The observability substrate, alert destinations, runbook hooks, cost budgets, and commitment strategy are architectural decisions. If a needed decision is missing, pause and raise an ADR candidate rather than guessing.
- The tag policy is consumed, not authored. `aws-account-and-organization-topology` defined the mandatory tag keys and enforces them via tag policies. This skill consumes those tags for cost allocation and FinOps discipline; it does not redefine or re-enforce the tag policy. Name the boundary.
- Every workload emits the three signals. CloudWatch metrics/logs, ADOT-collected metrics where richer, and X-Ray traces with propagation. A workload missing a signal is not observability-ready.
- Alarms are SLO-tied and actionable. Each CloudWatch alarm maps to an SLO or a concrete failure mode, has a tier-derived severity, an upstream destination, and a named runbook. An alarm with no SLO and no runbook is rejected.
- Logs are structured, retained per tier, and PII/secret-safe. Structured log format, retention from the tier, and redaction in the pipeline — secrets and PII never reach the log group.
- Cost is governed, not just observed. AWS Budgets with an owner and a defined breach action, Cost Anomaly Detection wired to a destination, and Cost Explorer views by the consumed tag dimensions. A budget with no owner or no breach action is decoration.
- FinOps tagging discipline consumes the org tag keys. Cost allocation, showback/chargeback, and untagged-resource detection use `Environment`/`Workload`/`CostCenter`/`Owner` as defined upstream; this skill reports tag-coverage gaps, it does not invent new mandatory keys.
- Commitment posture is explicit and tied to the budget. Savings Plans / Reserved Instances posture follows the `architecture/performance` strategy with a stated coverage target; "buy later" without a target is rejected for steady tier-0/1 baseline load.
- This skill owns observability + cost wiring + FinOps discipline. Org/tag-policy enforcement, network/identity, runtime, DR, and IaC mechanics are named handoffs.
- A workload whose alarms have not been test-fired and whose budget breach action has not been confirmed routable is not done.

## Output contract

The observability and cost wiring MUST conform to:

- [observability-standards](../../../../standards/observability-standards/README.md) — metrics/logs/traces wired, SLO-tied alarms with destinations, trace/log correlation, tier-based retention.
- [deployment-standards](../../../../standards/deployment-standards/README.md) — observability and cost wiring reproducible via IaC-ready definitions; no click-ops-only dashboards.
- [naming-conventions](../../../../standards/naming-conventions/README.md) — log-group, alarm, dashboard, and budget naming.
- [architecture-schema](../../../../standards/architecture-schema/README.md) — tier classification drives alarm strictness, log retention, and budget thresholds.

Upstream contract: `architecture/operations` is the source of truth for the observability substrate, alert destinations, and runbook hooks; `architecture/performance` is the source of truth for cost budgets and commitment strategy. The mandatory tag keys are owned by `aws-account-and-organization-topology`. If a needed decision is missing, pause and raise an ADR candidate. Org/tag-policy enforcement, network/identity, runtime, DR, and IaC mechanics are named handoffs.

## Progressive references

- Read `references/aws-observability-cost-playbook.md` when wiring any owned area or checking the anti-pattern list.
- Read `references/aws-observability-cost-quality-rubric.md` before declaring readiness complete.
- Use `assets/aws-observability-cost.template.md` as the CloudWatch/ADOT/X-Ray/Budgets/FinOps pattern reference.

## Process

1. Gather context: load `architecture/operations` (substrate, alert destinations, runbook hooks) and `architecture/performance` (cost budgets, commitment strategy); pull SLOs from `architecture/reliability`. Resolve the workload tier from `architecture-schema`. Confirm the runtime exists and the mandatory tag keys from `aws-account-and-organization-topology`. If a needed decision is missing, raise an ADR candidate before proceeding.
2. Wire metrics: CloudWatch metrics for the runtime primitives, ADOT collection where richer signal is needed, namespaced and dimensioned for SLO evaluation.
3. Wire logs: structured log format to CloudWatch Logs, tier-based retention, PII/secret redaction in the pipeline.
4. Wire tracing: X-Ray (or ADOT trace export) with context propagation; confirm trace↔log correlation.
5. Author SLO dashboards and alarms: each alarm tied to an SLO or failure mode, tier severity, the upstream destination, and a named runbook — no orphan alarms.
6. Configure cost governance: AWS Budgets with an owner and a defined breach action, Cost Anomaly Detection to a destination, Cost Explorer views by the consumed tag dimensions.
7. Apply FinOps discipline: cost allocation by the org-defined tag keys, an untagged-resource detection report, and a tag-coverage gap list (consuming, not redefining, the tag policy).
8. Set the commitment posture: Savings Plans / RI coverage target per the `architecture/performance` strategy, tied to the steady baseline load.
9. Validate: test-fire each alarm and confirm it routes to its destination; confirm the budget breach action is routable; confirm dashboards reflect live signal; document any check that cannot run.
10. Produce `observability-cost-readiness.md` (signal inventory, alarm→SLO→runbook map, retention, budget/anomaly config, FinOps tag-coverage, commitment posture) plus the gap list with ADR candidates and the named handoff list. Validate against observability-, deployment-standards, naming-conventions, and architecture-schema. Revise until all pass or the gap is documented.

## Outputs

Required:

- CloudWatch metrics + ADOT collection wiring for the runtime primitives.
- Structured CloudWatch Logs with tier-based retention and PII/secret redaction.
- X-Ray/ADOT tracing with context propagation and trace↔log correlation.
- SLO dashboards and alarms, each tied to an SLO/failure mode, severity, destination, runbook.
- AWS Budgets (owner + breach action), Cost Anomaly Detection, Cost Explorer tag-dimension views.
- FinOps tag-coverage report consuming the org-defined keys (not redefining them).
- Savings Plans / RI commitment posture with a coverage target.
- `observability-cost-readiness.md`, the gap list with ADR candidates, and the named handoff list.

Output rules:

- IaC-ready definitions, not click-ops or prose-only; not the Terraform module/state mechanics.
- No orphan alarms; no PII/secrets in log groups; no budget without an owner and a breach action.
- The mandatory tag policy is consumed, not redefined or re-enforced here.
- Org/tag-policy enforcement, network/identity, runtime, DR, and IaC mechanics are named handoffs.

## Quality checks

- [ ] Observability substrate, alert destinations, and runbook hooks are sourced from `architecture/operations`; cost budgets and commitment strategy from `architecture/performance` (or an ADR candidate is raised).
- [ ] The mandatory tag keys are consumed from `aws-account-and-organization-topology`; this skill does not redefine or re-enforce the tag policy.
- [ ] The workload emits metrics, structured logs, and propagated traces; trace↔log correlation works.
- [ ] Log retention is tier-based and PII/secrets are redacted in the pipeline (never reach the log group).
- [ ] Every alarm maps to an SLO or failure mode, with tier severity, an upstream destination, and a named runbook — no orphans.
- [ ] AWS Budgets have an owner and a defined breach action; Cost Anomaly Detection is wired to a destination.
- [ ] Cost Explorer views and cost allocation use the org-defined tag dimensions; an untagged-resource/tag-coverage report exists.
- [ ] Savings Plans / RI posture has a coverage target tied to steady baseline load per `architecture/performance`.
- [ ] Each alarm was test-fired to its destination and the budget breach action confirmed routable, or the gap is documented.
- [ ] Org/tag-policy enforcement, network/identity, runtime, DR, and IaC mechanics are named handoffs.

## References

- Upstream: [`architecture/operations`](../../../../architecture/operations/SKILL.md), [`architecture/performance`](../../../../architecture/performance/SKILL.md).
- Builds on: [`aws-workload-runtime-and-deployment`](../aws-workload-runtime-and-deployment/SKILL.md) (the runtime this skill instruments).
- Consumes the tag policy from: [`aws-account-and-organization-topology`](../aws-account-and-organization-topology/SKILL.md) (mandatory tag keys + enforcement).
- Related aws archetype skills: [`aws-network-and-identity-foundation`](../aws-network-and-identity-foundation/SKILL.md), [`aws-dr-and-multi-region-readiness`](../aws-dr-and-multi-region-readiness/SKILL.md).
- IaC mechanics handoff: the `terraform` Family H skills own module/state/plan/apply.
- Standards: [`observability-standards`](../../../../standards/observability-standards/README.md), [`deployment-standards`](../../../../standards/deployment-standards/README.md), [`naming-conventions`](../../../../standards/naming-conventions/README.md), [`architecture-schema`](../../../../standards/architecture-schema/README.md).
