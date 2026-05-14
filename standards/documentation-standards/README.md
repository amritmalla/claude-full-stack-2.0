# documentation-standards

Documentation contract for every artifact in this repository.

## Required files per skill

Every skill (capability skill, implementation skill, pattern skill, workflow skill) MUST contain:

```
<skill>/
├── SKILL.md             # entry point with frontmatter
├── README.md            # human-facing overview (optional if SKILL.md is sufficient)
├── references/          # progressively-loaded playbooks
├── assets/              # templates, schemas, examples consumed by the skill
└── checklists/          # gating checklists referenced by SKILL.md (when relevant)
```

Capabilities MAY additionally contain `principles.md`, `decision-frameworks/`, `anti-patterns/`.

## SKILL.md structure

Required sections, in order:

1. **Frontmatter** (`name`, `description` starting with "Use when").
2. **Title** (`# Title Case Name`).
3. **When to use** — single paragraph naming inputs and trigger conditions.
4. **Inputs** — Required vs Optional bullet lists.
5. **Operating rules** — non-negotiable behavior constraints.
6. **Progressive references** — pointer list explaining when to load each `references/*.md`.
7. **Output contract** — what the skill produces, including file paths and schemas.
8. **Gates** — checklists that must pass before output is considered complete.

## Progressive disclosure

`SKILL.md` is loaded eagerly by the agent matcher. Heavy procedural detail lives in `references/` and is loaded only when needed. Keep `SKILL.md` under 200 lines.

## Cross-references

Use repo-relative markdown links: `[api-standards](../../standards/api-standards/README.md)`. Never absolute paths.

## Status markers

A skill in progress MUST declare status near the top:

```markdown
> Status: scaffold | draft | beta | stable
```

`scaffold` = directory exists, no usable content. `draft` = usable but unreviewed. `beta` = reviewed, may change. `stable` = production-ready, breaking changes require deprecation notice.

## Diagrams

Architecture diagrams: prefer Mermaid (rendered inline) over external image files. PNG/SVG allowed only when Mermaid is insufficient; place under `assets/diagrams/`.

## Anti-patterns

- Burying trigger conditions inside prose — they belong in "When to use".
- Inlining 500-line playbooks into `SKILL.md`. Move them to `references/`.
- Using emoji or decorative formatting in normative documents.
- Documenting "what the code does" — link to the code; document *why* and *when to use*.
