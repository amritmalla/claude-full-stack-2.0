# architecture-pattern-schema

Canonical structure for the reference docs under `architecture-patterns/<name>/README.md`. These are decision-oriented reference pages — not invocable skills. Skills cite them through `Compatible patterns:` links to give architectural context.

## Scope

Applies to every `architecture-patterns/<name>/README.md`. A pattern doc is concise (target ~1 page): enough to decide whether the pattern fits and what it costs, not a tutorial.

## File layout

```text
architecture-patterns/<name>/
└── README.md      # required; the only file, conforming to this schema
```

`<name>` is lowercase, hyphen-separated, and the H1 title matches it. No YAML frontmatter (these docs are not loaded by the `Skill` tool and are not scanned by `scripts/validate_skills.py`).

## Required sections

Every pattern doc has exactly these H2 sections, in order:

1. `## Summary` — one paragraph stating what the pattern is.
2. `## Problem & forces` — the problem it solves and the forces/constraints that make it appropriate.
3. `## When to use / When not to use` — explicit signals in both directions, as two bulleted lists.
4. `## Structure` — components, boundaries, and data/control flow. Include a small fenced text diagram.
5. `## Key tradeoffs` — what you gain versus what you pay (complexity, operational cost, consistency, latency).
6. `## Failure modes & mitigations` — common ways the pattern goes wrong and how to prevent each.
7. `## Related skills & patterns` — links to relevant `skills/architecture/` skills and composing or conflicting `architecture-patterns/`.

## Rules

1. **Decision-oriented, not encyclopedic.** Every section helps a reader choose or reject the pattern. Cut history and vendor specifics.
2. **Both directions are mandatory.** "When not to use" and "Failure modes" are required, not optional — a pattern doc that only sells the pattern is incomplete.
3. **Cross-links resolve.** Every link in "Related skills & patterns" points at a path that exists. Relate patterns both ways (if A links B as composing, B links A).
4. **No scaffold placeholders.** A doc either conforms fully or is not merged. `> Status: scaffold.` must not appear.
5. **Template parity.** New patterns start from [`templates/pattern-template`](../../templates/pattern-template/README.md).

## Quality bar

- All seven sections present, in order, non-empty.
- "When to use / When not to use" and "Failure modes & mitigations" each list at least two concrete items.
- "Structure" contains a fenced diagram.
- Every cross-link target exists; related patterns reciprocate.
- Markdown lints clean.
