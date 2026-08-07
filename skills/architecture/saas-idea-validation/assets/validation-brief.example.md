---
product: petlog
status: approved
verdict: proceed-with-pivot
score: 62
owner: self
version: 0.2.0
last_reviewed: 2026-08-07
---

# Validation Brief — petlog (example output)

> Worked example of a brief produced by this skill. Use as a style and length anchor, not a copy-paste template. All figures are illustrative. The structure follows `validation-brief.template.md`; two conditional sections are omitted with rationale at the bottom.
>
> This example is deliberately a `proceed-with-pivot`: the pain is strongly evidenced but the economics do not close at the original segment. It shows how a pivot is named and re-scored without inflating raw scores.

## Problem Statement

Practice managers at independent US veterinary clinics (1-4 doctors) maintain DEA-required perpetual inventory logs for controlled substances on paper. `[tested]` Entries happen several times daily; reconciliation happens monthly and routinely fails to balance, sending the manager back through weeks of handwriting to find a transcription error. `[tested]`

Cost today: roughly 6 hours of practice-manager time per month, plus inspection exposure — a failed DEA audit carries fines and, in the worst case, registration risk. `[tested]` Eleven of fourteen interviewees had personally experienced a log that would not reconcile; four had been through an inspection. `[tested]`

## Value Hypothesis

> If practice managers can log controlled-substance transactions at the point of dispensing and reconcile continuously, they will close each month with a balanced log without a manual audit, because the error is caught at entry rather than four weeks later.

**Riskiest assumption:** that clinics will change the dispensing-moment behavior of veterinarians, who are not the buyer and gain nothing personally from logging correctly.

## Current Alternatives

| Alternative | What it costs them | Why they tolerate it | What would make them switch |
|---|---|---|---|
| Paper logbook (status quo) | ~6 hrs/month + audit exposure | DEA-accepted, zero setup, no IT involvement | A reconciliation failure or a bad inspection |
| Spreadsheet | ~4 hrs/month, weaker audit trail | Familiar, free | Being told it is non-compliant |
| Practice-management module (Cornerstone, ezyVet) | Bundled, often unused | Already paid for; clunky enough that staff revert to paper | Meaningfully faster entry than paper |

The real competitor is the third row: clinics already own software that nominally does this and do not use it. `[tested]` Displacing paper means beating a tool that already lost to paper once.

## Market Sizing

```text
28,000 independent US clinics (reachable via state board registries)  [researched]
x $1,800 ACV (2 sites x $75/mo)                                       [researched]
x 4% attainable share in 3 years                                      [assumed]
= ~$2.0M ARR
```

Bottom-up ceiling is modest. The segment is enumerable — state veterinary board registries and DEA registrant lists are public — which is what makes the channel scoreable at all. `[researched]`

## Value Proposition

> For practice managers at independent veterinary clinics who lose a day a month reconciling paper controlled-substance logs, petlog is a point-of-dispense logging tool that keeps the perpetual inventory continuously balanced, unlike bundled practice-management modules, which require more keystrokes at the moment of dispensing than a paper logbook does.

| Claim | Defensible or copyable | Why |
|---|---|---|
| Faster than paper at the dispensing moment | `copyable` | Pure UX; any incumbent can match it |
| DEA-format audit export | `copyable` | Format is public |
| Reconciliation engine that localizes the discrepancy to a transaction | `defensible` | Requires the transaction-level data model incumbents do not capture; retrofitting it breaks their existing schema |

Two of three are copyable. The bet is that incumbents are structurally slow, not that the product is unreachable.

## Pricing and Willingness to Pay

**Model:** flat per-site tier — usage is habitual, seat counts are tiny, and per-seat pricing would push clinics to share one login.
**Price point:** $75/site/month.
**WTP signal:** six interviewees named their current spend on compliance consulting ($200-400/visit, 2-3 visits/year); three said they would pay "under $100 a month" unprompted when asked what they spend on the problem today. `[tested]`

## Channel and CAC

**Channel:** outbound to state board registry lists, plus state veterinary association sponsorships.

```text
ACV                          = $1,800
Gross-margin ACV (82%)       = $1,476
CAC ceiling (12-mo payback)  = $1,476
```

Inside-sales outbound to single clinics runs an estimated $2,500 per closed account at this deal size — a 30-45 day cycle with a practice manager who is not at a desk. `[researched]` **That is 1.7x the ceiling.** No self-serve path was found: the buyer does not search for this software, because they do not think of paper as a problem with a software solution. `[tested]`

This is the finding that drives the pivot.

## Unit Economics

| Metric | Value | Arithmetic |
|---|---|---|
| Payback | 20.3 months | $2,500 CAC ÷ ($1,800 × 0.82 ÷ 12) |
| Gross margin | 82% | Hosting and support only; no human in the loop |
| Tolerable churn | < 1.5%/month | Required for a 20-month payback to return capital |

Tolerable churn of 1.5% sits below the 3-5% monthly norm for SMB self-serve. `[researched]` At the original segment the model does not close.

## Evidence Log

**Interviews conducted:** 14

Themes, in order of strength:

- Reconciliation failure is universal and remembered specifically — 11 of 14 could describe a particular incident. `[tested]`
- Inspection fear is acute but infrequent; it motivates purchase only shortly after an inspection or a peer's bad outcome. `[tested]`
- Veterinarians resist any added step at dispensing. Three managers independently said a prior tool failed for exactly this reason. `[tested]`
- Saturation reached at interview 11; interviews 12-14 produced no new pain theme.

> "I found it three weeks later. One number. I went through every page twice." — practice manager, 2-doctor clinic

> "We bought that module. Nobody uses it. It's four clicks and the doctor is holding a dog." — practice manager, 3-doctor clinic

**Demand tests:**

| Test | Pass threshold (declared before) | Result | Tier |
|---|---|---|---|
| Landing page + association newsletter placement | ≥ 3% visitor-to-waitlist | 4.1% (n=340) | `tested` |
| Prepay offer | — | not run | — |

## Scoring

| Dimension | Raw /5 | Weight | Tier | Multiplier | Weighted |
|---|---|---|---|---|---|
| Pain severity and frequency | 5 | 25 | tested | 1.0 | 25.00 |
| Willingness to pay | 4 | 20 | tested | 1.0 | 16.00 |
| Reachable channel | 3 | 20 | researched | 0.7 | 8.40 |
| Differentiation | 3 | 15 | researched | 0.7 | 6.30 |
| Unit economics | 2 | 12 | researched | 0.7 | 3.36 |
| Team-market fit | 4 | 8 | assumed | 0.4 | 2.56 |
| **Total** | | | | | **61.62 → 62** |

**Floors:** none triggered. Pain raw 5 clears the pain floor, channel raw 3 clears the channel floor, and 14 interviews clear the interview floor.

## Verdict

**PROCEED WITH PIVOT** — 62/100

1. The problem is real and well-evidenced. Pain and willingness to pay are the only `tested` dimensions and both score high; this is not a solution in search of a problem.
2. The economics do not close at the single-clinic segment. A $1,476 CAC ceiling against a $2,500 outbound CAC is not a marketing problem to be optimized away — it is a segment mismatch.
3. Differentiation is thin. Only the reconciliation engine is defensible, and it is defensible only for as long as incumbents decline to change their data model.

**Next action:** 10 interviews with operations directors at multi-site veterinary groups to test whether the pain survives at that level and whether $12k ACV is real.

## Pivot

**Move the segment upmarket: multi-site veterinary groups (10-60 clinics), not single independents.**

Same pain, same product, different buyer. An operations director carries compliance risk across every site, is reachable through a short list of roughly 2,500 groups, and can sign for all sites at once.

Re-scored at an assumed $12,000 ACV and $6,000 sales-led CAC:

| Dimension | Was | Now | Why |
|---|---|---|---|
| Reachable channel | 3 (researched) → 8.40 | 4 (researched) → 11.20 | Named-account outbound against a $9,840 ceiling |
| Unit economics | 2 (researched) → 3.36 | 4 (researched) → 6.72 | Payback 7.3 months at 82% margin |

**Re-scored total: 68.** Still short of `proceed`, and correctly so — the new segment has not been interviewed. No raw score was raised on the strength of the pivot alone; the ceiling now sits with the evidence tier, which is exactly what the next action buys.

## Regulatory and Compliance

DEA 21 CFR 1304 governs the record format, retention (2 years), and inspection access. The format is public and stable, so compliance is a build requirement rather than a moat. Multi-site groups will additionally expect a security review, which lengthens the sales cycle by an estimated 4-8 weeks and should be carried in the pivot's payback assumption. `[researched]`

## Omitted sections

- **Experiments To Run:** verdict is `proceed-with-pivot`, not `not-yet`; the single next action is stated in Verdict.
- **Team-Market Fit:** no unusual advantage or gap relative to this market; scored in the table and left at that.
