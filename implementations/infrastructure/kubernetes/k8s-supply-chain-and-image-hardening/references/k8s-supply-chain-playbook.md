# Kubernetes Supply Chain and Image Hardening Playbook

Load this when hardening any owned area of `k8s-supply-chain-and-image-hardening` or checking the anti-pattern list. It expands the operating rules and process steps in `SKILL.md` with the detail needed to produce a production-grade, enforced supply-chain posture.

## Why this workflow exists

Supply-chain defects are the breaches that do not need a bug in your code. A root container with a writable root filesystem turns one RCE into host compromise. An unsigned image means anyone who can push to the registry can ship to production. A scan that produces a report nobody gates on means a known critical CVE deploys anyway. A CI gate with no admission backstop means a bypassed pipeline (or a direct `kubectl apply`) deploys whatever it wants. None of this fails a functional test — the malicious image runs fine.

The goal is an image that cannot run as root, cannot deploy unsigned, cannot ship with a gating CVE, and is rejected at the cluster even if CI is bypassed — consuming the security and operations posture instead of inventing it.

## Behavioral rules in depth

### 1. Consume security and operations; do not invent it

Image-trust requirements, the scan severity gate, and the provenance posture come from `architecture/security`; registry, key custody, and attestation storage from `architecture/operations`. The CVE severity that blocks promotion is a security decision, not a tuning knob. If a needed decision is missing, raise an ADR candidate.

### 2. Harden the floor — do not just restate it

The manifest archetype set the security-context floor (`runAsNonRoot`, `readOnlyRootFilesystem`, `drop: [ALL]`). This skill hardens *the image itself* so the floor is real: a minimal base (distroless/scratch), an explicit non-root UID baked into the image, no shell or package manager in the runtime layer where avoidable. A `securityContext` saying non-root over an image whose only user is root is a contradiction this skill resolves.

### 3. Every promoted image is signed, on the digest

cosign signature, keyless/OIDC where the upstream key-custody decision allows (no long-lived signing key to steal). Sign the immutable digest, never a mutable tag — signing `:latest` proves nothing about what actually runs. An unsigned image is unpromotable.

### 4. The SBOM is generated and attached

Syft (or the upstream tool) produces an SBOM in the named format (SPDX/CycloneDX), attached or attested to the digest. The point is post-deploy auditability: when the next Log4Shell lands, "which running images contain it" must be answerable from the attested SBOM, not a guess.

### 5. The scan is a gate, not a report

| Posture | Effect |
|---|---|
| Scan runs, prints findings, build continues | Decoration — the CVE ships |
| Scan runs, fails the build at the tier severity | Gate — the CVE is blocked |

Trivy/Grype fails promotion at the upstream-defined, tier-correct severity. A report that does not block is not a control.

### 6. Admission enforces trust at the cluster — defense in depth

CI gates can be bypassed (a direct `kubectl apply`, a broken pipeline, an emergency push). The Kyverno/Gatekeeper admission policy is the backstop: it rejects unsigned images, root containers, mutable-tag/non-digest references, and missing provenance *at admission*, so an untrusted image cannot run even if CI never saw it. CI gate and admission are both required — not either/or.

### 7. The admission policy extends PSS — it does not replace it

The `pod-security.kubernetes.io/enforce` namespace label is owned by `k8s-network-and-identity-policy` and covers the built-in pod-security floor. This skill adds what PSS does not: signed-image verification, digest-pinning, provenance attestation. Duplicating the PSS label here creates two owners for one control — name the boundary instead.

### 8. Provenance proves how, not just who

A signature proves who signed. A SLSA-style build attestation proves the image was built by the expected pipeline from the expected source — defeating a "signed but built from a poisoned branch" attack. Where the upstream posture requires it, produce the attestation and have the admission policy verify it.

### 9. Untested enforcement is not enforcement

Deploy a deliberately bad image — unsigned, then root, then mutable-tag — and confirm the admission policy rejects each. Confirm a known-CVE image fails the scan gate. A policy never tested against a bad image is a policy that has never proven it works.

## Step detail

**Step 1 — Gather context.** Load `architecture/security` (image-trust, scan gate, provenance) and `architecture/operations` (registry, key custody, attestation storage). Resolve tier from `architecture-schema`. Confirm the image/build and the manifest security-context floor. Raise an ADR candidate for any missing decision.

**Step 2 — Harden the image.** Minimal base, explicit non-root UID, read-only root FS, `drop: [ALL]`, no runtime shell/pkg-manager where avoidable; reconcile with the manifest floor.

**Step 3 — Signing.** cosign on the digest via the upstream key-custody path; verification config for admission.

**Step 4 — SBOM.** Syft (or named tool), named format, attached/attested to the digest.

**Step 5 — Scan gate.** Trivy/Grype at the tier-correct severity, defined to fail promotion (gate definition; pipeline execution handed to the CI stack).

**Step 6 — Admission policy.** Kyverno/Gatekeeper rejecting unsigned/root/mutable-tag/missing-provenance, extending the PSS floor.

**Step 7 — Provenance.** SLSA-style attestation produced and admission-verified where required.

**Step 8 — Verify.** Bad-image rejection (unsigned/root/mutable-tag) + known-CVE scan-gate failure. Document any check that cannot run.

**Step 9 — Emit & validate.** Hardening + policy under `k8s/security/`, `supply-chain.md` (image posture, gate, admission matrix, provenance), handoff list. Validate against security-, deployment-, observability-standards, naming-conventions, architecture-schema.

## Anti-patterns to detect

Call these out explicitly when found:

- `securityContext: runAsNonRoot` over an image whose only user is root (contradiction)
- Shell / package manager left in the runtime layer of a minimal-base image
- Signing a mutable tag instead of the digest; no signing at all
- SBOM not generated, or generated but not attached/attested to the digest
- Scan that prints findings but does not fail promotion (report, not gate)
- CI gate with no admission backstop (bypassable by direct apply)
- Admission policy duplicating/replacing the PSS namespace label instead of extending it
- Provenance required by upstream but not produced or not admission-verified
- Long-lived signing key where keyless/OIDC was available and approved
- Enforcement declared done with no bad-image rejection test
- CI pipeline workflow authored here instead of handed to the `github-actions` stack
- Cluster provisioning / control-plane setup authored here (out of Family G)
