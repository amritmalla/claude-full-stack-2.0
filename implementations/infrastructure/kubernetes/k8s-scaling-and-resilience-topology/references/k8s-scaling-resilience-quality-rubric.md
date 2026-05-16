# Kubernetes Scaling and Resilience Topology Quality Rubric

Load this before declaring the scaling and resilience posture complete. Revise until each check passes or the unresolved gap is explicitly documented in `scaling-resilience.md`.

## Autoscaler selection & tuning

- [ ] The autoscaler matches the scaling signal (HPA resource/custom, KEDA event/queue, VPA recommendation).
- [ ] The choice is justified against the workload's scaling shape in `scaling-resilience.md`.
- [ ] HPA and VPA do not both manage the same dimension; VPA defaults to `recommendation` unless an ADR resolves the interaction.
- [ ] HPA/KEDA `min` equals the reliability replica floor; `max` comes from the performance/capacity envelope.
- [ ] Stabilization windows are tuned so the autoscaler neither flaps nor lags the SLO.

## Disruption budget

- [ ] A PDB exists and is tier-correct.
- [ ] A voluntary node drain can still proceed — no `maxUnavailable: 0` / `minAvailable: 100%` deadlock.
- [ ] The PDB is consistent with the replica floor (enough always-available, at least one always-evictable).

## Placement & zone topology

- [ ] Multi-replica workloads carry pod anti-affinity (hard/soft per tier).
- [ ] A topology-spread constraint prevents replica co-location on one node.
- [ ] Tier-0/1 workloads spread across zones (`topology.kubernetes.io/zone`) with tier-correct `whenUnsatisfiable`.

## Graceful shutdown & rollout

- [ ] `terminationGracePeriodSeconds` covers the longest in-flight request.
- [ ] A `preStop` hook or readiness-flip drain deregisters the pod before SIGTERM.
- [ ] Rollout `maxUnavailable`/`maxSurge` matches the tier and is bounded by cluster capacity.
- [ ] Rollout budgets are distinct from the PDB (one governs rollouts, the other voluntary disruptions).

## Verification & handoffs

- [ ] A simulated node drain honors the PDB with no SLO breach, or the gap is documented.
- [ ] A scale event shows the autoscaler reacting within the stabilization window, or the gap is documented.
- [ ] `scaling-resilience.md` documents autoscaler rationale, PDB math, zone posture, and shutdown budget.
- [ ] Base manifests, network/identity, metrics pipeline, image hardening, and the node-autoscaler layer are named handoffs — none implemented here.

## Standards conformance

- [ ] [deployment-standards](../../../../../standards/deployment-standards/README.md): rollout surge/unavailable per tier; graceful shutdown drops no traffic; rollback unaffected.
- [ ] [observability-standards](../../../../../standards/observability-standards/README.md): the autoscaler metric source is named and observable (pipeline wiring deferred).
- [ ] [naming-conventions](../../../../../standards/naming-conventions/README.md): HPA/PDB/constraint names `kebab-case`, kind-suffixed when ambiguous.
- [ ] [architecture-schema](../../../../../standards/architecture-schema/README.md): tier classification drove PDB strictness, replica floor, and zone-spread enforcement.

## Failure handling

If a check fails:

1. Identify the mis-sized or missing scaling/resilience element.
2. Ask the user for clarification if the decision cannot be inferred from `architecture/reliability` or `architecture/performance`.
3. Revise the object, re-run the simulated-drain and scale-event tests.
4. Keep any unresolved gap explicit in `scaling-resilience.md` — do not hide it as an assumption.
