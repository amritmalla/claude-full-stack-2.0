---
name: frontend-design
description: Use when a claude-full-stack-2.0 project needs visual, UI, component, interaction, or UX design work — turning an approved frontend architecture into concrete visual and interaction design. This skill is a router that injects repository context and asks which design generator to use: the external superpowers frontend-design skill, or Google Stitch via its official MCP. Do not use for frontend application architecture, routing, rendering, state, or data-flow decisions (use architecture/frontend-architecture); do not use for wiring design tokens or components into framework code (use the implementations/frontend/<ecosystem> design-system-and-accessibility archetype, for example react-design-system-and-accessibility).
---

# Frontend Design

## When to use

Invoke when a project needs visual, UI, component, interaction, or UX design — after `architecture/frontend-architecture` has produced a `frontend-architecture.md`, and before the `implementations/frontend/<ecosystem>` design-system-and-accessibility archetype wires the design into framework code.

Do not use for frontend application architecture, routing, rendering, state, or data-flow decisions (use [`architecture/frontend-architecture`](../../../architecture/frontend-architecture/SKILL.md)). Do not use for wiring design tokens or components into a specific framework (use that ecosystem's design-system-and-accessibility archetype).

## Generators

This skill does not perform design itself. It routes to one of two generators, chosen by the user each run:

- superpowers `frontend-design` — the external superpowers skill. Prerequisite: that skill is available in the session. Hard dependency for this path.
- Google Stitch — Google's official hosted Stitch MCP. Prerequisite: the Stitch MCP is configured in the session. Setup and operation live in `references/stitch-mcp.md`.

## Lifecycle position

Upstream is [`architecture/frontend-architecture`](../../../architecture/frontend-architecture/SKILL.md): this skill consumes its design-system seam, accessibility posture, and performance budgets. Downstream is the `implementations/frontend/<ecosystem>` design-system-and-accessibility archetype, which wires the resulting design into framework code. This skill owns no artifact and produces only what the chosen generator produces.

## Inputs

Required:

- A design or UI request scoped to a project in this repository.

Optional:

- The product's `frontend-architecture.md` (design-system seam, accessibility posture, performance budgets, brand and information-architecture inputs).

## Process

- [ ] Step 1: Locate the product's `frontend-architecture.md`. If present, extract the design-system seam, accessibility posture, performance budgets, and brand / information-architecture inputs into a context block. If absent, note that explicitly and proceed.
- [ ] Step 2: Present both generators and their prerequisites, and ask the user which generator to use for this design task. Do not pick a default.
- [ ] Step 3a: If the user chose superpowers `frontend-design`: confirm the external superpowers `frontend-design` skill is available. If it is not, state that it is required and stop. Otherwise invoke it, passing the assembled repo context block.
- [ ] Step 3b: If the user chose Google Stitch: load `references/stitch-mcp.md` and follow it, passing the assembled repo context block as the design brief source.
- [ ] Step 4: If the chosen generator's prerequisites are not present in the session, state the exact requirement (for Stitch, the setup command in `references/stitch-mcp.md`), then re-ask the generator choice or stop. Never silently fall back to the other generator.
- [ ] Step 5: Do not produce any repository artifact of this skill's own.

## Outputs

None owned. The output is whatever the chosen generator produces.

## Quality checks

- [ ] The user was presented the explicit choice between the two generators.
- [ ] The chosen generator's prerequisites were verified before proceeding.
- [ ] If Google Stitch was chosen, `references/stitch-mcp.md` was loaded.
- [ ] No repository artifact, schema, or template was fabricated by this skill.

## References

- Upstream: [`architecture/frontend-architecture`](../../../architecture/frontend-architecture/SKILL.md).
- Downstream: `implementations/frontend/<ecosystem>` design-system-and-accessibility archetype (e.g. [`react-design-system-and-accessibility`](../react/react-design-system-and-accessibility/SKILL.md)).
- Google Stitch path detail: [`references/stitch-mcp.md`](references/stitch-mcp.md).
- Delegated execution (superpowers path): the external superpowers `frontend-design` skill.
- Claude Design (Anthropic Labs) integration is deferred: it exposes no MCP or public API, only a one-directional Claude Code handoff bundle, so it cannot be driven from this skill.
