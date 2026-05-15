---
product: <kebab-case slug>          # matches the system-design / PRD slug
status: draft                       # draft | review | approved | superseded
owner: <name or role>
system_design: <relative path to source system-design.md>
prd: <relative path to source PRD, or null>
version: 0.1.0                      # semver
last_reviewed: YYYY-MM-DD
---

# Platform Architecture: [Product or Platform Name]

## Overview

[One paragraph: which workloads the platform hosts, the cloud/runtime substrate, what it optimizes for (security, cost, operability), and what it intentionally does not do.]

## Workload Inventory

| Workload | Class | Runtime Expectation | Scaling Shape | Criticality | Deployment Frequency |
|---|---|---|---|---|---|
| [name] | [API / job / scheduled / queue / streaming / database / edge / integration] | [expectation] | [shape] | [tier] | [frequency] |

## Cloud & Account Topology

| Concern | Decision |
|---|---|
| Cloud provider(s) | [provider] |
| Account/project structure | [structure] |
| Organizational boundaries | [boundaries] |
| Region strategy | [strategy] |
| Single vs multi-account | [decision + driver] |
| Single vs multi-cloud | [decision + driver] |
| Tenant isolation posture | [posture] |

## Environment Architecture

| Environment | Purpose | Isolation Level | Data Posture | Production Parity | Promotion Flow | Owner |
|---|---|---|---|---|---|---|
| [env] | [purpose] | [isolation] | [posture] | [parity] | [flow] | [owner] |

## Runtime Substrate Selection

| Workload Class | Substrate | Justification | Alternatives Rejected |
|---|---|---|---|
| [class] | [Kubernetes / serverless / managed app / VM / edge / batch] | [scaling/freq/latency/maturity/observability] | [why not X] |

## Network & Trust-Boundary Architecture

| Component | Trust Zone | Ingress Policy | Egress Policy | Internet Exposure |
|---|---|---|---|---|
| [component] | [internet edge / DMZ / internal / restricted / data plane / management plane] | [policy] | [policy] | [yes/no] |

VPC/VNet layout, subnet segmentation, DNS topology, private connectivity, east-west posture: [decisions].

## Identity & Access Architecture

| Concern | Decision |
|---|---|
| Workload identity | [federation / IAM roles / mTLS] |
| Human access model | [SSO / JIT elevation] |
| Service-to-service authentication | [mechanism] |
| Admin boundaries & break-glass | [decision] |
| Audit & privileged-session handling | [decision] |

## Secrets & Configuration Strategy

| Concern | Decision |
|---|---|
| Secrets store | [Vault / cloud secret manager] |
| Issuance path | [path] |
| Rotation cadence | [cadence] |
| Injection mechanism | [workload fetch / sidecar / runtime mount] |
| Config-vs-secret boundary | [rule] |

## Packaging & Artifact Strategy

| Concern | Decision |
|---|---|
| Base-image strategy | [strategy] |
| Artifact provenance & signing | [decision] |
| Vulnerability scanning | [policy] |
| Registry topology | [topology] |
| SBOM & immutability | [expectations] |

## Deployment & Release Architecture

| Workload Class | Deployment Substrate | Release Strategy | Gating Signals | Rollback | Blast-Radius Control |
|---|---|---|---|---|---|
| [class] | [GitOps / push] | [rolling / blue-green / canary / progressive / immutable] | [signals] | [behavior] | [control] |

## Infrastructure-as-Code Strategy

| Concern | Decision |
|---|---|
| IaC tool | [tool] |
| Repo layout | [layout] |
| Module boundaries | [platform-owned vs service-owned] |
| Policy-as-code | [posture] |
| State management | [strategy] |
| Drift detection & approval workflow | [decision] |

## CI/CD Platform Architecture

| Concern | Decision |
|---|---|
| Build trust model | [model] |
| Artifact promotion path | [path] |
| Environment promotion flow | [flow] |
| Secrets handling in CI | [mechanism] |
| Policy gates | [gates] |
| Provenance & supply-chain integrity | [guarantees] |
| Runner model & deployment authorization | [ephemeral / authorization] |

## Cross-Cutting Platform Services

*Conditional — include when shared platform services exist; otherwise list under Omitted sections.*

| Service | Ownership | Tenant Isolation | Operational Scaling |
|---|---|---|---|
| [observability / metrics / logging / tracing / certs / mesh / feature flags] | [owner] | [isolation] | [scaling] |

## Cost & FinOps Posture

| Concern | Decision |
|---|---|
| Tagging standards | [standard] |
| Budget ownership | [owner] |
| Autoscaling defaults | [defaults] |
| Reserved-capacity posture | [posture] |
| Off-hours policy | [policy] |
| Egress-risk & storage growth | [areas] |
| Budget-breach response | [process] |

## Disaster & Resilience Posture

| Concern | Decision |
|---|---|
| Backup substrate | [substrate] |
| Region-failover topology | [active-passive / active-active] |
| RTO / RPO assumptions | [RTO/RPO] |
| Restore-testing expectations | [cadence] |
| Regional isolation behavior | [behavior] |

## Multi-Region & Tenancy

*Conditional — include only when multi-region, multi-cluster, or multi-tenant complexity is opted in; otherwise list under Omitted sections.*

| Concern | Decision | Business Driver | ADR |
|---|---|---|---|
| [region/cluster/tenant complexity] | [decision] | [residency / availability / isolation] | [NNNN] |

## Implementation Handoffs

### implementations/infrastructure/<vendor>

- [IaC, cluster, pipeline handoff notes per workload class]

### security

- [Trust zones, identity, secrets, supply-chain posture]

### reliability / operations

- [DR, failover, observability substrate, runbook hooks]

### quality-engineering

- [Environment parity and deployment-gate test expectations]

## ADR Index

| ADR | Title | Status | Summary |
|---|---|---|---|
| NNNN | [title] | [proposed/accepted/...] | [summary] — links to `adrs/NNNN-<slug>.md` |

## Omitted sections

- [Conditional section name]: [one-line rationale for omission].

## Deferred Decisions

- [Decision, owner, deadline].
