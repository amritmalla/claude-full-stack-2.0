# Kubernetes Network and Identity Policy Playbook

Load this when authoring any owned policy of `k8s-network-and-identity-policy` or checking the anti-pattern list. It expands the operating rules and process steps in `SKILL.md` with the detail needed to produce a production-grade network and identity posture.

## Why this workflow exists

Network and identity defects are silent until they are a breach. A namespace with no NetworkPolicy means any compromised pod anywhere in the cluster can reach the database. The `default` ServiceAccount with an over-broad ClusterRole turns a single RCE into cluster-admin. A long-lived registry credential mounted cluster-wide is one `kubectl get secret` from exfiltration. A mesh installed but mTLS left `PERMISSIVE` means east-west traffic is plaintext while everyone believes it is encrypted. None of this shows up in a functional test — the app works fine wide open.

The goal is a default-deny, least-privilege, explicitly-encrypted posture where every allowed flow and every granted verb is justified — consuming the security architecture instead of inventing it.

## Behavioral rules in depth

### 1. Consume the security architecture; do not invent it

Read the trust zones, identity model, mesh/mTLS decision, and east-west posture in `architecture/security`, plus the network boundaries and registry-auth mechanism in `infrastructure-platform.md`, before writing a policy. Segmentation and identity are security decisions. If a needed decision is missing, raise an ADR candidate.

### 2. Default-deny is the foundation, not an option

Every workload-carrying namespace gets a NetworkPolicy that selects all pods and denies ingress (and egress where the posture requires) before any allow exists. Allows are carved out of deny, never added to an implicit allow-all. A namespace without a default-deny is a finding.

### 3. Every allowed flow is justified

| Allow | Requirement |
|---|---|
| Ingress | Label-selected source; named peer; stated reason |
| Egress to in-cluster peer | Label-selected destination; named peer; stated reason |
| Egress to DNS | Explicitly allowed (port 53) — a common omission that breaks resolution |
| Egress to internet | CIDR-scoped and justified; never blanket `0.0.0.0/0` without an ADR |

`podSelector: {}` as an allow target is allow-all and is rejected.

### 4. Identity is least privilege, Role is the default

A dedicated ServiceAccount per workload; never `default` (it is mountable by everything and accumulates grants). Bind the narrowest `Role` covering exactly the operational contract. `ClusterRole` requires a named reason (a genuinely cluster-scoped need). Wildcard `verbs: ["*"]` / `resources: ["*"]` is an ADR-justified exception, not a convenience.

### 5. Registry credentials are short-lived

Image-pull auth uses the platform's short-lived mechanism (IRSA / Workload Identity / federated token) where supported. A long-lived static `dockerconfigjson` is an ADR-justified exception and, even then, is namespace-scoped and never broadly mounted.

### 6. mTLS posture is explicit, never implied

Mesh adopted → declare `STRICT` mTLS and the concrete enforcement object (e.g. a mesh `PeerAuthentication`), not `PERMISSIVE` left as a default. No mesh → state the east-west decision (native TLS, CNI-level encryption, or an accepted-risk ADR). "We have a mesh so it's encrypted" is not a posture; the enforcement object is.

### 7. Pod Security Standards are enforced at the namespace

Set `pod-security.kubernetes.io/enforce: restricted` (baseline) plus `audit`/`warn` labels so violations are both blocked and visible. PSS is the built-in floor; the *extended* policy engine (Kyverno/Gatekeeper custom policies) belongs to `k8s-supply-chain-and-image-hardening` — set the namespace floor here and name the handoff.

### 8. External exposure is opt-in and typed

Only a workload the platform marks externally reached gets an Ingress/Gateway. TLS, host, and path come from the platform traffic shape. Default is no external exposure; an accidental public Service is a finding.

### 9. A policy not connectivity- and RBAC-tested is not done

Prove an allowed peer reaches the workload and a denied peer is blocked (a temporary test pod, or a mesh/CNI policy-test tool). Prove the ServiceAccount has no excess permission (`kubectl auth can-i --list` impersonating the SA). Untested policy is unverified.

## Step detail

**Step 1 — Gather context.** Load `architecture/security` (trust zones, identity, mesh/mTLS, east-west) and `infrastructure-platform.md` (network boundaries, registry-auth). Resolve tier from `architecture-schema`. Confirm the workload's ServiceAccount reference and Service exist. Raise an ADR candidate for any missing decision.

**Step 2 — Default-deny.** Author the all-pods deny-ingress (and deny-egress where required) NetworkPolicy.

**Step 3 — Explicit allows.** Label-selected ingress/egress to named peers plus DNS egress; annotate each with peer and reason.

**Step 4 — Identity.** Dedicated ServiceAccount; least-privilege Role (ClusterRole only with a named reason); binding scoped to the operational contract.

**Step 5 — Registry auth.** Image-pull secret via the platform short-lived path; flag long-lived static credentials as an ADR exception.

**Step 6 — mTLS posture.** Mesh: `STRICT` + enforcement object. No mesh: explicit east-west decision.

**Step 7 — PSS.** Namespace `enforce: restricted` + audit/warn; mark the admission-engine extension handoff.

**Step 8 — Exposure.** Ingress/Gateway only where externally reached, TLS/host/path from the platform shape.

**Step 9 — Verify.** Connectivity test (allowed reaches, denied blocked) + RBAC review (no excess). Document any check that cannot run.

**Step 10 — Emit & validate.** Policy set under `k8s/`, `network-identity.md` (allowed-flow matrix, RBAC rationale, mTLS posture), handoff list. Validate against security-, deployment-, observability-standards, naming-conventions, architecture-schema.

## Anti-patterns to detect

Call these out explicitly when found:

- A workload namespace with no NetworkPolicy (implicit allow-all)
- An allow policy with `podSelector: {}` (allow-all) or blanket `0.0.0.0/0` egress without an ADR
- Missing DNS egress allow (breaks resolution under default-deny)
- Use of the `default` ServiceAccount; ClusterRole or wildcard verbs/resources without a named reason
- Long-lived static registry credential committed or broadly mounted
- Mesh present but mTLS left `PERMISSIVE`, or no stated east-west posture
- PSS not enforced at the namespace, or set to `privileged`/`baseline` without a reason
- An accidental external Service/Ingress for an internal workload
- The admission-policy engine (Kyverno/Gatekeeper) authored here instead of handed to the supply-chain archetype
- Workload manifests / autoscaling / observability authored here (wrong archetype)
- Policy declared done with no connectivity test or RBAC review
- CNI installation / cluster provisioning authored here (out of Family G)
