---
name: frontend-design
description: Use when a claude-full-stack-2.0 project needs visual, UI, component, interaction, or UX design work — turning an approved frontend architecture into concrete visual and interaction design. This skill is a thin wrapper that injects repository context and delegates the actual design work to the external superpowers frontend-design skill. Do not use for frontend application architecture, routing, rendering, state, or data-flow decisions (use architecture/frontend-architecture); do not use for wiring design tokens or components into framework code (use the implementations/frontend/<ecosystem> design-system-and-accessibility archetype, for example react-design-system-and-accessibility).
---

# Frontend Design

## When to use

Invoke when a project needs visual, UI, component, interaction, or UX design — after `architecture/frontend-architecture` has produced a `frontend-architecture.md`, and before the `implementations/frontend/<ecosystem>` design-system-and-accessibility archetype wires the design into framework code.

Do not use for frontend application architecture, routing, rendering, state, or data-flow decisions (use [`architecture/frontend-architecture`](../../../architecture/frontend-architecture/SKILL.md)). Do not use for wiring design tokens or components into a specific framework (use that ecosystem's design-system-and-accessibility archetype).

## Dependency

This skill is a thin wrapper. The actual design work is performed by the external superpowers `frontend-design` skill, which is a hard dependency. If that skill is not available, state that it is required, do not attempt the design work inline, and stop. There is no fallback path.

## Lifecycle position

Upstream is [`architecture/frontend-architecture`](../../../architecture/frontend-architecture/SKILL.md): this skill consumes its design-system seam, accessibility posture, and performance budgets. Downstream is the `implementations/frontend/<ecosystem>` design-system-and-accessibility archetype, which wires the resulting design into framework code. This skill itself owns no artifact and produces only what the external skill produces.

## Inputs

Required:

- A design or UI request scoped to a project in this repository.

Optional:

- The product's `frontend-architecture.md` (design-system seam, accessibility posture, performance budgets, brand and information-architecture inputs).

## Process

- [ ] Step 1: Locate the product's `frontend-architecture.md`. If present, extract the design-system seam, accessibility posture, performance budgets, and brand / information-architecture inputs into a context block. If absent, note that explicitly and proceed.
- [ ] Step 2: Confirm the external superpowers `frontend-design` skill is available. If it is not, state that it is required and stop.
- [ ] Step 3: Invoke the external `frontend-design` skill, passing the assembled repo context block.
- [ ] Step 4: Do not produce any repository artifact of this skill's own.

## Outputs

None owned. The output is whatever the external `frontend-design` skill produces.

## Quality checks

- [ ] The external `frontend-design` skill was invoked.
- [ ] A repo context block was assembled from `frontend-architecture.md`, or its absence was explicitly noted.
- [ ] No repository artifact, schema, or template was fabricated by this skill.

## References

- Upstream: [`architecture/frontend-architecture`](../../../architecture/frontend-architecture/SKILL.md).
- Downstream: `implementations/frontend/<ecosystem>` design-system-and-accessibility archetype (e.g. [`react-design-system-and-accessibility`](../react/react-design-system-and-accessibility/SKILL.md)).
- Delegated execution: the external superpowers `frontend-design` skill.
