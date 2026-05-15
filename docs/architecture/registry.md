# Architecture Registry

> Single source of truth for architecture↔implementation mapping, domain/ecosystem ownership, and upstream/downstream wiring. Replaces the per-directory README.md files that previously held this metadata.
>
> Skills are discovered by file system (architecture/<domain>/SKILL.md and implementations/<category>/<ecosystem>/<skill>/SKILL.md). This file documents the *charter* of each domain and ecosystem.

## Architecture domains

### ai-native-engineering

**Status:** scaffold

**Purpose:** Augments engineering workflows using AI-native systems.

> See [research.md](./research.md) for the target spec.

---

### backend-architecture

**Status:** draft

**Purpose:** Defines backend execution architecture and service behavior from an approved system design: service boundaries, domain behavior, API and async contracts, transactional boundaries, consistency rules, security touchpoints, and implementation handoffs.

Technology-agnostic. Owns *what* a backend service exposes and *how* it behaves, not the framework that runs it. Framework-specific scaffolding lives under [implementations/backend](../../implementations/backend/).

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

- [implementations/backend/*](../../implementations/backend/) - server scaffolds, modules, controllers, DTOs, workers, and integration points follow the backend architecture.
- [implementations/data/*](../../implementations/data/) - schema and migration skills consume ownership, transaction, and consistency decisions.
- [implementations/frontend/*](../../implementations/frontend/) - client SDKs and typed fetch layers consume published contracts.
- [architecture/quality-engineering](#quality-engineering) - contract-driven and workflow-driven integration tests.

**Skills:**
- [backend-architecture](../../architecture/backend-architecture/SKILL.md) — turns approved system design into backend service architecture: boundaries, domain behavior, interface strategy, transactions, consistency, security touchpoints, operations, and implementation handoff notes.

---

### data-architecture

**Status:** scaffold

**Purpose:** Designs the operational data layer: database engine choice, schema and consistency model, index strategy, partitioning and replication topology, caching strategy, and retention.

> See [research.md](./research.md) for the target spec.

---

### frontend-architecture

**Status:** scaffold

**Purpose:** Designs scalable frontend application systems.

> See [research.md](./research.md) for the target spec.

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
- [architecture/system-design](#system-design)
- [architecture/backend-architecture](#backend-architecture)
- [architecture/frontend-architecture](#frontend-architecture)
- [architecture/quality-engineering](#quality-engineering)

**Skills:**
- [idea-development](../../architecture/idea-development/SKILL.md) — develops an informal product idea through discovery, refinement, validation, specification, and execution readiness; emits a decision-oriented PRD conforming to prd-schema plus a readiness note.

---

### infrastructure-platform

**Status:** scaffold

**Purpose:** Productionizes systems across cloud and runtime environments.

> See [research.md](./research.md) for the target spec.

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
- [operations](../../architecture/operations/SKILL.md) — produces blameless postmortems, reusable runbooks, and operational handoff notes for services entering support.

---

### performance

**Status:** scaffold

**Purpose:** Optimizes scalability, efficiency, and operational cost.

> See [research.md](./research.md) for the target spec.

---

### reliability

**Status:** scaffold

**Purpose:** Ensures resilience, observability, and operational recovery.

> See [research.md](./research.md) for the target spec.

---

### security

**Status:** scaffold

**Purpose:** Protects systems, users, infrastructure, and organizational assets.

> See [research.md](./research.md) for the target spec.

---

### system-design

**Status:** draft

**Purpose:** Designs scalable system architecture and technical topology from an approved PRD. Defines the architectural envelope that downstream implementation domains fill in.

Technology-agnostic. Owns *shape* and *boundaries*, not vendor or framework choices (those land in `implementations/`).

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

- [implementations/backend/*](../../implementations/backend/)
- [implementations/frontend/*](../../implementations/frontend/)
- [implementations/data/*](../../implementations/data/)
- [implementations/infrastructure/*](../../implementations/infrastructure/)
- [architecture/backend-architecture](#backend-architecture) (backend boundaries and contracts)
- [architecture/data-architecture](#data-architecture) (schemas and migrations)

**Skills:**
- [system-design](../../architecture/system-design/SKILL.md) - turns an approved PRD into a system design and inline ADRs.

---

### quality-engineering

**Status:** draft

**Purpose:** Validates correctness, reliability, and production readiness. Owns testing strategy, QA automation, validation pipelines, regression prevention, and contract testing.

Architecture-domain level. The *strategy* and *coverage decisions* are ecosystem-neutral; the *wiring* (specific test runners, fixtures, container libraries) lives in implementation skills under each `implementations/*` ecosystem.

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
- [implementations/backend/*](../../implementations/backend/) — each ecosystem wires the test strategy into its own runner and fixture library.
- [implementations/infrastructure/*](../../implementations/infrastructure/) — CI pipelines invoke the suites declared here.

**Skills:**
- [quality-engineering](../../architecture/quality-engineering/SKILL.md) — produces contract-driven test strategy, acceptance criteria, integration test planning, and CI quality gates.

---

## Implementation ecosystems

### ai (category)

**Purpose:** Technology-specific execution skills for ai.

---

### ai/anthropic

**Status:** scaffold

**Purpose:** Implements relevant architecture domains using the anthropic ecosystem.

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

**Status:** scaffold

**Purpose:** Implements relevant architecture domains using the langchain ecosystem.

---

### ai/openai

**Status:** scaffold

**Purpose:** Implements relevant architecture domains using the openai ecosystem.

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

**Status:** scaffold

**Purpose:** Implements relevant architecture domains using the fastapi ecosystem.

---

### backend/golang

**Status:** scaffold

**Purpose:** Implements relevant architecture domains using the golang ecosystem.

---

### backend/nodejs

**Status:** scaffold

**Purpose:** Implements relevant architecture domains using the nodejs ecosystem.

---

### backend/spring-boot

**Status:** draft

**Purpose:** Implements backend architecture domains using the Spring ecosystem. This is the *how* layer — framework-specific scaffolding, configuration, and hardening. Architecture decisions (API shape, domain modeling, auth strategy) come from [architecture/](../../architecture/) and are taken as inputs here.

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
- [modular-monolith](../../patterns/modular-monolith/README.md)
- [microservices](../../patterns/microservices/README.md)
- [event-driven](../../patterns/event-driven/README.md)
- [cqrs](../../patterns/cqrs/README.md)
- [hexagonal-architecture](../../patterns/hexagonal-architecture/README.md)

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
- Approved `backend-architecture.md` from [backend-architecture](../../architecture/backend-architecture/SKILL.md), plus `openapi.yaml` and `api-conventions.md` for any service exposing REST.

**Downstream consumers:**
- [implementations/data/postgres](../../implementations/data/postgres/) — Flyway migrations land in the scaffold's `db/migration/` directory.
- [implementations/infrastructure/*](../../implementations/infrastructure/) — built artifacts (Docker images) are deployed through the platform stack.

**Skills:**
- [spring-boot-service-scaffold](../../implementations/backend/spring-boot/spring-boot-service-scaffold/SKILL.md) — produces a production-ready service shell: package structure, profile-aware configuration, structured logging, observability, health probes, secure defaults, error handling, testing foundations, Docker packaging.
- [spring-security-auth-review](../../implementations/backend/spring-boot/spring-security-auth-review/SKILL.md) — reviews and hardens authentication / authorization for a Spring Boot service using Spring Security, JWT, OAuth2, sessions, or service-to-service auth.
- [spring-boot-observability-readiness](../../implementations/backend/spring-boot/spring-boot-observability-readiness/SKILL.md) — produces or audits Micrometer/Prometheus metrics, OpenTelemetry tracing, structured logs with trace correlation, SLI/SLO definitions, and multi-window multi-burn-rate alerts.
- [spring-kafka-event-integration](../../implementations/backend/spring-boot/spring-kafka-event-integration/SKILL.md) — produces or hardens Spring Kafka producers and consumers: delivery semantics, transactional outbox, idempotency, retry and DLQ topology, observability, and integration tests against embedded or Testcontainers Kafka.
- [spring-boot-performance-and-resilience](../../implementations/backend/spring-boot/spring-boot-performance-and-resilience/SKILL.md) — produces or hardens latency/throughput posture and resilience for a Spring Boot service: timeouts, retries, circuit breakers, bulkheads, rate limiting, connection-pool and thread-pool sizing, caching, and load-test gates.

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

**Purpose:** Implements `architecture/data-architecture` for MongoDB: document modeling, schema validation, index strategy, shard-key choice, read/write concern posture, and zero-downtime evolution.

Architecture decisions (which bounded contexts own which collections, consistency posture, sharding choice, replica topology) come from upstream and are taken as inputs here.

**Ecosystem:**
- MongoDB 6.0+ (replica set or sharded cluster)
- `$jsonSchema` validators
- mongock, mongo-migrate, or hand-rolled idempotent migration scripts
- Testcontainers for migration dry-runs

**Compatible patterns:**
- [modular-monolith](../../patterns/modular-monolith/README.md)
- [microservices](../../patterns/microservices/README.md)
- [event-driven](../../patterns/event-driven/README.md) (change-stream consumers; outbox patterns)
- [cqrs](../../patterns/cqrs/README.md) (read-model projections)

**Architecture domains implemented:**

| Architecture domain | How |
|---|---|
| [data-architecture](#data-architecture) | Document modeling, validation, indexing strategy, shard-key choice, retention rules, consistency posture. |
| [reliability](#reliability) | Zero-downtime migrations, backup/restore hooks, replica-set posture. |

**Skills:**
- [mongodb-data-model-and-migration](../../implementations/data/mongodb/mongodb-data-model-and-migration/SKILL.md) — produces document modeling decisions, `$jsonSchema` validators, index strategy, shard-key choice if sharded, read/write concern posture, and zero-downtime migration plans using expand-migrate-contract or dual-write.

---

### data/postgres

**Status:** draft

**Purpose:** Implements `architecture/data-architecture` for PostgreSQL: schema design, integrity constraints, indexing strategy, migrations (Flyway / Liquibase), and zero-downtime evolution.

Architecture decisions (which bounded contexts own which data, consistency model, retention strategy) come from upstream and are taken as inputs here.

**Ecosystem:**
- PostgreSQL 14+
- Flyway (default) or Liquibase
- Testcontainers for migration verification
- `pg_dump` / logical replication for migration rehearsals

**Compatible patterns:**
- [modular-monolith](../../patterns/modular-monolith/README.md)
- [microservices](../../patterns/microservices/README.md)
- [event-driven](../../patterns/event-driven/README.md) (outbox tables live here)
- [cqrs](../../patterns/cqrs/README.md) (read-model projections)

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
- [implementations/backend/spring-boot](../../implementations/backend/spring-boot/) — Flyway migrations land in the scaffold's `db/migration/` directory.
- [architecture/quality-engineering](../../architecture/quality-engineering/) — integration tests run against this schema via Testcontainers.

**Skills:**
- [postgres-schema-and-migration](../../implementations/data/postgres/postgres-schema-and-migration/SKILL.md) — produces normalized schema, integrity constraints, indexing strategy, Flyway migrations, and zero-downtime migration plans using expand / migrate / contract.

---

### data/redis

**Status:** scaffold

**Purpose:** Implements relevant architecture domains using the redis ecosystem.

---

### frontend (category)

**Purpose:** Technology-specific execution skills for frontend.

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

**Status:** scaffold

**Purpose:** Implements relevant architecture domains using the react ecosystem.

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

**Status:** scaffold

**Purpose:** Implements relevant architecture domains using the aws ecosystem.

---

### infrastructure/azure

**Status:** scaffold

**Purpose:** Implements relevant architecture domains using the azure ecosystem.

---

### infrastructure/docker

**Status:** draft

**Purpose:** Implements container packaging for services. Produces minimal, hardened images that conform to [deployment-standards](../../standards/deployment-standards/README.md) (env-agnostic, immutable, signed) and [security-standards](../../standards/security-standards/README.md) (no secrets baked, non-root, scanned).

**Architecture domains implemented:**

| Architecture domain | How |
|---|---|
| [infrastructure-platform](#infrastructure-platform) | Container packaging, JVM runtime tuning. |
| [security](#security) | Non-root, minimal base, scanned images. |
| [performance](#performance) | JVM heap and GC tuning for container memory limits. |

**Standards this implementation conforms to:**
- [deployment-standards](../../standards/deployment-standards/README.md) — env-agnostic image, config at deploy time, signed artifacts.
- [security-standards](../../standards/security-standards/README.md) — no baked secrets, container scan as a required gate.
- [naming-conventions](../../standards/naming-conventions/README.md) — `kebab-case` image names, registry-prefixed.

**Skills:**
- [dockerfile-and-jvm-tuning](../../implementations/infrastructure/docker/dockerfile-and-jvm-tuning/SKILL.md) — multi-stage Dockerfile for JVM services with distroless or jlink runtime, container-aware JVM tuning, layered jars, and image scanning.

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
- [github-actions-pipeline-hardened](../../implementations/infrastructure/github-actions/github-actions-pipeline-hardened/SKILL.md) — produces build/test/scan/sign/push workflows with pinned action versions, dependency caching, SBOM generation, and provenance signing.

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
- [k8s-deploy-manifest-review](../../implementations/infrastructure/kubernetes/k8s-deploy-manifest-review/SKILL.md) — authors or reviews Kubernetes manifests for production workloads (Deployment, Service, HPA, PDB, NetworkPolicy, security context).

---

### infrastructure/terraform

**Status:** scaffold

**Purpose:** Implements relevant architecture domains using the terraform ecosystem.

---
