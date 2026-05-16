# Kubernetes Network and Identity Policy — Layout Reference

Use this as the canonical NetworkPolicy / RBAC / PSS pattern reference. Placeholder tokens use `<kebab-case>`. Values are illustrative — replace with the trust zones, peer set, and tier from upstream. This skill authors policy; the admission-policy engine, workload manifests, scaling, and observability are handed off.

## Policy set layout

```
k8s/
├── networkpolicy-default-deny.yaml   # all-pods deny baseline
├── networkpolicy-allow-<peer>.yaml   # one explicit, annotated allow per flow
├── serviceaccount.yaml               # dedicated SA (never default)
├── role.yaml                         # least-privilege Role (ClusterRole = named reason)
├── rolebinding.yaml
├── imagepull-secret.yaml             # short-lived registry-auth reference
└── namespace-pss.yaml                # Pod Security Standards enforce labels
network-identity.md                   # allowed-flow matrix + RBAC rationale + mTLS posture
```

## Default-deny baseline (carve allows from this)

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
  namespace: <namespace>
spec:
  podSelector: {}                 # all pods in the namespace
  policyTypes: [Ingress, Egress]  # Egress included where the posture requires
  # No ingress/egress rules => deny all. Allows are added by separate policies.
```

## Explicit allow — label-selected, annotated

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-<peer>-to-<service>
  namespace: <namespace>
  annotations:
    policy.reason: "<peer> calls <service> for <named reason>"   # justification
spec:
  podSelector:
    matchLabels: { app.kubernetes.io/name: <service-name> }
  policyTypes: [Ingress]
  ingress:
    - from:
        - podSelector:
            matchLabels: { app.kubernetes.io/name: <peer-name> }
      ports: [{ port: http }]
---
# DNS egress is REQUIRED under default-deny egress, or resolution breaks:
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: { name: allow-dns-egress, namespace: <namespace> }
spec:
  podSelector: {}
  policyTypes: [Egress]
  egress:
    - to: [{ namespaceSelector: {} }]
      ports: [{ port: 53, protocol: UDP }, { port: 53, protocol: TCP }]
```

## Least-privilege identity — Role is the default

```yaml
apiVersion: v1
kind: ServiceAccount
metadata: { name: <service-name>-sa, namespace: <namespace> }
automountServiceAccountToken: false   # opt in only if the workload calls the API
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role                            # ClusterRole only with a named reason
metadata: { name: <service-name>-role, namespace: <namespace> }
rules:
  - apiGroups: [""]
    resources: ["configmaps"]
    resourceNames: ["<service-name>-config"]   # scope to the exact object
    verbs: ["get", "watch"]                     # no wildcard verbs
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata: { name: <service-name>-rb, namespace: <namespace> }
roleRef: { apiGroup: rbac.authorization.k8s.io, kind: Role, name: <service-name>-role }
subjects:
  - kind: ServiceAccount
    name: <service-name>-sa
```

## Pod Security Standards — namespace floor (engine extension handed off)

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: <namespace>
  labels:
    pod-security.kubernetes.io/enforce: restricted   # built-in floor
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
# Extended custom policy (Kyverno/Gatekeeper) -> k8s-supply-chain-and-image-hardening
```

## mTLS posture — explicit, with an enforcement object

```yaml
# Mesh adopted (example: Istio). STRICT, not PERMISSIVE.
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata: { name: default, namespace: <namespace> }
spec:
  mtls: { mode: STRICT }
# No mesh -> state the east-west decision in network-identity.md
# (native TLS / CNI encryption / accepted-risk ADR). Do not leave implied.
```

## Handoffs this skill names (does not implement)

| Concern | Owner |
|---|---|
| Deployment/Service/HPA/PDB authoring | `k8s-workload-packaging-and-manifest` |
| HPA/VPA sizing, anti-affinity, topology spread, graceful shutdown | `k8s-scaling-and-resilience-topology` |
| ServiceMonitor, log shipping, tracing, policy-deny audit wiring | `k8s-observability-and-operations-readiness` |
| Image hardening, cosign, SBOM, Kyverno/Gatekeeper admission policy | `k8s-supply-chain-and-image-hardening` |
| Holistic pre-promotion review | `k8s-deploy-manifest-review` (omnibus) |
| Cluster provisioning, CNI installation, control plane | Out of Family G — cloud platform stack + Terraform |
