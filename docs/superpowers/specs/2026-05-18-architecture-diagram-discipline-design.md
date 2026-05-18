# Architecture Diagram Discipline — Schema + Rubric Strengthening

- Date: 2026-05-18
- Status: approved (brainstorming complete)
- Area: `standards/architecture-schema`, `skills/architecture/*/references/*-quality-rubric.md`

## Goal

Close the audited gap where architecture diagrams have a mandated *format*
(Mermaid) but no enforced *presence* or *consistency with prose*. A
`system-design.md` can currently ship with no diagrams, or with a Mermaid graph
that contradicts its `## Components` / `## Bounded Contexts` sections, and every
quality-rubric passes.

Outcome: the schema requires specific diagrams on `system-design.md` and a
bidirectional diagram–prose consistency invariant; the validation rubrics
enforce it (full check in the system-design rubric, a scoped consistency line in
the 10 diagram-producing domain rubrics).

## Audit findings (why this is needed)

- `architecture-schema` §Diagrams (one sentence) mandates Mermaid format only.
- The only adjacent anti-pattern ("hand-drawn images … cannot be diffed") is
  about diffability, not semantic correctness or presence.
- SKILL.md Outputs list expected diagrams but softly (backend allows "sequence
  diagrams **or** numbered flow narratives").
- **Zero** mentions of "diagram"/"mermaid" across all ~13 architecture
  quality-rubrics and all playbooks — presence and consistency are unenforced.

## Decisions (locked in brainstorming)

- **Required diagrams: envelope-only.** Only `system-design.md` has a hard
  requirement. Other architecture docs keep their SKILL-listed topology diagram
  as conditional ("include when material"), omitted with a one-line rationale
  under `## Omitted sections` — same conditional-omission rule as sections.
- **Consistency rule: bidirectional, section-anchored.** (1) No phantom nodes —
  every diagram node maps to a named element in prose. (2) Completeness — every
  `## Bounded Contexts` entry appears in the context / bounded-context diagram.
  Anchored to sections that always exist in `system-design.md`, so it is
  checkable by reading.
- **Rollout: full in system-design, light elsewhere.**
  `system-design-quality-rubric` gets the full check; the 10 diagram-producing
  domain rubrics get one scoped consistency line; `idea-development` (PRD) and
  `operations` are excluded.
- **Execution: schema-first (Approach A).** Edit the authoritative schema
  first, then mirror into the rubrics. Single author, sequential — the edits
  are small and consistency-sensitive, not large independent units.
- **No separate implementation plan.** Per standing preference, implement
  directly from this approved spec; writing-plans is skipped.

## Change 1 — `standards/architecture-schema/README.md`

Replace the current one-sentence `## Diagrams` section with:

> ## Diagrams
>
> Use Mermaid (`graph`, `flowchart`, `sequenceDiagram`) inline. PNG/SVG only
> when Mermaid is insufficient; place under `assets/diagrams/`.
>
> `system-design.md` MUST contain at least:
>
> - a **context / bounded-context diagram** showing the system's bounded
>   contexts and their dependencies, and
> - a **primary-workflow diagram** (data-flow or sequence) for the core
>   workflow named in the PRD.
>
> Other architecture documents include the topology diagram their authoring
> skill's Outputs names *when it is material*; when omitted, list it under
> `## Omitted sections` with a one-line rationale (same conditional-omission
> rule as sections).
>
> **Diagram–prose consistency (required):**
>
> - Every node in a diagram MUST correspond to a named element in the
>   document's prose (bounded context, component, datastore, or actor present
>   in the relevant section). No phantom nodes.
> - Every entry in `## Bounded Contexts` MUST appear in the context /
>   bounded-context diagram. Diagram and prose cannot disagree.

Add to the `## Anti-patterns` list, after the hand-drawn-images bullet:

> - Diagram that names a component or context absent from the prose, or a
>   `## Bounded Contexts` entry missing from the context diagram — diagram and
>   prose must agree.

## Change 2 — `system-design-quality-rubric.md` (full check)

Append to the end of the `## Required checks` list (before `## Failure
handling`):

> - [ ] Required diagrams are present: a context / bounded-context diagram and
>   a primary-workflow (data-flow or sequence) diagram, per
>   `architecture-schema` §Diagrams.
> - [ ] Diagram–prose consistency holds: no diagram node is absent from the
>   prose, and every `## Bounded Contexts` entry appears in the context /
>   bounded-context diagram.

## Change 3 — 10 domain rubrics (scoped line)

Add one checkbox to each, in the existing checklist style of that file:

> - [ ] Any diagram present is prose-consistent: no node references an element
>   absent from this document; if this domain's primary topology diagram (per
>   its authoring skill's Outputs) is omitted, the omission is stated with a
>   rationale.

Target files:

- `skills/architecture/backend-architecture/references/backend-architecture-quality-rubric.md`
- `skills/architecture/data-architecture/references/data-architecture-quality-rubric.md`
- `skills/architecture/frontend-architecture/references/frontend-architecture-quality-rubric.md`
- `skills/architecture/infrastructure-platform/references/platform-architecture-quality-rubric.md`
- `skills/architecture/mobile-architecture/references/mobile-architecture-quality-rubric.md`
- `skills/architecture/ai-native-engineering/references/ai-architecture-quality-rubric.md`
- `skills/architecture/security/references/security-architecture-quality-rubric.md`
- `skills/architecture/performance/references/performance-architecture-quality-rubric.md`
- `skills/architecture/reliability/references/reliability-architecture-quality-rubric.md`
- `skills/architecture/quality-engineering/references/testing-strategy-quality-rubric.md`

Excluded (untouched): `idea-development` (prd-quality-rubric),
`operations` (operations-quality-rubric).

## Execution order (Approach A)

1. Edit `standards/architecture-schema/README.md` (Change 1).
2. Edit `system-design-quality-rubric.md` (Change 2).
3. Edit the 10 domain rubrics (Change 3).

## Verification

- Schema §Diagrams contains the required-diagram text and the bidirectional
  consistency rule; the new Anti-pattern bullet is present.
- All 11 target rubrics (system-design + 10 domain) contain the new diagram
  check; wording matches this spec.
- `prd-quality-rubric.md` and `operations-quality-rubric.md` are confirmed
  untouched.
- No `SKILL.md` or playbook changed.

## Out of scope

- No new skill (the audit concluded a standalone mermaid skill is low value).
- No changes to SKILL.md Outputs or playbooks; the backend "or numbered flow
  narratives" waiver is left as-is (not part of the agreed scope).
- No automated/CI diagram linting — the rubrics are read-and-judge checklists.
- PRD and operations artifacts are not in scope.
