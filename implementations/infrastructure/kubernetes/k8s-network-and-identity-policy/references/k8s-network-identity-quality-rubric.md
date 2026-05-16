# Kubernetes Network and Identity Policy Quality Rubric

Load this before declaring the policy set complete. Revise until each check passes or the unresolved gap is explicitly documented in `network-identity.md`.

## NetworkPolicy

- [ ] Every workload-carrying namespace has a default-deny NetworkPolicy (ingress, and egress where the posture requires).
- [ ] Every allow is label-selected and minimal; none use `podSelector: {}` allow-all.
- [ ] Every allow is annotated with the named peer and the reason.
- [ ] DNS egress (port 53) is explicitly allowed where egress is denied by default.
- [ ] Internet egress, if any, is CIDR-scoped and justified — no blanket `0.0.0.0/0` without an ADR.

## Identity & RBAC

- [ ] A dedicated ServiceAccount is used; the `default` ServiceAccount is not used.
- [ ] The bound role is a namespace `Role` unless a named reason justifies a `ClusterRole`.
- [ ] Verbs and resources are least-privilege; wildcards (`*`) have a named ADR reason.
- [ ] An RBAC review (`kubectl auth can-i --list` as the SA) shows no excess permission.

## Registry auth & mTLS

- [ ] Image-pull auth uses the platform short-lived path where supported.
- [ ] Any long-lived static registry credential is an ADR-justified exception and is namespace-scoped, not broadly mounted.
- [ ] The mTLS posture is explicit: mesh `STRICT` with a concrete enforcement object, or a stated no-mesh east-west decision.

## Pod Security Standards & exposure

- [ ] The namespace enforces Pod Security Standards (`enforce: restricted` baseline) with `audit`/`warn` set.
- [ ] The extended admission-policy engine (Kyverno/Gatekeeper) is handed off to `k8s-supply-chain-and-image-hardening`, not implemented here.
- [ ] An Ingress/Gateway exists only where the workload is externally reached.
- [ ] External exposure uses TLS/host/path from the platform traffic shape; no accidental public Service.

## Verification & handoffs

- [ ] A connectivity test confirms an allowed peer reaches the workload and a denied peer is blocked, or the gap is documented.
- [ ] `network-identity.md` documents the allowed-flow matrix, RBAC rationale, and mTLS posture.
- [ ] Workload manifests, autoscaling, observability wiring, and the admission-policy engine are named handoffs — none implemented here.
- [ ] Cluster provisioning / CNI installation is not present (out of Family G).

## Standards conformance

- [ ] [security-standards](../../../../../standards/security-standards/README.md): default-deny NetworkPolicy, least-privilege RBAC, non-default ServiceAccount, no broadly-mounted long-lived registry credentials, explicit mTLS.
- [ ] [deployment-standards](../../../../../standards/deployment-standards/README.md): NetworkPolicy present by default; policy reproducible via manifests.
- [ ] [observability-standards](../../../../../standards/observability-standards/README.md): policy-deny / authz-failure events observable (seam present; full wiring deferred).
- [ ] [naming-conventions](../../../../../standards/naming-conventions/README.md): policy, ServiceAccount, Role/Binding names `kebab-case`, kind-suffixed when ambiguous.
- [ ] [architecture-schema](../../../../../standards/architecture-schema/README.md): tier classification drove isolation granularity and RBAC strictness.

## Failure handling

If a check fails:

1. Identify the missing or over-broad policy element.
2. Ask the user for clarification if the decision cannot be inferred from `architecture/security` or `infrastructure-platform.md`.
3. Revise the policy, re-run the connectivity test and RBAC review.
4. Keep any unresolved gap explicit in `network-identity.md` — do not hide it as an assumption.
