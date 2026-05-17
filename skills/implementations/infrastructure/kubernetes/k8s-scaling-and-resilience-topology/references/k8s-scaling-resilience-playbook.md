# Kubernetes Scaling and Resilience Topology Playbook

Load this when tuning any owned object of `k8s-scaling-and-resilience-topology` or checking the anti-pattern list. It expands the operating rules and process steps in `SKILL.md` with the detail needed to produce a production-grade scaling and resilience posture.

## Why this workflow exists

Scaling and resilience defects stay invisible until the worst moment. An HPA on CPU for a queue-draining worker never scales because CPU is low while the queue explodes. A PDB of `maxUnavailable: 0` deadlocks every node drain, so a routine cluster upgrade stalls cluster-wide. No anti-affinity means three "replicas" landed on one node that just died. No `preStop` means every rollout drops in-flight requests. None of this fails a functional test — it fails at 2 a.m. during a node rotation or a traffic spike.

The goal is a posture that scales on the right signal, survives a node drain and a zone loss, and rolls out without dropping traffic — consuming reliability and performance decisions instead of inventing them.

## Behavioral rules in depth

### 1. Consume reliability and performance; do not invent it

SLOs, replica floors, and disruption budgets come from `architecture/reliability`; resource and latency targets from `architecture/performance`. The replica floor and the PDB tolerance are reliability decisions, not tuning preferences. If a needed decision is missing, raise an ADR candidate.

### 2. The autoscaler matches the scaling signal

| Scaling signal | Autoscaler | Why |
|---|---|---|
| CPU/memory-bound request load | HPA on resource metrics | Load tracks CPU/memory |
| Queue depth / event rate | KEDA on the event source | CPU is flat while backlog grows |
| Chronically mis-sized requests | VPA (`recommendation`) | Right-sizes requests; not a load response |

HPA for a queue worker is the canonical mismatch — it under-scales under backlog.

### 3. HPA and VPA must not fight

VPA in `auto`/`recreate` mutating CPU/memory while HPA scales on CPU is a documented conflict: VPA shrinks the request, HPA sees higher utilization, they oscillate. Keep VPA in `recommendation` mode, or scope VPA to a dimension HPA does not use, unless an ADR explicitly resolves the interaction.

### 4. A PDB must never deadlock a drain

The PDB protects availability *during voluntary disruption* — it does not forbid it. `maxUnavailable: 0` or `minAvailable: 100%` means the eviction API can never proceed, so `kubectl drain` hangs forever and blocks node upgrades cluster-wide. Size it relative to the replica floor: enough always-available, at least one always-evictable.

### 5. Replicas have a floor and never co-locate

The floor is the reliability tier's minimum. Every multi-replica workload carries pod anti-affinity (soft or hard per tier) plus a topology-spread constraint so replicas do not pile onto one node — otherwise N replicas is one node failure from zero.

### 6. Multi-zone is the tier-0/1 default

Spread across `topology.kubernetes.io/zone`. `whenUnsatisfiable: DoNotSchedule` for strict tiers (correctness over placement); `ScheduleAnyway` where staying up beats perfect balance. A tier-0 workload pinned to one zone is one AZ outage from down.

### 7. Graceful shutdown is wired, not hoped for

On termination Kubernetes sends SIGTERM, waits `terminationGracePeriodSeconds`, then SIGKILL. Without a `preStop` hook (or a readiness flip that drains the endpoint first) the pod keeps receiving traffic as it dies. Wire: readiness false → `preStop` sleep/drain → process handles SIGTERM → grace period covers the longest in-flight request.

### 8. Rollout budgets are distinct from the PDB

`maxUnavailable`/`maxSurge` in the Deployment strategy governs *rollouts*; the PDB governs *voluntary disruptions*. Tier-0/1: `maxUnavailable: 0` (surge a new pod before terminating an old one). Surge is bounded where node capacity is tight.

### 9. A posture not drain- and scale-tested is not done

Simulate a node drain (`kubectl drain --ignore-daemonsets` or cordon + delete a pod): the PDB must hold and the SLO must not breach. Trigger a scale event (load or queue depth): the autoscaler must react within the stabilization window. Untested resilience is unverified.

## Step detail

**Step 1 — Gather context.** Load `architecture/reliability` (SLOs, replica floors, disruption budgets) and `architecture/performance` (resource/latency). Resolve tier from `architecture-schema`. Confirm the baseline HPA/PDB exists. Raise an ADR candidate for any missing decision.

**Step 2 — Select the autoscaler.** Map the scaling signal to HPA / KEDA / VPA-recommendation; resolve any HPA/VPA dimension conflict.

**Step 3 — Tune HPA/KEDA.** Min = reliability floor; max = performance/capacity envelope; target metric + stabilization windows so it neither flaps nor lags the SLO.

**Step 4 — Size the PDB.** Tier-correct; a voluntary drain can still proceed; consistent with the replica floor.

**Step 5 — Anti-affinity + spread.** Replicas do not co-locate; tier-0/1 spread across zones with tier-correct `whenUnsatisfiable`.

**Step 6 — Graceful shutdown.** `terminationGracePeriodSeconds` covers the longest in-flight request; `preStop`/readiness-drain deregisters before SIGTERM.

**Step 7 — Rollout budgets.** Surge/`maxUnavailable` per tier, bounded by cluster capacity, distinct from the PDB.

**Step 8 — Verify.** Simulated node drain (PDB honored, no SLO breach) + scale event (reacts within stabilization). Document any check that cannot run.

**Step 9 — Emit & validate.** Tuned objects under `k8s/`, `scaling-resilience.md` (autoscaler rationale, PDB math, zone posture, shutdown budget), handoff list. Validate against deployment-, observability-standards, naming-conventions, architecture-schema.

## Anti-patterns to detect

Call these out explicitly when found:

- HPA on CPU for an event/queue-driven worker (should be KEDA)
- VPA in `auto` managing the same dimension HPA scales on, with no ADR
- PDB `maxUnavailable: 0` / `minAvailable: 100%` (deadlocks node drains)
- Multi-replica workload with no anti-affinity / no topology-spread (co-location risk)
- Tier-0/1 workload not spread across zones
- No `preStop`/readiness-drain — rollouts and scale-downs drop in-flight traffic
- `terminationGracePeriodSeconds` shorter than the longest in-flight request
- Rollout `maxUnavailable > 0` on an availability-critical workload
- HPA min below the reliability replica floor
- Cluster-autoscaler / Karpenter *node* provisioning authored here (out of Family G)
- Posture declared done with no simulated-drain or scale-event test
