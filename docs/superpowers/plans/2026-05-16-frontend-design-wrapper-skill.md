# frontend-design Wrapper Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a thin, pure-delegation `frontend-design` skill that fills the visual/UX-design gap `frontend-architecture` already references, and repoint those references in-repo.

**Architecture:** A single `SKILL.md` at `implementations/frontend/frontend-design/` — a cross-framework sibling of the per-ecosystem folders. It injects repo context from `frontend-architecture.md` and hard-delegates the actual design work to the external superpowers `frontend-design` skill. No artifact, schema, template, or fallback. Two prose references in `architecture/frontend-architecture` are repointed to resolve in-repo.

**Tech Stack:** Markdown only. Validation against `SKILL_SPEC.md` (frontmatter validity, ≤1024-char description, ≤~400-line SKILL.md, repo-relative link resolution, manual trigger-prompt invocation check).

**Spec:** [docs/superpowers/specs/2026-05-16-frontend-design-wrapper-skill-design.md](../specs/2026-05-16-frontend-design-wrapper-skill-design.md)

---

## File Structure

- **Create:** `implementations/frontend/frontend-design/SKILL.md` — the entire skill. One responsibility: trigger correctly, assemble repo context, delegate to the external `frontend-design` skill.
- **Modify:** `architecture/frontend-architecture/SKILL.md` — line 12 (When-to-use negative-scope sentence) and line 118 (References line).
- **Modify:** `architecture/frontend-architecture/README.md` — line 9 (Purpose paragraph).

The frontmatter `description` at `architecture/frontend-architecture/SKILL.md:3` is intentionally **not** changed: it is YAML trigger text, not a prose reference, and must stay link-free.

---

### Task 1: Author the frontend-design SKILL.md

**Files:**
- Create: `implementations/frontend/frontend-design/SKILL.md`

- [ ] **Step 1: Create the skill file with exact content**

Create `implementations/frontend/frontend-design/SKILL.md` with exactly:

```markdown
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
```

- [ ] **Step 2: Verify frontmatter validity**

Run: `powershell -Command "$f='implementations/frontend/frontend-design/SKILL.md'; $lines=Get-Content $f; $name=($lines | Select-String '^name:').ToString(); $desc=($lines | Select-String '^description:').ToString(); Write-Output $name; Write-Output ('desc-length=' + ($desc.Length)); Write-Output ('dir-matches=' + (Split-Path (Split-Path $f -Parent) -Leaf))"`

Expected: `name: frontend-design`; `desc-length=` a value well under 1024 (the `description:` line including prefix is ~760 chars); `dir-matches=frontend-design`. The `name` value MUST equal `frontend-design` and equal the directory name.

- [ ] **Step 3: Verify description starts with "Use when" and line count is within cap**

Run: `powershell -Command "$f='implementations/frontend/frontend-design/SKILL.md'; $d=(Get-Content $f | Select-String '^description: ').ToString(); Write-Output ('starts-ok=' + ($d -like 'description: Use when*')); Write-Output ('lines=' + (Get-Content $f).Count)"`

Expected: `starts-ok=True`; `lines=` a value under 400 (this skill is ~70 lines).

- [ ] **Step 4: Verify every repo-relative link resolves**

Run: `powershell -Command "cd implementations/frontend/frontend-design; foreach ($p in '../../../architecture/frontend-architecture/SKILL.md','../react/react-design-system-and-accessibility/SKILL.md') { Write-Output ($p + ' => ' + (Test-Path $p)) }"`

Expected: both lines end in `=> True`.

- [ ] **Step 5: Commit**

```bash
git add implementations/frontend/frontend-design/SKILL.md
git commit -m "feat(frontend): add thin frontend-design wrapper skill

Pure-delegation skill at implementations/frontend/frontend-design that
injects frontend-architecture.md context and hard-delegates design work
to the external superpowers frontend-design skill. No artifact, no
fallback. Implements the approved 2026-05-16 spec.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 2: Repoint frontend-architecture references in-repo

**Files:**
- Modify: `architecture/frontend-architecture/SKILL.md:12` and `:118`
- Modify: `architecture/frontend-architecture/README.md:9`

- [ ] **Step 1: Repoint the When-to-use sentence (SKILL.md line 12)**

In `architecture/frontend-architecture/SKILL.md`, replace this exact substring on line 12:

`when only visual or component design is needed (use \`frontend-design\`),`

with:

`when only visual or component design is needed (use [\`frontend-design\`](../../implementations/frontend/frontend-design/SKILL.md)),`

- [ ] **Step 2: Repoint the References line (SKILL.md line 118)**

In `architecture/frontend-architecture/SKILL.md`, replace this exact substring on line 118:

`Visual and component design lives in the \`frontend-design\` skill.`

with:

`Visual and component design lives in the [\`frontend-design\`](../../implementations/frontend/frontend-design/SKILL.md) skill.`

- [ ] **Step 3: Repoint the README Purpose paragraph (README.md line 9)**

In `architecture/frontend-architecture/README.md`, replace this exact substring on line 9:

`Visual and component design lives in the \`frontend-design\` skill;`

with:

`Visual and component design lives in the [\`frontend-design\`](../../implementations/frontend/frontend-design/SKILL.md) skill;`

- [ ] **Step 4: Verify the frontmatter description was NOT touched**

Run: `powershell -Command "$d=(Get-Content architecture/frontend-architecture/SKILL.md | Select-String '^description:').ToString(); Write-Output ('frontmatter-has-no-link=' + (-not ($d -match '\]\(')))"`

Expected: `frontmatter-has-no-link=True` (the YAML `description:` line must remain link-free).

- [ ] **Step 5: Verify the three new links resolve from frontend-architecture**

Run: `powershell -Command "Write-Output ('skill-link=' + (Test-Path architecture/frontend-architecture/../../implementations/frontend/frontend-design/SKILL.md))"`

Expected: `skill-link=True`.

- [ ] **Step 6: Verify exactly three prose references were repointed and no stray bare references remain**

Run: `powershell -Command "$s=Select-String -Path architecture/frontend-architecture/SKILL.md,architecture/frontend-architecture/README.md -Pattern 'frontend-design'; $s | ForEach-Object { Write-Output (\"{0}:{1}: {2}\" -f $_.Filename,$_.LineNumber,$_.Line.Trim()) }"`

Expected: 4 matches total — `SKILL.md:3` (frontmatter, unchanged, no link), `SKILL.md:12` (now linked), `SKILL.md:118` (now linked), `README.md:9` (now linked). Confirm lines 12, 118, and 9 each contain `](../../implementations/frontend/frontend-design/SKILL.md)` and line 3 does not.

- [ ] **Step 7: Commit**

```bash
git add architecture/frontend-architecture/SKILL.md architecture/frontend-architecture/README.md
git commit -m "docs(frontend): repoint frontend-design references in-repo

The frontend-design skill now exists at implementations/frontend/
frontend-design; resolve the prose references in frontend-architecture
to it. Frontmatter description left link-free by design.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 3: Trigger-prompt invocation verification (SKILL_SPEC quality bar)

**Files:** none modified — this is a manual verification task whose result goes in the PR description.

- [ ] **Step 1: Run the 3 "should match" prompts**

For each prompt below, confirm Claude would invoke `frontend-design` (the new skill), given a project that uses claude-full-stack-2.0:

1. "We have an approved frontend-architecture.md — now design the actual visual look and interaction patterns for the dashboard."
2. "Do the UI/UX design for the onboarding flow before we wire it into React."
3. "Turn our frontend architecture into a concrete component and visual design."

Expected: each should match `frontend-design`.

- [ ] **Step 2: Run the 2 "should NOT match" prompts**

1. "Decide our routing model, rendering strategy, and state tiers." → should match `frontend-architecture`, NOT `frontend-design`.
2. "Wire the design tokens and accessible primitives into our React components." → should match `react-design-system-and-accessibility`, NOT `frontend-design`.

Expected: neither matches `frontend-design`.

- [ ] **Step 3: Record results for the PR description**

Write the 3+2 prompts and observed invocation behavior into the PR description body when the branch is opened. No commit (no file change).

---

## Self-Review

**1. Spec coverage:**
- Thin wrapper SKILL.md at `implementations/frontend/frontend-design/` → Task 1.
- Frontmatter: name=dir, "Use when", ≤1024 → Task 1 Steps 2–3.
- Body sections (When to use / Dependency / Lifecycle / Inputs / Process / Outputs / Quality checks / References) → Task 1 Step 1.
- Hard dependency, no fallback → Dependency section in Task 1 content.
- Pure delegation, no artifact → Process Step 4 + Outputs + Quality checks.
- Repoint references only (SKILL.md ×2, README ×1; frontmatter untouched) → Task 2.
- SKILL_SPEC quality bar incl. 3+2 trigger prompts → Task 1 verifications + Task 3.
- Out of scope (mobile, schema, README/ROADMAP registration, per-ecosystem) → no tasks touch them. ✓

**2. Placeholder scan:** No TBD/TODO; full SKILL.md content and exact edit substrings are inline. ✓

**3. Type consistency:** Skill `name` is `frontend-design` everywhere; directory `implementations/frontend/frontend-design/`; link target `../../implementations/frontend/frontend-design/SKILL.md` from `architecture/frontend-architecture/` is consistent across Task 2 steps. ✓
