# Kubernetes Workload Packaging and Manifest Playbook

Load this when authoring any owned resource of `k8s-workload-packaging-and-manifest` or checking the anti-pattern list. It expands the operating rules and process steps in `SKILL.md` with the detail needed to produce a production-grade manifest set.

## Why this workflow exists

Manifest defects fail in production in ways a `kubectl apply` success never reveals. A missing `resources.requests` lets the scheduler overcommit a node until the kubelet evicts unrelated pods. A `livenessProbe` that hits the same slow endpoint as readiness restart-loops the pod under load. A `:latest` tag means two replicas of "the same" deploy run different code. No PDB means a routine node drain takes the whole service down. None of this reproduces in a one-replica dev namespace.

The goal is a manifest set that schedules fairly, gates traffic correctly, rolls out safely, and hands off cleanly to the archetypes that tune and harden it — consuming upstream decisions instead of inventing them.

## Behavioral rules in depth

### 1. Consume architecture; do not invent it

Read the Workload Inventory, Runtime Substrate Selection, and Deployment & Release Architecture in `infrastructure-platform.md`, plus the workload class and resource expectations in `backend-architecture.md`, before writing a single manifest. The release strategy and resource envelope are architectural decisions. If a needed decision is missing, raise an ADR candidate.

### 2. The workload kind follows the class, not habit

| Workload class | Kind | Signal |
|---|---|---|
| Stateless API / worker | Deployment | Interchangeable replicas, no identity |
| Ordered / identity-bound / per-replica storage | StatefulSet | Stable network ID, ordered rollout |
| Node-local agent | DaemonSet | One per node |
| Run-to-completion | Job | Finite work, retries with backoff |
| Scheduled | CronJob | Time-triggered Job, with concurrency policy |

Defaulting everything to Deployment is a defect when the class says otherwise.

### 3. Requests and limits are both mandatory

`requests` drives scheduling and is the fairness contract; `limits` caps blast radius. A container missing either is rejected. Memory limit without request invites OOM under pressure; CPU request without limit lets one pod starve neighbors. Derive both from the upstream resource expectation — never leave blank, never guess silently (guessing is an ADR candidate).

### 4. Three probes, three purposes

| Probe | Purpose | Failure effect |
|---|---|---|
| `startupProbe` | Cover slow init without tripping liveness | Holds liveness/readiness until first success |
| `readinessProbe` | Gate traffic | Pod removed from Service endpoints |
| `livenessProbe` | Detect a hung process | Pod restarted |

Pointing all three at one endpoint defeats the design: a slow start trips liveness and restart-loops; a missing readiness sends traffic to a cold pod.

### 5. Images are immutable references

Digest-pin where the registry supports it (`image@sha256:...`); otherwise an immutable tag, never `:latest`, for any promotable environment. Set `imagePullPolicy` explicitly. Two replicas must be byte-identical.

### 6. Configuration is injected, never baked

Config → ConfigMap; secrets → Secret *reference* (name only — values and the secret backend belong upstream / to the security archetype). No environment-branched manifests; the same manifest set parameterized per env is the contract, not `deployment-prod.yaml` vs `deployment-dev.yaml` with divergent logic.

### 7. Born safe, tuned later

Author a tier-correct baseline HPA and a PDB (required when replicas > 1) so the workload is never born unsafe — but sizing, VPA/KEDA selection, anti-affinity, and topology spread are `k8s-scaling-and-resilience-topology`'s ownership. Set a conservative default and mark the handoff in a comment. The same applies to the security-context baseline (set the floor) versus deep hardening/signing/admission (`k8s-supply-chain-and-image-hardening`).

### 8. Rolling-update parameters match the tier

`maxUnavailable: 0` for tier-0/1 availability-critical workloads (surge up before terminating old). Tighter `maxSurge` on capacity-constrained clusters. If upstream declares blue-green or canary, that mechanism is handed to the delivery layer — this skill does not invent a progressive-delivery controller.

### 9. A manifest that does not dry-run clean is not done

`kubectl apply --dry-run=server` (server-side schema + admission) or, with no cluster, `kubeconform`/client dry-run plus a policy lint. A manifest set declared done without a passing dry-run is unverified.

## Step detail

**Step 1 — Gather context.** Load `infrastructure-platform.md` (Workload Inventory, Runtime Substrate, Deployment & Release) and `backend-architecture.md` (class, resource expectations). Resolve tier from `architecture-schema`. Raise an ADR candidate for any missing decision.

**Step 2 — Package the container.** Invoke the language sub-skill (`dockerfile-and-jvm-tuning` for JVM; planned non-JVM siblings). Obtain a digest-pinnable reference.

**Step 3 — Author the controller.** Select kind from class; set replicas from tier default, security-context baseline, explicit `imagePullPolicy`, recommended `app.kubernetes.io/*` labels.

**Step 4 — Resources.** Set `requests` and `limits` on every container from the upstream envelope.

**Step 5 — Probes.** Author distinct `startupProbe`/`readinessProbe`/`livenessProbe` with purpose-appropriate endpoints and thresholds.

**Step 6 — Service & Ingress.** ClusterIP unless upstream declares external; Ingress only where externally reached, matching the upstream traffic shape.

**Step 7 — Config injection.** ConfigMap for config; Secret references (names only) for secrets. No values, no env-branched manifests.

**Step 8 — Baseline HPA & PDB.** Tier-correct safe defaults; PDB when replicas > 1; explicit handoff comment to the scaling archetype.

**Step 9 — Rollout parameters.** `maxUnavailable`/`maxSurge` per tier; honor the upstream release strategy; hand progressive delivery to the delivery layer.

**Step 10 — Verify.** Server-side dry-run or offline schema/policy lint; document any check that cannot run.

**Step 11 — Emit & validate.** Manifest set under `k8s/`, `deploy.md` (rollout + rollback), handoff list. Validate against deployment-, security-, observability-standards, naming-conventions, architecture-schema.

## Anti-patterns to detect

Call these out explicitly when found:

- Deployment used where the class is StatefulSet/DaemonSet/Job/CronJob
- A container missing `resources.requests` or `resources.limits`
- One endpoint reused for startup, readiness, and liveness; missing readiness
- Floating `:latest` (or a mutable tag) for a promotable environment
- Secret values inlined in a manifest; env-branched `deployment-<env>.yaml` with divergent logic
- No PDB for a multi-replica workload
- HPA/PDB sizing, anti-affinity, or topology spread authored here instead of handed to the scaling archetype
- Deep image hardening / signing / admission authored here instead of handed to the supply-chain archetype
- `maxUnavailable > 0` on a tier-0/1 availability-critical workload
- An invented progressive-delivery controller instead of honoring the upstream release strategy
- Manifest set declared done with no server-side dry-run or schema/policy lint
- Cluster provisioning / node pools authored here (out of Family G)
