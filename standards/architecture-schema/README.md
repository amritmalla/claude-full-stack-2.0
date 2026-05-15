# architecture-schema

Canonical structure for system architecture documents and Architecture Decision Records (ADRs). Produced by `architecture/system-design`; consumed by every downstream implementation domain.

## File layout

```
docs/architecture/<product-slug>/
├── system-design.md           # primary artifact, always present
├── data-architecture.md       # OPTIONAL — only when the design has a non-trivial data layer (see "data-architecture.md")
├── frontend-architecture.md   # OPTIONAL — only when the design has a user-facing frontend (see "frontend-architecture.md")
├── platform-architecture.md   # OPTIONAL — only when the design needs dedicated platform/infra architecture (see "platform-architecture.md")
├── security-architecture.md   # OPTIONAL — only when the design handles sensitive data or crosses trust/tenant boundaries (see "security-architecture.md")
├── ai-architecture.md         # OPTIONAL — only when the design has an AI surface (see "ai-architecture.md")
├── adrs/
│   └── NNNN-<slug>.md         # one per non-obvious decision, monotonic numbering
└── components/                # OPTIONAL — only when escalated (see "Per-component breakout")
    └── <component>.md
```

## `system-design.md`

Primary artifact. One file per system.

### Frontmatter (required)

```yaml
---
product: <kebab-case slug>         # matches the PRD slug
status: draft | review | approved | superseded
owner: <name or role>
prd: <relative path to source PRD>
version: <semver, starts at 0.1.0>
last_reviewed: YYYY-MM-DD
---
```

### Required sections

| Section | Purpose |
|---|---|
| `## Overview` | One-paragraph system summary: core workflows, primary actors, what it optimizes for and intentionally does not. |
| `## Architecture Style` | Chosen style with PRD-based justification, simpler alternatives considered, operational tradeoffs accepted. |
| `## Bounded Contexts` | Table or list: Name, Responsibility, Owned Data, Dependencies, Upstream/Downstream Interactions. |
| `## Components` | One subsection per component: Responsibility, Interfaces, Dependencies, Inputs/Outputs, Persistence, Consistency, Scaling Expectations. |
| `## Data Flow` | Entry points, request paths, async boundaries, consistency model per entity, idempotency, retry behavior, reconciliation. |
| `## Failure Modes` | Table or list: Component, Failure Scenario, User Impact, Detection, Recovery, Degradation. Specific to *this* design — no generic checklists. |
| `## ADR Index` | Table: ADR number, Title, Status, Summary. Links to `adrs/NNNN-<slug>.md`. |

### Conditional sections

Include if material; otherwise omit and add a one-line rationale under `## Omitted sections`.

| Section | When to include |
|---|---|
| `## Persistence Strategy` | Multiple stores, or non-trivial caching / retention / migration concerns. Omit when a single store with an obvious mapping suffices — fold one paragraph into Components instead. |
| `## Security and Compliance` | Always for external products and any system handling user data. Conforms to [security-standards](../security-standards/README.md). May be omitted with one-line rationale for purely internal reference workloads. |
| `## Operational Considerations` | When the design introduces durable operational burden (observability vendor choice, feature flag system, backfill machinery). May fold into Failure Modes if the design has one runtime topology and no durable operational decisions. Conforms to [observability-standards](../observability-standards/README.md) and [deployment-standards](../deployment-standards/README.md). |

## `data-architecture.md`

Secondary artifact. Present only when `system-design.md` includes a non-trivial operational data layer (multiple stores, cross-context read models, sharding, replication, or caching concerns). Produced by [`architecture/data-architecture`](../../architecture/data-architecture/SKILL.md); consumed by `implementations/data/<engine>`. One file per system.

### Frontmatter (required)

```yaml
---
product: <kebab-case slug>         # matches the system-design slug
status: draft | review | approved | superseded
owner: <name or role>
system_design: <relative path to source system-design.md>
prd: <relative path to source PRD, or null>
version: <semver, starts at 0.1.0>
last_reviewed: YYYY-MM-DD
---
```

### Required sections

| Section | Purpose |
|---|---|
| `## Overview` | Datasets and engines present, owning contexts, dominant access patterns, what it optimizes for and intentionally does not. |
| `## Dataset Inventory & Ownership` | Table: Dataset, Owning Context, Authoritative Write Path, Engine, Consumers, Consumption Mechanism. |
| `## Access Patterns` | Per dataset: read/write shapes, hot keys, read:write ratio, latency target, transactional grouping. |
| `## Engine Selection` | Per dataset: engine class, engine, justification, rejected alternatives. |
| `## Consistency & Concurrency Model` | Per write path: consistency guarantee, isolation/concurrency, conflict resolution, enforcement mechanism. |
| `## Schema Strategy` | Normalization posture, aggregate boundaries, key design, tenant isolation, soft-delete, referential integrity, audit/immutability. |
| `## Indexing Strategy` | Per access pattern: serving index, index type, write cost, cardinality assumption. No "just in case" indexes. |
| `## Retention & Deletion` | Per dataset: retention period, deletion mechanism, archival, PII handling, audit/legal-hold. |
| `## Migration Strategy` | Tooling, expand/migrate/contract phasing, online constraints, dual-write/shadow-read, backfill, rollback, compatibility. |
| `## Operational Readiness` | Backup cadence and restore validation, monitoring signals, query-performance monitoring, runbook hooks. |
| `## Implementation Handoffs` | Explicit handoffs to `implementations/data/<engine>`, `backend-architecture`, `security`, `reliability`, `operations`. |
| `## ADR Index` | Table: ADR number, Title, Status, Summary. Links to `adrs/NNNN-<slug>.md`. Shares the system's monotonic ADR numbering. |

### Conditional sections

Include if material; otherwise omit and add a one-line rationale under `## Omitted sections`.

| Section | When to include |
|---|---|
| `## Partitioning & Sharding` | A measured constraint (throughput, size, tenancy, blast radius, region) demands it. Must name the partition key and triggering constraint. |
| `## Replication & High Availability` | Replication/HA topology is non-trivial. Must state failover RTO/RPO and replica lag tolerance; replicas are not backups. |
| `## Cache Architecture` | One or more cache layers exist. Each layer names source of truth, invalidation rule, and staleness budget. |

`data-architecture.md` shares the system's ADR numbering, immutability rule, and supersede chain (see "ADRs"). It does not redefine bounded contexts, components, or data flow — those remain owned by `system-design.md`.

## `frontend-architecture.md`

Secondary artifact. Present only when `system-design.md` includes a user-facing web frontend. Produced by [`architecture/frontend-architecture`](../../architecture/frontend-architecture/SKILL.md); consumed by `implementations/frontend/<framework>`. One file per system.

### Frontmatter (required)

```yaml
---
product: <kebab-case slug>         # matches the system-design slug
status: draft | review | approved | superseded
owner: <name or role>
system_design: <relative path to source system-design.md>
prd: <relative path to source PRD, or null>
version: <semver, starts at 0.1.0>
last_reviewed: YYYY-MM-DD
---
```

### Required sections

| Section | Purpose |
|---|---|
| `## Overview` | Frontend surfaces present, primary user tasks, API/BFF boundary, what it optimizes for and intentionally does not. |
| `## Application Shell` | Number of apps, deployment boundaries, shared-shell strategy, micro-frontend posture, shared cross-cutting concerns. |
| `## Routing Model` | Route hierarchy, layouts, dynamic segments, route ownership, not-found/loading/error behavior, access constraints. |
| `## Rendering Strategy` | Per route/group: rendering mode, hydration, freshness, SEO posture, justification. |
| `## Data Fetching & Caching` | Per dependency: fetch location, owner, cache layer, invalidation trigger, retry/stale behavior, mutation flow. |
| `## State Architecture` | All four tiers (server-cache, URL, ephemeral UI, durable client): ownership, mechanism, sync, persistence, invalidation. Unused tiers stated. |
| `## Auth & Session Handling` | Token/session storage, refresh, route guards, RBAC, unauthenticated rendering, CSRF/XSS posture, session/multi-tab behavior. |
| `## Design System Boundary` | What the design system owns vs the app, theming/token propagation, component-extension contract. |
| `## Accessibility Posture` | WCAG target, keyboard/focus model, screen-reader expectations, semantic structure, testing posture. |
| `## Performance Budgets` | Numeric targets (LCP, INP, CLS, JS bundle, image, third-party) with breach actions and regression monitoring. |
| `## Client Observability` | Error reporting, RUM, session-replay posture, tracing correlation, sampling, PII redaction. |
| `## Implementation Handoffs` | Explicit handoffs to `implementations/frontend/<framework>`, `backend-architecture`, `security`, `performance`, `quality-engineering`. |
| `## ADR Index` | Table: ADR number, Title, Status, Summary. Links to `adrs/NNNN-<slug>.md`. Shares the system's monotonic ADR numbering. |

### Conditional sections

Include if material; otherwise omit and add a one-line rationale under `## Omitted sections`.

| Section | When to include |
|---|---|
| `## Internationalization & Localization` | Multi-locale or RTL is in scope. Defines locale routing, translation loading, and formatting/timezone handling. |
| `## Real-time, Offline & Resilience` | Realtime or offline features exist. Must define failure fallback, reconnect, and reconciliation behavior. |

`frontend-architecture.md` shares the system's ADR numbering, immutability rule, and supersede chain (see "ADRs"). It does not redefine bounded contexts, components, or data flow — those remain owned by `system-design.md`.

## `platform-architecture.md`

Secondary artifact. Present only when `system-design.md` needs dedicated platform and infrastructure architecture (cloud/account topology, runtime substrate, network trust zones, deployment substrate). Produced by [`architecture/infrastructure-platform`](../../architecture/infrastructure-platform/SKILL.md); consumed by `implementations/infrastructure/<vendor>`. One file per system.

### Frontmatter (required)

```yaml
---
product: <kebab-case slug>         # matches the system-design slug
status: draft | review | approved | superseded
owner: <name or role>
system_design: <relative path to source system-design.md>
prd: <relative path to source PRD, or null>
version: <semver, starts at 0.1.0>
last_reviewed: YYYY-MM-DD
---
```

### Required sections

| Section | Purpose |
|---|---|
| `## Overview` | Workloads hosted, cloud/runtime substrate, what it optimizes for and intentionally does not. |
| `## Workload Inventory` | Per workload: class, runtime expectation, scaling shape, criticality, deployment frequency. |
| `## Cloud & Account Topology` | Provider(s), account/project structure, region strategy, single/multi-account and single/multi-cloud posture with drivers. |
| `## Environment Architecture` | Per environment: purpose, isolation level, data posture, parity, promotion flow, owner. |
| `## Runtime Substrate Selection` | Per workload class: substrate, justification, rejected alternatives. |
| `## Network & Trust-Boundary Architecture` | Per component: trust zone, ingress/egress policy, internet exposure; VPC/subnet/DNS/east-west posture. |
| `## Identity & Access Architecture` | Workload identity, human access, service-to-service auth, admin boundaries, break-glass, audit. |
| `## Secrets & Configuration Strategy` | Store, issuance, rotation cadence, injection mechanism, config-vs-secret boundary. |
| `## Packaging & Artifact Strategy` | Base images, provenance/signing, scanning, registry topology, SBOM, immutability. |
| `## Deployment & Release Architecture` | Per workload class: deployment substrate, release strategy, gating signals, rollback, blast-radius control. |
| `## Infrastructure-as-Code Strategy` | Tool, repo layout, platform-vs-service module boundaries, policy-as-code, state management, drift detection. |
| `## CI/CD Platform Architecture` | Build trust model, artifact/environment promotion, secrets in CI, policy gates, provenance, deployment authorization. |
| `## Cost & FinOps Posture` | Tagging, budget ownership, autoscaling defaults, reserved capacity, egress risk, budget-breach response. |
| `## Disaster & Resilience Posture` | Backup substrate, failover topology, RTO/RPO, restore testing, regional isolation. |
| `## Implementation Handoffs` | Explicit handoffs to `implementations/infrastructure/<vendor>`, `security`, `reliability`, `operations`, `quality-engineering`. |
| `## ADR Index` | Table: ADR number, Title, Status, Summary. Links to `adrs/NNNN-<slug>.md`. Shares the system's monotonic ADR numbering. |

### Conditional sections

Include if material; otherwise omit and add a one-line rationale under `## Omitted sections`.

| Section | When to include |
|---|---|
| `## Cross-Cutting Platform Services` | Shared platform services exist (observability backend, mesh, certs, feature flags). Names ownership and tenant isolation. |
| `## Multi-Region & Tenancy` | Multi-region, multi-cluster, or multi-tenant complexity is opted in. Must name the business driver and the ADR. |

`platform-architecture.md` shares the system's ADR numbering, immutability rule, and supersede chain (see "ADRs"). It does not redefine bounded contexts, components, or data flow — those remain owned by `system-design.md`.

## `security-architecture.md`

Secondary artifact. Present only when `system-design.md` handles sensitive or regulated data, crosses trust or tenant boundaries, integrates third parties, or sits under a regulatory regime. Produced by [`architecture/security`](../../architecture/security/SKILL.md); consumed by security-relevant work across `implementations/*`. One file per system. Conforms to this schema for structure and to [security-standards](../security-standards/README.md) for security content.

### Frontmatter (required)

```yaml
---
product: <kebab-case slug>         # matches the system-design slug
status: draft | review | approved | superseded
owner: <name or role>
system_design: <relative path to source system-design.md>
prd: <relative path to source PRD, or null>
version: <semver, starts at 0.1.0>
last_reviewed: YYYY-MM-DD
---
```

### Required sections

| Section | Purpose |
|---|---|
| `## Overview` | Sensitive assets, the trust boundaries that matter most, what the security architecture optimizes for and intentionally does not cover. |
| `## Security Surface Inventory` | APIs, user/admin flows, jobs, integrations, datastore boundaries, ops interfaces, with sensitive assets and trust assumptions. |
| `## Data Classification` | Per dataset/payload: classification, storage, transmission, logging, retention, non-prod handling. |
| `## Trust Boundary Map` | Per boundary: what changes, authentication, authorization, encryption, audit. |
| `## Threat Model` | Threats tied to named components/flows/actors with category, impact, mitigation, residual risk. |
| `## Identity Architecture` | Per actor class: authentication, federation/MFA, credential lifecycle, session/recovery. |
| `## Authorization Architecture` | Policy model, enforcement points, default-deny posture, cross-tenant/delegated rules, audit signal. |
| `## Secrets & Key Management` | Storage, issuance, rotation, scoping, revocation, key hierarchy, ownership, break-glass. |
| `## Data Protection Rules` | Per classification: in-transit, at-rest, logs, backups, non-prod, deletion; field-level encryption/minimization. |
| `## Input & Output Protection` | Validation, encoding, deserialization, uploads, rendering boundaries, SSRF/untrusted content. |
| `## Logging & Audit Architecture` | Security-relevant events, redaction, retention, tamper-evidence. Pipeline details handed to `operations`. |
| `## Supply-Chain Security` | Dependency provenance/pinning, signing, SBOM, CI/CD trust, promotion controls, third-party trust. |
| `## Implementation Handoffs` | Explicit handoffs to backend/frontend/data architecture, `infrastructure-platform`, `operations`, `reliability`, `quality-engineering`. |
| `## ADR Index` | Table: ADR number, Title, Status, Summary. Links to `adrs/NNNN-<slug>.md`. Shares the system's monotonic ADR numbering. |

### Conditional sections

Include if material; otherwise omit and add a one-line rationale under `## Omitted sections`.

| Section | When to include |
|---|---|
| `## Tenant Isolation Strategy` | The system is multi-tenant. Must state isolation pattern, failure mode if broken, detection, and blast radius. |
| `## Abuse & Rate Protection` | Internet-facing or untrusted-actor surfaces exist. Defines actor-specific limits and enforcement points. |
| `## Compliance Mapping` | A regulatory regime applies (SOC 2, GDPR, HIPAA, PCI DSS, ISO 27001, residency). Maps controls with gaps and owners. |

`security-architecture.md` shares the system's ADR numbering, immutability rule, and supersede chain (see "ADRs"). It does not redefine bounded contexts, components, or data flow — those remain owned by `system-design.md`.

## `ai-architecture.md`

Secondary artifact. Present only when `system-design.md` includes an AI surface (LLM, agent, retrieval, classifier, extractor, or model-driven automation). Produced by [`architecture/ai-native-engineering`](../../architecture/ai-native-engineering/SKILL.md); consumed by `implementations/ai/<vendor>`. One file per system.

### Frontmatter (required)

```yaml
---
product: <kebab-case slug>         # matches the system-design slug
status: draft | review | approved | superseded
owner: <name or role>
system_design: <relative path to source system-design.md>
prd: <relative path to source PRD, or null>
version: <semver, starts at 0.1.0>
last_reviewed: YYYY-MM-DD
---
```

### Required sections

| Section | Purpose |
|---|---|
| `## Overview` | AI capabilities present, user tasks served, what it optimizes for and intentionally does not, highest escalation level reached and why. |
| `## AI Capability Inventory` | Table: Capability, Consumer, User Task, Business Objective, Acceptance Criteria, Risk Profile, Dependencies. |
| `## Capability Classification` | Per capability: escalation level, why that level, why lower levels were rejected. |
| `## Model Contracts` | Per capability: purpose, inputs, output schema, validation, success criteria, confidence handling, failure/retry/fallback/degradation, observability signals. |
| `## Context Architecture` | System prompt scope, instruction hierarchy, retrieval inclusion, prioritization/truncation, context budget, authoritative sources, explicit exclusions. |
| `## Failure Taxonomy` | Table: Failure Class, Detection, Mitigation, Observability Signal, Degradation, User-facing Response. Specific to *this* design. |
| `## Evaluation Strategy` | Per user-visible capability: offline datasets, online metrics, regression gate, ownership, edge/adversarial coverage, drift detection. |
| `## Guardrails & Trust Boundaries` | Explicit trust boundaries with sanitization rules; input filtering, output validation, PII/redaction, prompt-injection posture. |
| `## Cost & Latency Budgets` | Per capability: token/request/latency budget, throughput/concurrency, retrieval depth, tool-call ceiling, mapped to model tier and context size. |
| `## Observability & Operations` | Telemetry, logging/redaction, replay/trace retention, prompt/model versioning, rollback, deployment promotion criteria. |
| `## Implementation Handoffs` | Explicit handoffs to `implementations/ai/<vendor>`, `backend-architecture`, `data-architecture`, `security`, `operations`. |
| `## ADR Index` | Table: ADR number, Title, Status, Summary. Links to `adrs/NNNN-<slug>.md`. Shares the system's monotonic ADR numbering. |

### Conditional sections

Include if material; otherwise omit and add a one-line rationale under `## Omitted sections`.

| Section | When to include |
|---|---|
| `## State & Memory Design` | Conversational or adaptive behavior exists. Omit for stateless capabilities. |
| `## Retrieval Architecture` | Retrieval is in scope. Must classify retrieval as authoritative, assistive, or advisory; hand mechanics to `data-architecture`. |
| `## Tool & Action Surface` | The model can call tools or take actions. Each tool names schema, side-effect class, idempotency, authorization scope, and risk level. |
| `## Agent Control Flow` | The agent suitability test passes. Omit with the suitability rationale when deterministic workflows suffice. |
| `## Model Routing Strategy` | Multiple models or providers exist. Omit for single-model designs. |

`ai-architecture.md` shares the system's ADR numbering, immutability rule, and supersede chain (see "ADRs"). It does not redefine bounded contexts, components, or data flow — those remain owned by `system-design.md`.

## Diagrams

Use Mermaid (`graph`, `flowchart`, `sequenceDiagram`) inline. PNG/SVG only when Mermaid is insufficient; place under `assets/diagrams/`.

## Per-component breakout (optional escalation)

For small systems, the inline `## Components` section is sufficient. Promote a component to its own file in `components/<name>.md` when ANY of the following hold:

- The component is `tier: 0` (see "Component tiers" below).
- Its interface surface exceeds ~5 endpoints or topics.
- It has independent ownership distinct from the system as a whole.
- It implements a distinct pattern (e.g. event-driven module inside an otherwise synchronous system).

Per-component files use this frontmatter:

```yaml
---
component: <kebab-case>
owner: <team or role>
tier: 0 | 1 | 2 | 3
implements: [<architecture-domain-ref>, ...]
implementation: <impl-ref>           # e.g. implementations/backend/spring-boot
patterns: [<pattern-ref>, ...]
---
```

Required sections in a component file: Responsibility, Public interface, Data ownership, Runtime, Observability hooks, SLOs.

## Component tiers

Declared in component frontmatter and used by other standards (deployment gates, security review depth, observability coverage):

| Tier | Meaning |
|---|---|
| 0 | Critical path — outage is incident-grade |
| 1 | Important — degraded experience without it |
| 2 | Standard — affects a subset of users |
| 3 | Experimental — failure is acceptable |

## ADRs

`adrs/NNNN-<slug>.md`:

```markdown
---
id: NNNN
title: <Decision title>
status: proposed | accepted | superseded | deprecated
date: YYYY-MM-DD
supersedes: <NNNN or null>
---

## Context
## Decision
## Consequences
## Alternatives considered
```

Rules:

- Numbering is monotonic across the system; never reused.
- Once an ADR is `accepted`, the body MUST NOT be edited. Changes require a new ADR that `supersedes` the old one.
- ADRs are drafted inline as decisions are made, not retroactively.
- `Consequences` MUST include downsides, not only benefits.
- `Alternatives considered` is non-optional — the value of an ADR is the rejected options.

## Linkage contract

- `system-design.md` MUST link to its source PRD in frontmatter.
- Every component (inline subsection or breakout file) MUST list the `architecture/` it implements.
- Every ADR MUST be referenced from `system-design.md`'s ADR Index.
- `data-architecture.md`, `frontend-architecture.md`, `platform-architecture.md`, `security-architecture.md`, and `ai-architecture.md`, when present, MUST link to their source `system-design.md` in frontmatter and MUST NOT redefine bounded contexts, components, or data flow.
- Once `system-design.md` is `approved`, it is the sole upstream input to `implementations/*` scaffolding skills; when a non-trivial data layer exists, an `approved` `data-architecture.md` is the upstream input to `implementations/data/*`; when a user-facing frontend exists, an `approved` `frontend-architecture.md` is the upstream input to `implementations/frontend/*`; when dedicated platform/infra architecture exists, an `approved` `platform-architecture.md` is the upstream input to `implementations/infrastructure/*`; when the system handles sensitive data or crosses trust boundaries, an `approved` `security-architecture.md` constrains security-relevant work across `implementations/*`; when an AI surface exists, an `approved` `ai-architecture.md` is the upstream input to `implementations/ai/*`.

## Versioning

- Bump **patch** for typo / clarification edits.
- Bump **minor** for added components, ADRs, or failure modes.
- Bump **major** when architecture style or bounded contexts change — requires re-approval and a superseding ADR.

## Anti-patterns

- ADRs without "Alternatives considered" — the value of an ADR is the rejected options.
- Components that write to another component's data (silent coupling).
- Hand-drawn architecture images instead of Mermaid (cannot be diffed).
- Generic failure-mode checklists ("queue backlog" listed when there is no queue).
- Persistence Strategy section padded with "we use Postgres" when one paragraph in Components would do.
- ADRs retrofitted from prose at the end of the design pass instead of drafted inline.
