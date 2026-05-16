# AWS Observability and Cost Readiness — Layout Reference

Use this as the canonical CloudWatch / ADOT / X-Ray / Budgets / FinOps pattern reference. These are **IaC-ready definitions** — the `terraform` Family H skills own module/state/plan/apply. Placeholder tokens use `<kebab-case>`. The substrate and budgets are consumed from upstream; the tag keys are consumed from the org-topology skill.

## Definition set layout

```
observability-cost-readiness.md    # signal inventory + alarm->SLO->runbook map +
                                    #   retention + budget/anomaly + tag-coverage + commitments
definitions/
├── metrics.<fmt>                  # CloudWatch + ADOT collection
├── logs.<fmt>                     # structured log group + tier retention + redaction
├── tracing.<fmt>                  # X-Ray / ADOT export + propagation
├── alarms-dashboards.<fmt>        # SLO dashboards + alarms (each names a runbook)
└── cost.<fmt>                     # Budgets + Anomaly Detection + Cost Explorer views
```

## SLO alarm — tied to an SLO, names a runbook

```hcl
resource "aws_cloudwatch_metric_alarm" "<service>_error_budget_burn" {
  alarm_name          = "<service>-error-budget-burn-fast"
  comparison_operator = "GreaterThanThreshold"
  threshold           = 0.02                        # from architecture/reliability SLO
  alarm_actions       = [<upstream-destination-sns/onfailure>]
  alarm_description    = "SLO: availability 99.5% | runbook: runbooks/error-budget.md"
  # No SLO + no runbook  =>  orphan alarm, rejected.
}
```

## Log group — tier retention, NOT infinite by default

```hcl
resource "aws_cloudwatch_log_group" "<service>" {
  name              = "/<env>/<service>"
  retention_in_days = <tier-retention>    # from architecture-schema; never unset
  # Redaction happens in the pipeline (ADOT/Lambda) BEFORE the group.
}
```

## Cost governance — owner + breach action, not just a notice

```hcl
resource "aws_budgets_budget" "<workload>" {
  budget_type  = "COST"
  limit_amount = "<budget-from-architecture-performance>"
  cost_filter { name = "TagKeyValue" values = ["user:Workload$<workload>"] }  # org tag
  notification {
    threshold = 100
    subscriber_sns_topic_arns = [<monitored-destination>]   # routable breach action
  }
}
resource "aws_ce_anomaly_monitor" "<workload>" { /* -> monitored destination */ }
```

## FinOps — consume the org tag keys (do not redefine)

```
Cost allocation dimensions = Environment | Workload | CostCenter | Owner
   ^ defined + enforced by aws-account-and-organization-topology (consumed here)
Deliverable: untagged-resource report + tag-coverage gap list
   (this skill REPORTS coverage; it does not author the tag policy)
```

## Commitment posture — explicit target

```
Savings Plans / RI coverage target: <e.g. 70% of steady tier-0/1 baseline>
   per architecture/performance commitment strategy.
"Buy later" with no target for steady baseline => rejected.
```

## Handoffs this skill names (does not implement)

| Concern | Owner |
|---|---|
| AWS Organizations / OU / SCP / mandatory tag-policy enforcement | `aws-account-and-organization-topology` |
| VPC, IAM, KMS, Secrets, Route 53 | `aws-network-and-identity-foundation` |
| Compute selection, LB, autoscaling, deploy mechanics | `aws-workload-runtime-and-deployment` |
| Multi-region, cross-region replicas, failover drills | `aws-dr-and-multi-region-readiness` |
| IaC module structure, state, plan gate, apply/promotion | `terraform` Family H skills |
