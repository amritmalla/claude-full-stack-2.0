---
name: idea-development
description: Use when a user needs to develop an idea through discovery, refinement, validation, specification, and execution readiness for a product, feature, workflow, SaaS, AI tool, internal tool, marketplace, or service. Produces a concise, decision-oriented PRD or readiness brief that narrows v1 scope, names user pain, documents assumptions and risks, defines success metrics, and leaves only intentionally deferred questions open.
---

# Idea Development

## When to use

Invoke when the user describes an informal product idea and needs help discovering, refining, validating, specifying, or preparing it for execution before architecture, design, or implementation work.

Do not use for editing an existing PRD, architecture planning, implementation planning, sprint breakdowns, roadmap prioritization, UX copy, marketing copy, or broad brainstorming.

For a commercial SaaS idea whose viability is still in question — whether it is worth building at all, what it should cost, or how big the market is — run [saas-idea-validation](../saas-idea-validation/SKILL.md) first and bring its brief here. This skill scopes v1; that one decides whether there should be a v1.

## Inputs

Required:

- A 1-5 sentence informal idea description.

Optional:

- An approved `validation-brief.md` conforming to [standards/validation-brief-schema](../../../standards/validation-brief-schema/README.md), produced by [saas-idea-validation](../saas-idea-validation/SKILL.md). Import it rather than re-deriving its findings.
- Target users or customer segment.
- Business model assumptions.
- Budget, staffing, or timeline constraints.
- Regulatory, privacy, or security requirements.
- Existing tools, workflows, or competitors being replaced.
- Distribution or rollout assumptions.

## Operating rules

- Narrow before expanding. Default to one primary persona, one painful problem, one core workflow, and a small v1 scope.
- Act like a skeptical product lead. Challenge vague personas, low-severity pain, weak urgency, hidden operational work, AI magic thinking, marketplace liquidity assumptions, and platform ambitions without a wedge.
- Name every actor. Every workflow step must identify who performs it (user, system, upstream service, scheduled job, human operator). Unowned steps usually hide a missing service or out-of-scope automation — make it explicit in scope or non-goals.
- Ask no more than three related questions at once, and always with a recommended default and rationale (see `references/discovery-playbook.md` for the question format).
- Call out contradictions immediately. If a later answer conflicts with an earlier decision, explain the conflict and recommend which direction to keep for v1.
- Do not assume every idea deserves a PRD. If the idea is structurally weak, say why and recommend narrowing, reframing, or abandoning it.
- Treat execution readiness as earned. Do not mark an idea ready if the primary user, problem, v1 scope, assumptions, success metrics, or adoption/rollout path are still vague.

## Progressive references

- Read `references/discovery-playbook.md` when the idea needs interactive clarification, persona/JTBD work, v1 scoping, non-goals, open-question resolution, or success metrics.
- Read `references/product-critique-patterns.md` when evaluating idea quality, risks, distribution, adoption, marketplace dynamics, AI claims, or hidden operational burden.
- Read `references/prd-quality-rubric.md` before emitting the final PRD and use it as the validation checklist.
- Read `assets/PRD.example.md` before drafting if you need a concrete style and length anchor; it shows what conditional-section omission and a tight internal-service PRD look like.

## Process

Five phases. Do not advance past the credibility gate (step 7) unless the idea is credible enough to warrant a PRD.

### Discovery

- [ ] Step 1. Restate the idea in one sentence using only what the user said. If target user, pain, or workflow shift is ambiguous, name the ambiguity instead of inventing specifics. Ask the user to confirm or redirect.
- [ ] Step 2. Identify the primary persona, context, job-to-be-done, current workaround, and why the pain is urgent. Resolve multi-persona scope before continuing.

### Refinement

- [ ] Step 3. Define the problem and why-now without solutioning, feature references, or technology choices.
- [ ] Step 4. Narrow v1 scope to 3-5 outcomes (not features). Propose at least three non-goals with rationale.

### Validation

- [ ] Step 5. Document constraints, assumptions, and risks. Recommend cuts if constraints conflict with scope.
- [ ] Step 6. Test the workflow's path to users.
  - External products (SaaS, consumer, marketplace, AI tool): how the first 100 users realistically discover, adopt, or are required to use it.
  - Internal tools / reference workloads / system components: which upstream/downstream services or teams consume it, and how cutover is staged.
- [ ] Step 7. **Credibility gate.** Test the idea against pain severity, frequency, willingness or mandate to adopt, operational burden, and plausible alternatives.

  **If a validation brief is available:** a brief with `status: approved` and verdict `proceed` or `proceed-with-pivot` satisfies this gate. Import its Problem Statement, Value Proposition, Current Alternatives, Channel and CAC, and Evidence Log instead of re-deriving them, and carry its evidence tiers forward into Assumptions. Do not re-open decisions the brief settled with `tested` evidence. A brief with verdict `not-yet` or `kill` does not satisfy the gate — stop and return to [saas-idea-validation](../saas-idea-validation/SKILL.md).

  **Otherwise**, run the gate on judgment and choose one:
  - **Proceed** — pain, adoption, and wedge are credible. Continue to Specification.
  - **Narrow / reframe** — recommend a tighter wedge, different persona, or different problem. Return to step 1 with the user's confirmation.
  - **Abandon** — the idea is structurally weak (no urgent pain, no adoption path, no wedge). State this directly and stop. Do not produce a PRD.

### Specification

- [ ] Step 8. Resolve implementation-shaping open questions where possible. Keep only explicitly deferred decisions for the final `Open Questions` section.
- [ ] Step 9. Define 2-4 success metrics with unit, target, and timeframe.
- [ ] Step 10. Generate `PRD.md` from `assets/PRD.template.md`. Validate against [standards/prd-schema](../../../standards/prd-schema/README.md) AND against `references/prd-quality-rubric.md`. Revise until both pass or explicitly note any unresolved gap.

### Execution readiness

- [ ] Step 11. Run a final critique pass. Call out contradictions, weak positioning, bloated scope, distribution concerns, unrealistic assumptions, or missing downstream handoff context.
- [ ] Step 12. State whether the idea is ready for downstream architecture/design/implementation. If not ready, list the smallest set of decisions or evidence needed next.

## Outputs

- `PRD.md` at `docs/product/<slug>/PRD.md`. MUST conform to [standards/prd-schema](../../../standards/prd-schema/README.md), which is authoritative for frontmatter (`product`, `status`, `owner`, `version`, `last_reviewed`), the required/conditional section list, omission rules (use `## Omitted sections` at the bottom), and versioning. Use `assets/PRD.template.md` as the scaffold.
  - Required sections: Problem, Users, JTBD, Scope, Non-goals, Constraints, Assumptions, Success Metrics, Open Questions.
  - Conditional sections (include if material, otherwise omit with rationale): Why Now, Current Alternatives, Risks, Distribution and Adoption, Out of scope (future).
- Readiness note in the response: `Ready for execution`, `Ready with caveats`, or `Not ready`, with the top 1-3 reasons.

Output rules:

- Keep the PRD concise and decision-oriented.
- Focus on user pain, workflow outcomes, and v1 scope.
- Avoid implementation details unless a constraint changes product scope.
- Avoid feature catalogs, marketing language, and vague platform positioning.
- Include only intentionally deferred decisions in `Open Questions`.
- Distinguish validation evidence from assumptions. Do not present untested beliefs as proven facts.

## Quality checks

- [ ] `references/prd-quality-rubric.md` was loaded before finalizing.
- [ ] `PRD.md` validates against [standards/prd-schema](../../../standards/prd-schema/README.md): frontmatter present and complete; all required sections present; conditional sections either present with content or listed under `## Omitted sections` with rationale.
- [ ] `PRD.md` follows `assets/PRD.template.md`.
- [ ] Every user-facing question included a recommended answer and rationale.
- [ ] At least one meaningful critique or scope risk was surfaced, or the PRD explains why no major issue remains.
- [ ] Open Questions contains only decisions the user explicitly deferred.
- [ ] The final response states execution readiness and the smallest next step if the idea is not ready.

## References

- `references/discovery-playbook.md`
- `references/product-critique-patterns.md`
- `references/prd-quality-rubric.md`
- `assets/PRD.template.md`
- `assets/PRD.example.md`
