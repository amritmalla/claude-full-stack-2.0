# Kubernetes Observability and Operations Readiness Quality Rubric

Load this before declaring the workload operations-ready. Revise until each check passes or the unresolved gap is explicitly documented in `operations-readiness.md`.

## Three signals

- [ ] Metrics are scraped via ServiceMonitor/PodMonitor (or the substrate's CRD equivalent), not bare annotations where CRDs are expected.
- [ ] kube-state-metrics and cAdvisor coverage is present (object state + container resource visible).
- [ ] Logs ship from stdout as structured JSON to the named backend.
- [ ] Shipped logs carry trace/span correlation IDs and are PII/secret-redacted in-pipeline.
- [ ] Traces are emitted with the upstream propagation format and tier-correct sampling; trace↔log IDs correlate.

## Alerts

- [ ] Every alert rule maps to an SLO or a concrete known failure mode.
- [ ] Every alert has a tier-derived severity and a destination from the upstream alert config.
- [ ] Every alert names the runbook to follow — no orphan thresholds.
- [ ] Each alert was test-fired with a synthetic breach and confirmed to route to its destination, or the gap is documented.

## Platform & audit

- [ ] Node-pressure, eviction, and ImagePullBackOff signals are covered.
- [ ] Workload/namespace audit events (RBAC-deny, policy-deny, admission-reject) are collected.
- [ ] API-server audit-policy enablement is handed off to the control-plane owner, not attempted here.

## Runbook inputs

- [ ] Concrete input exists for pod-eviction storms (signal → query → first step → escalation).
- [ ] Concrete input exists for ImagePullBackOff sprees.
- [ ] Concrete input exists for node-pressure incidents.
- [ ] Each runbook input was dry-run against the live signals, or the gap is documented.

## Verification & handoffs

- [ ] `operations-readiness.md` documents the signal inventory, the alert→SLO→runbook map, and sampling/retention.
- [ ] The observability substrate is the one named upstream (or an ADR candidate is raised).
- [ ] Base manifests, network/identity, autoscaler tuning, image hardening, and substrate selection are named handoffs — none implemented here.

## Standards conformance

- [ ] [observability-standards](../../../../../../standards/observability-standards/README.md): metrics scraped, structured logs shipped, traces propagated, SLO-tied alerts, trace/log correlation.
- [ ] [deployment-standards](../../../../../../standards/deployment-standards/README.md): observability wiring is reproducible manifests, not click-ops; env-agnostic.
- [ ] [naming-conventions](../../../../../../standards/naming-conventions/README.md): ServiceMonitor/alert/dashboard names `kebab-case`, kind-suffixed when ambiguous.
- [ ] [architecture-schema](../../../../../../standards/architecture-schema/README.md): tier classification drove alert severity, retention, and sampling rate.

## Failure handling

If a check fails:

1. Identify the missing signal, orphan alert, or absent runbook input.
2. Ask the user for clarification if the decision cannot be inferred from `architecture/operations` or `architecture/reliability`.
3. Revise the wiring, re-test-fire the affected alerts and re-dry-run the runbook inputs.
4. Keep any unresolved gap explicit in `operations-readiness.md` — do not hide it as an assumption.
