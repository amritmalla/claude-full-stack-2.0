# Validation Scoring Rubric

Authoritative for dimensions, weights, evidence multipliers, hard floors, and verdict bands. Load before scoring. Score every dimension before writing the verdict — never the reverse.

## The arithmetic

For each dimension:

```text
weighted = (raw / 5) x weight x multiplier
```

Total the six weighted scores, round to the nearest integer, then apply the hard floors.

## Dimensions and weights

| # | Dimension | Weight |
|---|---|---|
| 1 | Pain severity and frequency | 25 |
| 2 | Willingness to pay / budget authority | 20 |
| 3 | Reachable acquisition channel | 20 |
| 4 | Differentiation vs. current alternatives | 15 |
| 5 | Unit-economics plausibility | 12 |
| 6 | Team-market fit and operational burden | 8 |

### 1. Pain severity and frequency (25)

| Raw | Meaning |
|---|---|
| 5 | Costs measurable money, time, or compliance exposure; recurs weekly or more; a named role owns the problem and is judged on it |
| 4 | Clear recurring cost, monthly or more, with an identifiable owner |
| 3 | Real annoyance with occasional cost; owner is diffuse |
| 2 | Inconvenience; buyers have absorbed it and stopped noticing |
| 1 | Only painful when described back to them |
| 0 | Cannot name a current workaround, which means there is no workflow to displace |

### 2. Willingness to pay / budget authority (20)

| Raw | Meaning |
|---|---|
| 5 | Budget line already exists; buyer identified; they pay for something adjacent today |
| 4 | Budget exists but must be reallocated; buyer identified |
| 3 | Buyer identified; budget would need creating |
| 2 | Buyer and user are different people and the buying trigger is unclear |
| 1 | Enthusiasm from users with no purchasing power |
| 0 | Everyone expects it free |

### 3. Reachable acquisition channel (20)

| Raw | Meaning |
|---|---|
| 5 | A specific channel reaches buyers at a cost comfortably under the CAC ceiling, demonstrated or closely analogous |
| 4 | Plausible channel with credible comparable CAC |
| 3 | Channel exists but CAC is uncertain and could exceed the ceiling |
| 2 | Only expensive outbound or enterprise sales against a small ACV |
| 1 | Depends on virality, SEO, or content with no evidence |
| 0 | No identified way to reach buyers |

### 4. Differentiation vs. current alternatives (15)

| Raw | Meaning |
|---|---|
| 5 | At least two claims tagged defensible: proprietary data, workflow lock-in, integration depth, regulatory position, or network effect |
| 4 | One defensible claim plus meaningful execution advantage |
| 3 | All claims copyable, but incumbents are slow or structurally conflicted |
| 2 | All claims copyable and incumbents are attentive |
| 1 | Differentiation is "ours will be better designed" |
| 0 | No articulable difference from an existing product |

### 5. Unit-economics plausibility (12)

| Raw | Meaning |
|---|---|
| 5 | Payback under 12 months, gross margin over 75%, churn tolerance realistic for the segment |
| 4 | Payback 12-18 months with healthy margin |
| 3 | Payback 18-24 months, or margin compressed by delivery cost |
| 2 | Payback over 24 months, or margin under 50% from infrastructure or human-in-the-loop cost |
| 1 | Economics only close under assumptions with no support |
| 0 | CAC exceeds lifetime value under any tested assumption |

### 6. Team-market fit and operational burden (8)

| Raw | Meaning |
|---|---|
| 5 | Team has direct domain experience and existing access to buyers; operational burden is low |
| 4 | Strong adjacent experience; burden manageable |
| 3 | Capable team, no domain edge, moderate burden |
| 2 | Significant hidden operations: manual review, data cleaning, integrations, or support intensity |
| 1 | Product requires expertise the team lacks and cannot easily hire |
| 0 | Delivery depends on an ongoing service business masquerading as software |

## Evidence multipliers

Each dimension takes the tier of the **weakest** claim materially supporting it.

| Tier | Multiplier |
|---|---|
| `assumed` | 0.4 |
| `researched` | 0.7 |
| `tested` | 1.0 |

An idea supported only by assertion caps at 40/100 and can never reach `proceed`. This is intentional: evidence moves the score, conviction does not.

Dimensions 1 and 2 are additionally capped at `researched` (0.7) when fewer than 10 target-user interviews have been conducted, since neither pain nor budget can be established without talking to buyers.

## Hard floors

Floors override the total. Any one of these caps the verdict regardless of score:

| Floor | Condition | Caps verdict at |
|---|---|---|
| Pain floor | Dimension 1 raw < 3 | `not-yet` |
| Channel floor | Dimension 3 raw < 2 | `not-yet` |
| Interview floor | Fewer than 10 qualifying target-user interviews | `not-yet` |

The pain floor blocks strong economics and a clever solution from papering over a problem nobody has. The channel floor blocks a real problem that cannot be sold to. The interview floor blocks `proceed` on desk research alone.

The interview floor is a gate, not an arithmetic consequence. A brief can score well above 70 on researched and tested non-interview evidence — a fake door converts, competitors price high, the channel is proven — and still be capped, because none of that establishes that *these* buyers feel *this* pain. Interviews count only if they follow the Mom Test discipline in `validation-playbook.md`: past behavior and actual spend, not hypothetical interest.

When a floor triggers, say so explicitly in the Verdict section and name which floor.

## Verdict bands

| Score | Verdict | Meaning |
|---|---|---|
| >= 70 | `proceed` | Evidence supports building. Unlocks `idea-development`. |
| 50-69 | `proceed-with-pivot` | Viable after a specific change. Name the pivot and re-score the affected dimensions. |
| 30-49 | `not-yet` | Not enough evidence, or a fixable weakness. Name the experiments. |
| < 30 | `kill` | Structurally weak. State the reasons and stop. |

## Worked example

An idea with strong asserted pain (raw 5, `assumed`), a researched budget signal (raw 4, `researched`), a researched channel (raw 3, `researched`), copyable differentiation (raw 2, `researched`), plausible economics (raw 4, `assumed`), and good team fit (raw 4, `assumed`):

| Dimension | Raw | Weight | Tier | Weighted |
|---|---|---|---|---|
| Pain | 5 | 25 | assumed 0.4 | 10.0 |
| WTP | 4 | 20 | researched 0.7 | 11.2 |
| Channel | 3 | 20 | researched 0.7 | 8.4 |
| Differentiation | 2 | 15 | researched 0.7 | 4.2 |
| Economics | 4 | 12 | assumed 0.4 | 3.8 |
| Team fit | 4 | 8 | assumed 0.4 | 2.6 |
| **Total** | | | | **40** |

Verdict `not-yet` — by score (30-49) and independently by the interview floor, since no interviews were run.

The idea is not obviously bad, it is unevidenced. The next action is 10-20 interviews. Lifting pain and WTP to `tested` without changing a single raw score moves the total to 60 and clears the interview floor, landing the idea at `proceed-with-pivot` — a different conversation entirely, bought with a week of calls.

## Re-scoring

When new evidence arrives, change only the multipliers and any raw scores the evidence actually contradicts. Do not quietly raise raw scores to reach a band. Bump the brief's version per [validation-brief-schema](../../../../standards/validation-brief-schema/README.md).
