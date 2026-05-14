# System Design Quality Rubric

Load this before emitting final artifacts. Revise until each check passes or the unresolved gap is explicitly documented.

## Required checks

- [ ] The design restates PRD elements that exist in the PRD (primary user, core workflow, constraints, success metrics, non-goals) and explicitly notes any structural gap rather than papering over it. Legitimate PRD omissions under `prd-from-idea`'s conditional-section rules (Why Now, Current Alternatives, Risks, Distribution) are not gaps.
- [ ] Every bounded context has one clear business responsibility.
- [ ] Bounded contexts use domain names, not technology names.
- [ ] Every component has a concise responsibility statement.
- [ ] Component names reflect domain responsibilities, not technologies.
- [ ] Architecture style is justified against explicit PRD constraints.
- [ ] Simpler architectures were considered and either chosen or explicitly rejected with reasons.
- [ ] The design does not introduce distributed complexity without explicit PRD justification.
- [ ] Data write ownership is unambiguous for every critical entity.
- [ ] Eventual consistency assumptions are documented where they exist.
- [ ] Idempotency and retry behavior are documented for async flows.
- [ ] Every major component includes at least one realistic failure mode.
- [ ] Failure modes include user impact, detection, recovery, and degradation.
- [ ] Security boundaries are explicitly addressed, not hand-waved.
- [ ] Sensitive data, tenant isolation, retention, and auditability are addressed where relevant.
- [ ] Operational burden introduced by the architecture is acknowledged.
- [ ] Every ADR contains Status, Context, Decision, and Consequences.
- [ ] Every ADR's Consequences section includes downsides and tradeoffs.
- [ ] ADR Index lists every generated ADR.
- [ ] At least one simplification was surfaced, or the intentional simplicity of the design was explained.

## Failure handling

If a check fails:

1. Identify the missing or weak decision.
2. Ask the user for clarification if the decision cannot be inferred from the PRD.
3. Revise `system-design.md` or the relevant ADR.
4. Keep unresolved architecture questions explicit; do not hide them as assumptions.
