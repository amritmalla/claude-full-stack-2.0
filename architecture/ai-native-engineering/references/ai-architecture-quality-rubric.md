# AI Architecture Quality Rubric

Load this before emitting `ai-architecture.md`. Revise until each check passes or the unresolved gap is explicitly documented.

## Coverage and classification

- [ ] Every AI-touched capability in `system-design.md` is covered by a named model contract.
- [ ] Each capability is classified to exactly one level of the escalation ladder.
- [ ] Each classification records why lower-complexity levels were rejected.
- [ ] No agent, memory, retrieval, or fine-tuning is introduced without a measured failure of the simpler alternative.

## Contract quality

- [ ] Every model contract names inputs, output schema, success criteria, failure modes, and degradation behavior.
- [ ] Confidence handling, retry, and fallback are explicit per contract.
- [ ] Structured outputs define canonical schema, coercion, malformed-output, and partial-validity behavior.
- [ ] User-facing prose is separated from machine-consumable output.

## Context, state, and retrieval

- [ ] Context budget, prioritization, truncation, and explicit exclusions are defined.
- [ ] Memory, where present, defines retention, invalidation, deletion, user visibility, and never supersedes authoritative system data.
- [ ] Every retrieval source names ownership, refresh cadence, and grounding classification (authoritative/assistive/advisory).
- [ ] Retrieval implementation mechanics are handed off to `data-architecture`, not specified here.

## Tools, agents, and autonomy

- [ ] Every tool defines schema, side-effect class, idempotency, authorization scope, and risk level.
- [ ] Higher-risk tools carry stricter authorization, confirmation gates, and lower autonomy ceilings.
- [ ] Agents are justified by the suitability test, not used for deterministic or predictable workflows.
- [ ] Agent control flow defines stop conditions, max-step limits, escalation, and irreversible-action controls.

## Failure, evaluation, and guardrails

- [ ] Each failure class defines detection, mitigation, observability signal, degradation, and user-facing response.
- [ ] Every user-visible capability has offline datasets, online metrics, and a regression-gating criterion.
- [ ] Golden task suites and replayable traces are defined; model/prompt/retrieval/tool changes pass regression gates before rollout.
- [ ] Guardrails address input filtering, output validation, PII/redaction, and prompt-injection posture.
- [ ] Trust boundaries are explicitly identified with sanitization rules; retrieved or tool-returned text cannot redefine system behavior.

## Budgets, routing, and operations

- [ ] Cost and latency budgets are stated per capability and reconcile with model tier, context size, and retrieval depth.
- [ ] Model routing, where multiple models or providers exist, defines criteria, fallback, and failover.
- [ ] Observability covers token usage, latency, retrieval quality, tool traces, refusal/fallback/retry rates, and rollback.
- [ ] No vendor SDK calls, framework class names, or deployment mechanics appear unless they materially change architecture behavior.

## Linkage and decisions

- [ ] `ai-architecture.md` conforms to [architecture-schema](../../../standards/architecture-schema/README.md): frontmatter complete, required sections present, conditional sections present or omitted with rationale.
- [ ] Every ADR candidate has Context, Decision, Consequences (including downsides), and Alternatives considered.
- [ ] Every capability traces to the approved system design or is marked as an open decision.

## Failure handling

If a check fails:

1. Identify the missing or weak decision.
2. Ask the user for clarification if it cannot be inferred from `system-design.md` or the PRD.
3. Revise `ai-architecture.md` or the relevant ADR.
4. Keep unresolved questions explicit; do not hide them as assumptions.
