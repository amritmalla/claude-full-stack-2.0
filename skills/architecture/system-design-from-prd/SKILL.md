---
name: system-design-from-prd
description: Use when an approved PRD exists and the team needs a decision-oriented system design before implementation begins. Produces bounded contexts, architecture style tradeoffs, component definitions, data flow and ownership, failure modes, security implications, operational requirements, and ADR-backed technical decisions. Do not invoke when the PRD is still unstable or requirements are unresolved; use prd-from-idea first. This skill produces the architectural envelope; downstream skills (rest-api-contract-design, spring-boot-service-scaffold, postgres-schema-and-migration) fill it with interfaces, schemas, and implementation.
---

# System Design from PRD

## When to use

Invoke when an approved PRD exists and implementation planning is about to begin.

Do not use when no PRD exists, requirements are still unstable, the user only wants implementation tasks, or architecture decisions are intentionally deferred.

## Inputs

Required:

- Approved `PRD.md`.

Optional:

- Existing architecture or system context.
- Team size and operational maturity.
- Infrastructure or deployment constraints.
- Security and compliance requirements.
- Traffic or load expectations.
- Budget constraints.
- Vendor preferences or restrictions.
- Reliability and SLO expectations.

## Operating rules

- Default to simplicity. Prefer modular monoliths, synchronous flows, and fewer moving parts unless PRD constraints justify distribution.
- Tie every architecture decision to a user need, scale requirement, reliability requirement, compliance requirement, or team constraint.
- Separate logical architecture from deployment topology. A bounded context is not automatically a service, and a queue is not a domain boundary.
- Challenge unrealistic assumptions, hidden operational burden, unclear ownership, inconsistent data models, and architecture that exceeds team maturity.
- Do not introduce microservices, Kafka, CQRS, event sourcing, service meshes, or multi-region complexity without explicit PRD justification.
- Every non-obvious decision needs an ADR with downsides and tradeoffs. Draft ADRs *as decisions are made*, not retroactively at the end — a decision and its ADR belong in the same beat of work.
- Failure modes must be specific to *this* design, not generic. Do not list queue backlog if there is no queue, model-provider failure if there is no model, or tenant isolation issues if there is no multi-tenancy. Each failure mode must name an actual component in the design.
- Recognize PRDs that legally omit sections (Why Now, Current Alternatives, Risks, Distribution) under `prd-from-idea`'s conditional-section rules. Do not flag legitimate omissions as PRD incompleteness; only flag missing decisions the design actually needs (primary user, core workflow, hard constraints).

## Progressive references

- Read `references/design-playbook.md` when identifying system goals, bounded contexts, components, data flow, data ownership, and persistence strategy.
- Read `references/architecture-tradeoffs.md` when choosing or critiquing architecture style, async boundaries, distribution, or scalability choices.
- Read `references/operational-and-security-review.md` when analyzing failure modes, observability, deployment burden, auth, compliance, tenant isolation, or sensitive data handling.
- Read `references/adr-guide.md` before writing ADRs or deciding which tradeoffs deserve ADRs.
- Read `references/system-design-quality-rubric.md` before finalizing and use it as the validation checklist.
- Use `assets/system-design.template.md` for `system-design.md`.
- Use `assets/adr.template.md` for each `adrs/000N-<slug>.md` file.
- Read `assets/system-design.example.md` and `assets/adr.example.md` before drafting if you need a concrete style and length anchor — they show what conditional-section omission, ADR cross-linking, and a tight internal-service design look like.

## Process

Progress:

ADRs are drafted *inline* as decisions are made (steps 3, 4, 5, 7, 8). Step 10 only consolidates numbering, status, and the ADR Index — it does not retrofit ADRs from prose.

- [ ] Step 1: Restate the PRD's system goals using only what the PRD contains: primary user, core workflow, constraints, success metrics, and any non-goals. Note explicit PRD omissions (e.g., Why Now omitted as foundational build) rather than treating them as gaps. Stop and ask only if a decision-shaping element is *missing* — no primary user, no core workflow, no hard constraints.
- [ ] Step 2: Identify bounded contexts with responsibilities, owned data, dependencies, and upstream/downstream interactions. Use domain language, not technology names.
- [ ] Step 3: Choose an architecture style and justify it against PRD constraints. Consider simpler alternatives and explain why they were chosen or rejected. **Draft the architecture-style ADR now.**
- [ ] Step 4: Define components with responsibilities, public interfaces, dependencies, inputs/outputs, persistence needs, consistency expectations, and scaling expectations. **Draft an ADR for any non-obvious component boundary decision (e.g., extracting a service, merging two contexts).**
- [ ] Step 5: Define data flow and ownership: entry points, request paths, async boundaries, persistence boundaries, source-of-truth ownership, retention, retries, idempotency, and reconciliation needs. **Draft ADRs for storage choice, consistency model, and any async/eventing decision.**
- [ ] Step 6: Identify failure modes for every major component in the design — specific to the chosen architecture, not a generic checklist. Include user impact, detection, recovery, and graceful degradation.
- [ ] Step 7: Review operational maturity requirements: observability, tracing, metrics, alerting, deployment, rollback, incident response, migrations, feature flags, secrets, and backfills. **Draft an ADR for any operational decision that adds durable burden (e.g., introducing feature flags, adopting a tracing vendor).**
- [ ] Step 8: Review security and compliance implications: auth, authorization, sensitive data, encryption, tenant isolation, abuse prevention, retention, deletion, auditability, and regulatory exposure. **Draft ADRs for auth model, tenant isolation strategy, and any retention/deletion decision with regulatory weight.**
- [ ] Step 9: Run a final architecture critique. Surface over-engineering, under-specified ownership, hidden coupling, distributed monolith risk, reliability gaps, and unnecessary infrastructure. Revise inline if needed.
- [ ] Step 10: Consolidate ADRs — assign sequential numbers, finalize statuses, ensure every ADR's Consequences section names downsides, and build the ADR Index. Generate `system-design.md` from `assets/system-design.template.md`, then validate all artifacts against `references/system-design-quality-rubric.md`. Revise until the checklist passes or explicitly note any unresolved gap.

## Outputs

- `system-design.md` containing: Overview, Architecture Style, Bounded Contexts, Components, Data Flow, Persistence Strategy, Failure Modes, Security and Compliance, Operational Considerations, and ADR Index.
- `adrs/000N-<slug>.md` files for non-obvious architecture decisions.

Output rules:

- Keep architecture decision-oriented, not infrastructure decorative.
- Document tradeoffs and downsides, not only the chosen path.
- Name boundaries and components by domain responsibility, not technology.
- Avoid speculative scalability planning unless the PRD requires it.
- Treat operational burden as part of the design, not a later implementation detail.

## Quality checks

- [ ] `references/system-design-quality-rubric.md` was loaded before finalizing.
- [ ] `system-design.md` follows `assets/system-design.template.md`.
- [ ] Every ADR follows `assets/adr.template.md`.
- [ ] Architecture style is justified against explicit PRD constraints.
- [ ] At least one simplification was surfaced, or the intentional simplicity of the design is explained.

## References

- `references/design-playbook.md`
- `references/architecture-tradeoffs.md`
- `references/operational-and-security-review.md`
- `references/adr-guide.md`
- `references/system-design-quality-rubric.md`
- `assets/system-design.template.md`
- `assets/adr.template.md`
- `assets/system-design.example.md`
- `assets/adr.example.md`
