# validation-brief-schema

Canonical structure for the validation brief produced by [skills/architecture/saas-idea-validation](../../skills/architecture/saas-idea-validation/SKILL.md). The brief records the evidence behind a SaaS idea and the verdict that evidence supports. It is the optional upstream input to [prd-schema](../prd-schema/README.md).

## File location

`docs/product/<slug>/validation-brief.md` — same folder as the PRD for that product.

## Frontmatter (required)

```yaml
---
product: <kebab-case slug>
status: draft | review | approved
verdict: proceed | proceed-with-pivot | not-yet | kill
score: <integer 0-100>
owner: <name or role>
version: <semver, starts at 0.1.0>
last_reviewed: YYYY-MM-DD
---
```

`verdict` and `score` MUST agree with the bands in [validation-scoring-rubric](../../skills/architecture/saas-idea-validation/references/validation-scoring-rubric.md), including the hard-floor overrides. A brief whose frontmatter contradicts its own scoring table is invalid.

## Evidence tiers

Every substantive claim in the brief carries exactly one tier tag.

| Tag | Meaning | Qualifies as |
|---|---|---|
| `assumed` | Stated belief with no external input | Founder intuition, analogy to another market, "obviously people want this" |
| `researched` | Desk evidence gathered without contacting users | Competitor pricing pages, review mining, search volume, public benchmarks, analyst reports, job postings |
| `tested` | Primary evidence from target users | Interviews, fake-door conversion, LOI or prepay, concierge delivery, pilot usage |

Tag claims inline as `[assumed]`, `[researched]`, or `[tested]`. An untagged claim is treated as `assumed` when scoring.

## Sections

### Required

| Section | Purpose | Gate |
|---|---|---|
| `## Problem Statement` | Customer, pain, frequency, and current cost of the pain | Names a specific buyer and a quantified or observed cost |
| `## Value Hypothesis` | One falsifiable sentence, plus the single riskiest assumption | Hypothesis is falsifiable; exactly one riskiest assumption named |
| `## Current Alternatives` | What buyers use today, including status quo and spreadsheets | At least 3 entries, one of which is the status quo |
| `## Market Sizing` | Bottom-up only: reachable accounts × realistic ACV × attainable share | Arithmetic is shown; no top-down TAM |
| `## Value Proposition` | One sentence plus 3 differentiation claims | Each claim tagged `defensible` or `copyable` |
| `## Pricing and Willingness to Pay` | Model, price point, and the WTP signal behind it | Names model (seat / usage / flat / hybrid) and a price |
| `## Channel and CAC` | Acquisition channel and the CAC ceiling the pricing implies | CAC ceiling is a number derived from ACV |
| `## Unit Economics` | Payback months, gross margin, tolerable churn | All three present with arithmetic |
| `## Evidence Log` | Interviews and demand tests actually run | Interview count stated; each test lists its pre-declared threshold and result |
| `## Scoring` | The six-dimension table with raw score, tier, multiplier, weighted score | Totals to the `score` in frontmatter |
| `## Verdict` | Verdict, top 1-3 reasons, and the single next action | Verdict matches frontmatter and the score bands |

### Conditional

Include if material; otherwise omit and add a one-line rationale under a final `## Omitted sections` heading.

| Section | When to include |
|---|---|
| `## Pivot` | Required when `verdict: proceed-with-pivot`. Names the specific pivot and which dimensions were re-scored. |
| `## Experiments To Run` | Required when `verdict: not-yet`. Each entry: method, sample size, cost, duration, pass threshold. |
| `## Regulatory and Compliance` | Whenever the buyer's industry constrains the product (health, finance, education, public sector). |
| `## Team-Market Fit` | Whenever the team has unusual advantage or unusual gaps relative to this market. |

## Versioning

- Bump **patch** for typo or clarification edits.
- Bump **minor** when new evidence is logged without changing the verdict.
- Bump **major** when the verdict or pivot changes — requires re-scoring.

## Linkage contract

A brief with `status: approved` and `verdict: proceed` or `proceed-with-pivot` is the optional upstream input to:

- [skills/architecture/idea-development](../../skills/architecture/idea-development/SKILL.md) — consumes Problem Statement, Value Proposition, Current Alternatives, Channel and CAC, Evidence Log.

`idea-development` MUST NOT import findings from a brief whose verdict is `not-yet` or `kill`, and MUST NOT treat `assumed` claims as validated.

## Anti-patterns

- Top-down TAM ("the market is $40B, we only need 0.1%"). Size bottom-up or not at all.
- Verdict written before the scoring table, then scores tuned to justify it.
- Claims left untagged so an assumption reads as a finding.
- Demand tests whose pass threshold was declared after the result was known.
- Interviews that asked about hypothetical interest instead of past behavior and actual spend.
- "Competitor X is bad" as differentiation, with no claim tagged defensible.
- A `kill` verdict softened into `not-yet` with no experiment that could plausibly change the outcome.
