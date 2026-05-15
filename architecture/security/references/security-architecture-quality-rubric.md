# Security Architecture Quality Rubric

Load this before emitting `security-architecture.md`. Revise until each check passes or the unresolved gap is explicitly documented.

## Data and trust boundaries

- [ ] Every dataset and notable payload has a classification with stated handling rules.
- [ ] Classification drives encryption, access, logging, backup, and non-production handling — not "all data is sensitive".
- [ ] Every trust boundary is explicitly named, with what changes at the boundary stated.
- [ ] No flat trust assumptions; internal traffic is not implicitly trusted.

## Threat model

- [ ] Threats reference real components, actors, and flows from `system-design.md`.
- [ ] Every trust boundary, high-value asset, privileged flow, and integration surface is threat-modeled.
- [ ] No generic OWASP recitation stands alone, disconnected from architecture.

## Identity and authorization

- [ ] Identity lifecycle is defined separately for end users, admins, services, workloads, and partners.
- [ ] No long-lived or shared operational credentials.
- [ ] Authorization names a policy model, enforcement points, default-deny posture, and audit signals.
- [ ] Authorization is consistent across services, not scattered per service.

## Tenant isolation and secrets

- [ ] Multi-tenant designs state data/compute/cache/namespace isolation and the failure mode if isolation breaks.
- [ ] Isolation is not enforced only in UI/application logic.
- [ ] Secrets posture defines storage, issuance, rotation, scoping, revocation, and auditability.
- [ ] Key hierarchy defines ownership, lifecycle, destruction, and break-glass.

## Data, input, abuse, and audit

- [ ] Data-protection rules cover in-transit, at-rest, logs, backups, and non-prod for every restricted/regulated class.
- [ ] Input/output protections cover validation, encoding, deserialization, uploads, SSRF, and untrusted content.
- [ ] Abuse and rate posture defines actor-specific limits, enforcement points, and escalation.
- [ ] Security-relevant events are audited with retention, tamper-evidence, and redaction; no restricted payloads in broad-access logs.

## Supply chain and compliance

- [ ] Supply-chain posture covers dependency provenance, image signing, build trust, and third-party scopes.
- [ ] No unverified dependencies promoted directly to production.
- [ ] If a compliance regime applies, controls are mapped with explicit gaps and owners — no copy-pasted catalogs.

## Linkage and decisions

- [ ] `security-architecture.md` conforms to [architecture-schema](../../../standards/architecture-schema/README.md): frontmatter complete, required sections present, conditional sections present or omitted with rationale.
- [ ] Security content conforms to [security-standards](../../../standards/security-standards/README.md).
- [ ] Every ADR candidate has Context, Decision, Consequences (including downsides), and Alternatives considered.
- [ ] Every control justifies the threat it mitigates and the operational tradeoff; no controls added for theater.
- [ ] No tool configuration, scanner rules, or CVE-level fixes leaked into the architecture.

## Failure handling

If a check fails:

1. Identify the missing or weak security decision.
2. Ask the user for clarification if it cannot be inferred from `system-design.md` or the PRD.
3. Revise `security-architecture.md` or the relevant ADR.
4. Keep unresolved questions explicit; do not hide them as assumptions.
