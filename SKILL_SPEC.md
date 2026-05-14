# Skill Specification

A skill is a single, repeatable engineering job that Claude can execute end-to-end. Skills in this repository follow Anthropic's official Claude Skills format so they are directly invocable by the `Skill` tool in Claude Code.

## File Layout

Each skill lives in a directory under either `capabilities/<capability>/<skill-name>/` (technology-agnostic) or `implementations/<category>/<ecosystem>/<skill-name>/` (ecosystem-specific). See [`docs/architecture/research.md`](docs/architecture/research.md) for the capabilities-vs-implementations distinction.

```
<capabilities|implementations>/.../<skill-name>/
├── SKILL.md           # required; the only file Claude reads by default
├── references/        # optional; on-demand deep-dive docs
├── assets/            # optional; templates and starter files the skill emits
└── checklists/        # optional; gating checklists referenced by SKILL.md
```

The directory name is the skill's identifier. It MUST be lowercase, hyphen-separated, and match the `name` field in `SKILL.md`'s frontmatter exactly.

## SKILL.md Format

```markdown
---
name: <kebab-case, matches directory name>
description: Use when <trigger>. <One-sentence outcome.>
---

# <Title Case Name>

## When to use
Trigger conditions; signals that this skill should be invoked.

## Inputs
What the user must supply.

## Process
Numbered steps Claude executes. Each step is a concrete action with a verifiable output.

## Outputs
Concrete artifacts the skill produces.

## Quality checks
Binary-verifiable conditions the output must satisfy.

## References
Optional links to `references/*.md` deep dives.
```

## Authoring Rules

1. **`description` is load-bearing.** It is the only text Claude reads to decide whether to invoke. It MUST start with "Use when", be ≤ 1024 characters, be specific enough to match real triggers, and generic enough to catch reasonable variants.
2. **`name` matches the directory name exactly.** Lowercase, hyphen-separated.
3. **`SKILL.md` is the only file Claude reads by default.** Files under `references/` load on demand when the skill body instructs Claude to read them.
4. **Skills are imperative recipes, not essays.** Every section answers "what does Claude do next?"
5. **Quality checks are binary-verifiable.** Never "ensure it's good." Always a pass/fail condition a human or Claude can confirm.
6. **One skill = one repeatable job.** If a skill produces two distinct outcomes, split it into two skills.

## Quality Bar

Every skill merged into this repository must pass:

- Valid frontmatter (`name` matches directory; `description` starts with "Use when"; ≤ 1024 chars).
- Author has invoked the skill end-to-end against the reference example and committed the output under `examples/spring-boot/orders-api/.skill-outputs/<skill-name>/`.
- Quality-checks section is concrete and binary-verifiable.
- Author supplies 3 "should match" and 2 "should NOT match" trigger prompts in the PR description and manually verifies Claude's invocation behavior on each.
- `SKILL.md` is ≤ ~400 lines; overflow moves to `references/`.
