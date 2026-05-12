# Product Critique Patterns

Use these patterns to challenge the idea before committing it to a PRD. Be direct, but give a narrowing recommendation.

## Common scope risks

- Multi-persona products: recommend one primary persona for v1.
- Platform ambitions: require a wedge workflow before platform scope.
- Feature soup: convert feature lists into 3-5 workflow outcomes.
- "AI does everything": identify the specific decision, draft, extraction, triage, or review job AI performs.
- Automation without exception handling: require a fallback or human review path.
- Enterprise and self-serve conflict: choose one motion for v1.
- Implicit actors: every workflow step must name who performs it (user, system, upstream service, scheduled job, human operator). Unowned steps usually hide a missing service, a fuzzy role boundary, or out-of-scope automation that needs to be made explicit in scope or non-goals.

## Weak pain signals

Flag weak pain when:

- the user cannot name the current workaround,
- the workflow is annoying but not costly,
- no one owns the problem,
- urgency depends on vague future trends,
- or the buyer is different from the user and the buying trigger is unclear.

Recommendation pattern:

> This reads like a convenience rather than a painful workflow. I recommend narrowing to the moment where delay, error, compliance exposure, or lost revenue is visible.

## Distribution and adoption risks

Challenge how the first 100 users discover, adopt, or are required to use the workflow.

Look for:

- existing channels,
- embedded workflows,
- internal rollout authority,
- sales motion,
- procurement friction,
- migration cost,
- SEO assumptions,
- virality assumptions,
- and mandatory usage.

If distribution is weak, state the concern plainly and recommend a narrower wedge or captive rollout path.

## Marketplace risks

For marketplace ideas, identify:

- which side has acute pain,
- how initial supply is acquired,
- how initial demand is acquired,
- whether liquidity must be local, vertical-specific, or time-sensitive,
- and what happens before the marketplace is liquid.

Recommend starting as a managed service, single-sided workflow tool, or narrow vertical if liquidity is unresolved.

## AI product risks

For AI-heavy ideas, check:

- hallucination impact,
- user trust,
- review and approval workflow,
- source-of-truth ownership,
- data privacy,
- evaluation approach,
- and fallback behavior.

Recommend human review for high-impact outputs unless the user explicitly accepts automation risk.

## Risk format

For each major risk, write:

- Risk: what may fail.
- Why it matters: impact on adoption, trust, cost, compliance, or delivery.
- Mitigation: narrowing, workflow change, validation plan, or explicit non-goal.
