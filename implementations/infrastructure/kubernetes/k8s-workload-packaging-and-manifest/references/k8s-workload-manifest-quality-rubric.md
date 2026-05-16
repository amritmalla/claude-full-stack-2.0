# Kubernetes Workload Packaging and Manifest Quality Rubric

Load this before declaring the manifest set complete. Revise until each check passes or the unresolved gap is explicitly documented in `deploy.md`.

## Workload selection & packaging

- [ ] Workload kind (Deployment / StatefulSet / DaemonSet / Job / CronJob) matches the workload class from `backend-architecture.md` / `infrastructure-platform.md`.
- [ ] The container image came from the matching language sub-skill and is digest-pinnable.
- [ ] `imagePullPolicy` is explicit; no floating `:latest` or mutable tag for any promotable environment.
- [ ] Recommended `app.kubernetes.io/*` labels are set.

## Resources & probes

- [ ] Every container has both `resources.requests` and `resources.limits`, derived from the upstream resource expectation.
- [ ] `startupProbe`, `readinessProbe`, and `livenessProbe` are all present.
- [ ] The three probes are distinct in endpoint and threshold, each serving its own purpose.

## Configuration injection

- [ ] Configuration is injected via ConfigMap; secrets via Secret *references* (names only).
- [ ] No secret values appear in any manifest.
- [ ] No environment-branched manifests with divergent logic; the set is parameterized per env.

## Availability baseline

- [ ] A baseline `HorizontalPodAutoscaler` exists, tier-correct.
- [ ] A `PodDisruptionBudget` exists for any workload with replicas > 1.
- [ ] The sizing/resilience handoff to `k8s-scaling-and-resilience-topology` is explicitly marked.
- [ ] Rolling-update parameters match the tier (`maxUnavailable: 0` for tier-0/1 availability-critical).
- [ ] The upstream release strategy (rolling/blue-green/canary) is honored, not invented; progressive delivery is handed off.

## Security baseline (floor only)

- [ ] Pod-template security context sets `runAsNonRoot`, `readOnlyRootFilesystem`, `allowPrivilegeEscalation: false`, and drops ALL capabilities.
- [ ] A non-default ServiceAccount is referenced (RBAC depth deferred to `k8s-network-and-identity-policy`).
- [ ] Deep image hardening, signing, SBOM, and admission control are named handoffs to `k8s-supply-chain-and-image-hardening`, not implemented here.

## Verification & handoffs

- [ ] `kubectl apply --dry-run=server` passes (or an offline schema/policy lint passes and the gap is documented).
- [ ] `deploy.md` declares the rollout strategy and rollback procedure.
- [ ] NetworkPolicy/RBAC depth, autoscaling sizing, observability wiring, image hardening, and cluster provisioning are all named handoffs — none implemented here.

## Standards conformance

- [ ] [deployment-standards](../../../../../standards/deployment-standards/README.md): rolling-update default; tier-0 canary/blue-green per upstream; probes mandatory; rollback declared; env-agnostic.
- [ ] [security-standards](../../../../../standards/security-standards/README.md): security-context baseline; non-default ServiceAccount; no secret values in manifests.
- [ ] [observability-standards](../../../../../standards/observability-standards/README.md): logs to stdout; scrape annotation or ServiceMonitor seam present (full wiring deferred).
- [ ] [naming-conventions](../../../../../standards/naming-conventions/README.md): `kebab-case` names suffixed by kind when ambiguous.
- [ ] [architecture-schema](../../../../../standards/architecture-schema/README.md): tier classification drove replica and PDB defaults.

## Failure handling

If a check fails:

1. Identify the missing or incorrect manifest element.
2. Ask the user for clarification if the decision cannot be inferred from `infrastructure-platform.md` or `backend-architecture.md`.
3. Revise the manifest, re-run the server-side dry-run / schema lint.
4. Keep any unresolved gap explicit in `deploy.md` — do not hide it as an assumption.
