# AWS DR and Multi-Region Readiness Playbook

Load this when designing any owned area of `aws-dr-and-multi-region-readiness` or checking the anti-pattern list. It expands the operating rules and process steps in `SKILL.md` with the detail needed to produce a rehearsed, production-grade DR posture.

## Why this workflow exists

DR defects are only discovered during the disaster. A "DR plan" that has never been executed fails on the day it matters — the replica was lagging beyond the RPO, the failover record had the wrong health check, the standby was missing an IAM role, the backup had never actually been restored. A single-region tier-0 workload is one regional event from total loss. Conversely, an active-active topology on a tier-2 internal tool burns money for resilience nobody needed. None of this is visible until the region goes down or the invoice arrives.

The goal is a topology sized to the RPO/RTO, replication that meets the RPO, failover that is health-driven and reversible, backups that have been restored, and a drill that has actually been run with the numbers recorded — consuming the reliability and operations posture instead of inventing it. **DR is rehearsed, not aspirational** — a locked infrastructure-tier constraint.

## Behavioral rules in depth

### 1. Consume reliability and operations; do not invent it

RPO/RTO per tier come from `architecture/reliability`; failover ownership and drill cadence from `architecture/operations`. The topology is chosen *to satisfy* the stated RPO/RTO, not by preference. If a needed decision is missing, raise an ADR candidate.

### 2. Extend the foundation and runtime — do not redesign them

`aws-network-and-identity-foundation` built the single-region network/identity; `aws-workload-runtime-and-deployment` built the single-region runtime. This skill extends them cross-region. Re-authoring the single-region VPC or compute here forks two skills' ownership.

### 3. Multi-AZ is the floor; multi-region is tier-driven

Multi-AZ is the non-negotiable baseline for tier-0/1 (the runtime skill set it; confirm it). Multi-region is added only where the tier and RPO/RTO require it. The two failure modes are symmetric defects:

| Defect | Example |
|---|---|
| Under-provisioned | Single-region tier-0 with a 5-minute RTO |
| Over-provisioned | Active-active multi-region for a tier-2 internal tool |

### 4. Topology follows RPO/RTO

| Pattern | Rough RTO | Rough RPO | Cost |
|---|---|---|---|
| Backup & restore | Hours | Hours | Lowest |
| Pilot light | 10s of min | Minutes | Low |
| Warm standby | Minutes | Seconds–min | Medium |
| Active-active | ~0 | ~0 | Highest |

The chosen pattern names the RTO/RPO it satisfies and the cost trade-off. A pattern that cannot meet the stated RTO/RPO is rejected.

### 5. Replication matches the store and the RPO

RDS/Aurora cross-region read replica (or Aurora Global Database), S3 Cross-Region Replication, DynamoDB Global Tables, EBS snapshot copy. Each has a replication-lag budget; if the typical lag exceeds the RPO, the RPO cannot be met and the design is wrong — surface it, do not paper over it.

### 6. Failover is health-driven and reversible

Route 53 health-check-based failover (or Application Recovery Controller) with a defined, tested trigger. The runbook covers promotion of the standby *and the fail-back* to the primary once it recovers. A one-way failover with no rehearsed return is half a plan.

### 7. Backups are immutable, encrypted, restore-tested

AWS Backup with tier-driven retention, cross-region and (for ransomware/account-compromise resilience) cross-account copy, encryption via the foundation CMK strategy, and Vault Lock/immutability where compliance requires. A backup that has never been restored is an assumption, not a recovery capability — restore it in the drill.

### 8. The drill is executed and measured

A failover runbook is necessary but not sufficient. Execute the drill: trigger failover, promote the standby, measure the *achieved* RPO (data loss window) and RTO (time to recovery), exercise fail-back, restore from a backup. Record achieved-vs-target. A gap is reported with an ADR candidate, never hidden.

### 9. An un-rehearsed DR posture is not done

The single completion gate: a drill has actually been run and the numbers recorded. Documentation alone does not satisfy it.

## Step detail

**Step 1 — Gather context.** Load `architecture/reliability` (RPO/RTO per tier) and `architecture/operations` (failover ownership, drill cadence, runbook hook). Resolve tier from `architecture-schema`. Confirm the single-region runtime and observability. Raise an ADR candidate for any missing decision.

**Step 2 — Baseline.** Confirm/specify multi-AZ for tier-0/1 (extend the runtime, do not redesign).

**Step 3 — Topology.** Choose backup-restore / pilot-light / warm-standby / active-active from tier + RPO/RTO; state what it satisfies and the cost trade-off.

**Step 4 — Replication.** Per store: RDS/Aurora replica, S3 CRR, DynamoDB Global Tables, EBS snapshot copy; each with a lag budget meeting the RPO.

**Step 5 — Failover.** Route 53 health-check failover, defined trigger, standby promotion, fail-back path.

**Step 6 — Backups.** AWS Backup: tier retention, cross-region/cross-account copy, foundation-CMK encryption, immutability where required.

**Step 7 — DR observability.** Failover health checks + DR alarms via the observability substrate; capture drill metrics.

**Step 8 — Drill.** Author the runbook; execute the drill; record achieved RPO/RTO vs targets.

**Step 9 — Validate.** Drill meets (or the gap to) targets; backup restore performed; fail-back exercised. Document any check that cannot run.

**Step 10 — Emit & validate.** `dr-multi-region-readiness.md` (baseline, topology + rationale, replication budgets, failover + fail-back, backup posture, drill results vs targets), gap list with ADR candidates, handoff list. Validate against deployment-, observability-, security-standards, naming-conventions, architecture-schema.

## Anti-patterns to detect

Call these out explicitly when found:

- A DR plan with no executed drill and no measured RPO/RTO (aspirational, not readiness)
- Single-region tier-0/1; or active-active for a tier-2 workload (both sized wrong)
- Topology that cannot meet the stated RTO/RPO
- Replication whose typical lag exceeds the RPO
- One-way failover with no rehearsed fail-back path
- Backups never restore-tested; no cross-region (or cross-account) copy
- Backups not encrypted via the foundation CMK strategy
- Single-region foundation/runtime re-authored here instead of extended
- Failover health/alarms not wired through the observability substrate
- Achieved-vs-target RPO/RTO gap hidden instead of reported
- Terraform module/state mechanics authored here (belongs to Family H)
