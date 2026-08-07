---
product: <kebab-case-slug>
status: draft
verdict: <proceed | proceed-with-pivot | not-yet | kill>
score: <0-100>
owner: <name or role; use "self" for solo/personal projects>
version: 0.1.0
last_reviewed: YYYY-MM-DD
---

# Validation Brief — <Product Name>

> Conforms to [standards/validation-brief-schema](../../../../standards/validation-brief-schema/README.md).
>
> **Evidence tags are mandatory.** Tag every substantive claim `[assumed]`, `[researched]`, or `[tested]`. Untagged claims score as `assumed`.
>
> **Required sections:** Problem Statement, Value Hypothesis, Current Alternatives, Market Sizing, Value Proposition, Pricing and Willingness to Pay, Channel and CAC, Unit Economics, Evidence Log, Scoring, Verdict.
>
> **Conditional sections:** Pivot (required for `proceed-with-pivot`), Experiments To Run (required for `not-yet`), Regulatory and Compliance, Team-Market Fit. Omit with a one-line rationale under `## Omitted sections`.

## Problem Statement

[Customer, pain, frequency, current cost. Name any of the four that is unknown rather than inventing it.]

## Value Hypothesis

> If [customer] can [capability], they will [measurable change], because [mechanism].

**Riskiest assumption:** [the one whose failure kills the idea fastest]

## Current Alternatives

[At least three. One must be the status quo.]

| Alternative | What it costs them | Why they tolerate it | What would make them switch |
|---|---|---|---|
| <name> | <cost> | <reason> | <trigger> |

## Market Sizing

[Bottom-up only. Show the arithmetic. No top-down TAM.]

```text
<reachable accounts> x <realistic ACV> x <attainable share> = <figure>
```

[Source and evidence tier for each factor.]

## Value Proposition

> For [customer] who [pain], [product] is a [category] that [key benefit], unlike [named alternative], which [specific shortfall].

| Claim | Defensible or copyable | Why |
|---|---|---|
| <claim 1> | <tag> | <reason> |
| <claim 2> | <tag> | <reason> |
| <claim 3> | <tag> | <reason> |

## Pricing and Willingness to Pay

**Model:** [seat / usage / flat / hybrid] — [why this model]
**Price point:** [figure]
**WTP signal:** [what supports this price] `[tier]`

## Channel and CAC

**Channel:** [specific channel, not "marketing"]

```text
ACV                          = <figure>
Gross-margin ACV             = <figure>
CAC ceiling (12-mo payback)  = <figure>
```

[Whether this channel plausibly acquires a customer under that ceiling, and what supports that.]

## Unit Economics

| Metric | Value | Arithmetic |
|---|---|---|
| Payback | <months> | <shown> |
| Gross margin | <%> | <shown> |
| Tolerable churn | <% monthly> | <shown> |

## Evidence Log

**Interviews conducted:** [count — state zero if zero]

[Themes, saturation point, verbatim quotes.]

**Demand tests:**

| Test | Pass threshold (declared before) | Result | Tier |
|---|---|---|---|
| <method> | <threshold> | <result or "not run"> | <tier> |

## Scoring

| Dimension | Raw /5 | Weight | Tier | Multiplier | Weighted |
|---|---|---|---|---|---|
| Pain severity and frequency | | 25 | | | |
| Willingness to pay | | 20 | | | |
| Reachable channel | | 20 | | | |
| Differentiation | | 15 | | | |
| Unit economics | | 12 | | | |
| Team-market fit | | 8 | | | |
| **Total** | | | | | **<score>** |

**Floors:** [none triggered, or name the floor and its effect]

## Verdict

**<VERDICT>** — <score>/100

[Top 1-3 reasons.]

**Next action:** [exactly one]

## Pivot

[Required for `proceed-with-pivot`. The specific change, and which dimensions were re-scored.]

## Experiments To Run

[Required for `not-yet`. Each attacks the riskiest assumption first.]

| Experiment | Method | Sample | Cost | Duration | Pass threshold |
|---|---|---|---|---|---|
| <name> | <method> | <n> | <cost> | <time> | <threshold> |

## Regulatory and Compliance

[Include when the buyer's industry constrains the product. Otherwise omit.]

## Team-Market Fit

[Include when the team has unusual advantage or gaps. Otherwise omit.]

## Omitted sections

[Each conditional section omitted, with a one-line rationale. Remove this heading if all are present.]
