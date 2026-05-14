---
name: security
description: Use when an approved system design exists and the team needs security architecture before implementation. Produces threat model, trust boundary map, data classification and handling rules, identity and authorization model, secrets and key management posture, tenant isolation strategy, input and output protection rules, supply-chain posture, audit and compliance mapping, and implementation handoff notes. Do not use for security-tool configuration, code-level vulnerability fixes, penetration testing, incident response, or compliance evidence collection; use the relevant implementations/* skill, quality-engineering, or operations instead.
---

# Security

## When to use

Invoke after `system-design` has approved a design and before implementation skills generate code, schemas, or infrastructure that hardens trust boundaries. Use it whenever a system handles user data, crosses tenant or org boundaries, integrates third parties, or sits under a regulatory regime.

Do not use for: security-tool configuration (route to the relevant implementation skill), CVE triage or specific vulnerability fixes (engineering work), penetration testing (a separate practice), incident response (use `operations` and `reliability`), or compliance audit evidence collection (use `operations`).

## Inputs

Required:

- Approved `system-design.md`.
- The security scope in question: the system, a new surface (new API, new integration, new tenant model), or a change that crosses a trust boundary.
- Data inventory: what data the system processes, stores, transmits, or derives.

Optional:

- PRD sections covering regulatory regime (GDPR, HIPAA, PCI, SOC 2), industry context, and user-trust commitments.
- Existing threat models, security reviews, or incident history.
- Identity providers, SSO, and existing authorization model.
- Platform topology from `infrastructure-platform` (trust zones, network segmentation).
- Third-party integrations and their data-sharing scope.

## Operating rules

- Security architecture starts from data and trust boundaries, not tools. Identify what is sensitive, who can cross which boundary, and what the abuse cases are before naming controls.
- Threat-model in this design's vocabulary. Use the components, dependencies, and flows from `system-design.md`; reject generic OWASP recitations as a substitute.
- Every piece of data has a classification. Public, internal, confidential, restricted/PII, regulated. Classification drives handling rules end-to-end.
- Identity is the new perimeter. Define authentication, session, authorization (RBAC/ABAC/ReBAC), service-to-service auth, and the human-access path separately.
- Authorization is decided at architecture time, not in scattered code. Name the policy model, the enforcement point, and the audit signal.
- Multi-tenant systems require an explicit isolation model: data isolation, compute isolation, and namespace isolation, with stated failure mode if isolation breaks.
- Secrets and keys are first-class. Define storage, issuance, rotation, scoping, and revocation; treat lifetime as a budget.
- Supply chain is in scope. Dependency provenance, image signing, build trust, and third-party integration trust all belong here.
- Defense in depth, but every layer must justify its existence against a specific threat or boundary; do not stack controls for theater.
- When a design choice forces a security trade-off (e.g., cross-tenant cache, exposed admin path, third-party data sharing, weakened auth for latency), raise an ADR candidate.

## Process

1. Load `system-design.md` and inventory: components, data stores, external dependencies, user roles, data flows, and admin surfaces.
2. Classify data: every dataset and notable payload gets a classification (public, internal, confidential, restricted/PII, regulated). Record system of record, retention link, and handling rules per class.
3. Define trust boundaries: every boundary where data, identity, or control crosses (internet to edge, edge to service, service to service, service to data, tenant to tenant, prod to non-prod, human to system). Name what changes at each.
4. Build the threat model in this design's vocabulary: for each trust boundary and high-value asset, list the relevant threats (spoofing, tampering, repudiation, info disclosure, denial of service, elevation; or equivalent abuse cases). Tie each to a named component or flow.
5. Define the identity model: authentication mechanisms per actor class (end user, admin, service, batch job, partner), session strategy, MFA posture, federation, and credential lifecycle.
6. Define the authorization model: policy style (RBAC, ABAC, ReBAC, scoped tokens), enforcement points, default-deny posture, and the audit signal per decision.
7. Define tenant isolation, if multi-tenant: data isolation pattern (shared schema with tenant column, schema-per-tenant, DB-per-tenant), compute isolation, identity scoping, and the failure mode if isolation breaks.
8. Define secrets and key management: secret types, store, issuance flow, rotation cadence per class, scoping rules, revocation path, and key hierarchy for encryption.
9. Define data protection rules per classification: in-transit, at-rest, in-use, in logs, in backups, in non-prod environments, and at deletion. Note tokenization, masking, and field-level encryption needs.
10. Define input and output protections: input validation surfaces, output encoding rules, deserialization posture, file upload posture, and rendering trust boundaries.
11. Define abuse and rate posture: anti-abuse signals, rate limiting per actor class, account takeover protections, bot posture, and the action taken on detection.
12. Define logging and audit posture: which events are security-relevant, what is logged, what is redacted, retention, and tamper-evidence expectations. Hand off pipeline details to `operations`.
13. Define supply-chain posture: dependency provenance and pinning, image signing and SBOM, build trust model, artifact promotion gates, and third-party integration trust (data shared, scopes, vendor security posture).
14. Map controls to compliance regime (if applicable): per relevant standard, list the controls the architecture satisfies, the gaps, and the owner. Avoid copy-pasting control catalogs.
15. Produce `security-architecture.md` with explicit handoffs to `backend-architecture`, `frontend-architecture`, `data-architecture`, `infrastructure-platform`, `operations`, `reliability`, and `quality-engineering`.

## Outputs

Required:

- `security-architecture.md` covering data classification, trust boundaries, threat model, identity model, authorization model, tenant isolation if applicable, secrets and key management, data protection rules per classification, input/output protections, abuse posture, audit posture, supply-chain posture, and compliance mapping if applicable.

Optional, when applicable:

- Data classification table.
- Trust boundary diagram.
- Threat catalog keyed by boundary or asset.
- Authorization policy matrix.
- Key hierarchy diagram.
- ADR drafts for identity, isolation, encryption, or supply-chain decisions.

## Quality checks

- [ ] Every dataset and notable payload has a classification with stated handling rules.
- [ ] Every trust boundary in the design is named, with what changes at the boundary stated.
- [ ] Threats are tied to named components or flows from `system-design.md`; no generic OWASP recitations stand alone.
- [ ] Identity model defines authentication, session, and credential lifecycle per actor class.
- [ ] Authorization model names a policy style, enforcement points, default-deny posture, and an audit signal.
- [ ] Multi-tenant designs state the isolation pattern and the failure mode if isolation breaks.
- [ ] Secrets and key management state store, issuance, rotation cadence, scoping, and revocation.
- [ ] Data-protection rules cover in-transit, at-rest, in logs, in backups, and in non-prod for every restricted/regulated class.
- [ ] Supply-chain posture covers dependency provenance, image signing, build trust, and third-party integration scopes.
- [ ] If a compliance regime applies, controls are mapped with explicit gaps and owners.
- [ ] No tool configuration, scanner rules, or CVE-level fixes appear in the architecture.

## References

- Upstream: [`architecture/system-design`](../system-design/SKILL.md).
- Related architecture skills: [`backend-architecture`](../backend-architecture/SKILL.md), `frontend-architecture`, `data-architecture`, `infrastructure-platform`, `operations`, `reliability`, `quality-engineering`.
- Downstream: security-relevant implementation work across `implementations/*` (e.g., `spring-security-auth-review`, `k8s-deploy-manifest-review`, `github-actions-pipeline-hardened`).
