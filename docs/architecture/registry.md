# Architecture Registry

> Single source of truth for architecture↔implementation mapping, domain/ecosystem ownership, and upstream/downstream wiring. Replaces the per-directory README.md files that previously held this metadata.
>
> Skills are discovered by file system (skills/architecture/<domain>/SKILL.md and skills/implementations/<category>/<ecosystem>/<skill>/SKILL.md). This file documents the *charter* of each domain and ecosystem.

## Architecture domains

### ai-native-engineering

**Status:** draft

**Purpose:** Defines AI system architecture from an approved system design: capability classification, model contracts, context and memory strategy, retrieval and grounding topology, tool and action surface, agent control flow, failure taxonomy, evaluation and guardrail plans, cost and latency budgets, model routing, and observability requirements.

Technology-agnostic. Owns *what* AI capabilities the system exposes and *how* they behave, not the SDK or framework that runs them. Vendor-specific runtime scaffolding lives under [skills/implementations/ai](../../skills/implementations/ai/).

**Owns:**
- AI capability boundaries and escalation-ladder classification
- Model contracts (inputs, outputs, success criteria, degradation)
- Context architecture, state, and memory strategy
- Retrieval topology and grounding authority (mechanics handed to data-architecture)
- Tool and action contract surface and autonomy ceilings
- Agent suitability test and control flow
- Failure taxonomy, guardrails, and trust boundaries
- Evaluation strategy and regression gates
- Cost/latency budgets, model routing, and AI observability

**Produces:**

| Artifact | Conforms to |
|---|---|
| `ai-architecture.md` | [architecture-schema](../../standards/architecture-schema/README.md), [documentation-standards](../../standards/documentation-standards/README.md) |
| ADR drafts (capability, retrieval authority, autonomy, memory, routing) | [architecture-schema](../../standards/architecture-schema/README.md) |

**Standards this architecture domain conforms to:**
- [architecture-schema](../../standards/architecture-schema/README.md) - `ai-architecture.md` artifact structure and system-design traceability.
- [security-standards](../../standards/security-standards/README.md) - guardrails, PII handling, trust boundaries.
- [observability-standards](../../standards/observability-standards/README.md) - AI telemetry and operational signals.
- [deployment-standards](../../standards/deployment-standards/README.md) - rollback and promotion criteria.
- [documentation-standards](../../standards/documentation-standards/README.md) - skill structure.

**Upstream inputs:** Requires an approved `system-design.md` per [architecture-schema](../../standards/architecture-schema/README.md) whose design includes an AI surface. Bounded contexts, component interfaces, data ownership, and ADRs shape the AI architecture produced here.

**Downstream consumers:**

AI architecture produced here is the source of truth for:

- [skills/implementations/ai/*](../../skills/implementations/ai/) - vendor runtimes (Anthropic, OpenAI, LangChain, AutoGen, CrewAI) follow model contracts, tool surfaces, and evaluation gates.
- [backend-architecture](#backend-architecture) - orchestration ownership and request-path touchpoints.
- [data-architecture](#data-architecture) - retrieval corpora ownership, ingestion, indexing, and embedding lifecycle.
- [security](#security) - trust boundaries, prompt-injection posture, and audit needs.

**Skills:**
- [ai-native-engineering](../../skills/architecture/ai-native-engineering/SKILL.md) — turns an approved system design with an AI surface into AI system architecture: capability classification, model contracts, context/memory, retrieval, tools, agent control flow, failure taxonomy, evaluation, guardrails, budgets, routing, observability, and implementation handoffs.

---

### backend-architecture

**Status:** draft

**Purpose:** Defines backend execution architecture and service behavior from an approved system design: service boundaries, domain behavior, API and async contracts, transactional boundaries, consistency rules, security touchpoints, and implementation handoffs.

Technology-agnostic. Owns *what* a backend service exposes and *how* it behaves, not the framework that runs it. Framework-specific scaffolding lives under [skills/implementations/backend](../../skills/implementations/backend/).

**Owns:**
- REST / GraphQL / event contracts
- Domain models and aggregates
- Commands, queries, lifecycle states, and invariants
- Transactional boundaries and consistency rules
- Async workflows, queues, jobs, retries, and compensations
- Idempotency and concurrency semantics
- Service-to-service communication patterns
- Backend security and operational touchpoints

**Produces:**

| Artifact | Conforms to |
|---|---|
| `backend-architecture.md` | [architecture-schema](../../standards/architecture-schema/README.md), [documentation-standards](../../standards/documentation-standards/README.md) |
| `openapi.yaml` (REST contracts, when needed) | [api-standards](../../standards/api-standards/README.md) |
| `api-conventions.md` (REST conventions, when needed) | [api-standards](../../standards/api-standards/README.md), [naming-conventions](../../standards/naming-conventions/README.md) |
| Event/job/workflow notes | [api-standards async/event rules](../../standards/api-standards/README.md) |

**Standards this architecture domain conforms to:**
- [architecture-schema](../../standards/architecture-schema/README.md) - system-design traceability and decision structure.
- [api-standards](../../standards/api-standards/README.md) - global REST/async contract rules.
- [security-standards](../../standards/security-standards/README.md) - auth schemes, scopes, secrets.
- [naming-conventions](../../standards/naming-conventions/README.md) - path segments, identifiers, topics.
- [documentation-standards](../../standards/documentation-standards/README.md) - skill structure.

**Upstream inputs:** Requires an approved `system-design.md` per [architecture-schema](../../standards/architecture-schema/README.md). Bounded contexts, component interfaces, data ownership, and ADRs in the system design shape the backend architecture produced here.

**Downstream consumers:**

Backend architecture produced here is the source of truth for:

- [skills/implementations/backend/*](../../skills/implementations/backend/) - server scaffolds, modules, controllers, DTOs, workers, and integration points follow the backend architecture.
- [skills/implementations/data/*](../../skills/implementations/data/) - schema and migration skills consume ownership, transaction, and consistency decisions.
- [skills/implementations/frontend/*](../../skills/implementations/frontend/) - client SDKs and typed fetch layers consume published contracts.
- [skills/architecture/quality-engineering](#quality-engineering) - contract-driven and workflow-driven integration tests.

**Skills:**
- [backend-architecture](../../skills/architecture/backend-architecture/SKILL.md) — turns approved system design into backend service architecture: boundaries, domain behavior, interface strategy, transactions, consistency, security touchpoints, operations, and implementation handoff notes.

---

### data-architecture

**Status:** draft

**Purpose:** Defines the operational data layer from an approved system design: data ownership boundaries, engine selection, consistency model, schema strategy, indexing posture, partitioning and replication topology, cache architecture, retention and deletion policy, and migration strategy.

Technology-agnostic and operationally focused. Owns *which* datasets exist, *who* owns them, and *how* they behave operationally, not the engine-specific DDL that implements them. Engine-specific schema and migration work lives under [skills/implementations/data](../../skills/implementations/data/).

**Owns:**
- Dataset ownership boundaries and authoritative write paths
- Engine selection justified by access patterns
- Consistency and concurrency model per write path
- Schema, key design, and tenant isolation strategy
- Indexing posture mapped to named access patterns
- Partitioning/sharding posture and replication/HA topology
- Cache architecture and invalidation contracts
- Retention, deletion, and compliance policy
- Migration strategy and operational readiness

**Produces:**

| Artifact | Conforms to |
|---|---|
| `data-architecture.md` | [architecture-schema](../../standards/architecture-schema/README.md), [documentation-standards](../../standards/documentation-standards/README.md) |
| ADR drafts (engine, consistency, partitioning, replication, retention) | [architecture-schema](../../standards/architecture-schema/README.md) |

**Standards this architecture domain conforms to:**
- [architecture-schema](../../standards/architecture-schema/README.md) - `data-architecture.md` artifact structure and system-design traceability.
- [security-standards](../../standards/security-standards/README.md) - tenant isolation, PII handling, encryption, audit.
- [observability-standards](../../standards/observability-standards/README.md) - data-layer monitoring signals.
- [deployment-standards](../../standards/deployment-standards/README.md) - migration phasing and rollback.
- [documentation-standards](../../standards/documentation-standards/README.md) - skill structure.

**Upstream inputs:** Requires an approved `system-design.md` per [architecture-schema](../../standards/architecture-schema/README.md) whose design declares bounded contexts and data ownership. Those boundaries, component interfaces, and ADRs shape the data architecture produced here.

**Downstream consumers:**

Data architecture produced here is the source of truth for:

- [skills/implementations/data/*](../../skills/implementations/data/) - Postgres, MongoDB, Redis, Elasticsearch, and ClickHouse schema and migration skills follow ownership, consistency, and indexing decisions.
- [backend-architecture](#backend-architecture) - transactional boundaries and consistency expectations.
- [ai-native-engineering](#ai-native-engineering) - retrieval corpora ownership and ingestion lifecycle.
- [security](#security) - tenant isolation, retention, and audit boundaries.

**Skills:**
- [data-architecture](../../skills/architecture/data-architecture/SKILL.md) — turns an approved system design into operational data architecture: ownership boundaries, engine selection, consistency, schema, indexing, partitioning, replication, cache, retention, migration, operations, and implementation handoffs.

---

### frontend-architecture

**Status:** draft

**Purpose:** Defines frontend application architecture from an approved system design: application-shell structure, routing and rendering strategy, state and data-flow architecture, auth and session handling, design-system boundaries, accessibility posture, performance budgets, resilience behavior, and client observability.

Technology-agnostic and framework-agnostic first. Owns *how the application is structured and behaves*, not the visual design or the framework that renders it. Visual and component design lives in the [frontend-design](../../skills/implementations/frontend/frontend-design/SKILL.md) skill; framework-specific scaffolding lives under [skills/implementations/frontend](../../skills/implementations/frontend/).

**Owns:**
- Application shell and micro-frontend posture
- Routing model and route-level rendering strategy
- State tiers (server-cache, URL, ephemeral UI, durable client)
- Data fetching and caching contracts
- Client auth and session handling
- Design-system seam and theming propagation
- Accessibility posture and testing expectations
- Performance budgets and breach actions
- Real-time/offline resilience and client observability

**Produces:**

| Artifact | Conforms to |
|---|---|
| `frontend-architecture.md` | [architecture-schema](../../standards/architecture-schema/README.md), [documentation-standards](../../standards/documentation-standards/README.md) |
| ADR drafts (framework, rendering, token storage, performance budget) | [architecture-schema](../../standards/architecture-schema/README.md) |

**Standards this architecture domain conforms to:**
- [architecture-schema](../../standards/architecture-schema/README.md) - `frontend-architecture.md` artifact structure and system-design traceability.
- [security-standards](../../standards/security-standards/README.md) - token storage, CSRF/XSS posture, PII rendering.
- [observability-standards](../../standards/observability-standards/README.md) - client telemetry and RUM signals.
- [deployment-standards](../../standards/deployment-standards/README.md) - performance-budget gates and rollout.
- [documentation-standards](../../standards/documentation-standards/README.md) - skill structure.

**Upstream inputs:** Requires an approved `system-design.md` per [architecture-schema](../../standards/architecture-schema/README.md) whose design includes a user-facing web frontend. Bounded contexts, component interfaces, API/BFF boundaries, and ADRs shape the frontend architecture produced here.

**Downstream consumers:**

Frontend architecture produced here is the source of truth for:

- [skills/implementations/frontend/*](../../skills/implementations/frontend/) - Next.js, React, Angular, Vue, and Svelte skills follow routing, rendering, state, and data-layer decisions.
- [backend-architecture](#backend-architecture) - BFF/API and streaming contract expectations.
- [security](#security) - token storage, CSRF/XSS, embedding, and PII-rendering boundaries.
- [performance](#performance) - performance-budget enforcement and regression gates.

**Skills:**
- [frontend-architecture](../../skills/architecture/frontend-architecture/SKILL.md) — turns an approved system design into frontend application architecture: shell, routing, rendering, state, data flow, auth, design-system seam, accessibility, performance, resilience, observability, and implementation handoffs.

---

### idea-development

**Status:** draft

**Purpose:** Develops an idea through discovery, refinement, validation, specification, and execution readiness for a product, feature, workflow, SaaS, AI tool, internal tool, marketplace, or service. Produces a concise, decision-oriented PRD or readiness brief that narrows v1 scope, names user pain, documents assumptions and risks, defines success metrics, and leaves only intentionally deferred questions open.

**Owns:**
- PRDs
- Idea discovery
- Idea refinement
- Idea validation
- MVP scoping
- Roadmap planning
- Feature decomposition
- User journeys
- Success metrics
- Feasibility analysis
- Execution readiness

**Produces:**

| Artifact | Conforms to |
|---|---|
| `PRD.md` | [prd-schema](../../standards/prd-schema/README.md) |
| Readiness note | — |

**Standards this architecture domain conforms to:**
- [prd-schema](../../standards/prd-schema/README.md)
- [documentation-standards](../../standards/documentation-standards/README.md)
- [naming-conventions](../../standards/naming-conventions/README.md)

**Downstream consumers:**
- [skills/architecture/system-design](#system-design)
- [skills/architecture/backend-architecture](#backend-architecture)
- [skills/architecture/frontend-architecture](#frontend-architecture)
- [skills/architecture/quality-engineering](#quality-engineering)

**Skills:**
- [idea-development](../../skills/architecture/idea-development/SKILL.md) — develops an informal product idea through discovery, refinement, validation, specification, and execution readiness; emits a decision-oriented PRD conforming to prd-schema plus a readiness note.

---

### infrastructure-platform

**Status:** draft

**Purpose:** Defines platform and infrastructure architecture from an approved system design: cloud and account topology, environment model, runtime substrate selection, network and trust-boundary architecture, identity and secrets strategy, deployment and release substrate, IaC ownership boundaries, CI/CD posture, operational platform services, cost strategy, and disaster posture.

Technology-agnostic and platform-oriented. Owns *what platform contracts exist and how workloads are isolated, deployed, and operated*, not the Terraform/manifests that implement them. Vendor-specific IaC and pipeline code lives under [skills/implementations/infrastructure](../../skills/implementations/infrastructure/).

**Owns:**
- Cloud/account topology and environment model
- Runtime substrate selection per workload class
- Network architecture and named trust boundaries
- Workload/human/service identity and secrets lifecycle
- Packaging, deployment, and release substrate
- IaC ownership boundaries and CI/CD trust model
- Cross-cutting platform services posture
- Cost/FinOps posture and disaster/resilience posture

**Produces:**

| Artifact | Conforms to |
|---|---|
| `platform-architecture.md` | [architecture-schema](../../standards/architecture-schema/README.md), [documentation-standards](../../standards/documentation-standards/README.md) |
| ADR drafts (substrate, region topology, IaC tool, deployment mechanism) | [architecture-schema](../../standards/architecture-schema/README.md) |

**Standards this architecture domain conforms to:**
- [architecture-schema](../../standards/architecture-schema/README.md) - `platform-architecture.md` artifact structure and system-design traceability.
- [security-standards](../../standards/security-standards/README.md) - trust zones, identity, secrets, supply-chain posture.
- [observability-standards](../../standards/observability-standards/README.md) - platform telemetry substrate.
- [deployment-standards](../../standards/deployment-standards/README.md) - release substrate, gating, rollback.
- [documentation-standards](../../standards/documentation-standards/README.md) - skill structure.

**Upstream inputs:** Requires an approved `system-design.md` per [architecture-schema](../../standards/architecture-schema/README.md) whose design needs dedicated platform/infrastructure architecture. Workload inventory, component boundaries, and ADRs shape the platform architecture produced here.

**Downstream consumers:**

Platform architecture produced here is the source of truth for:

- [skills/implementations/infrastructure/*](../../skills/implementations/infrastructure/) - AWS, GCP, Azure, Kubernetes, Terraform, and GitHub Actions skills follow topology, substrate, and trust-boundary decisions.
- [security](#security) - trust zones, identity, secrets, and supply-chain boundaries.
- [reliability](#reliability) - failover topology and RTO/RPO inputs.
- [operations](#operations) - observability substrate and runbook hooks.

**Skills:**
- [infrastructure-platform](../../skills/architecture/infrastructure-platform/SKILL.md) — turns an approved system design into platform architecture: topology, environments, runtime substrate, network/trust zones, identity, secrets, deployment, IaC, CI/CD, cost, disaster posture, and implementation handoffs.

---

### mobile-architecture

**Status:** draft

**Purpose:** Defines mobile application architecture from an approved system design: platform strategy, application and navigation architecture, state and offline/sync design, device-capability integration, performance and battery budgets, accessibility and localization, notifications and background behavior, error handling and recovery, observability, testing strategy, and a failure taxonomy.

Technology-agnostic and framework-agnostic first. Covers native (iOS/Android) and cross-platform-native (React Native, Flutter, KMP). Mobile-web and PWA are out of scope and belong to [frontend-architecture](#frontend-architecture). Deep mobile security/privacy and store-release/signing are not owned here — they are raised as callouts and ADR candidates owned by [security](#security) and [operations](#operations) / [infrastructure-platform](#infrastructure-platform).

**Owns:**
- Platform-target strategy (native vs cross-platform-native vs hybrid) as an ADR
- Application architecture and module boundaries
- Navigation architecture and state restoration
- State management and cache ownership
- Offline-first and synchronization strategy
- Device-capability integration and permission posture
- Performance and battery budgets
- Accessibility and localization
- Notifications and background behavior
- Error handling, recovery, and the failure taxonomy
- Observability and analytics posture
- Testing strategy

Not owned (callouts only): mobile security/privacy design, store-release/signing/rollout.

**Produces:**

| Artifact | Conforms to |
|---|---|
| `mobile-architecture.md` | [architecture-schema](../../standards/architecture-schema/README.md), [documentation-standards](../../standards/documentation-standards/README.md) |
| ADR drafts (platform target, offline/sync, security callouts, release callouts) | [architecture-schema](../../standards/architecture-schema/README.md) |

**Standards this architecture domain conforms to:**
- [architecture-schema](../../standards/architecture-schema/README.md) - `mobile-architecture.md` artifact structure and system-design traceability.
- [security-standards](../../standards/security-standards/README.md) - mobile security/privacy callout posture.
- [observability-standards](../../standards/observability-standards/README.md) - mobile telemetry and crash/latency signals.
- [deployment-standards](../../standards/deployment-standards/README.md) - release/rollout callout posture.
- [documentation-standards](../../standards/documentation-standards/README.md) - skill structure.

**Upstream inputs:** Requires an approved `system-design.md` per [architecture-schema](../../standards/architecture-schema/README.md) whose design includes a native or cross-platform-native mobile surface. Bounded contexts, component interfaces, API boundaries, and ADRs shape the mobile architecture produced here.

**Downstream consumers:**

Mobile architecture produced here is the source of truth for:

- Future `skills/implementations/mobile/<ecosystem>` - iOS, Android, and cross-platform-native skills follow platform, navigation, state, offline, and performance decisions.
- [security](#security) - owns the mobile security/privacy decisions raised here as callouts.
- [operations](#operations) / [infrastructure-platform](#infrastructure-platform) - own the release/signing/rollout decisions raised here as callouts.
- [performance](#performance) - performance and battery budget enforcement.

**Skills:**
- [mobile-architecture](../../skills/architecture/mobile-architecture/SKILL.md) — turns an approved system design into mobile application architecture: platform strategy, app and navigation architecture, state, offline/sync, device capabilities, performance and battery, accessibility, notifications, error handling, observability, testing, failure taxonomy, and implementation handoffs.

---

### operations

**Status:** draft

**Purpose:** Standardizes engineering execution and organizational delivery: workflows, governance, release management, sprint execution, incident response, documentation standards.

Technology-agnostic. Owns *how the team operates*, not the tooling.

**Owns:**
- Team workflows and rituals
- Technical leadership patterns
- Delivery coordination
- Release governance
- Incident response process
- Runbook standards
- Postmortem rigor

**Produces:**

| Artifact | Conforms to |
|---|---|
| Incident postmortems | TBD |
| Runbooks | references alerts in [observability-standards](../../standards/observability-standards/README.md) |
| Release governance docs | references [deployment-standards](../../standards/deployment-standards/README.md) |
| Operational playbooks | — |

**Standards this architecture domain conforms to:**
- [observability-standards](../../standards/observability-standards/README.md) — every alert has a runbook; runbooks live where this architecture domain says they live.
- [deployment-standards](../../standards/deployment-standards/README.md) — release governance and rollback expectations.
- [documentation-standards](../../standards/documentation-standards/README.md) — skill structure.

**Downstream consumers:**
- All implementation skills generate alerts that require runbooks defined here.
- [workflows/incident-response](../../workflows/) (when authored) orchestrates this architecture domain's incident process end-to-end.

**Skills:**
- [operations](../../skills/architecture/operations/SKILL.md) — produces blameless postmortems, reusable runbooks, and operational handoff notes for services entering support.

---

### performance

**Status:** draft

**Purpose:** Turns an approved system design into performance architecture before implementation or scale events: explicit latency, throughput, concurrency, and cost budgets per user-visible path, a capacity and headroom model, scaling and backpressure posture, hot-path and critical-path analysis, caching and precomputation strategy, and performance-regression gating.

Technology-agnostic and budget-driven. Owns *what "fast enough" means*, *where performance matters*, and *how the system behaves under saturation* — not the framework, query plan, or runtime flags that implement it. Implementation-level optimization lives under [skills/implementations/backend](../../skills/implementations/backend/), [skills/implementations/frontend](../../skills/implementations/frontend/), [skills/implementations/data](../../skills/implementations/data/), and [skills/implementations/infrastructure](../../skills/implementations/infrastructure/).

**Owns:**
- Latency, throughput, concurrency, and cost budgets per user-visible path
- Workload classification and load-shape modeling
- Capacity and headroom model
- Critical-path and hot-path analysis
- Scaling, partitioning, and saturation-ceiling posture
- Caching and precomputation strategy in budget terms
- Backpressure and load-shedding posture
- Performance testing and regression-gating policy
- Cost-performance tradeoff levers

**Produces:**

| Artifact | Conforms to |
|---|---|
| `performance-architecture.md` | [architecture-schema](../../standards/architecture-schema/README.md), [documentation-standards](../../standards/documentation-standards/README.md) |
| ADR drafts (budget, scaling, partitioning, caching) | [architecture-schema](../../standards/architecture-schema/README.md) |

**Standards this architecture domain conforms to:**
- [architecture-schema](../../standards/architecture-schema/README.md) - `performance-architecture.md` artifact structure and system-design traceability.
- [deployment-standards](../../standards/deployment-standards/README.md) - release/canary gates and rollback align with the promotion flow.
- [observability-standards](../../standards/observability-standards/README.md) - perf SLIs and saturation indicators map to user-impacting symptoms.
- [security-standards](../../standards/security-standards/README.md) - cache-reuse decisions crossing tenant boundaries.
- [documentation-standards](../../standards/documentation-standards/README.md) - skill structure.

**Upstream inputs:** Requires an approved `system-design.md` per [architecture-schema](../../standards/architecture-schema/README.md) whose design has user-visible paths constrained by latency, throughput, concurrency, or cost-per-request, or an anticipated scale event. Bounded contexts, service interactions, data flows, and ADRs in the system design shape the performance architecture produced here; they are consumed, not redefined.

**Downstream consumers:**

Performance architecture produced here is the source of truth for:

- [skills/implementations/backend/*](../../skills/implementations/backend/) - latency budgets, concurrency posture, timeout and async boundaries.
- [skills/implementations/frontend/*](../../skills/implementations/frontend/) - rendering, asset-loading, hydration, and interaction-latency budgets.
- [skills/implementations/data/*](../../skills/implementations/data/) - query latency budgets, cache ownership, partitioning pressure.
- [skills/implementations/infrastructure/*](../../skills/implementations/infrastructure/) - autoscaling, capacity assumptions, queueing posture.
- [reliability](#reliability) - degradation posture, saturation behavior, load-shedding policy.
- [operations](#operations) - regression gates, perf alerts, SLI measurement expectations.

**Skills:**
- [performance](../../skills/architecture/performance/SKILL.md) — turns an approved system design into performance architecture: workload shape, budgets, critical/hot paths, capacity model, scaling and backpressure posture, caching strategy, performance testing, regression gating, cost-performance tradeoffs, and implementation handoffs.

---

### reliability

**Status:** draft

**Purpose:** Turns an approved system design into production-grade reliability architecture before implementation and platform hardening: service-level objectives and error-budget policy, dependency criticality, failure-mode architecture, graceful degradation, blast-radius isolation, redundancy and failover posture, disaster recovery with RTO/RPO, chaos validation, and release safety.

Technology-agnostic and failure-oriented. Owns *what* reliability the system commits to and *how* it fails, degrades, and recovers — not the vendor failover tooling or telemetry pipeline that implements it. Vendor-specific failover, backup, and rollout mechanics live under [skills/implementations/infrastructure](../../skills/implementations/infrastructure/) and [skills/implementations/data](../../skills/implementations/data/).

**Owns:**
- Service-level objectives mapped to user journeys
- Error-budget policy and release/escalation consequences
- Dependency criticality classification
- Failure-mode architecture and blast-radius containment
- Graceful-degradation behavior per critical journey
- Redundancy and high-availability posture
- Disaster-recovery strategy with RTO/RPO and rehearsal
- Release-safety mechanisms and rollback posture

**Produces:**

| Artifact | Conforms to |
|---|---|
| `reliability-architecture.md` | [architecture-schema](../../standards/architecture-schema/README.md), [documentation-standards](../../standards/documentation-standards/README.md) |
| ADR drafts (redundancy, region topology, isolation, DR) | [architecture-schema](../../standards/architecture-schema/README.md) |

**Standards this architecture domain conforms to:**
- [architecture-schema](../../standards/architecture-schema/README.md) - `reliability-architecture.md` artifact structure and system-design traceability.
- [observability-standards](../../standards/observability-standards/README.md) - alerts map to user-impacting symptoms.
- [deployment-standards](../../standards/deployment-standards/README.md) - release gating and rollback align with the promotion flow.
- [security-standards](../../standards/security-standards/README.md) - failover and DR decisions crossing trust/tenant boundaries.
- [documentation-standards](../../standards/documentation-standards/README.md) - skill structure.

**Upstream inputs:** Requires an approved `system-design.md` per [architecture-schema](../../standards/architecture-schema/README.md) whose design has externally meaningful availability commitments, multi-component failure interactions, or stateful dependencies requiring a recovery plan. Component boundaries, data ownership, and ADRs in the system design shape the reliability architecture produced here; they are consumed, not redefined.

**Downstream consumers:**

Reliability architecture produced here is the source of truth for:

- [skills/implementations/infrastructure/*](../../skills/implementations/infrastructure/) - redundancy placement, failover mechanics, region topology, and rollout safety.
- [skills/implementations/data/*](../../skills/implementations/data/) - backup/restore, replication failover, and RTO/RPO expectations.
- [operations](#operations) - severity inputs, page-worthy symptoms, and runbook hooks.
- [performance](#performance) - latency-as-error-budget interaction and saturation thresholds.

**Skills:**
- [reliability](../../skills/architecture/reliability/SKILL.md) — turns an approved system design into reliability architecture: SLOs, error budgets, dependency criticality, failure modes, degradation, redundancy, isolation, disaster recovery, chaos validation, release safety, and implementation handoffs.

---

### security

**Status:** draft

**Purpose:** Defines security architecture from an approved system design: threat models, trust-boundary analysis, data classification, identity and authorization architecture, tenant-isolation strategy, secrets and key-management posture, abuse protections, supply-chain posture, audit requirements, and compliance mapping.

Technology-agnostic and threat-oriented. Owns *the security model* — trust boundaries, classification, identity, authorization, isolation — not the scanners, code fixes, or runtime hardening that enforce it. Tooling and remediation live in `skills/implementations/*` and `operations`.

**Owns:**
- Data classification and handling rules
- Trust-boundary analysis and threat models
- Identity and authorization architecture
- Tenant-isolation strategy
- Secrets and key-management posture
- Input/output, abuse, and rate protections
- Audit posture and supply-chain trust
- Compliance control mapping

**Produces:**

| Artifact | Conforms to |
|---|---|
| `security-architecture.md` | [architecture-schema](../../standards/architecture-schema/README.md) (structure), [security-standards](../../standards/security-standards/README.md) (content), [documentation-standards](../../standards/documentation-standards/README.md) |
| ADR drafts (identity, isolation, encryption, supply-chain) | [architecture-schema](../../standards/architecture-schema/README.md) |

**Standards this architecture domain conforms to:**
- [architecture-schema](../../standards/architecture-schema/README.md) — `security-architecture.md` artifact structure and system-design traceability.
- [security-standards](../../standards/security-standards/README.md) — auth schemes, scopes, secrets (security content).
- [observability-standards](../../standards/observability-standards/README.md) — security-event telemetry and audit signals.
- [deployment-standards](../../standards/deployment-standards/README.md) — supply-chain and artifact-promotion controls.
- [documentation-standards](../../standards/documentation-standards/README.md) — skill structure.

**Upstream inputs:** Requires an approved `system-design.md` per [architecture-schema](../../standards/architecture-schema/README.md). Components, data flows, trust boundaries, and ADRs in the system design shape the security architecture produced here. Platform topology from `infrastructure-platform` informs trust zones when available.

**Downstream consumers:**

Security architecture produced here constrains:

- Security-relevant work across [skills/implementations/*](../../skills/implementations/) (e.g. `spring-security-auth-review`, `k8s-deploy-manifest-review`, `github-actions-pipeline-hardened`).
- [backend-architecture](#backend-architecture) and [data-architecture](#data-architecture) — authorization, classification, and data-protection decisions.
- [infrastructure-platform](#infrastructure-platform) — workload identity, secrets substrate, supply-chain controls.
- [operations](#operations) — audit pipeline and security-incident clauses.

**Skills:**
- [security](../../skills/architecture/security/SKILL.md) — turns an approved system design into security architecture: classification, trust boundaries, threat model, identity, authorization, isolation, secrets, audit, supply chain, compliance, and implementation handoffs.

---

### system-design

**Status:** draft

**Purpose:** Designs scalable system architecture and technical topology from an approved PRD. Defines the architectural envelope that downstream implementation domains fill in.

Technology-agnostic. Owns *shape* and *boundaries*, not vendor or framework choices (those land in `skills/implementations/`).

**Owns:**
- Service boundaries
- Architecture patterns
- Distributed-systems decisions
- Scalability strategy
- Data flow topology
- Consistency models
- ADRs

**Produces:**

| Artifact | Conforms to |
|---|---|
| `system-design.md` | [architecture-schema](../../standards/architecture-schema/README.md) |
| `adrs/NNNN-<slug>.md` | [architecture-schema](../../standards/architecture-schema/README.md) |
| Optional `components/<name>.md` | [architecture-schema](../../standards/architecture-schema/README.md) |

**Standards this architecture domain conforms to:**
- [architecture-schema](../../standards/architecture-schema/README.md) — output contract.
- [security-standards](../../standards/security-standards/README.md) — informs Security and Compliance section.
- [observability-standards](../../standards/observability-standards/README.md) and [deployment-standards](../../standards/deployment-standards/README.md) — inform Operational Considerations section.
- [documentation-standards](../../standards/documentation-standards/README.md) — skill structure.

**Upstream inputs:** Requires a PRD with `status: approved` per [prd-schema](../../standards/prd-schema/README.md). Do not invoke if PRD is `draft` or `review`.

**Downstream consumers:**

An approved `system-design.md` is the sole upstream input to scaffolding skills in:

- [skills/implementations/backend/*](../../skills/implementations/backend/)
- [skills/implementations/frontend/*](../../skills/implementations/frontend/)
- [skills/implementations/data/*](../../skills/implementations/data/)
- [skills/implementations/infrastructure/*](../../skills/implementations/infrastructure/)
- [skills/architecture/backend-architecture](#backend-architecture) (backend boundaries and contracts)
- [skills/architecture/data-architecture](#data-architecture) (schemas and migrations)

**Skills:**
- [system-design](../../skills/architecture/system-design/SKILL.md) - turns an approved PRD into a system design and inline ADRs.

---

### quality-engineering

**Status:** draft

**Purpose:** Validates correctness, reliability, and production readiness. Owns testing strategy, QA automation, validation pipelines, regression prevention, and contract testing.

Architecture-domain level. The *strategy* and *coverage decisions* are ecosystem-neutral; the *wiring* (specific test runners, fixtures, container libraries) lives in implementation skills under each `skills/implementations/*` ecosystem.

**Owns:**
- Testing pyramid balance (unit / integration / contract / E2E)
- Coverage targets per tier
- Contract testing strategy
- Regression prevention policy
- Test data strategy
- Flake budget and quarantine policy

**Produces:**

| Artifact | Conforms to |
|---|---|
| Test plan per service | TBD |
| Integration test suite outline | consumed from API contracts ([api-standards](../../standards/api-standards/README.md)) |
| Acceptance criteria | derived from PRD Success Metrics ([prd-schema](../../standards/prd-schema/README.md)) |

**Standards this architecture domain conforms to:**
- [api-standards](../../standards/api-standards/README.md) — contract tests verify the published spec.
- [prd-schema](../../standards/prd-schema/README.md) — Success Metrics become acceptance criteria.
- [observability-standards](../../standards/observability-standards/README.md) — test runs emit structured signals into CI dashboards.
- [deployment-standards](../../standards/deployment-standards/README.md) — tests gate promotion through `dev → staging → production`.

**Upstream inputs:**
- Approved `system-design.md` (component boundaries shape test boundaries).
- Approved `openapi.yaml` (contract is the source of truth for endpoint tests).
- Approved `PRD.md` Success Metrics (become acceptance criteria).

**Downstream consumers:**
- [skills/implementations/backend/*](../../skills/implementations/backend/) — each ecosystem wires the test strategy into its own runner and fixture library.
- [skills/implementations/infrastructure/*](../../skills/implementations/infrastructure/) — CI pipelines invoke the suites declared here.

**Skills:**
- [quality-engineering](../../skills/architecture/quality-engineering/SKILL.md) — produces contract-driven test strategy, acceptance criteria, integration test planning, and CI quality gates.

---

## Implementation ecosystems

### ai (category)

**Purpose:** Technology-specific execution skills for ai.

---

### ai/anthropic

**Status:** draft

**Purpose:** Implements relevant architecture domains using the anthropic ecosystem. 1 of 5 archetypes authored (`anthropic-structured-output-runtime`); remaining mirror the openai archetype boundaries.

---

### ai/autogen

**Status:** scaffold

**Purpose:** Implements relevant architecture domains using the autogen ecosystem.

---

### ai/crewai

**Status:** scaffold

**Purpose:** Implements relevant architecture domains using the crewai ecosystem.

---

### ai/langchain

**Status:** draft

**Purpose:** Implements relevant architecture domains using the langchain ecosystem. 1 framework-orchestration skill authored (`langchain-agent-runtime`); RAG and eval-harness skills planned.

---

### ai/openai

**Status:** draft

**Purpose:** Implements relevant architecture domains using the openai ecosystem. 4 archetypes authored: structured-output, tool-calling, RAG runtime, and evals/observability.

---

### backend (category)

**Purpose:** Technology-specific execution skills for backend.

---

### backend/django

**Status:** scaffold

**Purpose:** Implements relevant architecture domains using the django ecosystem.

---

### backend/dotnet

**Status:** scaffold

**Purpose:** Implements relevant architecture domains using the dotnet ecosystem.

---

### backend/fastapi

**Status:** draft

**Purpose:** Implements backend architecture domains using the FastAPI (Python) ecosystem. This is the *how* layer — framework-specific scaffolding, configuration, and hardening. Architecture decisions (domain modeling, auth strategy, SLOs, budgets) come from [skills/architecture/](../../skills/architecture/) and are taken as inputs here. FastAPI is a single framework — there is no framework branching.

**Ecosystem:**
- FastAPI (Python 3.11+), Pydantic v2, Starlette
- Uvicorn/Gunicorn with `uvicorn.workers`, ASGI lifespan
- SQLAlchemy 2.x + Alembic (or the data layer declared by architecture)
- Celery / RQ / arq (or Kafka per architecture)
- OpenTelemetry Python SDK, structlog, prometheus-client
- pytest + httpx + Testcontainers

**Compatible patterns:**
- [microservices](../../architecture-patterns/microservices/README.md)
- [modular-monolith](../../architecture-patterns/modular-monolith/README.md)
- [event-driven](../../architecture-patterns/event-driven/README.md)

**Architecture domains implemented:**

| Architecture domain | How |
|---|---|
| [backend-architecture](#backend-architecture) | Service scaffold follows backend boundaries, contracts, and async integration. |
| [security](#security) | OAuth2/OIDC + API-key flows, default-deny authz, OWASP review per [security-standards](../../standards/security-standards/README.md). |
| [reliability](#reliability) | SLO/burn-rate alerts, retries, degradation behavior per [observability-standards](../../standards/observability-standards/README.md). |
| [performance](#performance) | Async-path discipline, pool sizing, caching, load-test gates. |

**Standards this implementation conforms to:**
- [api-standards](../../standards/api-standards/README.md) — contract, error shape, and status semantics.
- [security-standards](../../standards/security-standards/README.md) — no secrets in source/settings/image; default-deny authorization; fail-fast settings.
- [observability-standards](../../standards/observability-standards/README.md) — correlated structured logging, RED metrics, multi-burn-rate alerts.
- [deployment-standards](../../standards/deployment-standards/README.md) — env-agnostic non-root image; runtime config not baked.
- [naming-conventions](../../standards/naming-conventions/README.md) — service, module, and file naming.

**Upstream inputs:**
- Approved `backend-architecture.md` from [backend-architecture](../../skills/architecture/backend-architecture/SKILL.md) (domain boundaries, data layer, API/event contracts).
- Approved `architecture/security` (auth provider, session model, secret handling), `architecture/reliability` (SLO targets), `architecture/performance` (budgets, pool sizing).

**Downstream consumers:**
- [skills/implementations/data/postgres](../../skills/implementations/data/postgres/) — Alembic migrations land in the scaffold's data layer.
- [skills/implementations/infrastructure/*](../../skills/implementations/infrastructure/) — built non-root images are deployed through the platform stack.

**Skills:**
- [fastapi-service-scaffold](../../skills/implementations/backend/fastapi/fastapi-service-scaffold/SKILL.md) — produces a production-ready service shell: Pydantic Settings, structlog + request context, health probes, layered error handling, ASGI lifespan, `Depends` DI and principal seam, non-root container packaging.
- [fastapi-auth-and-security-review](../../skills/implementations/backend/fastapi/fastapi-auth-and-security-review/SKILL.md) — fills the principal seam with OAuth2/OIDC or API-key auth, adds default-deny authz, secure headers, boundary validation, secret handling, OWASP review, and a security test suite.
- [fastapi-observability-readiness](../../skills/implementations/backend/fastapi/fastapi-observability-readiness/SKILL.md) — replaces the telemetry seam with OpenTelemetry tracing, prometheus-client RED metrics, trace-correlated structlog, SLI/SLO definitions, and multi-burn-rate alerts.
- [fastapi-async-and-task-integration](../../skills/implementations/backend/fastapi/fastapi-async-and-task-integration/SKILL.md) — wires Celery/RQ/arq or Kafka producers and consumers: delivery semantics, transactional outbox, idempotent consumers, retry/DLQ, and Testcontainers integration tests.
- [fastapi-performance-and-resilience](../../skills/implementations/backend/fastapi/fastapi-performance-and-resilience/SKILL.md) — enforces async-path discipline, the worker model, connection-pool sizing, caching posture, circuit breakers/bulkheads, retry budgets, and a CI load-test gate.

---

### backend/golang

**Status:** scaffold

**Purpose:** Implements relevant architecture domains using the golang ecosystem.

---

### backend/nodejs

**Status:** draft

**Purpose:** Implements backend architecture domains using the Node.js (TypeScript) ecosystem. This is the *how* layer — framework-specific scaffolding, configuration, and hardening. Architecture decisions (domain modeling, auth strategy, SLOs, budgets) come from [skills/architecture/](../../skills/architecture/) and are taken as inputs here. One scaffold branches across Express, Fastify, and NestJS per the framework declared in `backend-architecture.md` — there is no per-framework split.

**Ecosystem:**
- Node.js 20+ LTS, TypeScript (`strict`)
- Express / Fastify / NestJS (framework-aware scaffold per architecture)
- Prisma / Drizzle / TypeORM (or the data layer declared by architecture)
- BullMQ / KafkaJS / SQS for async work
- pino logging, OpenTelemetry JS SDK, prom-client
- Vitest/Jest + supertest + Testcontainers

**Compatible patterns:**
- [microservices](../../architecture-patterns/microservices/README.md)
- [modular-monolith](../../architecture-patterns/modular-monolith/README.md)
- [event-driven](../../architecture-patterns/event-driven/README.md)

**Architecture domains implemented:**

| Architecture domain | How |
|---|---|
| [backend-architecture](#backend-architecture) | Service scaffold follows backend boundaries, contracts, and async integration. |
| [security](#security) | Passport/JWT/OAuth flows, default-deny authz, OWASP review per [security-standards](../../standards/security-standards/README.md). |
| [reliability](#reliability) | SLO/burn-rate alerts, retries, degradation behavior per [observability-standards](../../standards/observability-standards/README.md). |
| [performance](#performance) | Event-loop discipline, clustering, backpressure, load-test gates. |

**Standards this implementation conforms to:**
- [api-standards](../../standards/api-standards/README.md) — contract, error shape, and status semantics.
- [security-standards](../../standards/security-standards/README.md) — no secrets in source/config/image; default-deny authorization; fail-fast config.
- [observability-standards](../../standards/observability-standards/README.md) — correlated structured logging, RED metrics, multi-burn-rate alerts.
- [deployment-standards](../../standards/deployment-standards/README.md) — env-agnostic non-root image; runtime config not baked.
- [naming-conventions](../../standards/naming-conventions/README.md) — service, module, and file naming.

**Upstream inputs:**
- Approved `backend-architecture.md` from [backend-architecture](../../skills/architecture/backend-architecture/SKILL.md) (framework choice, domain boundaries, data layer, API/event contracts).
- Approved `architecture/security` (auth provider, session model, secret handling), `architecture/reliability` (SLO targets), `architecture/performance` (budgets).

**Downstream consumers:**
- [skills/implementations/data/postgres](../../skills/implementations/data/postgres/) — migrations land in the scaffold's data layer.
- [skills/implementations/infrastructure/*](../../skills/implementations/infrastructure/) — built non-root images are deployed through the platform stack.

**Skills:**
- [nodejs-service-scaffold](../../skills/implementations/backend/nodejs/nodejs-service-scaffold/SKILL.md) — produces a framework-aware service shell: validated config, structured pino logging + request context, health probes, layered error handling, DI and principal seam, non-root container packaging.
- [nodejs-auth-and-security-review](../../skills/implementations/backend/nodejs/nodejs-auth-and-security-review/SKILL.md) — fills the principal seam with Passport/JWT/OAuth auth, adds default-deny authz, secure headers, boundary validation, secret handling, OWASP review, and a security test suite.
- [nodejs-observability-readiness](../../skills/implementations/backend/nodejs/nodejs-observability-readiness/SKILL.md) — replaces the telemetry seam with OpenTelemetry tracing, prom-client RED metrics, trace-correlated logs, SLI/SLO definitions, and multi-burn-rate alerts.
- [nodejs-queue-and-event-integration](../../skills/implementations/backend/nodejs/nodejs-queue-and-event-integration/SKILL.md) — wires BullMQ/KafkaJS/SQS producers and consumers: delivery semantics, transactional outbox, idempotent consumers, retry/DLQ, and Testcontainers integration tests.
- [nodejs-performance-and-resilience](../../skills/implementations/backend/nodejs/nodejs-performance-and-resilience/SKILL.md) — enforces event-loop discipline, the clustering/worker-thread model, backpressure, circuit breakers/bulkheads, retry budgets, and a CI load-test gate.

---

### backend/rust

**Status:** draft

**Purpose:** Implements backend architecture domains using the Rust ecosystem. This is the *how* layer — framework-specific scaffolding, configuration, and hardening. Architecture decisions (domain modeling, auth strategy, SLOs, budgets) come from [skills/architecture/](../../skills/architecture/) and are taken as inputs here. One scaffold branches across axum and actix-web per the framework declared in `backend-architecture.md`.

Partially built: only the service scaffold exists today. The remaining four skills in the [backend skillset taxonomy](../../skills/implementations/backend/README.md) — auth-and-security-review, observability-readiness, async-and-event-integration, and performance-and-resilience-engineering — are planned.

**Ecosystem:**
- Rust stable, 2021 edition
- axum (default) / actix-web, tokio multi-thread runtime
- `sqlx` / `sea-orm` / `diesel` (or the data layer declared by architecture)
- `tracing` + `tracing-opentelemetry`, `metrics-exporter-prometheus`
- `thiserror` for typed errors, `config` for layered configuration
- `tokio::test` + `testcontainers-rs`

**Compatible patterns:**
- [microservices](../../architecture-patterns/microservices/README.md)
- [modular-monolith](../../architecture-patterns/modular-monolith/README.md)
- [event-driven](../../architecture-patterns/event-driven/README.md)

**Architecture domains implemented:**

| Architecture domain | How |
|---|---|
| [backend-architecture](#backend-architecture) | Service scaffold follows backend boundaries, contracts, and runtime shape. |
| [security](#security) | Secure defaults in the scaffold: no `unsafe`, no permissive CORS, no panicking request paths, rustls for service-to-service TLS. |
| [reliability](#reliability) | Health probes, graceful shutdown, structured `tracing` per [observability-standards](../../standards/observability-standards/README.md). |

**Standards this implementation conforms to:**
- [api-standards](../../standards/api-standards/README.md) — error envelope, pagination, rate-limit headers, OpenAPI consumption.
- [security-standards](../../standards/security-standards/README.md) — secrets, CORS, TLS, `cargo-audit`/`cargo-deny` scanning.
- [observability-standards](../../standards/observability-standards/README.md) — structured JSON `tracing` logs, RED metrics, W3C `traceparent`.
- [deployment-standards](../../standards/deployment-standards/README.md) — env-agnostic image, config injected at deploy time, readiness/liveness probes.
- [naming-conventions](../../standards/naming-conventions/README.md) — Cargo package `kebab-case`, Rust modules `snake_case`, env vars `SCREAMING_SNAKE_CASE`.

**Upstream inputs:**
- Approved `backend-architecture.md` from [backend-architecture](../../skills/architecture/backend-architecture/SKILL.md) (framework choice, domain boundaries, data layer, API/event contracts).
- `openapi.yaml` when a contract exists — handlers and DTOs derive from it, not the reverse.

**Downstream consumers:**
- [skills/implementations/data/postgres](../../skills/implementations/data/postgres/) — migrations land in the scaffold's data layer.
- [skills/implementations/infrastructure/*](../../skills/implementations/infrastructure/) — built non-root images are deployed through the platform stack.

**Skills:**
- [rust-service-scaffold](../../skills/implementations/backend/rust/rust-service-scaffold/SKILL.md) — produces a framework-aware service shell: layered `config` loading, structured `tracing`, health probes, one typed error enum implementing `IntoResponse`, `/metrics`, graceful shutdown, and non-root container packaging, verified by `cargo build`/`test`/`clippy`.

---

### backend/spring-boot

**Status:** draft

**Purpose:** Implements backend architecture domains using the Spring ecosystem. This is the *how* layer — framework-specific scaffolding, configuration, and hardening. Architecture decisions (API shape, domain modeling, auth strategy) come from [skills/architecture/](../../skills/architecture/) and are taken as inputs here.

**Ecosystem:**
- Spring Boot 3.x
- Spring Security
- Spring Data JPA / Hibernate
- Spring Kafka (where event-driven)
- Spring Cache + Redis
- Gradle (Kotlin DSL) or Maven
- Testcontainers
- Flyway

**Compatible patterns:**
- [modular-monolith](../../architecture-patterns/modular-monolith/README.md)
- [microservices](../../architecture-patterns/microservices/README.md)
- [event-driven](../../architecture-patterns/event-driven/README.md)
- [cqrs](../../architecture-patterns/cqrs/README.md)
- [hexagonal-architecture](../../architecture-patterns/hexagonal-architecture/README.md)

**Architecture domains implemented:**

| Architecture domain | How |
|---|---|
| [backend-architecture](#backend-architecture) | Service scaffold follows backend boundaries, modules, workers, controllers, DTOs, and REST contracts produced by `backend-architecture`. |
| [security](#security) | Spring Security configuration; auth review skill enforces [security-standards](../../standards/security-standards/README.md). |
| [reliability](#reliability) | Actuator health probes, structured logging, OpenTelemetry hooks per [observability-standards](../../standards/observability-standards/README.md). |
| [quality-engineering](#quality-engineering) | Contract-driven test strategy and CI quality gates. |

**Standards this implementation conforms to:**
- [api-standards](../../standards/api-standards/README.md) — generated controllers respect the global REST contract.
- [security-standards](../../standards/security-standards/README.md) — auth, secrets, TLS, dependency scanning posture.
- [observability-standards](../../standards/observability-standards/README.md) — structured JSON logs, RED metrics, OTel traces.
- [deployment-standards](../../standards/deployment-standards/README.md) — image build, config injection, env-agnostic artifacts.
- [naming-conventions](../../standards/naming-conventions/README.md) — package names, env vars, container images.

**Upstream inputs:**
- Approved `system-design.md` (selects Spring Boot as the runtime for one or more components).
- Approved `backend-architecture.md` from [backend-architecture](../../skills/architecture/backend-architecture/SKILL.md), plus `openapi.yaml` and `api-conventions.md` for any service exposing REST.

**Downstream consumers:**
- [skills/implementations/data/postgres](../../skills/implementations/data/postgres/) — Flyway migrations land in the scaffold's `db/migration/` directory.
- [skills/implementations/infrastructure/*](../../skills/implementations/infrastructure/) — built artifacts (Docker images) are deployed through the platform stack.

**Skills:**
- [spring-boot-service-scaffold](../../skills/implementations/backend/spring-boot/spring-boot-service-scaffold/SKILL.md) — produces a production-ready service shell: package structure, profile-aware configuration, structured logging, observability, health probes, secure defaults, error handling, testing foundations, Docker packaging.
- [spring-security-auth-review](../../skills/implementations/backend/spring-boot/spring-security-auth-review/SKILL.md) — reviews and hardens authentication / authorization for a Spring Boot service using Spring Security, JWT, OAuth2, sessions, or service-to-service auth.
- [spring-boot-observability-readiness](../../skills/implementations/backend/spring-boot/spring-boot-observability-readiness/SKILL.md) — produces or audits Micrometer/Prometheus metrics, OpenTelemetry tracing, structured logs with trace correlation, SLI/SLO definitions, and multi-window multi-burn-rate alerts.
- [spring-kafka-event-integration](../../skills/implementations/backend/spring-boot/spring-kafka-event-integration/SKILL.md) — produces or hardens Spring Kafka producers and consumers: delivery semantics, transactional outbox, idempotency, retry and DLQ topology, observability, and integration tests against embedded or Testcontainers Kafka.
- [spring-boot-performance-and-resilience](../../skills/implementations/backend/spring-boot/spring-boot-performance-and-resilience/SKILL.md) — produces or hardens latency/throughput posture and resilience for a Spring Boot service: timeouts, retries, circuit breakers, bulkheads, rate limiting, connection-pool and thread-pool sizing, caching, and load-test gates.

---

### data (category)

**Purpose:** Technology-specific execution skills for data.

---

### data/clickhouse

**Status:** scaffold

**Purpose:** Implements relevant architecture domains using the clickhouse ecosystem.

---

### data/elasticsearch

**Status:** scaffold

**Purpose:** Implements relevant architecture domains using the elasticsearch ecosystem.

---

### data/mongodb

**Status:** draft

**Purpose:** Implements `skills/architecture/data-architecture` for MongoDB: document modeling, schema validation, index strategy, shard-key choice, read/write concern posture, and zero-downtime evolution.

Architecture decisions (which bounded contexts own which collections, consistency posture, sharding choice, replica topology) come from upstream and are taken as inputs here.

**Ecosystem:**
- MongoDB 6.0+ (replica set or sharded cluster)
- `$jsonSchema` validators
- mongock, mongo-migrate, or hand-rolled idempotent migration scripts
- Testcontainers for migration dry-runs

**Compatible patterns:**
- [modular-monolith](../../architecture-patterns/modular-monolith/README.md)
- [microservices](../../architecture-patterns/microservices/README.md)
- [event-driven](../../architecture-patterns/event-driven/README.md) (change-stream consumers; outbox patterns)
- [cqrs](../../architecture-patterns/cqrs/README.md) (read-model projections)

**Architecture domains implemented:**

| Architecture domain | How |
|---|---|
| [data-architecture](#data-architecture) | Document modeling, validation, indexing strategy, shard-key choice, retention rules, consistency posture. |
| [reliability](#reliability) | Zero-downtime migrations, backup/restore hooks, replica-set posture. |

**Skills:**
- [mongodb-data-model-and-migration](../../skills/implementations/data/mongodb/mongodb-data-model-and-migration/SKILL.md) — produces document modeling decisions, `$jsonSchema` validators, index strategy, shard-key choice if sharded, read/write concern posture, and zero-downtime migration plans using expand-migrate-contract or dual-write.

---

### data/postgres

**Status:** draft

**Purpose:** Implements `skills/architecture/data-architecture` for PostgreSQL: schema design, integrity constraints, indexing strategy, migrations (Flyway / Liquibase), and zero-downtime evolution.

Architecture decisions (which bounded contexts own which data, consistency model, retention strategy) come from upstream and are taken as inputs here.

**Ecosystem:**
- PostgreSQL 14+
- Flyway (default) or Liquibase
- Testcontainers for migration verification
- `pg_dump` / logical replication for migration rehearsals

**Compatible patterns:**
- [modular-monolith](../../architecture-patterns/modular-monolith/README.md)
- [microservices](../../architecture-patterns/microservices/README.md)
- [event-driven](../../architecture-patterns/event-driven/README.md) (outbox tables live here)
- [cqrs](../../architecture-patterns/cqrs/README.md) (read-model projections)

**Architecture domains implemented:**

| Architecture domain | How |
|---|---|
| [data-architecture](#data-architecture) | Schema definition, migration plans, index strategy, retention rules. |
| [reliability](#reliability) | Zero-downtime migrations, backup/recovery hooks. |

**Standards this implementation conforms to:**
- [architecture-schema](../../standards/architecture-schema/README.md) — data ownership rules: each table is owned by exactly one component.
- [naming-conventions](../../standards/naming-conventions/README.md) — `snake_case` plural tables, singular columns.
- [security-standards](../../standards/security-standards/README.md) — at-rest encryption, PII tagging, no secrets in migrations.
- [deployment-standards](../../standards/deployment-standards/README.md) — backwards-compatible migrations gating service deploys (expand → migrate → contract).

**Upstream inputs:**
- Approved `system-design.md` with bounded contexts and data ownership declared.
- Where relevant, `openapi.yaml` for idempotency / concurrency requirements that shape constraints.

**Downstream consumers:**
- [skills/implementations/backend/spring-boot](../../skills/implementations/backend/spring-boot/) — Flyway migrations land in the scaffold's `db/migration/` directory.
- [skills/architecture/quality-engineering](../../skills/architecture/quality-engineering/) — integration tests run against this schema via Testcontainers.

**Skills:**
- [postgres-schema-and-migration](../../skills/implementations/data/postgres/postgres-schema-and-migration/SKILL.md) — produces normalized schema, integrity constraints, indexing strategy, Flyway migrations, and zero-downtime migration plans using expand / migrate / contract.
- [postgres-indexing-and-query-optimization](../../skills/implementations/data/postgres/postgres-indexing-and-query-optimization/SKILL.md) — index audit, `EXPLAIN (ANALYZE, BUFFERS)`-driven query review, `pg_stat_statements` hot-query identification, partitioning validation, N+1 and join-order remediation, autovacuum and bloat posture.
- [postgres-replication-and-ha-readiness](../../skills/implementations/data/postgres/postgres-replication-and-ha-readiness/SKILL.md) — streaming/logical replication topology, sync vs async RPO trade-off, automated failover (Patroni/repmgr/Multi-AZ), replica-lag thresholds, read-replica routing, split-brain prevention, multi-region posture.
- [postgres-backup-and-operational-readiness](../../skills/implementations/data/postgres/postgres-backup-and-operational-readiness/SKILL.md) — backup strategy (pgBackRest/WAL archiving for PITR), rehearsed restore drills with measured RPO/RTO, retention and cost posture, day-2 observability (bloat, wraparound, connection saturation), and runbook inputs.
- [postgres-security-and-data-access-hardening](../../skills/implementations/data/postgres/postgres-security-and-data-access-hardening/SKILL.md) — TLS and connection security, least-privilege role/grant model, RLS tenant isolation, column grants and encryption for PII, `pgaudit` configuration, secret rotation posture, and network-exposure review.

---

### data/redis

**Status:** scaffold

**Purpose:** Implements relevant architecture domains using the redis ecosystem.

---

### frontend (category)

**Purpose:** Technology-specific execution skills for frontend.

---

### frontend/frontend-design

**Status:** draft

**Purpose:** Visual and interaction design execution for web frontends. A router skill that injects repository context and delegates to the external superpowers frontend-design skill or Google Stitch via its official MCP. Turns an approved `frontend-architecture` into concrete visual and interaction design.

**Skills:**
- [frontend-design](../../skills/implementations/frontend/frontend-design/SKILL.md) — visual, UI, component, interaction, and UX design work from an approved frontend architecture.

---

### frontend/angular

**Status:** scaffold

**Purpose:** Implements relevant architecture domains using the angular ecosystem.

---

### frontend/nextjs

**Status:** scaffold

**Purpose:** Implements relevant architecture domains using the nextjs ecosystem.

---

### frontend/react

**Status:** draft

**Purpose:** Implements `skills/architecture/frontend-architecture` using React as a standalone SPA or as the base for a meta-framework. Base stack owning all 5 frontend archetypes; meta-frameworks (e.g. nextjs) inherit where their surface does not meaningfully diverge.

Architecture decisions (rendering strategy per route, state-tier model, design-system seam, perf budgets, auth flow) come from upstream and are taken as inputs here.

**Architecture domains implemented:**

| Architecture domain | How |
|---|---|
| [frontend-architecture](#frontend-architecture) | App shell, routing, rendering, state, design-system seam, a11y. |
| [performance](#performance) | Per-route Web Vitals budgets and CI gates. |
| [security](#security) | Auth provider wiring, CSP, token storage discipline, no secrets in bundles. |

**Skills:**
- [react-app-scaffold-and-runtime](../../skills/implementations/frontend/react/react-app-scaffold-and-runtime/SKILL.md) — Vite/Webpack project layout, env/profile handling, layered error boundaries, structured logging client, RUM + error-reporting wiring, auth provider/wrapper baseline (seam only), CSP/security headers, container or static-CDN packaging.
- [react-routing-and-rendering-strategy](../../skills/implementations/frontend/react/react-routing-and-rendering-strategy/SKILL.md) — React Router 6 data-router topology, CSR-only posture, per-route loading/error UI, suspense/transition boundaries, route-level metadata, protected-route gates and redirect flows wired to the scaffold auth seam.
- [react-state-management-and-data-fetching](../../skills/implementations/frontend/react/react-state-management-and-data-fetching/SKILL.md) — 4-tier state discipline (URL/server/global/local), TanStack Query server-state layer, query/mutation conventions, optimistic-update posture, and the auth-token storage/refresh/CSRF/logout lifecycle the scaffold and routing skills deferred.
- [react-design-system-and-accessibility](../../skills/implementations/frontend/react/react-design-system-and-accessibility/SKILL.md) — design-token wiring, accessible primitive composition (Radix/React Aria/Headless UI), theming/dark-mode, WCAG 2.2 AA posture, focus/keyboard/ARIA discipline, i18n seam, accessible auth UIs. Inherited by meta-frameworks.
- [react-performance-and-delivery-optimization](../../skills/implementations/frontend/react/react-performance-and-delivery-optimization/SKILL.md) — per-route Web Vitals budgets, code-splitting topology, image/font posture, third-party-script audit, LCP/CLS/INP/TTFB instrumentation, Lighthouse and bundle CI gates, CDN cache-control posture.

---

### frontend/svelte

**Status:** scaffold

**Purpose:** Implements relevant architecture domains using the svelte ecosystem.

---

### frontend/vue

**Status:** scaffold

**Purpose:** Implements relevant architecture domains using the vue ecosystem.

---

### infrastructure (category)

**Purpose:** Technology-specific execution skills for infrastructure.

---

### infrastructure/aws

**Status:** draft

**Purpose:** Implements `skills/architecture/infrastructure-platform`, `skills/architecture/security`, `skills/architecture/reliability`, and `skills/architecture/operations` on AWS. Family F — Cloud platforms. Architecture decisions (org structure, environment ladder, trust zones, compute primitive per workload, RPO/RTO) come from upstream and are taken as inputs here.

**Architecture domains implemented:**

| Architecture domain | How |
|---|---|
| [infrastructure-platform](#infrastructure-platform) | Account topology, network, compute primitives, deployment. |
| [security](#security) | IAM model, KMS, Secrets Manager, SCPs, trust zones. |
| [reliability](#reliability) | Multi-AZ/region posture, backups, failover. |
| [operations](#operations) | CloudWatch alarms, runbook inputs, audit. |
| [performance](#performance) | Compute right-sizing, cost monitoring, anomaly detection. |

**Skills:**
- [aws-account-and-organization-topology](../../skills/implementations/infrastructure/aws/aws-account-and-organization-topology/SKILL.md) — AWS Organizations OU structure, landing-zone approach, SCP guardrails mapped to security rationale, environment-isolated account layout, centralized audit (CloudTrail/Config/GuardDuty), and mandatory tagging/cost-allocation policy.

---

### infrastructure/azure

**Status:** scaffold

**Purpose:** Implements relevant architecture domains using the azure ecosystem.

---

### infrastructure/gcp

**Status:** scaffold

**Purpose:** Implements relevant architecture domains using the gcp ecosystem.

---

### infrastructure/github-actions

**Status:** draft

**Purpose:** Implements CI/CD pipelines on GitHub Actions for any service in the repo. Pipelines enforce the gates declared in [deployment-standards](../../standards/deployment-standards/README.md) and security scans declared in [security-standards](../../standards/security-standards/README.md).

**Architecture domains implemented:**

| Architecture domain | How |
|---|---|
| [infrastructure-platform](#infrastructure-platform) | CI/CD pipeline definitions and runner topology. |
| [security](#security) | SAST, SCA, container scanning, secret scanning, image signing. |

**Standards this implementation conforms to:**
- [deployment-standards](../../standards/deployment-standards/README.md) — CI gates (lint, test, build, scan, lint OpenAPI, migration plan review), env-ladder enforcement.
- [security-standards](../../standards/security-standards/README.md) — SCA + SAST + container scan + secret scan as required gates; signed artifacts.
- [naming-conventions](../../standards/naming-conventions/README.md) — workflow file names, environment variable casing.

**Skills:**
- [github-actions-pipeline-hardened](../../skills/implementations/infrastructure/github-actions/github-actions-pipeline-hardened/SKILL.md) — produces build/test/scan/sign/push workflows with pinned action versions, dependency caching, SBOM generation, and provenance signing.

---

### infrastructure/kubernetes

**Status:** draft

**Purpose:** Implements Kubernetes deployment topology for services: Deployment, Service, HPA, PDB, NetworkPolicy, ServiceAccount, and related resources.

**Architecture domains implemented:**

| Architecture domain | How |
|---|---|
| [infrastructure-platform](#infrastructure-platform) | Workload topology, autoscaling, disruption budgets. |
| [reliability](#reliability) | Readiness/liveness probes, PDBs, multi-replica defaults. |
| [security](#security) | NetworkPolicy, non-root containers, read-only root FS, dropped capabilities. |

**Standards this implementation conforms to:**
- [deployment-standards](../../standards/deployment-standards/README.md) — rolling update strategy, readiness probes mandatory, canary/blue-green for tier-0.
- [security-standards](../../standards/security-standards/README.md) — non-root, drop ALL caps, NetworkPolicy by default, ServiceAccount scoping.
- [observability-standards](../../standards/observability-standards/README.md) — Prometheus scrape annotations or ServiceMonitor.
- [naming-conventions](../../standards/naming-conventions/README.md) — `kebab-case` resource names, suffixed by kind when ambiguous.

**Skills:**
- [k8s-deploy-manifest-review](../../skills/implementations/infrastructure/kubernetes/k8s-deploy-manifest-review/SKILL.md) — authors or reviews Kubernetes manifests for production workloads (Deployment, Service, HPA, PDB, NetworkPolicy, security context).
- [dockerfile-and-jvm-tuning](../../skills/implementations/infrastructure/kubernetes/dockerfile-and-jvm-tuning/SKILL.md) — multi-stage Dockerfile for JVM services with distroless or jlink runtime, container-aware JVM tuning, layered jars, and image scanning. *(Container packaging is now folded into the kubernetes stack as a sub-skill of `workload-packaging-and-manifest`; the former `infrastructure/docker` stack has been retired.)*

---

### infrastructure/terraform

**Status:** draft

**Purpose:** Implements `skills/architecture/infrastructure-platform`, `skills/architecture/security`, `skills/architecture/reliability`, and `skills/architecture/operations` as Terraform code. Family H — Infrastructure-as-code. Architecture decisions (env ladder, blast-radius tiers, module boundaries, secrets handling, promotion gates) come from upstream and are taken as inputs here.

**Architecture domains implemented:**

| Architecture domain | How |
|---|---|
| [infrastructure-platform](#infrastructure-platform) | Module boundaries, env ladder, deployment mechanics. |
| [security](#security) | State secret discipline, policy-as-code, no plaintext credentials. |
| [reliability](#reliability) | Drift detection, rollback procedure, lock management. |
| [operations](#operations) | Promotion gates, runbook inputs for apply failures. |

**Skills:**
- [terraform-module-and-repository-scaffold](../../skills/implementations/infrastructure/terraform/terraform-module-and-repository-scaffold/SKILL.md) — repo layout (root + `modules/` + `environments/<env>/`), provider and `required_version` pinning, typed input/output conventions, per-module `README` + `examples/`, and blast-radius-tiered CODEOWNERS/review rules.
- [terraform-state-and-secret-management](../../skills/implementations/infrastructure/terraform/terraform-state-and-secret-management/SKILL.md) — remote backend selection (S3+DynamoDB / GCS / Azure / TFC), state encryption at rest, locking, per-environment state isolation, secret-manager references, `sensitive` discipline, and backend-migration procedure.
- [terraform-plan-gate-and-policy-as-code](../../skills/implementations/infrastructure/terraform/terraform-plan-gate-and-policy-as-code/SKILL.md) — blocking pre-merge gate (`fmt`/`validate`/`plan` diff to PR), policy-as-code (OPA/Conftest, Checkov, tfsec, Sentinel) with tier-scaled strictness, secret scan, and scheduled drift detection.
- [terraform-apply-and-promotion-mechanics](../../skills/implementations/infrastructure/terraform/terraform-apply-and-promotion-mechanics/SKILL.md) — apply orchestration across the env ladder, manual-vs-auto-apply per tier, reviewed-plan apply, blast-radius control, rollback procedure, drift-remediation playbook, and apply-failure/lock-recovery runbook inputs.
- [terraform-module-reuse-and-supply-chain](../../skills/implementations/infrastructure/terraform/terraform-module-reuse-and-supply-chain/SKILL.md) — versioned module registry strategy, semantic versioning, consumer pinning + committed lockfile, provenance review for community modules/providers, SBOM-equivalent of the dependency tree, and breaking-change deprecation policy.

---

### mobile (category)

**Purpose:** Technology-specific execution skills for mobile.

---

### mobile/flutter

**Status:** draft

**Purpose:** Implements `mobile-architecture` using Flutter. All 5 archetypes authored at mature tier (SKILL.md + playbook + quality rubric + template).

**Skills:**
- [flutter-app-scaffold-and-runtime](../../skills/implementations/mobile/flutter/flutter-app-scaffold-and-runtime/SKILL.md) — project layout, flavors, layered error handling, observability seams, DI/session shell, CI signing scaffolding.
- [flutter-navigation-and-routing](../../skills/implementations/mobile/flutter/flutter-navigation-and-routing/SKILL.md) — route hierarchy, deep links, back stack, auth-gate routing, OS-interruption state restoration.
- [flutter-state-and-data-fetching](../../skills/implementations/mobile/flutter/flutter-state-and-data-fetching/SKILL.md) — state wiring, network layer, caching, offline queue, token storage/refresh, background sync.
- [flutter-design-system-and-accessibility](../../skills/implementations/mobile/flutter/flutter-design-system-and-accessibility/SKILL.md) — tokens, theming, components, accessibility posture, i18n seam, permission-request UX.
- [flutter-performance-and-reliability](../../skills/implementations/mobile/flutter/flutter-performance-and-reliability/SKILL.md) — startup/frame budgets, memory/battery telemetry, crash-free-rate / ANR gates, CI gates.

---
