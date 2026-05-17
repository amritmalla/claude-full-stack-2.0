# Kubernetes Supply Chain and Image Hardening — Layout Reference

Use this as the canonical image / signing / SBOM / scan / admission pattern reference. Placeholder tokens use `<kebab-case>`. Tools shown are illustrative — replace with the upstream-named registry, signer, scanner, and admission engine. This skill defines the gate and admission policy; the CI pipeline that runs them is the `github-actions` stack's ownership.

## Layout

```
k8s/security/
├── admission-policy.yaml      # Kyverno/Gatekeeper: signed + non-root + digest + provenance
├── scan-gate.md               # severity threshold + fail-promotion definition
└── verify-config.yaml         # cosign verification config the admission policy uses
supply-chain.md                # image posture + gate + admission matrix + provenance
# Image hardening lands in the Dockerfile owned by the packaging sub-skill;
# this skill specifies and verifies it.
```

## Hardened image — non-root UID baked in, not just asserted

```dockerfile
# Final runtime stage — minimal base, explicit non-root UID, no shell/pkg-mgr.
FROM gcr.io/distroless/static:nonroot
USER 65532:65532                       # baked in — matches securityContext
COPY --chown=65532:65532 app /app
ENTRYPOINT ["/app"]
# Pair with the manifest securityContext (set by the manifest archetype):
#   runAsNonRoot: true, readOnlyRootFilesystem: true,
#   allowPrivilegeEscalation: false, capabilities: { drop: [ALL] }
# This skill ensures the IMAGE actually satisfies that floor.
```

## Sign the digest, generate + attest the SBOM

```bash
# Keyless/OIDC where the upstream key-custody decision allows.
cosign sign --yes <registry>/<service>@sha256:<digest>

# SBOM in the upstream-named format, attested to the digest:
syft <registry>/<service>@sha256:<digest> -o spdx-json > sbom.spdx.json
cosign attest --yes --predicate sbom.spdx.json \
  --type spdxjson <registry>/<service>@sha256:<digest>
```

## Scan as a gate (definition — pipeline execution handed to the CI stack)

```markdown
# scan-gate.md
- Scanner:    Trivy (or upstream-named)
- Threshold:  fail on CRITICAL (tier-0/1) | HIGH+ (tier-0) per architecture/security
- Effect:     NON-ZERO EXIT BLOCKS PROMOTION (gate, not report)
- Runs in:    the github-actions pipeline (handoff) — this file defines the gate
```

## Admission policy — backstop even if CI is bypassed (Kyverno example)

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata: { name: require-trusted-images }
spec:
  validationFailureAction: Enforce          # reject, not just audit
  rules:
    - name: require-signed
      match: { any: [{ resources: { kinds: [Pod] } }] }
      verifyImages:
        - imageReferences: ["<registry>/*"]
          attestors:
            - entries: [{ keyless: { issuer: "<oidc-issuer>", subject: "<ci-identity>" } }]
    - name: require-digest-not-tag
      match: { any: [{ resources: { kinds: [Pod] } }] }
      validate:
        message: "images must be digest-pinned, not mutable tags"
        pattern: { spec: { containers: [{ image: "*@sha256:*" }] } }
    - name: deny-root
      match: { any: [{ resources: { kinds: [Pod] } }] }
      validate:
        message: "containers must run as non-root"
        pattern: { spec: { =(securityContext): { runAsNonRoot: true } } }
# Extends the PSS namespace floor (owned by k8s-network-and-identity-policy).
# Does NOT set pod-security.kubernetes.io/* labels — that is the network archetype.
```

## Handoffs this skill names (does not implement)

| Concern | Owner |
|---|---|
| Base Deployment/Service authoring, securityContext floor | `k8s-workload-packaging-and-manifest` |
| PSS namespace `enforce` label, NetworkPolicy/RBAC | `k8s-network-and-identity-policy` |
| Autoscaler tuning | `k8s-scaling-and-resilience-topology` |
| Admission-rejection / scan-gate-failure signal collection | `k8s-observability-and-operations-readiness` |
| The CI pipeline that runs scan/sign/SBOM steps | `github-actions` stack (I.5 supply-chain-and-artifact-integrity) |
| Language image build | `dockerfile-and-jvm-tuning` + planned non-JVM siblings |
| Holistic pre-promotion review | `k8s-deploy-manifest-review` (omnibus) |
| Cluster provisioning, control-plane setup | Out of Family G — cloud platform stack + Terraform |
