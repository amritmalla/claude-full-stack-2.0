# Security Architecture Playbook

Load this when inventorying the security surface, classifying data, or making any security-architecture decision. It expands the operating rules and process steps in `SKILL.md` with the detail needed to produce `security-architecture.md`.

## Why this workflow exists

Design security architecture before implementation hardens assumptions into code, infrastructure, and operational processes. It prevents implicit trust boundaries, authorization sprawl, weak tenant isolation, insecure secret handling, accidental exposure of regulated data, supply-chain compromise, and security controls added reactively after incidents.

The goal is not "adding security controls" — it is explicit trust boundaries, resilient identity and authorization, secure data handling, operationally enforceable protections, and security decisions aligned with system architecture.

## Behavioral rules in depth

### 1. Security starts with data and trust boundaries

Do not begin with tools. Start with what data exists, where it flows, who can access it, and which boundaries are crossed. Identify sensitive assets, trust boundaries, threat surfaces, and abuse paths. Reject vendor-product-defined security and checklist-driven security without architectural reasoning.

### 2. Threat-model in the system's own vocabulary

Threats reference real services, APIs, actors, flows, and dependencies, mapping directly to system-design components, data flows, and operational surfaces. Reject generic OWASP recitations disconnected from architecture.

### 3. Every dataset has a classification

Every dataset and notable payload defines classification (public, internal, confidential, restricted/PII, regulated), handling rules, retention, and exposure boundaries. Classification drives encryption posture, access rules, logging policy, backup posture, and non-production handling. Reject "all data is sensitive" without operational differentiation.

### 4. Identity is the new perimeter

Separately define end-user authentication, admin authentication, service authentication, machine/workload identity, and credential lifecycle. Reject shared service accounts, static credentials, and authentication assumptions hidden in infrastructure.

### 5. Authorization is an architectural decision

Define policy model, enforcement points, default-deny behavior, and audit signals. Models: RBAC, ABAC, ReBAC, scoped-token authorization. Every protected action defines who can perform it, where enforcement occurs, and how decisions are audited. Reject authorization logic scattered across services.

### 6. Multi-tenant isolation must be explicit

Define data, compute, namespace isolation, and the blast radius if isolation fails. Patterns: shared-schema, schema-per-tenant, database-per-tenant, cluster-per-tenant. Every choice defines operational tradeoffs, migration implications, and breach consequences. Reject implicit tenant isolation assumptions.

### 7. Secrets and keys are first-class architecture

Secrets architecture defines storage, issuance, rotation, scoping, revocation, and auditability. Key management defines hierarchy, ownership, lifecycle, and destruction path. Reject secrets embedded in code, static production credentials, and undefined rotation ownership.

### 8. Supply chain is part of the threat model

Include dependency provenance, artifact signing, build trust, CI/CD trust boundaries, and third-party integration posture. Reject "trusted because internal" assumptions.

### 9. Defense in depth must remain explainable

Every control justifies which threat it mitigates, which boundary it protects, and what operational tradeoff it introduces. Reject layered controls added only for theater.

### 10. Challenge insecure assumptions directly

Be direct, architectural, and threat-oriented. Examples of the kind of feedback to give:

- "This admin API crosses trust boundaries without separate authorization posture."
- "Your tenant isolation depends entirely on application correctness."
- "This service-to-service trust model assumes network trust."
- "Your logs may leak restricted payloads into lower-trust systems."
- "Your CI pipeline currently has production mutation privileges without workload identity separation."

## Step detail

**Security surface inventory (step 1).** Inventory APIs, user flows, admin paths, background jobs, external integrations, datastore boundaries, and operational interfaces. Clarify sensitive assets, attack surfaces, and trust assumptions.

**Data classification (step 2).** Classify datasets, payloads, credentials, and notable derived artifacts. Per class define storage, transmission, logging, retention, masking/tokenization, and non-production handling. Reject production PII replicated freely into lower environments.

**Trust boundary mapping (step 3).** Boundaries: internet→edge, edge→service, service→service, service→datastore, tenant→tenant, human→system, prod→non-prod. Per boundary define what changes, authentication, authorization, encryption, and audit expectations. Reject flat trust assumptions.

**Threat modeling (step 4).** Categories: spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege. Tie every threat to a named component, actor, or data flow. Reject disconnected threat lists.

**Identity architecture (step 5).** Actors: end users, administrators, workloads/services, batch jobs, external partners. Mechanisms: OIDC, SAML, workload identity federation, mTLS, short-lived credentials. Specify federation, MFA posture, credential lifecycle, session handling, recovery. Reject long-lived or shared operational identities.

**Authorization architecture (step 6).** Models: RBAC, ABAC, ReBAC, capability/scoped tokens. Clarify default-deny posture, cross-tenant rules, admin escalation, and delegated access. Reject per-service authorization without policy consistency.

**Tenant isolation (step 7).** Patterns: shared schema, schema-per-tenant, database-per-tenant, isolated runtime. Define data/compute/cache/namespace isolation, identity scoping, failure mode if isolation breaks, detection, and operational blast radius. Reject isolation enforced only in frontend code.

**Secrets & key management (step 8).** Define secret types, storage, issuance, injection, rotation cadence, revocation, auditability. Key hierarchy: root keys, service keys, envelope encryption, signing keys. Clarify ownership, destruction lifecycle, break-glass. Reject manual secret distribution and undefined key ownership.

**Data protection (step 9).** Per classification define in-transit, at-rest, in-use, log handling, backup posture, non-production handling, deletion posture, and masking/tokenization. Clarify field-level encryption, data minimization, and derived-data exposure. Reject unrestricted production-data cloning.

**Input & output protection (step 10).** Define validation boundaries, encoding, deserialization posture, file-upload controls, rendering trust boundaries, and API abuse protections. Clarify SSRF posture, template rendering risks, and untrusted-content handling. Reject trust inherited automatically from upstream.

**Abuse & rate protection (step 11).** Define anti-abuse posture, rate limiting, bot protections, account-takeover protections, and anomaly detection. Specify actor-specific limits, enforcement points, escalation behavior. Reject globally shared anonymous rate limits for sensitive systems.

**Logging & audit (step 12).** Security-relevant events: authentication, authorization, privilege escalation, secrets access, tenant-boundary access, admin actions, deployment mutations. Define retention, tamper-evidence, and redaction. Reject sensitive payloads logged into broad-access systems.

**Supply-chain security (step 13).** Define dependency provenance, package pinning, image signing, SBOM, CI/CD trust posture, and artifact-promotion controls. Clarify third-party integrations, OAuth scopes, vendor trust, and data-sharing posture. Reject unverified dependencies promoted to production.

**Compliance mapping (step 14).** Standards: SOC 2, GDPR, HIPAA, PCI DSS, ISO 27001, residency rules. Per standard identify covered controls, gaps, ownership, and unresolved risks. Reject copy-pasted control catalogs without architectural linkage.

## Anti-patterns to detect

Call these out explicitly when detected:

- Flat trust boundaries
- Shared admin accounts
- Long-lived credentials
- Authorization logic scattered across services
- Tenant isolation enforced only in UI/application logic
- Secrets in Git or container images
- Production data cloned into lower environments
- Excessive service privileges
- Logs leaking restricted payloads
- Cross-tenant cache leakage risk
- CI/CD pipelines with unrestricted production access
- Implicit trust of internal traffic
- Build pipelines without provenance guarantees
- Unverified third-party integrations
- Security controls added only for compliance optics
- Undefined credential rotation ownership
- Shared service credentials
- Missing auditability for privileged actions
- Default-allow authorization posture
- No account-takeover protections
- Insecure session persistence
- Blind trust in upstream validation

## Writing style

Threat-oriented, architecture-focused, operationally grounded, explicit about trust boundaries. Avoid generic OWASP checklists, vendor/tool worship, fear-driven language, and implementation-level vulnerability detail. The objective is resilient security architecture integrated into the system design — not security theater.
