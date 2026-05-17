---
name: cloud-foundation-on-aws
description: Use when establishing a production-grade AWS landing zone and
  Terraform delivery foundation before any application workloads ship.
  Sequences 11 infrastructure skills across four phases covering platform
  strategy, account and network topology, identity, Terraform repository
  and state, policy-as-code gates, promotion mechanics, workload runtime,
  observability, cost, and disaster recovery.
---

# Cloud Foundation on AWS

This workflow chains pure infrastructure skills — no application code. It takes an organization from a platform strategy to a governed AWS landing zone with a Terraform delivery pipeline. Each phase has an explicit Entry artifact, Exit artifact, and Gate. Do not advance to the next phase until the Gate is satisfied.

## Phases

### Phase 1 — Platform strategy (skills: `infrastructure-platform`)

**Entry:** Organization and workload requirements.
**Exit:** Platform architecture and landing-zone decisions documented.
**Gate:** Architecture sign-off.

### Phase 2 — Account & network foundation (skills: `aws-account-and-organization-topology`, `aws-network-and-identity-foundation`)

**Entry:** Approved platform strategy.
**Exit:** Organization, OU, and account topology defined; network and identity baseline established.
**Gate:** Security and network review approved.

### Phase 3 — IaC mechanics (skills: `terraform-module-and-repository-scaffold`, `terraform-state-and-secret-management`, `terraform-module-reuse-and-supply-chain`, `terraform-plan-gate-and-policy-as-code`, `terraform-apply-and-promotion-mechanics`)

**Entry:** Phase 2 baseline defined.
**Exit:** Terraform repository scaffold; state and secret strategy; module supply-chain controls; policy-as-code plan gate; promotion mechanics.
**Gate:** Plan gate enforced in CI.

### Phase 4 — Workload & operations (skills: `aws-workload-runtime-and-deployment`, `aws-observability-and-cost-readiness`, `aws-dr-and-multi-region-readiness`)

**Entry:** IaC mechanics in place.
**Exit:** Workload runtime defined; observability and cost guardrails; disaster-recovery and multi-region posture.
**Gate:** DR test executed and cost guardrails reviewed.

## Rules

- Workflows sequence; they do not duplicate skill logic. Procedural detail lives in the linked skills.
- A phase is not complete until its Gate is satisfied.
- If a skill's Quality Checks fail, return to that skill before advancing.
- This is an infrastructure foundation workflow; application delivery is out of scope.
