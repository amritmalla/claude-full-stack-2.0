---
name: security
description: Use when an approved system design exists and the team needs production-grade security architecture before implementation. Produces threat models, trust-boundary analysis, data-classification rules, identity and authorization architecture, tenant-isolation strategy, secrets and key-management posture, abuse protections, supply-chain security posture, audit requirements, compliance mapping, and implementation handoff guidance. Do not use for vulnerability remediation, CVE triage, penetration testing, security-tool configuration, incident response, or compliance evidence collection; use the relevant implementations/* skill, quality-engineering, or operations instead.
---

# Security

## When to use

Invoke after `system-design` has approved a design and before implementation skills generate code, schemas, or infrastructure that hardens trust boundaries. Use it whenever a system handles sensitive or regulated data, crosses tenant or org boundaries, integrates third parties, or sits under a regulatory regime.

Do not use for security-tool configuration (route to the relevant implementation skill), CVE triage or specific vulnerability fixes, penetration testing, incident response (use `operations` and `reliability`), or compliance audit evidence collection (use `operations`).

## Inputs

Required:

- Approved `system-design.md` and the relevant ADRs.
- The security scope in question: the system, a new surface (new API, new integration, new tenant model), or a change that crosses a trust boundary.
- Data inventory: what data the system processes, stores, transmits, or derives.

Optional:

- PRD sections covering regulatory regime (GDPR, HIPAA, PCI, SOC 2), industry context, and user-trust commitments.
- Existing threat models, security reviews, or incident history.
- Identity providers, SSO, and existing authorization model.
- Platform topology from `infrastructure-platform` (trust zones, network segmentation).
- Third-party integrations and their data-sharing scope.

## Operating rules

- Security starts with data and trust boundaries, not tools. Identify sensitive assets, trust boundaries, threat surfaces, and abuse paths before naming controls. Reject vendor-defined or checklist-driven security without architectural reasoning.
- Threat-model in this design's vocabulary. Threats reference real services, APIs, actors, flows, and dependencies from `system-design.md`. Reject generic OWASP recitations disconnected from architecture.
- Every dataset and notable payload has a classification (public, internal, confidential, restricted/PII, regulated) that drives encryption, access, logging, backup, and non-production handling. Reject "all data is sensitive" without operational differentiation.
- Identity is the new perimeter. Define end-user, admin, service, and workload authentication and credential lifecycle separately. Reject shared service accounts, static credentials, and auth assumptions hidden in infrastructure.
- Authorization is an architectural decision: name the policy model (RBAC/ABAC/ReBAC/scoped tokens), enforcement points, default-deny behavior, and audit signals. Reject authorization logic scattered across services.
- Multi-tenant isolation must be explicit: data, compute, cache, and namespace isolation, plus the blast radius and failure behavior if isolation breaks. Reject implicit isolation and isolation enforced only in application code.
- Secrets and keys are first-class: storage, issuance, rotation, scoping, revocation, auditability, and a key hierarchy with ownership and destruction path. Reject secrets in code/images, static production credentials, and undefined rotation ownership.
- Supply chain is part of the threat model: dependency provenance, artifact signing, build trust, CI/CD trust boundaries, and third-party integration posture. Reject "trusted because internal" assumptions.
- Defense in depth must remain explainable: every control justifies the threat it mitigates, the boundary it protects, and the operational tradeoff it introduces. Reject controls added for theater.
- Challenge insecure assumptions directly and architecturally: implicit trust, authorization ambiguity, weak tenant isolation, excessive privilege, insecure token handling, overexposed admin surfaces.
- When a design choice forces a security tradeoff (cross-tenant cache, exposed admin path, third-party data sharing, weakened auth for latency), raise an ADR candidate against `system-design`.

## Output contract

`security-architecture.md` MUST conform to [standards/architecture-schema](../../standards/architecture-schema/README.md), which is authoritative for its frontmatter, required and conditional sections, conditional-section omission rules, and linkage back to `system-design.md` and its ADRs.

Security content additionally conforms to [security-standards](../../standards/security-standards/README.md) (auth schemes, scopes, secrets); audit and supply-chain content aligns with [observability-standards](../../standards/observability-standards/README.md) and [deployment-standards](../../standards/deployment-standards/README.md). Skill structure conforms to [documentation-standards](../../standards/documentation-standards/README.md).

Use `assets/security-architecture.template.md` as the scaffold; it implements the schema. No tool configuration, scanner rules, or CVE-level fixes appear in the architecture unless they materially change architecture behavior.

## Progressive references

- Read `references/security-architecture-playbook.md` when inventorying the security surface, classifying data, mapping trust boundaries, threat-modeling, defining identity/authorization/tenant-isolation, secrets and key management, data-protection rules, input/output protection, abuse and rate posture, logging/audit, supply-chain posture, or compliance mapping, and to check the anti-pattern list.
- Read `references/security-architecture-quality-rubric.md` before finalizing and use it as the validation checklist.
- Use `assets/security-architecture.template.md` for `security-architecture.md`.

## Process

Progress:

ADR candidates are drafted inline as decisions are made (steps 5, 6, 7, 8, 13). Step 15 only consolidates them; it does not retrofit ADRs from prose.

- [ ] Step 1: Load `system-design.md` and relevant ADRs. Inventory components, data stores, external dependencies, user roles, data flows, admin surfaces, background jobs, and operational interfaces. See `references/security-architecture-playbook.md`.
- [ ] Step 2: Classify every dataset and notable payload (public, internal, confidential, restricted/PII, regulated). Per class define storage, transmission, logging, retention, masking/tokenization, and non-production handling. Reject production PII replicated freely into lower environments.
- [ ] Step 3: Map every trust boundary (internet→edge, edge→service, service→service, service→datastore, tenant→tenant, human→system, prod→non-prod). Per boundary state what changes, authentication, authorization, encryption, and audit expectations.
- [ ] Step 4: Build the threat model in this design's vocabulary. Per trust boundary, high-value asset, privileged flow, and integration surface, enumerate threats (spoofing, tampering, repudiation, info disclosure, DoS, elevation) tied to a named component, actor, or data flow.
- [ ] Step 5: Define the identity architecture per actor class (end user, admin, workload/service, batch job, partner): authentication mechanisms, federation, MFA, credential lifecycle, session handling, recovery. Draft an ADR candidate for the identity-model decision. Reject long-lived/shared credentials.
- [ ] Step 6: Define the authorization architecture: policy model (RBAC/ABAC/ReBAC/scoped tokens), enforcement points, default-deny posture, cross-tenant rules, admin escalation, delegated access, and audit signals. Draft an ADR candidate for the authorization-model decision.
- [ ] Step 7: If multi-tenant, define the tenant-isolation strategy: data/compute/cache/namespace isolation and identity scoping, the failure mode if isolation breaks, detection, and operational blast radius. Draft an ADR candidate for the isolation-pattern decision.
- [ ] Step 8: Define secrets and key management: secret types, storage, issuance, injection, rotation cadence, revocation, auditability, and key hierarchy (root/service/envelope/signing) with ownership, destruction, and break-glass. Draft an ADR candidate for the key-management decision.
- [ ] Step 9: Define data-protection rules per classification: in-transit, at-rest, in-use, in logs, in backups, in non-prod, at deletion; field-level encryption, data minimization, and derived-data exposure. Reject unrestricted production-data cloning.
- [ ] Step 10: Define input and output protections: validation boundaries, encoding, deserialization posture, file-upload controls, rendering trust boundaries, SSRF posture, and untrusted-content handling. Reject trust inherited automatically from upstream.
- [ ] Step 11: Define abuse and rate protection: anti-abuse posture, rate limiting per actor class, bot and account-takeover protections, anomaly-detection expectations, enforcement points, and escalation behavior.
- [ ] Step 12: Define logging and audit architecture: security-relevant events (auth, authz, privilege escalation, secrets access, tenant-boundary access, admin actions, deployment mutations), retention, tamper-evidence, and redaction. Hand off pipeline details to `operations`.
- [ ] Step 13: Define supply-chain security: dependency provenance and pinning, image signing, SBOM, CI/CD trust posture, artifact-promotion controls, and third-party integration trust (scopes, vendor posture, data sharing). Draft an ADR candidate for supply-chain trust decisions.
- [ ] Step 14: If a compliance regime applies (SOC 2, GDPR, HIPAA, PCI DSS, ISO 27001, residency), map architecture controls per standard: covered controls, gaps, ownership, unresolved risks. Avoid copy-pasted control catalogs without architectural linkage.
- [ ] Step 15: Generate `security-architecture.md` from `assets/security-architecture.template.md`. Consolidate ADR candidates (numbering, status, alternatives, downsides). Validate against [standards/architecture-schema](../../standards/architecture-schema/README.md) and `references/security-architecture-quality-rubric.md`; revise until both pass or explicitly note any unresolved gap.

## Outputs

Required:

- `security-architecture.md` at `docs/architecture/<product-slug>/security-architecture.md`, with frontmatter and sections per [standards/architecture-schema](../../standards/architecture-schema/README.md).

Optional, when applicable:

- Data-classification table; trust-boundary diagram.
- Threat catalog keyed by boundary or asset; authorization policy matrix.
- Key hierarchy diagram; abuse-control matrix.
- ADR drafts for identity, isolation, encryption, or supply-chain decisions.

Output rules:

- Keep the architecture threat-oriented and explicit about trust boundaries, not security theater.
- Document the threat each control mitigates and the operational tradeoff, not only the control.
- Name assets and boundaries by data sensitivity and trust posture, not by vendor product.
- Treat audit, supply chain, and compliance mapping as part of the design, not later implementation detail.

## Quality checks

- [ ] `references/security-architecture-quality-rubric.md` was loaded before finalizing.
- [ ] `security-architecture.md` validates against [standards/architecture-schema](../../standards/architecture-schema/README.md): frontmatter complete; required sections present; conditional sections present with content or listed under `## Omitted sections` with rationale.
- [ ] Every dataset and notable payload has a classification with stated handling rules.
- [ ] Every trust boundary in the design is named, with what changes at the boundary stated.
- [ ] Threats are tied to named components or flows from `system-design.md`; no generic OWASP recitations stand alone.
- [ ] Identity model defines authentication, session, and credential lifecycle per actor class.
- [ ] Authorization model names a policy style, enforcement points, default-deny posture, and an audit signal.
- [ ] Multi-tenant designs state the isolation pattern and the failure mode if isolation breaks.
- [ ] Secrets and key management state store, issuance, rotation cadence, scoping, and revocation.
- [ ] Data-protection rules cover in-transit, at-rest, logs, backups, and non-prod for every restricted/regulated class.
- [ ] Supply-chain posture covers dependency provenance, image signing, build trust, and third-party scopes.
- [ ] If a compliance regime applies, controls are mapped with explicit gaps and owners.
- [ ] No tool configuration, scanner rules, or CVE-level fixes appear unless they materially change architecture behavior.

## References

- Upstream: [`architecture/system-design`](../system-design/SKILL.md).
- Related architecture skills: [`backend-architecture`](../backend-architecture/SKILL.md), [`frontend-architecture`](../frontend-architecture/SKILL.md), [`data-architecture`](../data-architecture/SKILL.md), [`infrastructure-platform`](../infrastructure-platform/SKILL.md), [`operations`](../operations/SKILL.md), [`reliability`](../reliability/SKILL.md), [`quality-engineering`](../quality-engineering/SKILL.md).
- Downstream: security-relevant implementation work across `implementations/*` (e.g., `spring-security-auth-review`, `k8s-deploy-manifest-review`, `github-actions-pipeline-hardened`).
