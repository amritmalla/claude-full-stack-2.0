# SaaS Economics Patterns

Method for Phase 3, plus the SaaS-specific failure patterns to challenge throughout.

## Pricing model

Pick one and state why. The model matters more than the number at this stage, because it determines who buys and how you grow.

| Model | Fits when | Breaks when |
|---|---|---|
| Per seat | Value scales with people using it; usage is habitual | Buyers ration seats, capping expansion and encouraging shared logins |
| Usage | Value scales with volume; cost scales with volume | Bills are unpredictable, which procurement resists |
| Flat tiers | Value is a capability, not a volume | Large and small accounts pay alike, leaving money on the table |
| Hybrid (platform fee + usage) | Fixed value plus variable delivery cost — common for AI features | Complexity confuses self-serve buyers |

For AI-heavy products, per-seat pricing against per-token cost is the classic margin trap: revenue is capped per user while cost scales with how much they use it. Your best customers become your worst accounts. Hybrid or usage pricing usually beats per-seat here.

### Willingness to pay

The price needs a signal behind it, tagged with a tier:

- `tested` — a prepay, an LOI at a stated price, or a buyer naming their current spend on the alternative.
- `researched` — competitor pricing pages, published budget benchmarks, the cost of the labour being replaced.
- `assumed` — a number that felt right.

Anchor to **what the buyer spends today** on the alternative, including labour. A product replacing four hours a week of an ops manager's time is anchored to a real salaried number, not to what a competitor charges.

Never anchor to cost-plus. What it costs you to run has no relationship to what it is worth to them.

## Channel and the CAC ceiling

Derive the ceiling before assessing the channel, so the channel is judged against a number.

```text
ACV = price x expected accounts-worth-of-seats-or-usage
Gross-margin ACV = ACV x gross margin
CAC ceiling (12-month payback) = gross-margin ACV
```

A common rule of thumb is CAC payback under 12 months and LTV:CAC above 3:1. Treat both as sanity checks, not laws.

Then ask whether any channel plausibly acquires a customer under that ceiling.

| ACV | Channels that can work | Channels that cannot |
|---|---|---|
| < $1k/yr | Self-serve, product-led, marketplace, content | Any human sales touch |
| $1k-10k/yr | Inbound plus light sales assist, partnerships | Field sales, conferences as primary |
| $10k-50k/yr | Inside sales, outbound, partner channel | Pure self-serve with no onboarding |
| > $50k/yr | Field sales, pilots, procurement cycles | Self-serve as the primary motion |

**The most common fatal mismatch:** a $600/year price with a sales-led motion. One rep costs six figures and closes perhaps a few hundred accounts a year. The arithmetic never closes. Either the price rises by an order of magnitude or the motion becomes self-serve.

Also test whether the buyer is reachable at all. Some real pains sit with people who read no publication, attend no conference, join no community, and answer no cold email. That is a channel score of 0 or 1 regardless of how acute the pain is.

## Unit economics

Show the arithmetic for all three.

**Payback months** = CAC ÷ (gross-margin monthly revenue per account). Under 12 is healthy, 12-18 workable, over 24 usually needs funded patience.

**Gross margin** = (revenue − cost of delivery) ÷ revenue. Cost of delivery includes infrastructure, third-party APIs, model inference, and any human in the loop. Software margins run 75-85%. If yours lands near 50%, name the cause — usually inference cost or a services component — and say whether it compresses further with scale or improves.

**Tolerable churn** = the monthly logo churn at which the model still works. SMB self-serve commonly runs 3-5% monthly; mid-market 1-2%; enterprise under 1%. If the model only closes at churn well below the segment norm, the model does not close.

Watch for the treadmill: high SMB churn plus long payback means every new customer funds replacing a lost one. Growth flattens no matter how good acquisition is.

## Critique patterns

Challenge these directly when they appear.

**Seat pricing on a shared workflow.** If one person per company uses it, seat expansion never arrives and the account is worth its initial sale forever.

**Free tier with no conversion mechanism.** A free tier needs a specific wall a growing user hits. Free tiers that are merely "smaller" convert poorly and carry full support cost.

**Enterprise features, self-serve price.** SSO, audit logs, custom contracts, security review, and procurement all cost real money to serve. If the plan sells to enterprises at self-serve prices, the margin is fictional.

**Both motions at once.** Self-serve and sales-led need different products, pricing, hiring, and metrics. Pick one for v1 and say which.

**Replacing a tool nobody hates.** Displacing an incumbent costs migration, retraining, and political capital. "Cheaper and nicer" rarely covers it. Look for a wedge the incumbent structurally cannot serve.

**AI-native as the differentiation.** If the entire advantage is a model call, an incumbent with distribution and customer data ships it in a quarter. Ask what remains defensible after they do.

**Services revenue counted as SaaS.** Implementation, data cleanup, and managed operations are real revenue but carry services margins and do not compound. Separate them in the sizing.

**Hidden operational burden.** Manual review queues, data curation, integration maintenance, and support intensity are the cost of delivery. They belong in gross margin and in dimension 6, not in a footnote.

## Regulatory drag

When the buyer sits in health, finance, education, or public sector, add to the model: security review adds months to the sales cycle, compliance certification (SOC 2, HIPAA, FedRAMP) costs money and time before the first enterprise deal, and procurement extends payback. Cheap self-serve acquisition rarely survives contact with a regulated buyer.
