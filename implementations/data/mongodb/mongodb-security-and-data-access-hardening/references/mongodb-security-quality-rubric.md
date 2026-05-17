# MongoDB Security and Data Access Hardening Quality Rubric

Load this before declaring the posture complete. Revise until each check passes or the unresolved gap is explicitly documented in `security-hardening.md`.

## Context & boundary

- [ ] Auth model and encryption posture are sourced from `architecture/security`; PII classification from `data-architecture.md` (or an ADR candidate is raised).
- [ ] PII classification is consumed from `mongodb-data-model-and-migration` / `data-architecture.md`; a mis/unclassified field is a finding handed back, not classified here.
- [ ] No KMS/secret-store provisioning is done here (infrastructure layer).

## Authentication & authorization

- [ ] Authentication is enabled; the mechanism (SCRAM/x.509/LDAP/Kerberos) matches the identity model.
- [ ] No unauthenticated reachable path exists; no internet-reachable deployment with auth off.
- [ ] RBAC is least-privilege: one role per access pattern; no shared superuser.
- [ ] Application principals are scoped to their own collections (never `root`/`dbOwner`).
- [ ] Replica-set internal auth (keyfile/x.509) + member TLS satisfy the requirement named by `mongodb-replication-and-ha-readiness`.

## Encryption in transit & at rest

- [ ] TLS is enforced for client and intra-cluster traffic; no plaintext listener.
- [ ] Certificate provenance and rotation procedure are stated.
- [ ] Every classification-marked PII field has a CSFLE key mapping.
- [ ] The encryption mode (standard vs queryable) matches each field's access pattern (no broken required queries).
- [ ] Role-scoped redaction/views exist where PII visibility is role-dependent.

## Network & audit

- [ ] The deployment binds to private interfaces; no `0.0.0.0` on an internet-reachable host.
- [ ] IP allowlist / security-group posture is stated; unjustified reachability is a finding.
- [ ] Audit logging covers auth failures, role/grant changes, privileged ops, and PII-collection access.
- [ ] The audit destination is tamper-resistant.
- [ ] No PII values or secrets are written into the audit stream.

## Backup key model & negative testing

- [ ] A backup-artifact key/access model is provided for `mongodb-backup-and-operational-readiness`.
- [ ] An unauthorized principal was confirmed denied, or the gap is documented.
- [ ] An over-broad grant was confirmed absent, or the gap is documented.
- [ ] A CSFLE-protected field was confirmed unreadable without the key (raw read = ciphertext), or the gap is documented.

## Standards conformance & handoffs

- [ ] [security-standards](../../../../../standards/security-standards/README.md): auth always on, least-privilege RBAC, TLS in transit, engine-enforced PII, no secrets in audit, KMS-based key custody.
- [ ] [architecture-schema](../../../../../standards/architecture-schema/README.md): classification enforced not authored; access scoped to the owning component.
- [ ] [observability-standards](../../../../../standards/observability-standards/README.md): auth-failure, grant-change, PII-access signals to a tamper-resistant destination.
- [ ] [deployment-standards](../../../../../standards/deployment-standards/README.md): roles, TLS, audit config reproducible from configuration.
- [ ] [naming-conventions](../../../../../standards/naming-conventions/README.md): role and audit-filter naming.
- [ ] Modeling, query tuning, topology, backup procedure, and KMS/secret-store provisioning are named handoffs — none implemented here.

## Failure handling

If a check fails:

1. Identify the open auth path, the over-broad grant, or the unencrypted PII field.
2. Ask the user for clarification if the decision cannot be inferred from `architecture/security` or `data-architecture.md`.
3. Revise the configuration, re-run the negative tests (unauthorized denied; PII unreadable without key).
4. Keep any unresolved gap explicit in `security-hardening.md` — do not hide it as an assumption.
