# Kubernetes Scaling and Resilience Topology — Layout Reference

Use this as the canonical HPA / KEDA / VPA / PDB / affinity pattern reference. Placeholder tokens use `<kebab-case>`. Values are illustrative — replace with the SLOs, replica floors, and budgets from upstream. This skill tunes the baseline the manifest archetype created; node provisioning is out of family.

## Object set layout

```
k8s/
├── hpa.yaml                  # tuned (or KEDA ScaledObject) — replaces the baseline
├── pdb.yaml                  # tier-correct sizing — never drain-deadlocking
├── deployment-patch.yaml     # affinity + topology spread + graceful shutdown patch
scaling-resilience.md         # autoscaler rationale + PDB math + zone posture + shutdown budget
```

## Autoscaler — match the signal

```yaml
# CPU/memory-bound -> HPA on resource metrics
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata: { name: <service-name> }
spec:
  scaleTargetRef: { apiVersion: apps/v1, kind: Deployment, name: <service-name> }
  minReplicas: <reliability-floor>          # from architecture/reliability
  maxReplicas: <performance-envelope>       # from architecture/performance
  metrics:
    - type: Resource
      resource: { name: cpu, target: { type: Utilization, averageUtilization: 70 } }
  behavior:
    scaleDown: { stabilizationWindowSeconds: 300 }   # tuned, not default
    scaleUp:   { stabilizationWindowSeconds: 30 }
```

```yaml
# Event/queue-driven -> KEDA (NOT HPA-on-CPU)
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata: { name: <service-name> }
spec:
  scaleTargetRef: { name: <service-name> }
  minReplicaCount: <reliability-floor>
  maxReplicaCount: <performance-envelope>
  triggers:
    - type: <queue-source>                  # e.g. aws-sqs, kafka, rabbitmq
      metadata: { queueLength: "20" }
```

```yaml
# Right-sizing -> VPA in recommendation mode (does NOT fight HPA)
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata: { name: <service-name> }
spec:
  targetRef: { apiVersion: apps/v1, kind: Deployment, name: <service-name> }
  updatePolicy: { updateMode: "Off" }       # recommendation only unless ADR
```

## PDB — tier-correct, never drain-deadlocking

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata: { name: <service-name> }
spec:
  # WRONG: maxUnavailable: 0  / minAvailable: 100%  -> deadlocks kubectl drain
  minAvailable: <floor - 1>                 # leaves >=1 always evictable
  selector:
    matchLabels: { app.kubernetes.io/name: <service-name> }
```

## Anti-affinity + zone spread (Deployment patch)

```yaml
spec:
  template:
    spec:
      terminationGracePeriodSeconds: 60     # >= longest in-flight request
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:   # required for strict tiers
            - weight: 100
              podAffinityTerm:
                topologyKey: kubernetes.io/hostname
                labelSelector:
                  matchLabels: { app.kubernetes.io/name: <service-name> }
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: ScheduleAnyway  # DoNotSchedule for strict tier-0
          labelSelector:
            matchLabels: { app.kubernetes.io/name: <service-name> }
      containers:
        - name: <service-name>
          lifecycle:
            preStop:
              exec: { command: ["sh", "-c", "sleep 10"] }   # drain before SIGTERM
```

## Handoffs this skill names (does not implement)

| Concern | Owner |
|---|---|
| Base Deployment/Service/HPA/PDB authoring | `k8s-workload-packaging-and-manifest` |
| NetworkPolicy, ServiceAccount RBAC | `k8s-network-and-identity-policy` |
| Metrics pipeline that feeds the autoscaler (Prometheus adapter, ServiceMonitor) | `k8s-observability-and-operations-readiness` |
| Image hardening, signing, admission | `k8s-supply-chain-and-image-hardening` |
| Holistic pre-promotion review | `k8s-deploy-manifest-review` (omnibus) |
| Cluster-autoscaler / Karpenter node provisioning, node pools | Out of Family G — cloud platform stack + Terraform |
