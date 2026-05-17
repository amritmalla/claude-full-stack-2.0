---
product: <kebab-case slug>          # matches the system-design / PRD slug
status: draft                       # draft | review | approved | superseded
owner: <name or role>
system_design: <relative path to source system-design.md>
prd: <relative path to source PRD, or null>
version: 0.1.0                      # semver
last_reviewed: YYYY-MM-DD
---

# Security Architecture: [Product or System Name]

## Overview

[One paragraph: sensitive assets, the trust boundaries that matter most, what the security architecture optimizes for, and what it intentionally does not cover.]

## Security Surface Inventory

| Surface | Type | Sensitive Assets | Trust Assumptions |
|---|---|---|---|
| [name] | [API / user flow / admin path / job / integration / datastore / ops interface] | [assets] | [assumptions] |

## Data Classification

| Dataset / Payload | Classification | Storage Rule | Transmission Rule | Logging | Retention | Non-prod Handling |
|---|---|---|---|---|---|---|
| [name] | [public / internal / confidential / restricted-PII / regulated] | [rule] | [rule] | [policy] | [period] | [masking/tokenization] |

## Trust Boundary Map

| Boundary | What Changes | Authentication | Authorization | Encryption | Audit |
|---|---|---|---|---|---|
| [internet→edge / edge→service / service→service / service→datastore / tenant→tenant / human→system / prod→non-prod] | [change] | [expectation] | [posture] | [requirement] | [expectation] |

## Threat Model

| Threat | Category | Component / Flow / Actor | Impact | Mitigation | Residual Risk |
|---|---|---|---|---|---|
| [threat] | [spoofing / tampering / repudiation / info disclosure / DoS / elevation] | [named element] | [impact] | [control] | [risk] |

## Identity Architecture

| Actor Class | Authentication | Federation / MFA | Credential Lifecycle | Session / Recovery |
|---|---|---|---|---|
| [end user / admin / service / workload / batch / partner] | [OIDC / SAML / mTLS / workload-IF / short-lived] | [posture] | [issuance→rotation→revocation] | [behavior] |

## Authorization Architecture

| Concern | Decision |
|---|---|
| Policy model | [RBAC / ABAC / ReBAC / scoped tokens] |
| Enforcement points | [where] |
| Default posture | [default-deny] |
| Cross-tenant / delegated rules | [rules] |
| Admin escalation | [behavior] |
| Audit signal per decision | [signal] |

## Tenant Isolation Strategy

*Conditional — include when multi-tenant; otherwise list under Omitted sections.*

| Dimension | Pattern | Failure Mode if Broken | Detection | Blast Radius |
|---|---|---|---|---|
| Data | [shared-schema / schema-per-tenant / db-per-tenant / isolated runtime] | [mode] | [mechanism] | [radius] |
| Compute / Cache / Namespace | [pattern] | [mode] | [mechanism] | [radius] |
| Identity scoping | [approach] | [mode] | [mechanism] | [radius] |

## Secrets & Key Management

| Concern | Decision |
|---|---|
| Secret types & storage | [types / store] |
| Issuance & injection | [flow] |
| Rotation cadence (per class) | [cadence] |
| Revocation path | [path] |
| Key hierarchy | [root / service / envelope / signing] |
| Ownership, destruction, break-glass | [decision] |

## Data Protection Rules

| Classification | In-transit | At-rest | In Logs | Backups | Non-prod | Deletion |
|---|---|---|---|---|---|---|
| [class] | [TLS/mTLS] | [encryption] | [redaction] | [posture] | [handling] | [posture] |

Field-level encryption, data minimization, derived-data exposure: [decisions].

## Input & Output Protection

| Concern | Decision |
|---|---|
| Validation boundaries | [where] |
| Output encoding | [rules] |
| Deserialization posture | [posture] |
| File-upload controls | [controls] |
| Rendering trust boundaries | [boundaries] |
| SSRF / untrusted-content posture | [posture] |

## Abuse & Rate Protection

*Conditional — include for internet-facing or untrusted-actor surfaces; otherwise list under Omitted sections.*

| Concern | Decision |
|---|---|
| Anti-abuse posture | [posture] |
| Rate limiting (per actor class) | [limits] |
| Bot / account-takeover protections | [protections] |
| Anomaly detection | [expectations] |
| Enforcement points & escalation | [behavior] |

## Logging & Audit Architecture

| Security Event | Logged | Redaction | Retention | Tamper-evidence |
|---|---|---|---|---|
| [auth / authz / privilege escalation / secrets access / tenant-boundary / admin action / deploy mutation] | [what] | [rules] | [period] | [posture] |

Pipeline details handed off to `operations`.

## Supply-Chain Security

| Concern | Decision |
|---|---|
| Dependency provenance & pinning | [decision] |
| Image signing & SBOM | [decision] |
| CI/CD trust posture | [posture] |
| Artifact-promotion controls | [controls] |
| Third-party integration trust | [scopes / vendor posture / data sharing] |

## Compliance Mapping

*Conditional — include when a regulatory regime applies; otherwise list under Omitted sections.*

| Standard | Covered Controls | Gaps | Owner | Unresolved Risk |
|---|---|---|---|---|
| [SOC 2 / GDPR / HIPAA / PCI DSS / ISO 27001 / residency] | [controls] | [gaps] | [owner] | [risk] |

## Implementation Handoffs

### backend-architecture / frontend-architecture / data-architecture

- [Auth, authorization, classification, and data-protection notes consumed downstream]

### infrastructure-platform

- [Trust zones, workload identity, secrets substrate, supply-chain controls]

### operations / reliability

- [Audit pipeline, security-incident clauses, monitoring of security signals]

### quality-engineering

- [Security test expectations: authz tests, abuse tests, isolation tests]

## ADR Index

| ADR | Title | Status | Summary |
|---|---|---|---|
| NNNN | [title] | [proposed/accepted/...] | [summary] — links to `adrs/NNNN-<slug>.md` |

## Omitted sections

- [Conditional section name]: [one-line rationale for omission].

## Deferred Decisions

- [Decision, owner, deadline].
