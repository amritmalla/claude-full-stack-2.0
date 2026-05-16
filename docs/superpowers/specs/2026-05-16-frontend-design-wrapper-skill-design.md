# frontend-design wrapper skill — design

> Status: approved
> Date: 2026-05-16

## Context

`architecture/frontend-architecture` repeatedly defers visual, component, and
interaction design to "the `frontend-design` skill", but no such skill exists in
this repository — the reference resolves only to the external superpowers
`frontend-design` skill. Downstream, `implementations/frontend/<ecosystem>`
design-system-and-accessibility archetypes wire tokens and primitives into real
framework code. There is a gap between "frontend application architecture
decided" and "design-system wired into a framework": the actual visual /
interaction / UX design work has no in-repo entry point.

This effort fills that gap with a thin wrapper skill. It does **not** add a
design-decision artifact, schema, or methodology of its own — the real design
work is delegated to the external `frontend-design` skill.

A second requested effort — a mobile layer (`mobile-architecture` domain plus an
`implementations/mobile/<ecosystem>` archetype set) — is explicitly **deferred**
to a separate later effort and is out of scope here.

## Decisions

| Decision | Choice |
|---|---|
| Sequencing | UI/UX design now; mobile deferred to a separate effort |
| Skill scope | Thin wrapper — pure delegation to the external `frontend-design` skill |
| Placement | `implementations/frontend/frontend-design/`, a cross-framework sibling of the per-ecosystem folders (`react/`, `vue/`, …) |
| Name | `frontend-design` (matches the existing references in `frontend-architecture`) |
| Tier | `SKILL.md`-only, matching the archetype-skill convention. No `references/`, `assets/`, `checklists/`, README, schema, or template |
| Artifact | None owned — produces only whatever the external skill produces |
| Input contract | Reads `frontend-architecture.md` if present and injects repo context; proceeds (noting absence) if missing |
| External-skill absence | Hard dependency — documented, no fallback path |
| Repo wiring | Repoint `frontend-architecture` references only; no README skills-table / ROADMAP edits |
| SKILL body shape | Approach A (context-injecting router) with a one-paragraph lifecycle note folded in |

## File layout

```
implementations/frontend/frontend-design/
└── SKILL.md          # only file
```

The folder name `frontend-design` is the skill identifier and MUST equal the
`name` field in the frontmatter.

## SKILL.md

### Frontmatter (load-bearing)

- `name: frontend-design`
- `description:` starts with "Use when"; triggers on visual / UI / component /
  interaction / UX / design-system-visual requests **within a
  claude-full-stack-2.0 project**; states that it delegates execution to the
  external superpowers `frontend-design` skill; negative-scopes away from
  frontend application architecture (use `frontend-architecture`) and from
  framework token-wiring / component codegen (use the
  `implementations/frontend/<ecosystem>` design-system-and-accessibility
  archetype). ≤ 1024 characters.

### Body sections

- **When to use** — visual / interaction / component / design-system-visual
  work, positioned after `frontend-architecture` and before the ecosystem
  design-system-and-accessibility archetype.
- **Dependency** — hard dependency on the external superpowers `frontend-design`
  skill. If it is not available, state that it is required and stop. No
  fallback, no inline design guidance.
- **Lifecycle position** — one paragraph: upstream is `frontend-architecture`
  (this skill consumes its design-system seam, accessibility posture, and
  performance budgets); downstream is the
  `implementations/frontend/<ecosystem>` design-system-and-accessibility
  archetype, which wires the resulting design into framework code.
- **Process** —
  1. Locate the product's `frontend-architecture.md`. If present, extract the
     design-system seam, accessibility posture, performance budgets, and
     brand / information-architecture inputs into a context block. If absent,
     note that explicitly and proceed.
  2. Invoke the external `frontend-design` skill, passing the assembled context
     block.
  3. Produce no repo artifact of its own.
- **Outputs** — none owned; whatever the external skill emits.
- **Quality checks** (binary) —
  - The external `frontend-design` skill was invoked.
  - A repo context block was assembled from `frontend-architecture.md`, or its
    absence was explicitly noted.
  - No repo artifact, schema, or template was fabricated by this skill.

## Repoint changes (wiring: references only)

In both `architecture/frontend-architecture/SKILL.md` and
`architecture/frontend-architecture/README.md`, change the prose references to
"the `frontend-design` skill" so they link, repo-relative, to
`../../implementations/frontend/frontend-design/SKILL.md` instead of implying an
external-only skill. No other files change.

Specifically:

- `architecture/frontend-architecture/SKILL.md` — the negative-scope sentence in
  *When to use* and the *References* line that says visual/component design
  lives in the `frontend-design` skill.
- `architecture/frontend-architecture/README.md` — the *Purpose* paragraph
  sentence that delegates visual and component design to the `frontend-design`
  skill.

No edits to the root `README.md` skills table, `ROADMAP.md`, or any frontend
index.

## Out of scope

- Mobile (`mobile-architecture` domain and `implementations/mobile/*`) —
  deferred to a separate later effort.
- Any new artifact, schema, standard, or template.
- README skills-table / ROADMAP registration of the new skill.
- Per-ecosystem (`react/`, `vue/`, …) changes.
- Fallback behavior when the external skill is absent.

## Quality bar (from SKILL_SPEC.md)

- Valid frontmatter: `name` equals the skill directory; `description` starts
  with "Use when"; ≤ 1024 chars.
- Quality-checks section is concrete and binary-verifiable.
- `SKILL.md` well under the ~400-line cap (this skill is short by design).
- 3 "should match" and 2 "should NOT match" trigger prompts supplied at
  implementation time for invocation verification.
