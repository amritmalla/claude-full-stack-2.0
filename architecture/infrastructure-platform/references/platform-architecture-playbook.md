# Platform Architecture Playbook

Load this when inventorying workloads, choosing substrate, or making any platform-architecture decision. It expands the operating rules and process steps in `SKILL.md` with the detail needed to produce `platform-architecture.md`.

## Why this workflow exists

Design scalable, secure, operable, evolvable infrastructure platforms before IaC implementation begins. It prevents infrastructure sprawl, accidental trust-boundary violations, runtime/platform mismatch, insecure identity and secret handling, ungoverned Kubernetes adoption, brittle deployment systems, uncontrolled cloud costs, and operational complexity hidden behind tooling.

The goal is not "where workloads run" — it is clear platform contracts, operationally sustainable infrastructure, secure workload isolation, predictable deployment behavior, and resilient platform foundations.

## Behavioral rules in depth

### 1. Separate platform from application concerns

The platform provides contracts: deployability, networking, identity, secrets, telemetry, runtime guarantees. Applications consume them. Reject application teams owning foundational infrastructure primitives ad hoc, and platform logic leaking into application services.

### 2. Runtime substrate follows workload shape

Choose based on workload behavior, scaling characteristics, operational maturity, compliance needs, and deployment frequency. Substrates: Kubernetes, serverless functions, managed application platforms, VMs, batch substrates, edge runtimes. Reject Kubernetes-by-default and serverless-by-trend. Every substrate has operational costs, scaling tradeoffs, and failure modes.

### 3. Environment topology is explicit

Environments are contracts. Every environment defines purpose, isolation boundary, data posture, parity expectations, promotion flow, and ownership. Reject ad hoc staging environments and environment sprawl without lifecycle governance.

### 4. Network starts with trust boundaries

Every workload exists inside a named trust zone with explicit ingress rules, egress rules, and connectivity assumptions. Zones: internet edge, public DMZ, internal services, restricted workloads, data plane, management plane. Reject flat networks, unrestricted east-west traffic, and implicit trust.

### 5. Identity is the new perimeter

Define workload identity, human access, service-to-service authentication, and secrets lifecycle. Reject static credentials, shared admin accounts, and long-lived machine secrets. Prefer federated identity, workload identity, short-lived credentials, and centralized policy enforcement.

### 6. Deployment is architecture, not scripting

Strategies: rolling, blue-green, canary, progressive delivery, immutable deployment. Every workload class defines rollout mechanism, rollback behavior, blast-radius expectations, and deployment gating signals. Reject one deployment strategy for all workloads.

### 7. Infrastructure ownership boundaries are explicit

IaC defines platform-owned modules, service-owned modules, policy-enforced boundaries, and state ownership. Reject giant monolithic Terraform repos and unrestricted infrastructure mutation.

### 8. Complexity is opt-in

Multi-region, multi-account, multi-cluster, and multi-tenant architecture each require a measurable business driver, operational ownership, and an ADR. Reject speculative geo-distribution and future-proofing through uncontrolled complexity.

### 9. Cost is a first-class constraint

Decisions consider idle cost, autoscaling behavior, storage growth, network egress, reserved capacity, and operational staffing cost. Reject "optimize later" cost posture.

### 10. Challenge weak platform assumptions directly

Be direct and operationally grounded. Examples of the kind of feedback to give:

- "This workload does not justify Kubernetes operational overhead."
- "Your network zones effectively collapse into one trust boundary."
- "Your CI system has excessive production mutation privileges."
- "This multi-region design lacks a clear residency or availability driver."
- "Your secrets rotation story is operationally incomplete."

## Step detail

**Workload inventory (step 1).** Identify APIs, background jobs, scheduled workloads, queues, streaming workloads, databases, edge services, third-party integrations. Per workload determine runtime expectations, scaling shape, criticality, and deployment frequency.

**Cloud & account topology (step 2).** Clarify single-account vs multi-account, single-cloud vs multi-cloud, shared-services accounts, and tenant isolation posture. Justify against blast radius, billing isolation, compliance, operational ownership, and residency. Reject multi-cloud without operational justification.

**Environment architecture (step 3).** Typical: local, development, staging, pre-production, production, ephemeral preview. Per environment define isolation level, production parity, data posture, and deployment gating. Reject shared mutable staging and production-only infrastructure assumptions.

**Runtime substrate (step 4).** Substrates: Kubernetes, serverless, managed app platform, VM, edge runtime, batch execution platform. Justify using scaling behavior, deployment frequency, startup latency, operational maturity, and observability requirements. Reject one-substrate-for-everything.

**Network & trust boundaries (step 5).** Define VPC/VNet layout, subnet segmentation, ingress model, egress controls, DNS topology, private connectivity, and east-west posture. Every component defines trust zone, ingress/egress policy, and internet exposure. Clarify zero-trust posture and cross-region/account links. Reject unrestricted lateral movement.

**Identity & access (step 6).** Mechanisms: workload identity federation, IAM roles, OIDC federation, mTLS, SSO, JIT elevation. Clarify admin boundaries, break-glass access, audit logging, and privileged-session handling. Reject static cloud credentials and shared operational identities.

**Secrets & configuration (step 7).** Mechanisms: Vault, cloud secret managers, workload identity fetch, sidecar injection, runtime mount. Define store, issuance path, rotation cadence, injection mechanism, and config-vs-secret boundary. Reject secrets in Git, secrets in images, and manual rotation.

**Packaging & artifacts (step 8).** Define base-image strategy, artifact provenance, image-signing posture, vulnerability scanning, registry topology, SBOM, trusted build pipeline, runtime hardening, and immutable-artifact expectations. Reject mutable production artifacts and unscanned images.

**Deployment & release (step 9).** Mechanisms: GitOps, push-based deployment, progressive delivery, canary analysis, blue-green. Per workload define deployment frequency, rollback expectation, and blast-radius controls. Reject direct production mutation and deployments without rollback posture.

**IaC strategy (step 10).** Define tool selection, repo layout, module boundaries, policy-as-code posture, state management, platform-owned vs service-owned infrastructure, drift detection, module versioning, and approval workflow. Reject unbounded Terraform state and no-ownership repos.

**CI/CD platform (step 11).** Define build trust model, artifact promotion path, environment promotion flow, secrets handling in CI, policy gates, provenance guarantees, supply-chain integrity, ephemeral runners, and deployment authorization. Reject CI with unrestricted production credentials.

**Cross-cutting services (step 12).** Shared services: observability backend, metrics pipeline, logging pipeline, tracing infrastructure, certificate management, service mesh, feature-flag infrastructure. Clarify ownership boundaries, tenant isolation, and operational scaling. Reject observability added ad hoc per service.

**Cost & FinOps (step 13).** Define tagging standards, budget ownership, autoscaling defaults, reserved-capacity posture, off-hours policies, egress-risk areas, storage growth posture, cost-allocation visibility, and budget-breach response. Reject invisible shared-cost infrastructure.

**Disaster & resilience (step 14).** Define backup substrate, region-failover topology, DR posture, RTO/RPO assumptions, active-passive vs active-active, restore testing, and regional isolation behavior. Reject backups without restore drills and untested failover assumptions.

## Anti-patterns to detect

Call these out explicitly when detected:

- Kubernetes-by-default
- Multi-cloud without business driver
- Flat network topology
- Shared production credentials
- Secrets in CI variables forever
- No workload identity
- Shared mutable staging
- Unbounded Terraform state
- Push-to-production from laptops
- Production drift without detection
- No rollback strategy
- Serverless used for long-running workloads
- VM sprawl
- Multi-region without residency/availability need
- Observability as an afterthought
- Shared admin accounts
- Long-lived machine credentials
- Uncontrolled egress
- No artifact provenance
- CI/CD with unrestricted production access
- Cost-blind autoscaling
- Backups without restore validation

## Writing style

Operationally rigorous, platform-oriented, security-conscious, systems-focused. Avoid vendor hype, tool tribalism, implementation-level IaC detail, and infrastructure trends without operational reasoning. The objective is a secure, scalable, operable platform architecture — not just provisioning infrastructure.
