---
name: infrastructure-platform
description: Use when an approved system design exists and the team needs platform and infrastructure architecture before IaC implementation. Produces environment topology, cloud and runtime substrate selection, network and trust-boundary layout, compute and packaging strategy, secrets and identity model, deployment substrate and release mechanics, IaC ownership and module boundaries, cost posture, and implementation handoff notes. Do not use for application code, in-cluster service tuning, runbook authoring, or vendor-specific Terraform or Kubernetes manifest writing; use the relevant implementations/infrastructure/<vendor> skill instead.
---

# Infrastructure Platform

## When to use

Invoke after `system-design` has approved a design and before `implementations/infrastructure/*` skills generate Terraform, Kubernetes manifests, Helm charts, Dockerfiles, or CI/CD pipelines.

Do not use for application-level configuration, in-cluster service tuning, runbook or oncall workflow design (use `operations`), incident response (use `reliability`), or vendor-specific resource code (use the relevant implementation skill).

## Inputs

Required:

- Approved `system-design.md`.
- The platform scope in question: greenfield platform, new environment, new tenant or region, or platform evolution.
- Workload inventory: services, jobs, datastores, and external integrations the platform must host.

Optional:

- PRD or system-design sections covering scale, residency, compliance regime, and SLOs.
- Existing platform state: cloud accounts, networks, clusters, IaC repos, and golden paths.
- Vendor, region, or hosting constraints.
- Cost envelope and FinOps expectations.
- Team operating model: who owns platform, who owns services, what is paved-road vs free-for-all.

## Operating rules

- Separate the platform from the applications running on it. The platform exposes contracts (deploy, ingress, secrets, identity, telemetry); applications consume them.
- Choose the runtime substrate from workload needs, not vendor enthusiasm. Containers on Kubernetes, serverless functions, managed app platforms, and VMs have different operational costs.
- Environments are a contract: name them, state what they isolate, and state how parity is maintained. Avoid ad-hoc environments.
- Network architecture starts from trust boundaries: internet edge, DMZ, internal, restricted, and data-plane segments. Every component sits in a named zone with stated ingress and egress rules.
- Identity is the new perimeter. Define workload identity, human access, service-to-service auth, and the secrets lifecycle from issuance to rotation.
- Deployment is a substrate decision, not a script. Choose the release mechanism (rolling, blue-green, canary, progressive delivery) per workload class and state the rollback path.
- IaC is owned in modules with explicit boundaries: platform modules vs service modules, who can change what, and what is policy-enforced.
- Multi-region, multi-account, multi-tenant complexity is opt-in. Each requires a measured driver (residency, blast radius, isolation) recorded in an ADR.
- Cost is an architectural concern. Reserve, autoscale, and shutdown policies are decided at design time, not after the first bill.
- When a platform decision changes a regulatory, residency, or trust boundary, raise an ADR candidate against `system-design`.

## Process

1. Load `system-design.md` and inventory every workload that needs a runtime home: services, batch jobs, scheduled jobs, datastores, queues, edge functions, and third-party integrations.
2. Choose the cloud and account topology: provider(s), account or project structure, organizational boundaries, and the rationale (blast radius, billing, compliance).
3. Define environments: their names, purpose, isolation level, data posture, parity rules with production, and promotion flow between them.
4. Choose the runtime substrate per workload class: containers/Kubernetes, serverless, managed app platform, VM, or managed service. Justify against operational cost, scaling shape, and team maturity.
5. Define the network architecture: VPC/VNet layout, subnet tiers, trust zones, ingress and egress controls, private connectivity, DNS strategy, and inter-region or inter-account links.
6. Define the identity model: workload identity (instance profiles, workload identity federation), human access (SSO, just-in-time elevation), service-to-service authentication, and audit expectations.
7. Define the secrets and configuration model: secret store, issuance, rotation cadence, mounting or injection mechanism, and configuration-vs-secret boundary.
8. Define the packaging and image strategy: base images, image provenance and signing, registry topology, vulnerability scanning policy, and SBOM expectations.
9. Define the deployment substrate: GitOps vs push, release mechanism per workload class (rolling, blue-green, canary, progressive), gating signals, and rollback path.
10. Define the IaC strategy: tool choice, repo layout, module boundaries between platform and service, state management, policy-as-code surface, and drift detection.
11. Define the CI/CD substrate: build trust model, artifact provenance, environment promotion path, secrets in CI, and policy gates between stages.
12. Define cross-cutting platform services: observability backends, log routing, metrics and trace pipelines, certificate management, service mesh posture, and feature-flag substrate. Note that detailed observability instrumentation belongs to `operations`.
13. Define cost posture: tagging strategy, budget alerts, autoscaling defaults, off-hours shutdown, and reserved or committed-spend strategy.
14. Define disaster posture at the platform level: backup substrates, region failover topology, and RTO/RPO inputs that downstream `reliability` work will refine.
15. Produce `platform-architecture.md` with explicit handoffs to `implementations/infrastructure/<vendor>`, `operations`, `reliability`, `security`, and `quality-engineering`.

## Outputs

Required:

- `platform-architecture.md` covering account/cloud topology, environment model, runtime substrate per workload class, network and trust zones, identity model, secrets model, packaging strategy, deployment substrate, IaC strategy, CI/CD substrate, cross-cutting services, cost posture, and handoff notes.

Optional, when applicable:

- Account/project topology diagram.
- Network diagram with trust zones.
- Workload-to-substrate mapping table.
- IaC module boundary table.
- ADR drafts for substrate, region topology, IaC tool, or deployment mechanism decisions.

## Quality checks

- [ ] Every workload class names its runtime substrate and the justification.
- [ ] Environment list states isolation level, data posture, and parity rules.
- [ ] Every component sits in a named trust zone with stated ingress and egress rules.
- [ ] Workload identity, human access, and service-to-service auth are each explicitly defined.
- [ ] Secrets model names the store, issuance path, rotation cadence, and mounting mechanism.
- [ ] Image strategy covers base images, signing, scanning, and registry topology.
- [ ] Each workload class names its release mechanism and rollback path.
- [ ] IaC strategy names the module boundary between platform and service ownership.
- [ ] Multi-region, multi-account, or multi-tenant complexity, if present, is justified by a stated driver and has an ADR.
- [ ] Cost posture states tagging, autoscaling defaults, and a budget-breach action.
- [ ] No vendor-specific Terraform, manifests, or pipeline YAML appear in the architecture unless they materially change behavior.

## References

- Upstream: [`architecture/system-design`](../system-design/SKILL.md).
- Downstream implementation skills: `implementations/infrastructure/aws`, `implementations/infrastructure/gcp`, `implementations/infrastructure/azure`, `implementations/infrastructure/kubernetes`, `implementations/infrastructure/terraform`, `implementations/infrastructure/docker`, `implementations/infrastructure/github-actions`.
- Related architecture skills: `operations`, `reliability`, `security`, `performance`.
