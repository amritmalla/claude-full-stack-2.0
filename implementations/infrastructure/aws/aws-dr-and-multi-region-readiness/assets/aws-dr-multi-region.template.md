# AWS DR and Multi-Region Readiness — Layout Reference

Use this as the canonical replication / failover / backup / drill pattern reference. These are **IaC-ready definitions** — the `terraform` Family H skills own module/state/plan/apply. Placeholder tokens use `<kebab-case>`. RPO/RTO and tier are consumed from upstream; the single-region foundation/runtime is extended, not redesigned.

## Definition set layout

```
dr-multi-region-readiness.md       # baseline + topology+RTO/RPO rationale +
                                    #   replication budgets + failover/fail-back +
                                    #   backup posture + DRILL RESULTS vs targets
definitions/
├── replication.<fmt>              # RDS/Aurora replica, S3 CRR, DDB Global Tables
├── failover.<fmt>                 # Route 53 health-check failover + fail-back
├── backup.<fmt>                   # AWS Backup: retention, x-region/x-acct, CMK
└── drill-runbook.md               # executed; achieved RPO/RTO recorded
```

## Topology decision — sized to RPO/RTO (no gold-plating)

```
tier-0, RTO ~minutes, RPO ~seconds  -> warm standby or active-active
tier-1, RTO 10s of min, RPO minutes -> pilot light
tier-2, RTO hours, RPO hours        -> backup & restore
# State, in dr-multi-region-readiness.md, the RTO/RPO the pick satisfies + cost.
```

## Cross-region replication — lag budget must meet the RPO

```hcl
# RDS/Aurora cross-region (or Aurora Global Database)
resource "aws_rds_cluster" "<db>_replica" {
  replication_source_identifier = <primary-arn>
  # typical replica lag MUST be <= architecture/reliability RPO; else design is wrong
}
# S3 Cross-Region Replication
resource "aws_s3_bucket_replication_configuration" "<bucket>" { /* CRR rule */ }
# DynamoDB Global Tables
resource "aws_dynamodb_table" "<t>" { replica { region_name = "<dr-region>" } }
```

## Failover — health-driven AND reversible

```hcl
resource "aws_route53_health_check" "<svc>_primary" { /* defined trigger */ }
resource "aws_route53_record" "<svc>" {
  failover_routing_policy { type = "PRIMARY" }       # SECONDARY record -> standby
  health_check_id = aws_route53_health_check.<svc>_primary.id
}
# Runbook MUST cover standby promotion AND fail-back to primary on recovery.
```

## Backup — immutable, encrypted, cross-region/cross-account, restore-tested

```hcl
resource "aws_backup_plan" "<wl>" {
  rule {
    lifecycle { delete_after = <tier-retention> }
    copy_action { destination_vault_arn = <dr-region-vault> }   # x-region
  }
  # x-account copy where ransomware/account-compromise resilience requires
  # encrypted via the FOUNDATION CMK strategy; Vault Lock where compliance requires
}
# A backup that has never been restored is an ASSUMPTION — restore it in the drill.
```

## Drill — executed, measured (the completion gate)

```markdown
# drill-runbook.md  (EXECUTED, not just written)
1. Trigger failover (disable primary health check)
2. Promote standby; measure RTO (time to serve from DR)
3. Measure RPO (data-loss window vs last replicated point)
4. Restore one data store from AWS Backup; verify integrity
5. Fail back to primary; confirm reversibility
Recorded: achieved RPO = <x> (target <y>) | achieved RTO = <a> (target <b>)
Gap (if any): <reported with ADR candidate — never hidden>
```

## Handoffs this skill names (does not implement)

| Concern | Owner |
|---|---|
| AWS Organizations / OU / SCP / account vending | `aws-account-and-organization-topology` |
| Single-region VPC, IAM, KMS, Secrets, Route 53 zones | `aws-network-and-identity-foundation` |
| Single-region compute, LB, autoscaling, deploy mechanics | `aws-workload-runtime-and-deployment` |
| CloudWatch/ADOT/X-Ray substrate, dashboards, budgets | `aws-observability-and-cost-readiness` |
| IaC module structure, state, plan gate, apply/promotion | `terraform` Family H skills |
