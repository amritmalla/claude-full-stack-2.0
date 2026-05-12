---
name: system-design-from-prd
description: Use when an approved PRD exists and the team needs a system design
  document before scaffolding any code. Produces a component diagram, bounded
  contexts, technology choices, failure modes, and ADRs for non-obvious decisions.
---

# System Design from PRD

## When to use

Invoke when a PRD is approved and the next step is choosing an architecture style, identifying components, and capturing the trade-offs in ADRs. Do not invoke for greenfield architecture without a PRD — use `prd-from-idea` first.

## Inputs

- An approved `PRD.md` (problem, users, scope, non-goals, metrics).
- (Optional) Existing system context, constraints, target deployment environment.

## Process

1. Identify bounded contexts implied by the PRD's scope. Name each.
2. Choose an architecture style (monolith, modular monolith, microservices, serverless). Justify against the PRD's non-functional requirements.
3. Draft a component diagram: components, their responsibilities, and their interfaces.
4. For each component, list its data inputs, outputs, and persistence needs.
5. Identify failure modes: for each component, what can fail and how the system degrades.
6. List every non-obvious decision and write an ADR for it under `adrs/000N-<slug>.md` using the standard ADR template (Status, Context, Decision, Consequences).
7. Emit `system-design.md` with sections: Overview, Components, Data Flow, Failure Modes, ADR Index.

## Outputs

- `system-design.md`.
- `adrs/0001-*.md`, `adrs/0002-*.md`, … (one per non-obvious decision).

## Quality checks

- [ ] Each component has a one-sentence responsibility statement.
- [ ] Each component has at least one listed failure mode.
- [ ] Architecture style choice references at least one PRD non-functional requirement.
- [ ] Every ADR has Status, Context, Decision, Consequences.
- [ ] No component is named after a technology (e.g., "RedisService"); names reflect domain responsibility.

## References

(None in v0.1.)
