# saas-idea-validation — Design

**Date:** 2026-08-07
**Status:** approved
**Scope:** One new architecture skill, one new standard, and the registration and handoff edits required to wire them in.

## Problem

`skills/architecture/idea-development` is the repository's only product-idea skill. Its Validation phase is three steps: document assumptions and risks, test the path to users, and pass a **credibility gate** that resolves to proceed / narrow / abandon on unaided judgment.

That gate has no rubric, no evidence model, and no artifact of its own. Nothing distinguishes a belief the founder asserted from one they researched or tested, so a confidently-stated idea passes as easily as a validated one. Validation reasoning is never written down — it dissolves into `PRD.md`, which is a build specification, not a kill/pivot decision record.

For commercial SaaS specifically, the gate omits the dimensions that decide viability: pricing and willingness to pay, CAC ceiling implied by the acquisition channel, payback period, gross margin, and tolerable churn.

## Solution

A new sibling skill, `skills/architecture/saas-idea-validation`, that owns the validate-or-kill decision and emits its own artifact. It runs **before** `idea-development` and gates it: only a `proceed` or `proceed-with-pivot` verdict unlocks PRD work.

The two skills split cleanly. `saas-idea-validation` answers *should this be built at all* and produces `validation-brief.md`. `idea-development` answers *what exactly is v1* and produces `PRD.md`. Neither re-derives the other's work.

### Why not extend idea-development

Folding validation in would roughly double a skill already at twelve steps, mix two audiences (kill/pivot vs. build-spec) in one artifact, and make validation impossible to run standalone against an idea that already has a PRD. `SKILL_SPEC.md` rule 6 — one skill, one repeatable job — points the same way.

## Scoring model

Six weighted dimensions, each scored 0–5, each multiplied by the evidence tier standing behind it.

| Dimension | Weight | Scores |
|---|---|---|
| Pain severity and frequency | 25 | How costly and how often; whether anyone owns the problem |
| Willingness to pay / budget authority | 20 | Whether a budget exists and who signs |
| Reachable acquisition channel | 20 | Whether a channel exists that reaches buyers at tolerable cost |
| Differentiation vs. current alternatives | 15 | Whether the value proposition survives contact with incumbents |
| Unit-economics plausibility | 12 | Whether payback, margin, and churn tolerance close |
| Team–market fit and operational burden | 8 | Whether this team can build and run it |

### Evidence multipliers

| Tier | Multiplier | Qualifies as |
|---|---|---|
| `assumed` | ×0.4 | Stated belief; no external input |
| `researched` | ×0.7 | Desk evidence — competitor pricing pages, review mining, search volume, public benchmarks, analyst data |
| `tested` | ×1.0 | Primary evidence — target-user interviews, fake-door conversion, LOI or prepay, concierge delivery |

**This is the load-bearing mechanic.** An idea supported only by assertion caps at 40/100 and can never reach Proceed. Evidence, not conviction, moves the score.

### Verdict bands

| Score | Verdict | Meaning |
|---|---|---|
| ≥ 70 | `proceed` | Unlocks `idea-development` |
| 50–69 | `proceed-with-pivot` | Name the specific pivot; re-score the changed dimensions |
| 30–49 | `not-yet` | Run the named experiments and return with evidence |
| < 30 | `kill` | State the reasons plainly and stop |

### Hard floors

Floors override the total. Either condition caps the verdict at `not-yet` regardless of score:

- Pain severity raw score < 3/5
- Reachable channel raw score < 2/5

This blocks the failure mode where strong economics and a clever solution paper over a problem nobody has, or a product nobody can be sold to.

### Interview gate

Fewer than 10 target-user interviews caps **pain severity** and **willingness to pay** at the `researched` multiplier. With both capped, the arithmetic ceiling is ~68/100 — under the 70 threshold. No idea reaches `proceed` without primary conversations.

Interviews follow Mom Test discipline: ask about past behavior and actual spend, never about hypothetical interest. Record themes, the saturation point, and verbatim quotes.

## Process — 5 phases, 13 steps

**Phase 1 — Frame** (steps 1–2)
1. Problem statement: customer, pain, frequency, current cost of the pain.
2. Falsifiable value hypothesis and the single riskiest assumption.

**Phase 2 — Market** (steps 3–5)
3. Current-alternatives teardown, including status quo and spreadsheets.
4. Bottom-up market sizing. Top-down TAM is rejected.
5. Value proposition: one sentence plus three differentiation claims, each tagged defensible or copyable.

Step 5 is authored *after* step 3 so the claim is written against named competitors rather than in a vacuum.

**Phase 3 — Economics** (steps 6–8)
6. Pricing hypothesis (seat / usage / flat / hybrid) and willingness-to-pay signal.
7. Channel viability and the CAC ceiling it implies.
8. Unit-economics sanity: payback months, gross margin, tolerable churn.

Channel sits with economics, not market research, because CAC is a channel property — assessing a channel apart from what a customer is worth is the wrong seam.

**Phase 4 — Evidence** (steps 9–11)
9. 10–20 problem interviews with Mom Test discipline.
10. Demand test with a pre-declared pass threshold: landing page, fake door, LOI, or concierge.
11. Tag every claim in the brief with its evidence tier.

**Phase 5 — Verdict** (steps 12–13)
12. Score six dimensions, apply multipliers and floors.
13. Emit `validation-brief.md` with verdict and the single next action.

## Files

### New

```text
skills/architecture/saas-idea-validation/
  SKILL.md
  references/validation-playbook.md              # framing, desk research, interviews, demand tests, evidence tiers
  references/saas-economics-patterns.md          # pricing, CAC/LTV, payback, churn, motion, critique patterns
  references/validation-scoring-rubric.md        # dimensions, weights, multipliers, floors, verdict bands
  references/validation-brief-quality-rubric.md  # artifact and process checks before emitting
  assets/validation-brief.template.md
  assets/validation-brief.example.md
standards/validation-brief-schema/README.md
```

Two rubrics, because they answer different questions: *is the idea good* (scoring) versus *is the brief well-formed* (quality). Merging them would bury the scoring method inside a checklist.

Artifact location: `docs/product/<slug>/validation-brief.md`, alongside `PRD.md`.

### Modified

| File | Change |
|---|---|
| `skills/architecture/idea-development/SKILL.md` | Optional `validation-brief.md` input; steps 6–7 import a `proceed` brief instead of re-deriving; standalone path preserved for non-SaaS ideas |
| `skills/architecture/idea-development/references/prd-quality-rubric.md` | Check that assumptions marked validated cite the brief's evidence tier |
| `standards/prd-schema/README.md` | validation-brief noted as optional upstream input; anti-pattern for `validated` assumptions with no cited evidence |
| `README.md` | Row in the skill table under Idea |
| `docs/architecture/registry.md` | New domain section; idea-development gains an upstream link |
| `docs/skill-authoring-guide.md` | Domain list |
| `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json` | Skill arrays, kept aligned |
| `workflows/idea-to-production-full-stack/WORKFLOW.md` | Conditional first step in Phase 1, commercial SaaS only |

The Flutter workflow is left unchanged.

## Non-goals

- **MVP build.** Handled by `idea-development` → `system-design` → implementation skills.
- **Post-launch learn-and-iterate.** No home in this repo today; deliberately not added here, and not folded into this skill.
- **Non-SaaS idea types.** Marketplace, consumer, and internal-tool ideas fall back to `idea-development`. The SaaS commitment is what makes the economics guidance sharp.
- **Automated research.** The skill directs the user to evidence; it does not scrape competitors or run experiments.

## Verification

- `python scripts/validate_skills.py`
- `python -m pytest`
- Frontmatter `name` matches the directory; `description` starts with "Use when" and stays well under 300 characters per repository preference.
- All local markdown links resolve.
- `SKILL.md` under 400 lines.
- Three should-match and two should-not-match trigger prompts recorded for the PR.
