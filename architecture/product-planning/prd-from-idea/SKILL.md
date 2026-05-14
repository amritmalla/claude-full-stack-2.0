---
name: prd-from-idea
description: Use when a user has a rough product, feature, workflow, SaaS, AI tool, internal tool, marketplace, or service idea and no existing PRD. Produces a concise, decision-oriented PRD that narrows v1 scope, names user pain, documents assumptions and risks, defines success metrics, and leaves only intentionally deferred questions open.
---

# PRD from Idea

## When to use

Invoke when the user describes an informal product idea and needs a sharp PRD before architecture, design, or implementation work.

Do not use for editing an existing PRD, architecture planning, implementation planning, sprint breakdowns, roadmap prioritization, UX copy, marketing copy, or broad brainstorming.

## Inputs

Required:

- A 1-5 sentence informal idea description.

Optional:

- Target users or customer segment.
- Business model assumptions.
- Budget, staffing, or timeline constraints.
- Regulatory, privacy, or security requirements.
- Existing tools, workflows, or competitors being replaced.
- Distribution or rollout assumptions.

## Operating rules

- Narrow before expanding. Default to one primary persona, one painful problem, one core workflow, and a small v1 scope.
- Act like a skeptical product lead. Challenge vague personas, low-severity pain, weak urgency, hidden operational work, AI magic thinking, marketplace liquidity assumptions, and platform ambitions without a wedge.
- Ask no more than three related questions at once.
- Every user-facing question must include a recommended default and one-line rationale. Use: "I recommend X because Y. Confirm or redirect."
- Call out contradictions immediately. If a later answer conflicts with an earlier decision, explain the conflict and recommend which direction to keep for v1.
- Do not assume every idea deserves a PRD. If the idea is structurally weak, say why and recommend narrowing, reframing, or abandoning it.

## Output contract

`PRD.md` MUST conform to [standards/prd-schema](../../../standards/prd-schema/README.md). That schema is authoritative for:

- Frontmatter (`product`, `status`, `owner`, `version`, `last_reviewed`).
- Required and conditional section list.
- Conditional section omission rules (use `## Omitted sections` at the bottom).
- Versioning rules.

Use `assets/PRD.template.md` as the scaffold — it implements the schema.

## Progressive references

- Read `references/discovery-playbook.md` when the idea needs interactive clarification, persona/JTBD work, v1 scoping, non-goals, open-question resolution, or success metrics.
- Read `references/product-critique-patterns.md` when evaluating idea quality, risks, distribution, adoption, marketplace dynamics, AI claims, or hidden operational burden.
- Read `references/prd-quality-rubric.md` before emitting the final PRD and use it as the validation checklist.
- Read `assets/PRD.example.md` before drafting if you need a concrete style and length anchor — it shows what conditional-section omission and a tight internal-service PRD look like.

## Process

Progress:

- [ ] Step 1: Restate the idea in one sentence using only what the user said. If the target user, pain, or workflow shift is ambiguous or unstated, name the ambiguity instead of inventing specifics — persona and pain work happen in steps 2 and 3. Ask the user to confirm or redirect.
- [ ] Step 2: Identify the primary persona, context, job-to-be-done, and current workaround. Resolve multi-persona scope before continuing.
- [ ] Step 3: Define the problem and why-now without solutioning, feature references, or technology choices.
- [ ] Step 4: Narrow v1 scope to 3-5 outcomes, not features. Propose at least three non-goals with rationale.
- [ ] Step 5: Document constraints, assumptions, and risks. Recommend cuts if constraints conflict with scope.
- [ ] Step 6: Resolve implementation-shaping open questions where possible. Keep only explicitly deferred decisions for the final `Open Questions` section.
- [ ] Step 7: Challenge how the workflow actually reaches users.
    - For external products (SaaS, consumer, marketplace, AI tool): identify how the first 100 users realistically discover, adopt, or are required to use the workflow.
    - For internal tools, reference workloads, or system components: replace distribution with *integration and rollout* — which upstream/downstream services or teams consume this, and how is cutover staged?
- [ ] Step 8: Define 2-4 success metrics with unit, target, and timeframe.
- [ ] Step 9: Run a final critique pass against the original idea and confirmed decisions. Call out contradictions, weak positioning, bloated scope, distribution concerns, or unrealistic assumptions.
- [ ] Step 10: Generate `PRD.md` from `assets/PRD.template.md`. Validate against [standards/prd-schema](../../../standards/prd-schema/README.md) (frontmatter, required sections, conditional-section omission rules) AND against `references/prd-quality-rubric.md`. Revise until both pass or explicitly note any unresolved gap.

## Outputs

- `PRD.md` at `docs/product/<slug>/PRD.md`, with frontmatter and sections per [standards/prd-schema](../../../standards/prd-schema/README.md). Required sections: Problem, Users, JTBD, Scope, Non-goals, Constraints, Assumptions, Success Metrics, Open Questions. Conditional sections (include if material, otherwise omit with rationale): Why Now, Current Alternatives, Risks, Distribution and Adoption, Out of scope (future).

Output rules:

- Keep the PRD concise and decision-oriented.
- Focus on user pain, workflow outcomes, and v1 scope.
- Avoid implementation details unless a constraint changes product scope.
- Avoid feature catalogs, marketing language, and vague platform positioning.
- Include only intentionally deferred decisions in `Open Questions`.

## Quality checks

- [ ] `references/prd-quality-rubric.md` was loaded before finalizing.
- [ ] `PRD.md` validates against [standards/prd-schema](../../../standards/prd-schema/README.md): frontmatter present and complete; all required sections present; conditional sections either present with content or listed under `## Omitted sections` with rationale.
- [ ] `PRD.md` follows `assets/PRD.template.md`.
- [ ] Every user-facing question included a recommended answer and rationale.
- [ ] At least one meaningful critique or scope risk was surfaced, or the PRD explains why no major issue remains.
- [ ] Open Questions contains only decisions the user explicitly deferred.

## References

- `references/discovery-playbook.md`
- `references/product-critique-patterns.md`
- `references/prd-quality-rubric.md`
- `assets/PRD.template.md`
- `assets/PRD.example.md`
