# Kubernetes Observability and Operations Readiness Playbook

Load this when wiring any owned signal of `k8s-observability-and-operations-readiness` or checking the anti-pattern list. It expands the operating rules and process steps in `SKILL.md` with the detail needed to make a workload genuinely operable in production.

## Why this workflow exists

The cost of missing observability is paid once, at the worst time. A workload with no scrape wiring is a black box during its first incident — the on-call engineer is guessing. Logs that ship unstructured cannot be queried under pressure. Traces with no propagation stop at the first hop, so the slow dependency is invisible. An alert with no runbook wakes someone who does not know what to do. kube-state-metrics absent means an eviction storm is only noticed when users complain. None of this is felt until production breaks and the telemetry that would explain it does not exist.

The goal is a workload that emits all three signals, alerts only on things that matter with a runbook attached, and exposes the platform failure modes — consuming the operations substrate instead of inventing it.

## Behavioral rules in depth

### 1. Consume operations and reliability; do not invent it

The observability substrate, alert destinations, and runbook hooks come from `architecture/operations`; SLOs and error budgets from `architecture/reliability`. Alert thresholds are derived from the SLO, not picked. If a needed decision is missing, raise an ADR candidate.

### 2. The backend is consumed, not chosen

ServiceMonitor targets the Prometheus the platform runs; the log shipper targets the named log backend; the collector exports to the named tracing backend. "Should we use Datadog or Prometheus" is an upstream decision — a missing substrate is an ADR candidate, never a default this skill picks.

### 3. Three signals, every workload

| Signal | Wiring | Failure if absent |
|---|---|---|
| Metrics | ServiceMonitor/PodMonitor scrape (CRD where the stack supports it, not bare annotations) | Black box in incidents |
| Logs | stdout → structured shipper → backend | Cannot query under pressure |
| Traces | OTel emit + context propagation | Slow dependency invisible past hop 1 |

A workload missing one is not operations-ready.

### 4. Alerts are SLO-tied and actionable

Every alert rule maps to an SLO (latency/availability/error-budget burn) or a concrete known failure mode. It carries a tier-derived severity, a destination from the upstream alert config, and the name of the runbook to follow. A threshold alert with no runbook and no SLO is noise and is rejected — it trains on-call to ignore alerts.

### 5. Cover the platform, not just the app

App latency is not enough. Wire kube-state-metrics (pod/deployment/replica state, restart counts), cAdvisor (container CPU/memory throttling), and node-pressure conditions. Eviction storms, OOMKills, and node MemoryPressure must be visible as first-class signals — they cause "the app is slow" without any app metric moving.

### 6. Logs are structured and PII-safe in the pipeline

Ship JSON, not free text. Inject the trace and span ID so a log line jumps to its trace. Redact secrets and PII in the shipper config — not "downstream will handle it." A token in a log line shipped to a third-party backend is an incident.

### 7. Audit collection is scoped; enablement is handed off

Collect the workload/namespace-relevant audit events: RBAC denials, the policy-deny events the network archetype produces, admission rejections. *Enabling* the API-server audit policy (a control-plane file/flag) is not this skill's ownership — name the handoff to the control-plane owner.

### 8. Runbook inputs are concrete, structured, dry-runnable

For each named incident class, produce: the signal that fires, the exact query to confirm it, the first diagnostic step, and the escalation path — as structured input the operations runbook consumes. Prose ("investigate the pods") is not a runbook input. The three required classes: pod-eviction storms, ImagePullBackOff sprees, node-pressure incidents.

### 9. Untested observability is not observability

Test-fire each alert with a synthetic breach and confirm it actually routes to the destination (a rule that does not fire, or fires into the void, is worse than none). Dry-run each runbook input against the live signals so the query and first step are known-good. Unverified wiring is unverified.

## Step detail

**Step 1 — Gather context.** Load `architecture/operations` (substrate, destinations, runbook hooks) and `architecture/reliability` (SLOs, error budgets). Resolve tier from `architecture-schema`. Confirm the workload exposes a metrics port and stdout logs. Raise an ADR candidate for any missing decision.

**Step 2 — Metrics.** ServiceMonitor/PodMonitor scrape; confirm kube-state-metrics and cAdvisor coverage.

**Step 3 — Logs.** Upstream-named shipper: stdout → structured JSON → trace/span ID injection → PII/secret redaction → named backend.

**Step 4 — Traces.** OTel collector, upstream propagation format, tier-correct sampling; verify trace↔log correlation.

**Step 5 — SLO alerts.** Each tied to an SLO/failure mode, tier severity, upstream destination, named runbook. No orphans.

**Step 6 — Platform signals.** Node-pressure, eviction, ImagePullBackOff coverage.

**Step 7 — Audit scope.** Collect workload/namespace RBAC-deny, policy-deny, admission-reject; hand off API-server audit-policy enablement.

**Step 8 — Runbook inputs.** Concrete signal→query→first-step→escalation for the three incident classes.

**Step 9 — Verify.** Test-fire each alert to its destination; dry-run each runbook input. Document any check that cannot run.

**Step 10 — Emit & validate.** Wiring under `k8s/observability/`, `operations-readiness.md` (signal inventory, alert→SLO→runbook map, sampling/retention), handoff list. Validate against observability-, deployment-standards, naming-conventions, architecture-schema.

## Anti-patterns to detect

Call these out explicitly when found:

- A workload missing any of the three signals (metrics / logs / traces)
- Bare scrape annotations where the stack supports ServiceMonitor CRDs and the platform expects them
- Choosing the observability backend here instead of consuming the upstream substrate
- An alert with no SLO/failure-mode mapping and no named runbook (orphan threshold)
- Only app metrics; no kube-state-metrics / cAdvisor / node-pressure coverage
- Unstructured logs, or logs with no trace/span correlation IDs
- Secrets/PII shipped in logs (no in-pipeline redaction)
- API-server audit-policy enablement attempted here instead of handed off
- Runbook "inputs" written as prose instead of signal→query→step→escalation
- Alerts never test-fired; runbook inputs never dry-run
- Cluster provisioning / control-plane audit enablement authored here (out of Family G)
