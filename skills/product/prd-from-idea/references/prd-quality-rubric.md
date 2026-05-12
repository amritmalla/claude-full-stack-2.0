# PRD Quality Rubric

Load this before emitting the final PRD. Revise until each check passes or the unresolved gap is explicitly documented.

## Required checks

- [ ] Problem names one specific primary user and one specific painful workflow.
- [ ] `Why Now` explains current urgency **or** is explicitly omitted with rationale (e.g., foundational build, no external trigger).
- [ ] `Current Alternatives` names the workaround or competing behavior **or** is explicitly omitted because no incumbent exists.
- [ ] Scope is limited to one primary persona and one core v1 workflow unless the user explicitly accepted the added complexity.
- [ ] Scope lists outcomes, not a feature catalog.
- [ ] Non-goals include at least three explicit exclusions with rationale.
- [ ] Constraints are documented separately from assumptions and risks.
- [ ] Assumptions are explicit and testable.
- [ ] Risks (if present) include why each matters and at least one mitigation or narrowing recommendation. The Risks section may be omitted only if no material risks remain after scope narrowing, with the omission noted.
- [ ] Distribution and Adoption is addressed for external products **or** replaced with integration and rollout for internal tools / reference workloads / system components.
- [ ] Every success metric has a unit, target, and timeframe.
- [ ] Problem section contains no solutioning, features, or technology choices.
- [ ] Open Questions contains only decisions the user explicitly deferred.
- [ ] Every user-facing question included a recommended answer and rationale.
- [ ] At least one meaningful critique or scope risk was surfaced, or the PRD explains why no major issue remains.
- [ ] Conflicting personas, workflows, or sales motions are explicitly addressed if present.

## Failure handling

If a check fails:

1. Identify the missing or weak decision.
2. Ask the user a recommended-default question if the decision cannot be inferred.
3. Revise the PRD after the user confirms, redirects, or explicitly defers.
4. Keep deferred decisions in `Open Questions`; do not hide them in assumptions.
