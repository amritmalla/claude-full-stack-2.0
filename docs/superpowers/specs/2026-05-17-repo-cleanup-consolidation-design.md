# Repository Cleanup & Consolidation — Design

**Date:** 2026-05-17
**Status:** Approved (design)
**Scope:** Remove redundant files and consolidate overlapping docs. Scaffold/placeholder READMEs are explicitly **out of scope** (kept as-is — they encode intentional taxonomy/roadmap structure).

## Goal

Eliminate genuine duplication and dangling references without touching the skills taxonomy. Four independent workstreams, each leaving the repo with a single source of truth and no broken links.

## Workstreams

### 1. Remove shell wrapper scripts

`scripts/lint-markdown.sh` and `scripts/validate-skills.sh` are 5-line bash facades that just invoke `node scripts/lint_markdown.mjs` and `python3 scripts/validate_skills.py`. CI (`.github/workflows/ci.yml`) already calls the `.mjs`/`.py` directly, so the wrappers are unused by automation and can drift out of sync.

**Changes:**
- Delete `scripts/lint-markdown.sh`.
- Delete `scripts/validate-skills.sh`.
- Update live references to call the real commands directly (matching CI exactly):
  - `.github/PULL_REQUEST_TEMPLATE.md:10` → `python scripts/validate_skills.py`
  - `docs/skill-authoring-guide.md:65` → `python scripts/validate_skills.py`

**Out of scope / leave alone:** historical references under `docs/superpowers/plans/` and `docs/superpowers/specs/` (frozen artifacts).

### 2. Consolidate the philosophy docs

`docs/philosophy/` contains 4 evergreen conceptual essays (`full-stack-2.0.md`, `ai-native-engineering.md`, `operational-excellence.md`, `production-engineering.md`). `docs/philosophy.md` is stale v0.1 framing ("ships 12 skills", orders-api-only) that the repo (50+ skills) has outgrown. Neither is referenced anywhere live.

**Changes:**
- Review `docs/philosophy.md` for any still-true unique point; fold it into the relevant essay in `docs/philosophy/` if it adds value.
- Delete `docs/philosophy.md`.
- Add `docs/philosophy/README.md` — a short index linking the 4 essays.
- Add a link to `docs/philosophy/README.md` from the main `README.md` (so the philosophy is discoverable).

### 3. De-duplicate spec vs authoring guides (do NOT merge)

`SKILL_SPEC.md`/`WORKFLOW_SPEC.md` are normative contracts; `docs/skill-authoring-guide.md`/`docs/workflow-authoring-guide.md` are tutorials that explicitly cross-reference the specs ("For the formal contract, see SKILL_SPEC.md"). The contract/tutorial separation is intentional and must be preserved. The redundancy is that the guides **restate** normative content (the SKILL.md/WORKFLOW.md format block and the authoring-rules list).

**Changes:**
- In `docs/skill-authoring-guide.md`: remove the duplicated `SKILL.md` format block and any restated authoring-rules; replace with a one-line pointer to `SKILL_SPEC.md`. Keep the step-by-step walkthrough.
- In `docs/workflow-authoring-guide.md`: same treatment relative to `WORKFLOW_SPEC.md`.
- Specs remain the single source of truth for format and rules.

### 4. Finalize ROADMAP.md deletion

`ROADMAP.md` is already staged for deletion (`D ROADMAP.md`). The only **live** reference is `README.md:69` ("See [`ROADMAP.md`](ROADMAP.md) for the full release plan."). Historical references under `docs/superpowers/specs|plans/` are frozen artifacts and are left untouched.

**Changes:**
- Commit the `ROADMAP.md` deletion.
- Remove the dangling line at `README.md:69`. Do **not** repoint to `CHANGELOG.md` — the changelog is a history log, not a forward release plan, so it would mislead.

> Note: the surrounding "What's in v0.1, what's not" section of `README.md` is also stale (frontend/mobile skills now exist in-repo). Rewriting it is **out of scope** for this cleanup to avoid scope creep; flagged here for a future pass.

## Non-Goals

- No changes to scaffold/placeholder READMEs or the skills taxonomy.
- No rewrite of the stale README "v0.1" narrative beyond removing the broken ROADMAP link.
- No edits to frozen `docs/superpowers/` plans and specs.

## Verification

- `python scripts/validate_skills.py` passes.
- `node scripts/lint_markdown.mjs` passes (no broken internal links — specifically no dangling `ROADMAP.md` or `docs/philosophy.md` references).
- `python -m pytest` (`tests/test_repository_integrity.py`) passes.
- `grep` confirms zero live references to deleted files outside frozen `docs/superpowers/` artifacts.
