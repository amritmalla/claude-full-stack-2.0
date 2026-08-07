# Validation Playbook

Method for Phases 1, 2, and 4. Pricing and economics live in `saas-economics-patterns.md`.

## Question style

- Ask in clusters of one to three related questions.
- Every question carries a recommended default and rationale.
- Prefer tradeoff prompts over open brainstorming.
- Fold confirmed answers back into the brief with an evidence tier attached.

Example:

> I recommend treating the ops manager as the buyer rather than the analyst, because they hold the tooling budget and are measured on the cycle time you are compressing. Confirm or redirect.

## Phase 1 — Problem statement

Four elements. Name any that are unknown rather than inventing them.

| Element | Question that gets it |
|---|---|
| Customer | Who specifically — role, company size, industry? Not "teams" or "businesses". |
| Pain | What breaks, and what happens because it breaks? |
| Frequency | Daily, weekly, monthly, or per-event? |
| Current cost | Hours, headcount, error rate, penalty exposure, or lost revenue? |

If the user cannot name a current workaround, that is the finding. There is no workflow to displace, and dimension 1 scores 0.

### Value hypothesis

One falsifiable sentence:

> If [customer] can [capability], they will [measurable change], because [mechanism].

Falsifiable means an experiment could return "no". "Users will love it" is not falsifiable. Then name the **single riskiest assumption** — the one whose failure kills the idea fastest, not the one easiest to test.

## Phase 2 — Market

### Alternatives teardown

At least three, one of which must be the status quo. Buyers always have an alternative; doing nothing is one.

For each: what it costs (licence, labour, or tolerance), why buyers put up with it, and what would make them switch. Switching cost is usually the real competitor — data migration, retraining, and integration rework routinely exceed the value of a better product.

Sources for desk work, all `researched` tier: competitor pricing pages, G2/Capterra reviews filtered to one and two stars, changelogs, job postings that reveal roadmap, community threads where people describe their workaround.

### Bottom-up sizing

```text
reachable accounts x realistic ACV x attainable share in 3 years
```

Each factor needs a source and a tier. Reachable means you can name a list, directory, association, or database that enumerates them. If you cannot enumerate the accounts, you cannot reach them, and dimension 3 is affected.

Reject top-down TAM whenever offered. "The market is $40B and we only need 0.1%" describes no customer and predicts no revenue.

### Value proposition

One sentence, written **after** the teardown so it is aimed at named competitors:

> For [customer] who [pain], [product] is a [category] that [key benefit], unlike [named alternative], which [specific shortfall].

Then three differentiation claims, each tagged:

- `defensible` — proprietary data, workflow lock-in, integration depth, regulatory position, network effect, or structural cost advantage.
- `copyable` — UX, speed, price, features, support quality, being AI-native.

If all three are copyable, say so. It is a real signal about dimension 4, not a failure to conceal. Plenty of businesses win on execution against slow incumbents — but that is a bet on speed, and it should be made knowingly.

## Phase 4 — Evidence

### Problem interviews

Target 10-20 target users. Fewer than 10 triggers the interview floor in `validation-scoring-rubric.md`.

**Mom Test discipline.** Ask about the past, not the future. People are generous with hypothetical enthusiasm and stingy with real budget.

| Ask | Never ask |
|---|---|
| "Walk me through the last time this happened." | "Would you use a tool that did this?" |
| "What did you do about it?" | "Does this sound useful?" |
| "What did that cost you?" | "Would you pay $50 a month for this?" |
| "What have you already tried or bought?" | "How much would you pay?" |
| "Who else was involved in fixing it?" | "Do you think your team would like it?" |

Signals that count as `tested` evidence of pain: they built a workaround, they pay for something adjacent, they have a recurring calendar block for it, someone was hired partly to do it, or they can name what it cost last quarter.

Signals that count for nothing: "that sounds great", "we'd definitely look at that", "let me know when it launches".

Record themes, the saturation point (the interview after which no new pain theme appeared), and verbatim quotes. Quotes are the evidence; summaries are your interpretation of it.

If zero interviews were run, record zero. Do not fill the section with plausible-sounding synthetic findings.

### Demand tests

One test, threshold declared **before** the result.

| Test | Measures | Typical threshold | Cost |
|---|---|---|---|
| Landing page + ad spend | Message resonance | Signup rate vs. category baseline | Low |
| Fake door | Intent at the moment of use | Click-through to a "not built yet" page | Low |
| Concierge | Whether the outcome is wanted when delivered manually | Repeat requests from the same user | Medium |
| Pilot with LOI | Institutional commitment | Signed intent from a named account | Medium |
| Prepay or deposit | Actual willingness to pay | Money received | High |

Strength runs down the table. Prepay outranks every other signal; a landing-page signup is weak evidence that mostly measures your copywriting.

A test whose threshold was set after seeing the result is not evidence. Note it as `assumed` and say why.

## Handling thin evidence

Most ideas arrive with nothing tested. That is normal and is not a reason to soften the score.

State the position plainly: the idea scores where it scores because nothing has been checked, and here is the cheapest sequence that would change that. Then name the experiment that attacks the **riskiest assumption from step 2** — not the easiest experiment, and not all of them at once.

The output of a thin-evidence session is a `not-yet` verdict with a concrete week of work attached. That is a useful result, not a failure.
