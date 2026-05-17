# MongoDB Security and Data Access Hardening Playbook

Load this when hardening any owned area of `mongodb-security-and-data-access-hardening` or checking the anti-pattern list. It expands the operating rules and process steps in `SKILL.md` with the detail needed to produce an engine-enforced security posture.

## Why this workflow exists

MongoDB security defects are the breaches that make headlines, and they share one root cause: the protection was assumed, not enforced at the engine. An auth-disabled MongoDB bound to a public interface is the single most common database breach in the wild. An application connecting as `root` turns one app RCE into total data loss. PII "redacted by the service layer" leaks the moment any other client (a migration script, a BI tool, an attacker with the connection string) reads the collection directly. CSFLE "planned" but not wired means the sensitive fields are plaintext at rest. None of this fails a functional test — the data flows fine, unprotected.

The goal is auth always on, least-privilege roles, TLS everywhere, and PII the engine itself will not surrender without the key — consuming the security and classification posture instead of inventing it.

## Behavioral rules in depth

### 1. PII is enforced at the engine for tier-0 — non-negotiable

Where MongoDB supports CSFLE, field-level redaction, or role-scoped views, the protection is at the engine. "The application filters it out" is rejected for tier-0 PII (a locked data-tier constraint), because any direct-connection client bypasses the application entirely.

### 2. Consume security and classification; do not invent it

The auth model and encryption posture come from `architecture/security`; which fields are PII from `data-architecture.md` / `mongodb-data-model-and-migration`. This skill *enforces* that classification. If a needed decision is missing, raise an ADR candidate.

### 3. Harden the engine — do not reclassify the data

A field that looks like PII but is unclassified, or one classified wrong, is a **finding handed back** to the model/architecture owner — not silently reclassified here. One owner for the classification contract.

### 4. Auth is always on; the mechanism matches the identity model

SCRAM at minimum. x.509 for certificate-based service identity; LDAP/Kerberos where enterprise identity federates. The non-negotiable: no enabled-but-bypassable path, and never an internet-reachable deployment with auth off — that is rejected outright, not flagged.

### 5. Least-privilege RBAC, one role per access pattern

Built-in roles only where they fit exactly (most do not). Custom roles scoped to the minimal actions on the minimal resources. The application connects with a role scoped to its collections — never `root`, `dbOwner`, or a shared superuser. A read service gets a read role; it does not get write "to be safe".

### 6. Internal auth is the replication skill's requirement, specified here

`mongodb-replication-and-ha-readiness` declared that members must authenticate (keyfile/x.509) with member TLS. This skill specifies that mechanism. An unauthenticated replica set means any host that can reach a member can join or read it.

### 7. TLS everywhere, plaintext nowhere

Client connections and intra-cluster traffic are TLS. Plaintext listeners are disabled, not merely "not used". State certificate provenance (internal CA vs public) and the rotation procedure — an expired cert is an outage; an unrotated one is a liability.

### 8. CSFLE protects exactly the classified fields

Map each classification-marked PII field to an encryption key and the mode the access pattern needs (standard CSFLE for store/retrieve; queryable encryption where equality/range queries on the encrypted field are required). The KMS that holds the keys is an infrastructure handoff; the field→key mapping and encrypted-field schema are owned here. Encrypting nothing, or encrypting everything blindly (breaking queries), are both defects.

### 9. Network exposure is minimized and justified

Bind to private interfaces. IP allowlist / security-group posture stated. No `0.0.0.0` bind on an internet-reachable host. Any reachability the trust zones do not justify is a finding — defense in depth behind auth, not instead of it.

### 10. Audit captures security events without becoming a leak

Audit authentication failures, role/grant changes, privileged operations, and access to PII collections, to a tamper-resistant destination. Critically: the audit stream itself must not record PII values or secrets — an audit log full of the data it was meant to protect is a new breach surface.

### 11. This skill provides the backup key model

`mongodb-backup-and-operational-readiness` requires backup artifacts encrypted with a defined key/access model but does not own key custody. This skill provides that model so there is a single owner for key management across live data and backups.

### 12. Un-negative-tested access control is unverified

Prove an unauthorized principal is actually denied. Prove a CSFLE field is actually unreadable without the key (read it raw, confirm ciphertext). Prove no role grants more than intended. A control asserted but never adversarially tested is a hypothesis.

## Step detail

**Step 1 — Gather context.** Load `architecture/security` (auth, encryption) and `data-architecture.md` (PII classification). Pull PII-tagged fields from `mongodb-data-model-and-migration` and the internal-auth requirement from `mongodb-replication-and-ha-readiness`. Resolve tier from `architecture-schema`. Raise an ADR candidate for any missing decision.

**Step 2 — Authentication.** SCRAM baseline; x.509/LDAP/Kerberos per identity model; confirm enabled, no unauthenticated reachable path.

**Step 3 — RBAC.** One role per access pattern; least-privilege; no shared superuser; app principals scoped to their collections.

**Step 4 — Internal auth.** Keyfile/x.509 + member TLS, satisfying the replication requirement.

**Step 5 — TLS.** Client + intra-cluster; cert provenance/rotation; plaintext listeners disabled.

**Step 6 — CSFLE.** Field→key map + mode (standard vs queryable) for each classified PII field; reference the provisioned KMS.

**Step 7 — Redaction/views.** Role-scoped views/redaction where PII visibility is role-dependent.

**Step 8 — Network.** Private bind; IP allowlist/security-group posture; no unjustified reachability.

**Step 9 — Audit.** Auth failures, grant changes, privileged ops, PII-collection access → tamper-resistant destination; verify no PII/secrets in the stream.

**Step 10 — Backup key model.** Provide the artifact key/access model `mongodb-backup-and-operational-readiness` consumes.

**Step 11 — Negative-test.** Unauthorized denied; over-broad grant absent; CSFLE field unreadable without key. Document any check that cannot run.

**Step 12 — Emit & validate.** `security-hardening.md` (auth, role/grant matrix, TLS, CSFLE map, redaction/views, network, audit, negative-test results, backup key model), handoff list. Validate against security-, architecture-schema, observability-, deployment-standards, naming-conventions.

## Anti-patterns to detect

Call these out explicitly when found:

- Auth disabled, or an internet-reachable deployment without auth (reject outright)
- Application connecting as `root`/`dbOwner`/a shared superuser
- Built-in role used where it grants more than the access pattern needs
- Replica-set members with no internal auth / no member TLS
- Plaintext listener enabled; certificate provenance/rotation unstated
- PII "enforced by the application" for tier-0 data
- Classification-marked PII field with no CSFLE key mapping (plaintext at rest)
- Encrypting everything blindly, breaking required queries (use queryable encryption)
- `0.0.0.0` bind on an internet-reachable host; reachability the trust zones do not justify
- Audit stream recording PII values or secrets
- Data fields *reclassified* here instead of a finding handed back to the model/architecture owner
- Access controls never negative-tested (no proof unauthorized is denied / PII unreadable)
- KMS/secret-store provisioning authored here (infrastructure layer)
