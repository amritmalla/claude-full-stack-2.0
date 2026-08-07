---
name: saas-idea-validation
description: Use when a SaaS product idea needs validating, sizing, pricing, or a kill/pivot decision before any PRD or build work. Produces an evidence-scored validation brief with a verdict.
---

# SaaS Idea Validation

## When to use

Invoke when someone has a commercial software product idea and needs to know whether it is worth building — before scoping v1, writing a PRD, or designing anything. Typical triggers: "is this idea any good", "how do I validate this", "should I build this", "what should I charge", "how big is this market", "am I wasting my time".

Do not use for: scoping a v1 or writing a PRD (use `idea-development`), validating a feature inside a product that already has customers, marketplace / consumer / internal-tool ideas where SaaS economics do not apply (use `idea-development`), or post-launch iteration.

This skill decides **whether to build**. `idea-development` decides **what v1 is**. Run this first; its verdict gates that skill.

## Inputs

Required:

- A 1-5 sentence description of the SaaS idea.

Optional:

- Target customer segment, company size, or industry.
- Any evidence already gathered: interviews, waitlist numbers, competitor research, pilot conversations.
- Pricing intuition or comparable products.
- Team background relative to this market.
- Regulatory or compliance context.

## Operating rules

- **Evidence outranks conviction.** Every substantive claim carries an evidence tier (`assumed`, `researched`, `tested`). Confidence in the user's voice is not evidence. Tag it `assumed` and move on.
- **Never invent evidence.** If the user has not talked to customers, the pain claim is `assumed`. Do not manufacture plausible-sounding market data, competitor pricing, or conversion benchmarks. If a number is needed and unknown, say it is unknown and name how to get it.
- **Size bottom-up only.** Reachable accounts × realistic ACV × attainable share. Reject top-down TAM framing whenever the user offers it.
- **Ask no more than three related questions at once**, each with a recommended default and rationale.
- **Be willing to say kill.** A skill that never returns `kill` is worthless. If the evidence says the idea is not viable, say so plainly, give the top reasons, and stop.
- **Do not soften a verdict to be encouraging.** Recommend the cheapest experiment that could change the answer instead.
- Score before writing the verdict, never the reverse.

## Progressive references

- Read `references/validation-playbook.md` when framing the problem, running the market teardown, sizing, designing interviews, or designing demand tests.
- Read `references/saas-economics-patterns.md` when working pricing, CAC, payback, margin, churn, or sales motion, and when critiquing SaaS-specific failure patterns.
- Read `references/validation-scoring-rubric.md` before scoring. It is authoritative for dimensions, weights, multipliers, floors, and verdict bands.
- Read `references/validation-brief-quality-rubric.md` before emitting the brief and use it as the validation checklist.
- Read `assets/validation-brief.example.md` for a concrete style and length anchor.

## Process

Five phases, thirteen steps. Do not score before Phase 4 is honestly recorded, including when the answer is "no evidence gathered".

### Phase 1 — Frame

- [ ] Step 1. Write the problem statement: which customer, what pain, how often it occurs, and what it costs them today in money, time, risk, or lost revenue. If any of the four is unknown, name it as unknown rather than inventing it.
- [ ] Step 2. State the value hypothesis as one falsifiable sentence, then name the **single riskiest assumption** — the one whose failure kills the idea fastest.

### Phase 2 — Market

- [ ] Step 3. Tear down current alternatives. List at least three, one of which must be the status quo (spreadsheet, manual process, doing nothing). For each: what it costs, why buyers tolerate it, and what would make them switch.
- [ ] Step 4. Size the market bottom-up: reachable accounts × realistic ACV × attainable share, with the arithmetic shown. Reject top-down TAM.
- [ ] Step 5. Write the value proposition: one sentence, plus three differentiation claims. Tag each claim `defensible` or `copyable`. If all three are copyable, say so — it is a scoring signal, not a failure to hide.

### Phase 3 — Economics

- [ ] Step 6. Choose a pricing model (seat / usage / flat / hybrid) and a price point. State the willingness-to-pay signal behind it and its evidence tier.
- [ ] Step 7. Identify the acquisition channel and derive the CAC ceiling the pricing implies. A channel with no plausible path to that ceiling is a scoring failure, not a detail.
- [ ] Step 8. Run the unit-economics sanity check: payback months, gross margin, tolerable churn. Show the arithmetic.

### Phase 4 — Evidence

- [ ] Step 9. Problem interviews. Target 10-20 target users. Use Mom Test discipline: ask about past behavior and actual spend, never about hypothetical interest. Record themes, the saturation point, and verbatim quotes. If the user has run none, record zero — do not skip the step.
- [ ] Step 10. Demand test. Design or record one: landing page, fake door, LOI, prepay, or concierge delivery. Every test states its pass threshold **before** the result.
- [ ] Step 11. Tag every claim across the brief with its evidence tier. Untagged claims count as `assumed`.

### Phase 5 — Verdict

- [ ] Step 12. Score all six dimensions per `references/validation-scoring-rubric.md`: raw score 0-5, evidence multiplier, weighted score. Apply the hard floors. Total to 0-100.
- [ ] Step 13. Generate `validation-brief.md` from `assets/validation-brief.template.md`. Validate against [standards/validation-brief-schema](../../../standards/validation-brief-schema/README.md) AND `references/validation-brief-quality-rubric.md`. State the verdict, the top 1-3 reasons, and the single next action.

## Outputs

- `validation-brief.md` at `docs/product/<slug>/validation-brief.md`. MUST conform to [standards/validation-brief-schema](../../../standards/validation-brief-schema/README.md), which is authoritative for frontmatter (`product`, `status`, `verdict`, `score`, `owner`, `version`, `last_reviewed`), the required/conditional section list, evidence-tier vocabulary, omission rules, and versioning. Use `assets/validation-brief.template.md` as the scaffold.
  - Required sections: Problem Statement, Value Hypothesis, Current Alternatives, Market Sizing, Value Proposition, Pricing and Willingness to Pay, Channel and CAC, Unit Economics, Evidence Log, Scoring, Verdict.
  - Conditional sections: Pivot, Experiments To Run, Regulatory and Compliance, Team-Market Fit.
- Verdict in the response: `proceed`, `proceed-with-pivot`, `not-yet`, or `kill`, with the top 1-3 reasons and the single next action.

Output rules:

- Lead with the verdict. Do not bury it under summary.
- Every claim carries an evidence tier.
- Report the score honestly even when it is low. Do not round up to clear a band.
- When the verdict is `not-yet`, the `Experiments To Run` section must name experiments that could plausibly change the outcome.
- When the verdict is `kill`, do not append encouragement or alternative business ideas unless asked.

## Handoff

- `proceed` or `proceed-with-pivot` → [idea-development](../idea-development/SKILL.md) consumes the brief and skips re-deriving persona, pain, alternatives, and channel.
- `not-yet` → the user runs the named experiments and re-invokes this skill with results.
- `kill` → stop. No PRD.

## Quality checks

- [ ] `references/validation-scoring-rubric.md` was loaded before scoring.
- [ ] `references/validation-brief-quality-rubric.md` was loaded before emitting the brief.
- [ ] `validation-brief.md` validates against [standards/validation-brief-schema](../../../standards/validation-brief-schema/README.md): frontmatter complete; all required sections present; conditional sections present or listed under `## Omitted sections` with rationale.
- [ ] Every substantive claim carries `assumed`, `researched`, or `tested`.
- [ ] Market sizing is bottom-up with arithmetic shown, and contains no top-down TAM.
- [ ] Interview count is stated explicitly, including when it is zero.
- [ ] Every demand test lists a pass threshold declared before its result.
- [ ] The scoring table totals to the `score` in frontmatter, and `verdict` matches the band including hard-floor overrides.
- [ ] Each of the three differentiation claims is tagged `defensible` or `copyable`.
- [ ] Unit economics show payback months, gross margin, and tolerable churn with arithmetic.
- [ ] The response states the verdict and one next action.

## References

- `references/validation-playbook.md`
- `references/saas-economics-patterns.md`
- `references/validation-scoring-rubric.md`
- `references/validation-brief-quality-rubric.md`
- `assets/validation-brief.template.md`
- `assets/validation-brief.example.md`
