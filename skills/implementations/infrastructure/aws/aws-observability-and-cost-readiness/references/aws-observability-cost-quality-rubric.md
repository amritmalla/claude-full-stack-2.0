# AWS Observability and Cost Readiness Quality Rubric

Load this before declaring readiness complete. Revise until each check passes or the unresolved gap is explicitly documented in `observability-cost-readiness.md`.

## Context & boundary

- [ ] Observability substrate, alert destinations, and runbook hooks are sourced from `architecture/operations`; cost budgets and commitment strategy from `architecture/performance` (or an ADR candidate is raised).
- [ ] SLOs are pulled from `architecture/reliability` and drive alarm thresholds.
- [ ] The mandatory tag keys are consumed from `aws-account-and-organization-topology` — not redefined or re-enforced here.

## Three signals

- [ ] CloudWatch metrics (and ADOT where richer) cover the runtime primitives, dimensioned for SLO evaluation.
- [ ] Logs are structured to CloudWatch Logs with tier-based retention (not infinite by default).
- [ ] PII and secrets are redacted in the pipeline and never reach the log group.
- [ ] X-Ray / ADOT tracing has context propagation; trace↔log correlation works.

## Alarms & dashboards

- [ ] SLO dashboards reflect live signal.
- [ ] Every alarm maps to an SLO or a concrete failure mode.
- [ ] Every alarm has a tier-derived severity, an upstream destination, and a named runbook — no orphans.
- [ ] Each alarm was test-fired and confirmed to route to its destination, or the gap is documented.

## Cost governance & FinOps

- [ ] AWS Budgets exist with an owner and a defined breach action (not a notification into the void).
- [ ] Cost Anomaly Detection is wired to a real, monitored destination.
- [ ] Cost Explorer views and cost allocation use the org-defined tag dimensions.
- [ ] An untagged-resource detection report and a tag-coverage gap list exist.
- [ ] Savings Plans / RI posture has a coverage target tied to steady baseline load per `architecture/performance`.
- [ ] The budget breach action was confirmed routable, or the gap is documented.

## Standards conformance & handoffs

- [ ] [observability-standards](../../../../../../standards/observability-standards/README.md): metrics/logs/traces wired, SLO-tied alarms with destinations, trace/log correlation, tier retention.
- [ ] [deployment-standards](../../../../../../standards/deployment-standards/README.md): observability and cost wiring reproducible via IaC-ready definitions; no click-ops-only.
- [ ] [naming-conventions](../../../../../../standards/naming-conventions/README.md): log-group, alarm, dashboard, budget naming.
- [ ] [architecture-schema](../../../../../../standards/architecture-schema/README.md): tier drove alarm strictness, log retention, budget thresholds.
- [ ] Org/tag-policy enforcement, network/identity, runtime, DR, and Terraform module/state mechanics are named handoffs — none implemented here.

## Failure handling

If a check fails:

1. Identify the missing signal, orphan alarm, or ungoverned cost control.
2. Ask the user for clarification if the decision cannot be inferred from `architecture/operations` or `architecture/performance`.
3. Revise the wiring, re-test-fire the affected alarms and re-confirm the budget breach action.
4. Keep any unresolved gap explicit in `observability-cost-readiness.md` — do not hide it as an assumption.
