# Platform Architecture Quality Rubric

Load this before emitting `platform-architecture.md`. Revise until each check passes or the unresolved gap is explicitly documented.

## Topology and environments

- [ ] Cloud provider(s) and account/project structure are justified against blast radius, billing, compliance, and residency.
- [ ] Single-account/multi-account and single-cloud/multi-cloud posture is explicit; multi-cloud has an operational driver.
- [ ] Every environment defines isolation level, data posture, parity expectations, promotion flow, and ownership.
- [ ] No shared mutable staging or production-only infrastructure assumptions.

## Runtime and network

- [ ] Every workload class names its runtime substrate and operational rationale; no one-substrate-for-everything.
- [ ] No Kubernetes-by-default or serverless-for-long-running-workloads without justification.
- [ ] Every component sits in a named trust zone with explicit ingress and egress rules.
- [ ] East-west posture and internet exposure are explicit; no flat network or implicit trust.

## Identity and secrets

- [ ] Workload identity, human access, and service-to-service authentication are each defined separately.
- [ ] Admin boundaries, break-glass, and privileged-session handling are defined; no shared admin accounts.
- [ ] Secrets strategy defines store, issuance, rotation cadence, and injection mechanism.
- [ ] No static cloud credentials, secrets in Git/images, or manual rotation.

## Packaging and deployment

- [ ] Artifact strategy includes provenance, signing, vulnerability scanning, registry topology, and immutability.
- [ ] Every workload class defines release mechanism, rollback path, and blast-radius controls.
- [ ] No direct production mutation or deployments without rollback posture.

## IaC, CI/CD, and platform services

- [ ] IaC strategy names platform-owned vs service-owned module boundaries, state management, and drift detection.
- [ ] CI/CD defines build trust model, provenance, secrets handling, and deployment authorization; no unrestricted production credentials.
- [ ] Cross-cutting platform services (observability, certs, mesh, flags) name ownership boundaries and tenant isolation.

## Cost, complexity, and resilience

- [ ] Multi-region/account/cluster/tenant complexity has a measurable driver, operational owner, and an ADR.
- [ ] Cost posture defines tagging, autoscaling defaults, egress-risk areas, and a budget-breach response.
- [ ] Disaster posture defines backup substrate, failover topology, RTO/RPO, and restore-testing expectations.

## Linkage and decisions

- [ ] `platform-architecture.md` conforms to [architecture-schema](../../../../standards/architecture-schema/README.md): frontmatter complete, required sections present, conditional sections present or omitted with rationale.
- [ ] Every ADR candidate has Context, Decision, Consequences (including downsides), and Alternatives considered.
- [ ] No vendor-specific Terraform, manifests, or pipeline YAML leaked into the architecture.
- [ ] At least one weak-platform assumption was surfaced, or the design's intentional simplicity was explained.

## Failure handling

If a check fails:

1. Identify the missing or weak decision.
2. Ask the user for clarification if it cannot be inferred from `system-design.md` or the PRD.
3. Revise `platform-architecture.md` or the relevant ADR.
4. Keep unresolved questions explicit; do not hide them as assumptions.
