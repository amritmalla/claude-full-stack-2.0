# Kubernetes Workload Packaging and Manifest — Layout Reference

Use this as the canonical manifest-set and pattern reference. Placeholder tokens use `<kebab-case>` or `<PascalCase>`. Values shown are illustrative defaults — replace with the tier and resource envelope from upstream. This skill authors the set; sizing, hardening, network, and observability depth are handed off.

## Manifest set layout

```
k8s/
├── deployment.yaml            # or statefulset / daemonset / job / cronjob per class
├── service.yaml               # ClusterIP unless upstream declares external
├── ingress.yaml               # only where externally reached
├── hpa.yaml                   # BASELINE — sizing handed to scaling archetype
├── pdb.yaml                   # required when replicas > 1
├── configmap.yaml             # config only — never secret values
└── kustomization.yaml         # per-env overlay parameterization (no logic branches)
deploy.md                      # rollout strategy + rollback + handoff list
```

## Controller — kind follows the class

```yaml
apiVersion: apps/v1
kind: Deployment                 # StatefulSet / DaemonSet / Job / CronJob per class
metadata:
  name: <service-name>
  labels:
    app.kubernetes.io/name: <service-name>
    app.kubernetes.io/part-of: <system-name>
spec:
  replicas: <tier-default>       # from architecture-schema tier
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 0          # tier-0/1 availability-critical: surge before terminate
      maxSurge: 1
  selector:
    matchLabels: { app.kubernetes.io/name: <service-name> }
  template:
    metadata:
      labels: { app.kubernetes.io/name: <service-name> }
    spec:
      serviceAccountName: <service-name>-sa      # non-default; RBAC depth -> archetype 2
      securityContext:                            # FLOOR — deep hardening -> archetype 5
        runAsNonRoot: true
        seccompProfile: { type: RuntimeDefault }
      containers:
        - name: <service-name>
          image: <registry>/<service-name>@sha256:<digest>   # digest-pinned
          imagePullPolicy: IfNotPresent
          securityContext:
            readOnlyRootFilesystem: true
            allowPrivilegeEscalation: false
            capabilities: { drop: [ALL] }
          resources:
            requests: { cpu: "<from-upstream>", memory: "<from-upstream>" }
            limits:   { cpu: "<from-upstream>", memory: "<from-upstream>" }
          startupProbe:                            # slow-init budget
            httpGet: { path: /health/startup, port: http }
            failureThreshold: 30
            periodSeconds: 2
          readinessProbe:                          # traffic gate (distinct endpoint)
            httpGet: { path: /health/ready, port: http }
            periodSeconds: 5
          livenessProbe:                           # hang restart (distinct endpoint)
            httpGet: { path: /health/live, port: http }
            periodSeconds: 10
          envFrom:
            - configMapRef: { name: <service-name>-config }
          env:
            - name: DB_PASSWORD                    # REFERENCE only — no value here
              valueFrom:
                secretKeyRef: { name: <service-name>-secrets, key: db-password }
```

## Baseline HPA — sizing handed off

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: <service-name>
  # NOTE: baseline only. Target metrics, min/max, VPA/KEDA selection ->
  # handed off to k8s-scaling-and-resilience-topology.
spec:
  scaleTargetRef: { apiVersion: apps/v1, kind: Deployment, name: <service-name> }
  minReplicas: <tier-default>
  maxReplicas: <tier-default x N>
  metrics:
    - type: Resource
      resource: { name: cpu, target: { type: Utilization, averageUtilization: 70 } }
```

## PDB — required when replicas > 1

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: <service-name>
spec:
  maxUnavailable: 1              # tier-correct default; sizing -> scaling archetype
  selector:
    matchLabels: { app.kubernetes.io/name: <service-name> }
```

## Handoffs this skill names (does not implement)

| Concern | Owner |
|---|---|
| NetworkPolicy, ServiceAccount RBAC depth, ingress/mesh identity | `k8s-network-and-identity-policy` |
| HPA/VPA/KEDA sizing, PDB sizing, anti-affinity, topology spread, graceful shutdown | `k8s-scaling-and-resilience-topology` |
| ServiceMonitor/PodMonitor, log shipping, tracing wiring, runbooks | `k8s-observability-and-operations-readiness` |
| Minimal/non-root image build, cosign signing, SBOM, Trivy gate, Kyverno/Gatekeeper admission | `k8s-supply-chain-and-image-hardening` |
| Container build (language-specific) | `dockerfile-and-jvm-tuning` + planned non-JVM siblings |
| Holistic pre-promotion review | `k8s-deploy-manifest-review` (omnibus) |
| Cluster provisioning, node pools, control plane | Out of Family G — cloud platform stack + Terraform |
