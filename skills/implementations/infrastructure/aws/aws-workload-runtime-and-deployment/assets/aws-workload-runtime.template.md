# AWS Workload Runtime and Deployment — Layout Reference

Use this as the canonical compute / load-balancing / autoscaling / deployment pattern reference. These are **IaC-ready definitions** — the `terraform` Family H skills own module/state/plan/apply. Placeholder tokens use `<kebab-case>`. Values are illustrative — replace with the substrate decision, SLOs, and tier from upstream.

## Definition set layout

```
workload-runtime-deployment.md     # primitive selection + rationale + LB + autoscaling
                                    #   + deploy/rollback mechanics + multi-AZ posture
definitions/
├── compute.<fmt>                  # selected primitive into the FOUNDATION subnets/role/CMK
├── load-balancer.<fmt>            # ALB (HTTP host/path) or NLB (TCP/UDP/throughput)
├── autoscaling.<fmt>              # policy: floor=reliability tier, ceiling=cost envelope
└── deployment.<fmt>               # blue/green | canary | rolling + rollback trigger
```

## Primitive selection — by workload class

```
class: event-driven   -> Lambda            (reserved/provisioned concurrency for floor)
class: managed-container -> Fargate (ECS)  (task role = FOUNDATION role)
class: orchestrated   -> EKS cluster + node groups  ──► in-cluster manifests:
                                                       HANDOFF to kubernetes Family G
class: legacy/licensed -> EC2 + ASG
class: relational     -> RDS / Aurora      (Multi-AZ for tier-0/1)
class: key-value      -> DynamoDB          (on-demand or autoscaling)
# Justify the pick AND the rejected alternatives in workload-runtime-deployment.md.
```

## Compute placed INTO the foundation (no new VPC/role/key)

```hcl
resource "aws_ecs_service" "<service>" {
  cluster         = <foundation-or-runtime-cluster>
  task_definition = aws_ecs_task_definition.<service>.arn
  network_configuration {
    subnets          = [<FOUNDATION private-app subnets>]   # from skill 2
    security_groups  = [<FOUNDATION sg>]
  }
  # task role / execution role = FOUNDATION least-privilege role (skill 2)
  # encryption = FOUNDATION CMK (skill 2)
}
```

## Load balancing — protocol-matched, traffic-gating health check

```hcl
resource "aws_lb" "<service>" { load_balancer_type = "application" }   # NLB if TCP/UDP
resource "aws_lb_target_group" "<service>" {
  health_check {                          # GATES traffic; distinct from liveness probe
    path = "/health/ready"
    matcher = "200"
  }
}
```

## Autoscaling — floor from reliability tier, ceiling from cost

```hcl
resource "aws_appautoscaling_target" "<service>" {
  min_capacity = <reliability-tier-floor>     # non-zero for tier-0/1
  max_capacity = <capacity-cost-ceiling>
}
resource "aws_appautoscaling_policy" "<service>" {
  policy_type = "TargetTrackingScaling"
  target_tracking_scaling_policy_configuration { target_value = 60 }
}
```

## Deployment — safe and reversible

```hcl
# tier-0: blue/green via CodeDeploy + ALB; instant shift-back
resource "aws_codedeploy_deployment_group" "<service>" {
  deployment_style { deployment_type = "BLUE_GREEN" }
  auto_rollback_configuration {
    enabled = true
    events  = ["DEPLOYMENT_FAILURE", "DEPLOYMENT_STOP_ON_ALARM"]   # the trigger
  }
}
# tier-2+: rolling with bounded surge. Every deploy declares the rollback trigger.
```

## Handoffs this skill names (does not implement)

| Concern | Owner |
|---|---|
| AWS Organizations / OU / SCP / account vending | `aws-account-and-organization-topology` |
| VPC, subnets, IAM roles, KMS, Secrets, Route 53 | `aws-network-and-identity-foundation` |
| In-cluster Deployment/Service/HPA/PDB (when EKS) | `kubernetes` Family G skills |
| CloudWatch/ADOT/X-Ray, dashboards, Cost Explorer/Budgets | `aws-observability-and-cost-readiness` |
| Multi-region, cross-region replicas, failover drills | `aws-dr-and-multi-region-readiness` |
| IaC module structure, state, plan gate, apply/promotion | `terraform` Family H skills |
