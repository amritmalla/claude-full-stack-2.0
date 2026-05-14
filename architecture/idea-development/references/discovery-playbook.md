# Discovery Playbook

Use this playbook for interactive clarification. Keep the conversation focused on decisions that change the PRD.

## Question style

- Ask in small clusters of one to three related questions.
- Include a recommended default and rationale for every question.
- Prefer tradeoff prompts over open-ended brainstorming.
- Fold confirmed answers back into scope, non-goals, constraints, assumptions, risks, metrics, or open questions.

Example:

> I recommend using operations managers as the primary persona because they own the current manual workflow and feel the coordination pain. Confirm or redirect.

## Persona, JTBD, and workaround

Produce:

- Persona: the one primary user who alone can justify v1.
- Context: where the workflow happens and what pressure the user is under.
- JTBD: what progress the user is trying to make.
- Current workaround: spreadsheet, email, Slack, manual ops, agency, legacy SaaS, human assistant, or internal tool.

If multiple primary personas emerge, treat it as a scope risk. Recommend one persona for v1 and move the rest to non-goals or later phases.

## Problem and why-now

Write 2-4 sentences that describe:

- who is affected,
- what painful workflow exists today,
- why current alternatives fail,
- and why the pain matters now.

Do not mention the product, features, technology, implementation, or "we will build." Ask: "Does this capture the real pain, or am I inventing one?"

If urgency is weak, say so and ask whether this is a nice-to-have instead of a painful workflow problem.

## Scope and non-goals

Scope should be 3-5 v1 outcomes, not a feature catalog.

Good:

- Reduce onboarding setup time from days to under 30 minutes.
- Cut manual approval handoffs from five steps to two.

Bad:

- Add dashboard.
- Support AI chat.
- Create notifications.

Use these prompts:

- "If only one workflow survives v1, which is it?"
- "Which user alone justifies the product?"
- "What can slip six months without breaking the core value proposition?"

Non-goals must exclude tempting expansion paths and explain why they are excluded. Include at least three.

## Constraints, assumptions, and open questions

Separate these categories:

- Constraints: known limits such as deadline, staffing, budget, compliance, integrations, deployment, latency, region, or stack.
- Assumptions: beliefs that must be true for success, such as user trust, structured data, buyer/user alignment, integration access, or operational capacity.
- Open questions: unresolved decisions that change scope or acceptance.

Resolve open questions during discovery when possible. Ask only questions that shape the PRD, such as auth model, permissions, billing, data retention, AI review workflow, source-of-truth ownership, audit logging, export needs, offline behavior, or fallback workflows.

## Success metrics

Propose 2-4 metrics. Every metric must include:

- unit,
- target,
- timeframe.

Reject metrics that are vanity-only, immeasurable, disconnected from user pain, missing a baseline, or missing a timeframe.
