# Kubernetes Supply Chain and Image Hardening Quality Rubric

Load this before declaring hardening complete. Revise until each check passes or the unresolved gap is explicitly documented in `supply-chain.md`.

## Image hardening

- [ ] The image uses a minimal base (distroless / scratch / minimal language base).
- [ ] An explicit non-root UID is baked into the image (not only asserted in `securityContext`).
- [ ] `readOnlyRootFilesystem` is enforced and the image works under it.
- [ ] All Linux capabilities are dropped (`drop: [ALL]`); any added back is justified.
- [ ] No shell or package manager remains in the runtime layer where avoidable.

## Signing & SBOM

- [ ] Every promoted image is cosign-signed on the immutable digest (not a mutable tag).
- [ ] Signing uses the upstream key-custody path (keyless/OIDC preferred; long-lived key is an ADR exception).
- [ ] An SBOM is generated in the named format (SPDX/CycloneDX).
- [ ] The SBOM is attached or attested to the image digest for post-deploy auditability.

## Scan gate & provenance

- [ ] A vulnerability scan (Trivy/Grype) runs at the tier-correct severity threshold from `architecture/security`.
- [ ] The scan fails promotion on breach — it is a gate, not a report.
- [ ] Build provenance (SLSA-style) is produced and admission-verified where the upstream posture requires it.

## Admission enforcement

- [ ] A Kyverno/Gatekeeper policy rejects unsigned images at admission.
- [ ] The policy rejects root containers and mutable-tag / non-digest image references.
- [ ] The policy verifies provenance where required.
- [ ] The policy extends the PSS namespace floor (owned by `k8s-network-and-identity-policy`) — it does not duplicate or replace it.

## Verification & handoffs

- [ ] A deliberately unsigned image is rejected by admission, or the gap is documented.
- [ ] A deliberately root / mutable-tag image is rejected by admission, or the gap is documented.
- [ ] A known-CVE image fails the scan gate, or the gap is documented.
- [ ] `supply-chain.md` documents image posture, the gate, the admission matrix, and provenance.
- [ ] Base manifests, network/identity, scaling, observability, and the CI pipeline are named handoffs — none implemented here.

## Standards conformance

- [ ] [security-standards](../../../../../../standards/security-standards/README.md): minimal non-root read-only-root-FS image, dropped caps, signed images, SBOM, scan-as-gate, admission enforcement.
- [ ] [deployment-standards](../../../../../../standards/deployment-standards/README.md): image signed and scanned before promotion; gate blocks promotion; enforcement reproducible as policy.
- [ ] [observability-standards](../../../../../../standards/observability-standards/README.md): admission rejections and scan-gate failures are observable (collection wiring handed off).
- [ ] [naming-conventions](../../../../../../standards/naming-conventions/README.md): policy and attestation names `kebab-case`, kind-suffixed when ambiguous.
- [ ] [architecture-schema](../../../../../../standards/architecture-schema/README.md): tier classification drove scan-severity strictness and the signing/provenance requirement.

## Failure handling

If a check fails:

1. Identify the unhardened image aspect or unenforced policy.
2. Ask the user for clarification if the decision cannot be inferred from `architecture/security` or `architecture/operations`.
3. Revise the image/policy, re-run the bad-image rejection and known-CVE scan-gate tests.
4. Keep any unresolved gap explicit in `supply-chain.md` — do not hide it as an assumption.
