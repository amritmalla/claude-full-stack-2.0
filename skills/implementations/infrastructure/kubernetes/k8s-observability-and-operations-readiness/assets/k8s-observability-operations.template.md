# Kubernetes Observability and Operations Readiness — Layout Reference

Use this as the canonical ServiceMonitor / log / trace / alert / runbook pattern reference. Placeholder tokens use `<kebab-case>`. The substrate is consumed from upstream — these patterns target whatever `architecture/operations` named. This skill wires workload/namespace collection; cluster/control-plane provisioning is out of family.

## Wiring layout

```
k8s/observability/
├── servicemonitor.yaml       # scrape wiring (or substrate equivalent)
├── prometheusrule.yaml       # SLO-tied alert rules, each with a runbook ref
├── log-shipper-config.yaml   # Fluent Bit / Vector / cloud-native — structured + redacted
├── otel-collector.yaml       # trace collector + propagation + sampling
└── audit-collection.yaml     # workload/namespace audit events (enablement handed off)
operations-readiness.md       # signal inventory + alert->SLO->runbook map + sampling/retention
runbooks/                     # concrete inputs for the three incident classes
```

## Metrics scrape — CRD, not bare annotations

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: <service-name>
  labels: { release: <prometheus-release-from-upstream> }
spec:
  selector:
    matchLabels: { app.kubernetes.io/name: <service-name> }
  endpoints:
    - port: metrics
      interval: 30s
# Confirm cluster-wide: kube-state-metrics + cAdvisor are scraped so object
# state and container throttling are visible — not only app latency.
```

## SLO-tied alert — every rule names a runbook

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata: { name: <service-name>-slo }
spec:
  groups:
    - name: <service-name>.slo
      rules:
        - alert: <ServiceName>ErrorBudgetBurnFast
          expr: |
            (sum(rate(http_requests_total{job="<service-name>",code=~"5.."}[5m]))
             / sum(rate(http_requests_total{job="<service-name>"}[5m]))) > 0.02
          for: 5m
          labels: { severity: <tier-severity> }          # from architecture-schema
          annotations:
            slo: "availability 99.5%"                     # mapped to a real SLO
            runbook: "runbooks/error-budget-burn.md"      # NOT an orphan threshold
```

## Log shipping — structured, correlated, redacted

```yaml
# Fluent Bit example (use the upstream-named shipper). Key requirements:
#  - parse stdout to JSON
#  - inject trace_id / span_id for log<->trace correlation
#  - redact secrets/PII IN THE PIPELINE (not "downstream")
[FILTER]
    Name    modify
    Match   *
    Remove  password
    Remove  authorization
[OUTPUT]
    Name    <loki|es|cloud-native-from-upstream>
    Match   *
```

## Trace collector — propagation + tier sampling

```yaml
apiVersion: opentelemetry.io/v1beta1
kind: OpenTelemetryCollector
metadata: { name: <service-name> }
spec:
  config:
    receivers:  { otlp: { protocols: { http: {}, grpc: {} } } }
    processors: { probabilistic_sampler: { sampling_percentage: <tier-rate> } }
    exporters:  { otlp: { endpoint: "<tracing-backend-from-upstream>" } }
# Propagation format (W3C tracecontext / B3) per upstream; trace_id must match
# the ID injected into logs above.
```

## Runbook input — concrete, not prose

```markdown
## Incident: pod-eviction storm
- Fires:   KubeletEvictionRate > 0 for 10m  (kube-state-metrics)
- Confirm: kubectl get events --field-selector reason=Evicted -A | sort
- First:   check node MemoryPressure/DiskPressure; identify the noisy pod
- Escalate: <on-call path from architecture/operations>
```
(Repeat for **ImagePullBackOff sprees** and **node-pressure incidents**.)

## Handoffs this skill names (does not implement)

| Concern | Owner |
|---|---|
| Base Deployment/Service authoring, metrics-port exposure | `k8s-workload-packaging-and-manifest` |
| NetworkPolicy/RBAC (produces the policy-deny events collected here) | `k8s-network-and-identity-policy` |
| Autoscaler that consumes these metrics | `k8s-scaling-and-resilience-topology` |
| Image hardening, signing, admission | `k8s-supply-chain-and-image-hardening` |
| Observability backend/substrate selection | Upstream — `infrastructure-platform.md` / `architecture/operations` |
| API-server audit-policy enablement, cluster provisioning | Out of Family G — control-plane owner / cloud platform stack + Terraform |
