# Validation Brief Quality Rubric

Load before emitting `validation-brief.md`. Revise until each check passes or the unresolved gap is explicitly documented in the brief.

Two parts:

- **Artifact checks** — verifiable by reading `validation-brief.md` alone.
- **Process checks** — verifiable only from the conversation that produced it.

## Artifact checks (read validation-brief.md)

### Structure

- [ ] Frontmatter complete: `product`, `status`, `verdict`, `score`, `owner`, `version`, `last_reviewed`.
- [ ] All eleven required sections present.
- [ ] Conditional sections either present with content or listed under `## Omitted sections` with rationale.
- [ ] `Pivot` is present when `verdict: proceed-with-pivot`.
- [ ] `Experiments To Run` is present when `verdict: not-yet`.

### Evidence integrity

- [ ] Every substantive claim carries `assumed`, `researched`, or `tested`.
- [ ] No claim is tagged `tested` without a named source in the Evidence Log.
- [ ] Interview count is stated explicitly, including when it is zero.
- [ ] Interview findings quote users rather than paraphrasing them into agreement.
- [ ] Every demand test lists a pass threshold declared before the result.
- [ ] No fabricated market data, competitor pricing, or conversion benchmarks. Unknown numbers are named as unknown.

### Content

- [ ] Problem Statement names a specific customer, pain, frequency, and current cost — or marks any of the four unknown.
- [ ] Value Hypothesis is one falsifiable sentence, and exactly one riskiest assumption is named.
- [ ] Current Alternatives lists at least three, one of which is the status quo.
- [ ] Market Sizing is bottom-up with arithmetic shown, and contains no top-down TAM.
- [ ] Value Proposition names a specific alternative it is defined against.
- [ ] Each of the three differentiation claims is tagged `defensible` or `copyable`.
- [ ] Pricing names a model and a price point, with a WTP signal and its tier.
- [ ] CAC ceiling is a number derived from ACV and gross margin, not an assertion.
- [ ] Channel assessment is judged against that ceiling, not in isolation.
- [ ] Unit Economics shows payback months, gross margin, and tolerable churn, each with arithmetic.

### Scoring and verdict

- [ ] Scoring table lists all six dimensions with raw score, weight, evidence tier, and weighted score.
- [ ] Weighted values recompute correctly as `(raw / 5) x weight x multiplier`.
- [ ] The column totals to the `score` in frontmatter.
- [ ] `verdict` matches the score band, including any hard-floor override.
- [ ] Any triggered floor is named explicitly in the Verdict section.
- [ ] Verdict states the top 1-3 reasons and exactly one next action.

## Process checks (read the conversation)

- [ ] `validation-scoring-rubric.md` was loaded before any score was assigned.
- [ ] Scores were assigned before the verdict was written, not reverse-engineered from it.
- [ ] Every user-facing question included a recommended answer and rationale.
- [ ] Top-down TAM framing, if the user offered it, was rejected and replaced with bottom-up sizing.
- [ ] At least one substantive challenge was raised — weak pain, channel mismatch, margin problem, copyable differentiation, or hidden operational burden — or the brief explains why none applies.
- [ ] Claims the user asserted confidently were still tagged `assumed` when no evidence backed them.
- [ ] A `kill` or `not-yet` verdict was stated plainly, without softening it into encouragement.

## Failure handling

If a check fails:

1. Identify the missing evidence or the unsupported claim.
2. Ask the user a recommended-default question if it cannot be resolved from what they have said.
3. Downgrade the evidence tier rather than inventing support. A lower score with honest tags beats a higher score with invented ones.
4. Re-score after any tier changes, and re-check the verdict band and floors.

## The failure mode this rubric exists to prevent

A brief that reads as thorough, scores in the seventies, and is built entirely on confident assertion. Length is not evidence. The tags are what make the score mean anything — if every tag is `assumed`, the correct total is under 40 no matter how well-argued the prose is.
