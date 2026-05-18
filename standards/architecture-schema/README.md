# architecture-schema

Canonical structure for system architecture documents and Architecture Decision Records (ADRs). Produced by `skills/architecture/system-design`; consumed by every downstream implementation domain.

## File layout

```
docs/architecture/<product-slug>/
├── system-design.md           # primary artifact, always present
├── data-architecture.md       # OPTIONAL — only when the design has a non-trivial data layer (see "data-architecture.md")
├── frontend-architecture.md   # OPTIONAL — only when the design has a user-facing frontend (see "frontend-architecture.md")
├── mobile-architecture.md     # OPTIONAL — only when the design has a native or cross-platform-native mobile app (see "mobile-architecture.md")
├── platform-architecture.md   # OPTIONAL — only when the design needs dedicated platform/infra architecture (see "platform-architecture.md")
├── security-architecture.md   # OPTIONAL — only when the design handles sensitive data or crosses trust/tenant boundaries (see "security-architecture.md")
├── ai-architecture.md         # OPTIONAL — only when the design has an AI surface (see "ai-architecture.md")
├── reliability-architecture.md # OPTIONAL — only when the design has externally meaningful availability commitments (see "reliability-architecture.md")
├── performance-architecture.md # OPTIONAL — only when user-visible latency, throughput, or cost-per-request materially constrains the design (see "performance-architecture.md")
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

Secondary artifact. Present only when `system-design.md` includes a non-trivial operational data layer (multiple stores, cross-context read models, sharding, replication, or caching concerns). Produced by [`skills/architecture/data-architecture`](../../skills/architecture/data-architecture/SKILL.md); consumed by `skills/implementations/data/<engine>`. One file per system.

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
| `## Implementation Handoffs` | Explicit handoffs to `skills/implementations/data/<engine>`, `backend-architecture`, `security`, `reliability`, `operations`. |
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

Secondary artifact. Present only when `system-design.md` includes a user-facing web frontend. Produced by [`skills/architecture/frontend-architecture`](../../skills/architecture/frontend-architecture/SKILL.md); consumed by `skills/implementations/frontend/<framework>`. One file per system.

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
| `## Implementation Handoffs` | Explicit handoffs to `skills/implementations/frontend/<framework>`, `backend-architecture`, `security`, `performance`, `quality-engineering`. |
| `## ADR Index` | Table: ADR number, Title, Status, Summary. Links to `adrs/NNNN-<slug>.md`. Shares the system's monotonic ADR numbering. |

### Conditional sections

Include if material; otherwise omit and add a one-line rationale under `## Omitted sections`.

| Section | When to include |
|---|---|
| `## Internationalization & Localization` | Multi-locale or RTL is in scope. Defines locale routing, translation loading, and formatting/timezone handling. |
| `## Real-time, Offline & Resilience` | Realtime or offline features exist. Must define failure fallback, reconnect, and reconciliation behavior. |

`frontend-architecture.md` shares the system's ADR numbering, immutability rule, and supersede chain (see "ADRs"). It does not redefine bounded contexts, components, or data flow — those remain owned by `system-design.md`.

## `mobile-architecture.md`

Secondary artifact. Present only when `system-design.md` includes a native or cross-platform-native mobile application. Produced by [`skills/architecture/mobile-architecture`](../../skills/architecture/mobile-architecture/SKILL.md); consumed by `skills/implementations/mobile/<ecosystem>`. One file per system. Mobile-web and PWA are not in scope here — those remain in `frontend-architecture.md`.

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
| `## Executive Summary` | Mobile app(s) and platforms present, primary user journeys, API boundary, what it optimizes for and intentionally does not. |
| `## Platform Strategy` | Native vs cross-platform-native vs hybrid with rationale, trade-offs, rejected alternatives, minimum OS, device classes. |
| `## Application Architecture` | Layers, module boundaries, state ownership, side effects, concurrency, lifecycle, dependency injection. |
| `## Navigation Architecture` | Hierarchy, route ownership, deep links, modals, auth transitions, tab/shell, back-navigation and restoration. |
| `## State Management Strategy` | Local/session/cached/persistent state: ownership, mechanism, sync, persistence, invalidation; optimistic updates and conflict resolution. |
| `## Offline & Synchronization Design` | Offline capabilities, sync model, queueing, retry, conflict resolution, authoritative sources, reconciliation, degraded-mode per journey. |
| `## Device Capability Integration` | Per capability: permission strategy, fallback, privacy, battery impact, failure handling, platform limits. |
| `## Performance & Battery Budgets` | Measurable targets (start, latency, memory, background, battery, network, storage) with degradation behavior. |
| `## Security & Privacy Callouts` | Callout only — mobile-specific security/privacy concerns summarized as ADR candidates; ownership belongs to `security`. |
| `## Accessibility & Localization` | Screen-reader support, dynamic text, reduced motion, contrast, RTL, font scaling, internationalization. |
| `## Error Handling & Recovery` | Global error strategy, retry ceilings, crash recovery, interrupted-session handling, degraded-mode UX. |
| `## Observability & Analytics` | Crash, performance, network, journey/screen, startup/battery telemetry, release monitoring, PII redaction, sampling, retention. |
| `## Testing Strategy` | Unit/integration/UI-automation/offline/device-compat/accessibility/perf-regression scope, release gating, rollback validation. |
| `## Release & Operations Callouts` | Callout only — release channels, staged rollout, store submission, forced-upgrade, deprecation as ADR candidates; ownership belongs to `operations`/`infrastructure-platform`. |
| `## Failure Taxonomy` | Per failure: detection, mitigation, recovery, observability, user-facing behavior. |
| `## Implementation Handoffs` | Explicit handoffs to `skills/implementations/mobile/<ecosystem>`, `backend-architecture`, `security`, `operations`/`infrastructure-platform`, `quality-engineering`. |
| `## ADR Index` | Table: ADR number, Title, Status, Summary. Links to `adrs/NNNN-<slug>.md`. Shares the system's monotonic ADR numbering. |

### Conditional sections

Include if material; otherwise omit and add a one-line rationale under `## Omitted sections`.

| Section | When to include |
|---|---|
| `## Notifications & Background Behavior` | Push notifications or background work exist. Defines push types, delivery, priority, opt-in, rate-limiting, and silent-notification handling. |

`mobile-architecture.md` shares the system's ADR numbering, immutability rule, and supersede chain (see "ADRs"). It does not redefine bounded contexts, components, or data flow — those remain owned by `system-design.md`. It does not own security/privacy or release/operations design — those are callouts whose decisions are owned by `security` and `operations`/`infrastructure-platform`. Cross-references to a product's `frontend-architecture.md` are optional and non-binding; `mobile-architecture.md` is independently valid without one.

## `platform-architecture.md`

Secondary artifact. Present only when `system-design.md` needs dedicated platform and infrastructure architecture (cloud/account topology, runtime substrate, network trust zones, deployment substrate). Produced by [`skills/architecture/infrastructure-platform`](../../skills/architecture/infrastructure-platform/SKILL.md); consumed by `skills/implementations/infrastructure/<vendor>`. One file per system.

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
| `## Implementation Handoffs` | Explicit handoffs to `skills/implementations/infrastructure/<vendor>`, `security`, `reliability`, `operations`, `quality-engineering`. |
| `## ADR Index` | Table: ADR number, Title, Status, Summary. Links to `adrs/NNNN-<slug>.md`. Shares the system's monotonic ADR numbering. |

### Conditional sections

Include if material; otherwise omit and add a one-line rationale under `## Omitted sections`.

| Section | When to include |
|---|---|
| `## Cross-Cutting Platform Services` | Shared platform services exist (observability backend, mesh, certs, feature flags). Names ownership and tenant isolation. |
| `## Multi-Region & Tenancy` | Multi-region, multi-cluster, or multi-tenant complexity is opted in. Must name the business driver and the ADR. |

`platform-architecture.md` shares the system's ADR numbering, immutability rule, and supersede chain (see "ADRs"). It does not redefine bounded contexts, components, or data flow — those remain owned by `system-design.md`.

## `security-architecture.md`

Secondary artifact. Present only when `system-design.md` handles sensitive or regulated data, crosses trust or tenant boundaries, integrates third parties, or sits under a regulatory regime. Produced by [`skills/architecture/security`](../../skills/architecture/security/SKILL.md); consumed by security-relevant work across `skills/implementations/*`. One file per system. Conforms to this schema for structure and to [security-standards](../security-standards/README.md) for security content.

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

Secondary artifact. Present only when `system-design.md` includes an AI surface (LLM, agent, retrieval, classifier, extractor, or model-driven automation). Produced by [`skills/architecture/ai-native-engineering`](../../skills/architecture/ai-native-engineering/SKILL.md); consumed by `skills/implementations/ai/<vendor>`. One file per system.

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
| `## Implementation Handoffs` | Explicit handoffs to `skills/implementations/ai/<vendor>`, `backend-architecture`, `data-architecture`, `security`, `operations`. |
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

## `reliability-architecture.md`

Secondary artifact. Present only when `system-design.md` has externally meaningful availability commitments, multi-component failure interactions, or stateful dependencies whose loss requires a recovery plan. Produced by [`skills/architecture/reliability`](../../skills/architecture/reliability/SKILL.md); consumed by reliability-relevant work in `skills/implementations/infrastructure/<vendor>` and `skills/implementations/data/<engine>`. One file per system.

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
| `## Overview` | Reliability scope, critical user journeys, what the reliability architecture optimizes for and intentionally does not cover. |
| `## Service-Level Objectives` | Table: Journey/Workflow, SLI, Measurement Point, Target, Time Window, Owner. SLOs are user-visible, not infrastructure vanity metrics. |
| `## Error-Budget Policy` | Per SLO: budget, burn-rate thresholds, alert posture, and the operational response (deploy freeze, focus shift, escalation). |
| `## Dependency Criticality` | Per dependency: class (critical / degradable / optional), outage impact, fallback posture, detection signal. No hidden hard dependencies. |
| `## Failure Modes` | Table: Component, Failure Shape, Trigger, Blast Radius, Detection, Mitigation, Recovery. Specific to *this* design — no generic checklists. |
| `## Graceful Degradation` | Per critical journey: degraded behavior, user-visible signal, fallback mechanism, recovery path, acceptable degradation window. |
| `## Redundancy & High Availability` | Per component: strategy, placement topology, failover trigger, failover time, the failure mode it addresses, consistency tradeoff. |
| `## Blast-Radius Isolation` | Isolation unit, containment boundary, saturation controls, trip and recovery thresholds. |
| `## Disaster Recovery` | Per critical datastore/workflow: backup strategy, restore tooling, failover topology, RTO, RPO, rehearsal cadence, last validated date. |
| `## Release Safety` | Deploy gating signals, rollback path, progressive-delivery posture, feature-flag fallbacks, automatic-rollback triggers. |
| `## Implementation Handoffs` | Explicit handoffs to `operations`, `infrastructure-platform`, `performance`, `security`, `backend-architecture`, `data-architecture`. |
| `## ADR Index` | Table: ADR number, Title, Status, Summary. Links to `adrs/NNNN-<slug>.md`. Shares the system's monotonic ADR numbering. |

### Conditional sections

Include if material; otherwise omit and add a one-line rationale under `## Omitted sections`.

| Section | When to include |
|---|---|
| `## Chaos & Game-Day Validation` | Failover, degradation, or restore paths exist that must be exercised. Must name exercises, cadence, success criterion, and operational ownership. |
| `## Incident Posture` | Reliability seeds severity/paging inputs that `operations` refines. Defines severity model, page-worthy symptom set, customer-impact threshold. Omit when `operations` fully owns the incident model. |
| `## Multi-Region Strategy` | Multi-region or active-active topology is opted in. Must name the business driver, the ADR, and the consistency tradeoff. |

`reliability-architecture.md` shares the system's ADR numbering, immutability rule, and supersede chain (see "ADRs"). It does not redefine bounded contexts, components, or data flow — those remain owned by `system-design.md`.

## `performance-architecture.md`

Secondary artifact. Present only when `system-design.md` has user-visible paths whose latency, throughput, concurrency, or cost-per-request materially constrains the design, or when a scale event is anticipated. Produced by [`skills/architecture/performance`](../../skills/architecture/performance/SKILL.md); consumed by performance-relevant work in `skills/implementations/backend/<framework>`, `skills/implementations/frontend/<framework>`, `skills/implementations/data/<engine>`, and `skills/implementations/infrastructure/<vendor>`. One file per system.

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
| `## Overview` | Performance scope, the user-visible paths that matter, what the architecture optimizes for and intentionally does not. |
| `## Workload Shape` | Per workload: class (interactive/streaming/background/batch/event-driven), steady-state and peak RPS, concurrency, burst shape, growth horizon, worst plausible spike. |
| `## Performance Budgets` | Per user-visible path: p50/p95/p99 latency, throughput, concurrency, timeout posture, cost-per-request/user/job, measurement point, owner. Numerical, not "fast". |
| `## Critical & Hot Paths` | Per journey: synchronous critical path (drives latency), hot path (drives cost), fan-out and serialization points. The two may diverge. |
| `## Capacity Model` | Per workload: CPU, memory, IOPS, network, connections, queue depth, payload size, cache memory at peak and worst plausible spike; headroom factor and exhaustion threshold. |
| `## Scaling Posture` | Per workload: vertical/horizontal/autoscaled/queue-buffered/partitioned, trigger, scaling lag, ceiling, and ceiling behavior (queue/degrade/shed/fail). |
| `## Backpressure & Load Shedding` | Per saturable dependency: queue posture, retry/timeout posture, concurrency cap, circuit-breaker behavior, shed behavior, user-visible symptom, recovery condition. |
| `## Performance Testing` | Load/stress/soak/spike/failover tests: workload simulated, production likeness, budgets validated, pass/fail criteria, environment parity. |
| `## Regression Gating` | Which metrics block release, which alert, which are informational; CI/release/canary gates, rollback thresholds, measurement source of truth, ownership. |
| `## Cost-Performance Tradeoffs` | Hard limits vs negotiable budgets, elasticity posture, cost-escalation triggers, which paths justify higher spend, which degrade under cost pressure. |
| `## Implementation Handoffs` | Explicit handoffs to `backend-architecture`, `frontend-architecture`, `data-architecture`, `infrastructure-platform`, `reliability`, `operations`. |
| `## ADR Index` | Table: ADR number, Title, Status, Summary. Links to `adrs/NNNN-<slug>.md`. Shares the system's monotonic ADR numbering. |

### Conditional sections

Include if material; otherwise omit and add a one-line rationale under `## Omitted sections`.

| Section | When to include |
|---|---|
| `## Caching & Precomputation` | One or more cache, read-model, or precomputation layers exist. Each names source of truth, cached entity, invalidation trigger, TTL/staleness budget, warm-up, stampede protection, and the budget delta it buys. |
| `## Geographic Distribution` | Users or workloads span regions and latency/correctness is region-sensitive. Names region topology and the synchronous cross-region cost. |

`performance-architecture.md` shares the system's ADR numbering, immutability rule, and supersede chain (see "ADRs"). It does not redefine bounded contexts, components, or data flow — those remain owned by `system-design.md`. Cache mechanics, when in scope, are decided here in budget terms and handed to `data-architecture` and `backend-architecture` for implementation.

## Diagrams

Use Mermaid (`graph`, `flowchart`, `sequenceDiagram`) inline. PNG/SVG only when Mermaid is insufficient; place under `assets/diagrams/`.

`system-design.md` MUST contain at least:

- a **context / bounded-context diagram** showing the system's bounded contexts and their dependencies, and
- a **primary-workflow diagram** (data-flow or sequence) for the core workflow named in the PRD.

Other architecture documents include the topology diagram their authoring skill's Outputs names *when it is material*; when omitted, list it under `## Omitted sections` with a one-line rationale (same conditional-omission rule as sections).

**Diagram–prose consistency (required):**

- Every node in a diagram MUST correspond to a named element in the document's prose (bounded context, component, datastore, or actor present in the relevant section). No phantom nodes.
- Every entry in `## Bounded Contexts` MUST appear in the context / bounded-context diagram. Diagram and prose cannot disagree.

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
implementation: <impl-ref>           # e.g. skills/implementations/backend/spring-boot
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
- Every component (inline subsection or breakout file) MUST list the `skills/architecture/` it implements.
- Every ADR MUST be referenced from `system-design.md`'s ADR Index.
- `data-architecture.md`, `frontend-architecture.md`, `platform-architecture.md`, `security-architecture.md`, `ai-architecture.md`, `reliability-architecture.md`, and `performance-architecture.md`, when present, MUST link to their source `system-design.md` in frontmatter and MUST NOT redefine bounded contexts, components, or data flow.
- Once `system-design.md` is `approved`, it is the sole upstream input to `skills/implementations/*` scaffolding skills; when a non-trivial data layer exists, an `approved` `data-architecture.md` is the upstream input to `skills/implementations/data/*`; when a user-facing frontend exists, an `approved` `frontend-architecture.md` is the upstream input to `skills/implementations/frontend/*`; when dedicated platform/infra architecture exists, an `approved` `platform-architecture.md` is the upstream input to `skills/implementations/infrastructure/*`; when the system handles sensitive data or crosses trust boundaries, an `approved` `security-architecture.md` constrains security-relevant work across `skills/implementations/*`; when an AI surface exists, an `approved` `ai-architecture.md` is the upstream input to `skills/implementations/ai/*`; when the system has externally meaningful availability commitments, an `approved` `reliability-architecture.md` is the upstream input to reliability-relevant work in `skills/implementations/infrastructure/*` and `skills/implementations/data/*`; when user-visible latency, throughput, or cost-per-request materially constrains the design, an `approved` `performance-architecture.md` is the upstream input to performance-relevant work across `skills/implementations/backend/*`, `skills/implementations/frontend/*`, `skills/implementations/data/*`, and `skills/implementations/infrastructure/*`.

## Versioning

- Bump **patch** for typo / clarification edits.
- Bump **minor** for added components, ADRs, or failure modes.
- Bump **major** when architecture style or bounded contexts change — requires re-approval and a superseding ADR.

## Anti-patterns

- ADRs without "Alternatives considered" — the value of an ADR is the rejected options.
- Components that write to another component's data (silent coupling).
- Hand-drawn architecture images instead of Mermaid (cannot be diffed).
- Diagram that names a component or context absent from the prose, or a `## Bounded Contexts` entry missing from the context diagram — diagram and prose must agree.
- Generic failure-mode checklists ("queue backlog" listed when there is no queue).
- Persistence Strategy section padded with "we use Postgres" when one paragraph in Components would do.
- ADRs retrofitted from prose at the end of the design pass instead of drafted inline.
