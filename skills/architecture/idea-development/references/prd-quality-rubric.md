# PRD Quality Rubric

Load this before emitting the final PRD. Revise until each check passes or the unresolved gap is explicitly documented.

The rubric has two parts:

- **Artifact checks** — verifiable by reading `PRD.md` alone.
- **Process checks** — verifiable only from the conversation that produced the PRD.

## Artifact checks (read PRD.md)

- [ ] Problem names one specific primary user and one specific painful workflow.
- [ ] Problem section contains no solutioning, features, or technology choices.
- [ ] `Why Now` explains current urgency **or** is listed under `Omitted sections` with rationale (e.g., foundational build, no external trigger).
- [ ] `Current Alternatives` names the workaround or competing behavior **or** is listed under `Omitted sections` because no incumbent exists.
- [ ] Scope is limited to one primary persona and one core v1 workflow.
- [ ] Scope lists outcomes, not a feature catalog.
- [ ] Non-goals include at least three explicit exclusions with rationale.
- [ ] Constraints are documented separately from assumptions and risks.
- [ ] Assumptions are explicit and testable.
- [ ] Any assumption tagged `validated` cites its evidence — the validation brief's evidence tier and source, or an equivalent named source. An assumption asserted confidently but never checked is `unvalidated`.
- [ ] Risks (if present) include why each matters and at least one mitigation or narrowing recommendation. The Risks section may be omitted only if no material risks remain after scope narrowing, with the omission noted.
- [ ] Distribution and Adoption is addressed for external products **or** replaced with integration and rollout for internal tools / reference workloads / system components.
- [ ] Every success metric has a unit, target, and timeframe.
- [ ] Every workflow step in Scope names who performs it (user, system, upstream service, scheduled job, human operator).
- [ ] Open Questions contains only decisions the user explicitly deferred (each has question, owner, decision deadline).

## Process checks (read the conversation)

- [ ] Every user-facing question included a recommended answer and rationale.
- [ ] At least one meaningful critique or scope risk was surfaced, or the PRD explains why no major issue remains.
- [ ] Conflicting personas, workflows, or sales motions raised during discovery are either resolved in the PRD or listed in Open Questions.
- [ ] Multi-persona scope, if it surfaced, was narrowed to one v1 persona with user confirmation.
- [ ] The credibility gate (process step 7) was passed with user confirmation, not skipped — or satisfied by an approved validation brief with verdict `proceed` or `proceed-with-pivot`.
- [ ] If a validation brief was supplied, its findings were imported rather than re-derived, and no decision it settled with `tested` evidence was silently re-opened.

## Failure handling

If a check fails:

1. Identify the missing or weak decision.
2. Ask the user a recommended-default question if the decision cannot be inferred.
3. Revise the PRD after the user confirms, redirects, or explicitly defers.
4. Keep deferred decisions in `Open Questions`; do not hide them in assumptions.
