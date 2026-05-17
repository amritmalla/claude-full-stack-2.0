# Architecture-Patterns Content — Design

**Date:** 2026-05-17
**Status:** Approved (design)
**Goal:** Replace the 10 empty `architecture-patterns/*` scaffold READMEs with consistent, decision-oriented reference content, governed by a normative schema and a fill-in template (matching the repo convention that every artifact type has a `standards/` schema + a `templates/` starter).

## Decisions locked

- 7-section pattern doc schema (below), approved.
- Normative schema lives in a new `standards/architecture-pattern-schema/README.md` (not template-only), consistent with how `standards/architecture-schema`, `standards/prd-schema`, etc. work.
- Scope: define structure, then author all 10 patterns in one pass.
- Depth: concise reference pages (~1 page each), not deep playbooks. These are "Compatible patterns" reference targets linked from skills, not invocable skills.

## Part A — Structure

### `standards/architecture-pattern-schema/README.md` (new)

Normative. Defines the required sections every `architecture-patterns/<name>/README.md` must contain, in order:

1. **Summary** — one paragraph: what the pattern is.
2. **Problem & forces** — the problem it solves and the constraints/forces that make it appropriate.
3. **When to use / When not to use** — explicit signals in both directions.
4. **Structure** — components, boundaries, data/control flow; a small text diagram.
5. **Key tradeoffs** — what you gain vs. what you pay (complexity, operational cost, consistency).
6. **Failure modes & mitigations** — common ways it goes wrong and how to prevent them.
7. **Related skills & patterns** — links to relevant `architecture/` skills and composing/conflicting `architecture-patterns/`.

Title is the pattern name as an H1 matching the directory. No YAML frontmatter (these are reference docs, not Skill-tool-invoked; `validate_skills.py` does not scan `architecture-patterns/`).

### `templates/pattern-template/README.md` (rewrite)

Replace the 2-line stub with a fill-in skeleton of the 7 sections plus one-line guidance per section. Directory name stays `pattern-template` (unambiguous under `templates/`; avoids collision with `architecture-template`).

## Part B — The 10 pattern docs

Each replaces its scaffold README with full schema-conformant content:

`microservices`, `modular-monolith`, `event-driven`, `cqrs`, `hexagonal-architecture`, `domain-driven-design`, `multi-tenant-saas`, `real-time-systems`, `serverless-platform`, `ai-rag-platform`.

Cross-links wired both ways where patterns relate, at minimum:

- `microservices` ↔ `modular-monolith` (the explicit "start here" tradeoff pair).
- `cqrs` ↔ `event-driven` (read-model projections fed by events).
- `domain-driven-design` ↔ `hexagonal-architecture` (bounded contexts realized via ports/adapters).
- `ai-rag-platform` → `event-driven` (ingestion/index-update pipeline).
- `real-time-systems` → `event-driven` (stream transport).

"Related skills" links point at existing `architecture/` domains (`system-design`, `backend-architecture`, `data-architecture`, `reliability`, `security`, `performance`, `ai-native-engineering`) and, where natural, the implementation skills that already cite the pattern.

## Part C — Governance + verification

- `CONVENTIONS.md`: note that `architecture-patterns/` docs conform to `standards/architecture-pattern-schema`.
- Confirm the existing skill→pattern links (the "Compatible patterns:" references) still resolve to the now-populated docs (no path change — content only).

### Verification

- `python scripts/validate_skills.py` passes (skill local-link validation still green; pattern targets now have real content).
- `python -m pytest` passes.
- `node scripts/lint_markdown.mjs` passes — schema, template, and all 10 docs lint clean with no broken internal links.
- `grep` confirms zero remaining `Status: scaffold` lines under `architecture-patterns/`.

## Non-Goals

- No new skills; patterns remain reference docs, not invocable skills.
- No frontmatter/CI validation for pattern docs (out of scope; could be a later schema-enforcement task).
- No changes to skills beyond confirming existing links resolve.
- Frozen `docs/superpowers/` artifacts untouched.
