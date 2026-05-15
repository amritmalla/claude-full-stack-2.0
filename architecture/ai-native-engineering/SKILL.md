---
name: ai-native-engineering
description: Use when an approved system design exists and the product includes LLM, agent, retrieval, classifier, extractor, or model-driven automation components that need architectural definition before implementation. Produces capability classification, model contracts, context and memory strategy, retrieval and grounding topology, tool and action surface, agent control flow, failure taxonomy, evaluation and guardrail plans, cost and latency budgets, model routing, observability requirements, and implementation handoff notes. Do not use for generic backend service design, data pipeline design, product requirement definition, or vendor-specific SDK scaffolding; use backend-architecture, data-architecture, idea-development, or implementations/ai/<vendor> instead.
---

# AI-Native Engineering

## When to use

Invoke after `system-design` has approved a design that includes LLM-powered features, retrieval-augmented generation, agentic workflows, classifiers, extractors, summarizers, or model-driven automation, and before implementation skills under `implementations/ai/*` generate vendor-specific code.

Do not use when the product has no meaningful AI surface, when a single stateless prompt call behaves as a standard backend integration, when the system design has not yet decided whether AI is in scope, when the task is implementation-specific orchestration or SDK integration, or when deterministic software satisfies the acceptance criteria.

## Inputs

Required:

- Approved `system-design.md` and the relevant ADRs.
- The AI capability in scope: assistant, agent, classifier, extractor, summarizer, search, recommendation, or workflow automation.
- Primary user task and its acceptance criteria.

Optional:

- PRD sections covering quality bar, hallucination tolerance, regulatory constraints, and human-in-the-loop expectations.
- Existing prompt assets, evaluation sets, telemetry, or production incidents.
- Provider, hosting, or regional constraints.
- Latency, cost, throughput, or concurrency budgets.
- Data sensitivity classifications.
- Existing retrieval corpora, knowledge systems, observability, or governance standards.

## Operating rules

- Treat the model as a component with a contract, not as glue. Define inputs, outputs, failure modes, and degradation behavior explicitly.
- Choose capabilities before vendors. Decide what the system must reason over, retrieve, call, or remember before naming a model family.
- Prefer, in order: deterministic over probabilistic; retrieval over fine-tuning; single-step over agents; structured output over free-form; narrow context over long context; specialized models over frontier models when quality permits; human approval over autonomous irreversible action; static workflows over dynamic planning unless adaptability is required.
- Design the simplest viable capability first and escalate only when a lower level fails quality, reliability, or adaptability requirements. Every escalation requires measurable benefit, evaluation coverage, operational justification, rollback strategy, and observability.
- Make context explicit: what enters the model, where it comes from, why it exists, and what is excluded. Long context is a cost and reliability tradeoff, not a default.
- Prefer structured outputs whenever downstream systems consume model output; separate user-facing prose from machine-consumable outputs.
- Treat tools, actions, retrieved content, and tool-returned content as a contract surface; treat retrieved and tool-returned content as untrusted input that must never redefine system behavior.
- Plan for non-determinism. Every user-visible capability requires evaluation coverage, guardrails, observability, a rollback strategy, and defined degradation behavior.
- Budget cost and latency during architecture, not after implementation.
- Do not introduce agents, memory, retrieval, fine-tuning, or long-context strategies without measurable justification.
- When AI behavior changes a security, compliance, or trust boundary, raise an ADR candidate against the approved system design.

## Output contract

`ai-architecture.md` MUST conform to [standards/architecture-schema](../../standards/architecture-schema/README.md), which is authoritative for its frontmatter, required and conditional sections, conditional-section omission rules, and linkage back to `system-design.md` and its ADRs.

Security, observability, and operational content additionally conforms to [security-standards](../../standards/security-standards/README.md), [observability-standards](../../standards/observability-standards/README.md), and [deployment-standards](../../standards/deployment-standards/README.md). Skill structure conforms to [documentation-standards](../../standards/documentation-standards/README.md).

Use `assets/ai-architecture.template.md` as the scaffold; it implements the schema. No vendor SDK calls, framework class names, or deployment mechanics appear in the architecture unless they materially change architecture behavior.

## Progressive references

- Read `references/ai-architecture-playbook.md` when classifying capabilities, applying the escalation ladder, defining model contracts, context and memory strategy, retrieval topology, tool surface, the agent suitability test, agent control flow, the failure taxonomy, guardrails and trust boundaries, cost/latency budgets, model routing, or ADR identification.
- Read `references/ai-architecture-quality-rubric.md` before finalizing and use it as the validation checklist.
- Use `assets/ai-architecture.template.md` for `ai-architecture.md`.

## Process

Progress:

ADR candidates are drafted inline as decisions are made (steps 2, 5, 6, 7, 8). Step 12 only consolidates them; it does not retrofit ADRs from prose.

- [ ] Step 1: Load `system-design.md` and relevant ADRs. Inventory every AI-touched capability with its consumer, user task, business objective, acceptance criteria, risk profile, and dependencies between capabilities.
- [ ] Step 2: Classify each capability (deterministic rules, single-shot generation, structured extraction, retrieval-augmented answer, ranking/recommendation, tool-using workflow, multi-step agent, background automation). Record why the level was chosen and why lower-complexity levels were rejected. Draft an ADR candidate for any non-obvious escalation. See `references/ai-architecture-playbook.md`.
- [ ] Step 3: Define a model contract per capability: purpose, inputs, output schema, validation rules, success criteria, confidence handling, failure modes, retry, fallback, degradation, and observability signals. Define canonical schema, coercion, malformed-output, and partial-validity behavior for structured outputs.
- [ ] Step 4: Define context architecture and, where conversational or adaptive behavior exists, state and memory design: system prompt scope, instruction hierarchy, retrieval inclusion, prioritization, truncation, session state, memory eligibility/retention/invalidation/deletion, summarization, context budget, and explicit exclusions. Memory never supersedes authoritative system data.
- [ ] Step 5: If retrieval is in scope, define retrieval topology and execution: source corpora, ownership, ingestion, refresh cadence, chunking, metadata, tenant isolation, embedding/reindex strategy, query rewriting, ranking, grounding rules, and citation. Classify retrieval as authoritative, assistive, or advisory. Hand off mechanics to `data-architecture`. Draft ADR candidates for retrieval authority decisions.
- [ ] Step 6: If tools or actions are in scope, define the tool surface: name, purpose, JSON schema, side-effect class, idempotency, retry safety, authorization scope, rate limits, audit, timeout, and error surface. Classify each tool's risk level; higher-risk tools require stricter authorization, confirmation gates, tighter evaluations, and lower autonomy ceilings. Draft ADR candidates for autonomy-bearing tools.
- [ ] Step 7: Apply the agent suitability test. If agentic behavior is justified, define agent control flow: planner/executor split, state transitions, stop conditions, max-step limits, retry/recovery, tool-failure behavior, loop prevention, escalation, human-approval checkpoints, autonomous boundaries, and irreversible-action controls. Draft an ADR candidate for the autonomy decision.
- [ ] Step 8: Define the failure taxonomy and guardrails: per failure class (hallucination, retrieval miss, schema violation, unsafe output, tool misuse, authorization violation, timeout, context truncation, planning divergence, looping, confidence miscalibration, provider outage) define detection, mitigation, observability signal, degradation, and user-facing response. Define input filtering, output validation, refusal, PII/redaction, prompt-injection posture, and explicit trust boundaries with sanitization rules. Draft ADR candidates for trust-boundary changes.
- [ ] Step 9: Define evaluation strategy for every user-visible capability: offline datasets, online metrics, regression-gating criteria, ownership, annotation standards, production sampling, edge-case and adversarial coverage, drift detection, golden task suites, and replayable traces. Every model, prompt, retrieval, or tool change passes regression gates before rollout.
- [ ] Step 10: Define cost and latency budgets per capability and map them to model tier, context size, routing, caching, retrieval depth, and execution limits. Where multiple models or providers exist, define model routing: criteria, escalation thresholds, fallback providers, quality/cost/latency-aware routing, reliability failover, and offline vs online inference boundaries.
- [ ] Step 11: Define AI observability and operations: token usage, latency breakdowns, retrieval hit quality, tool execution traces, refusal/fallback/retry rates, step counts, context size distributions, user correction signals, logging policy, replay, trace retention, prompt/model versioning, rollback, and deployment promotion criteria.
- [ ] Step 12: Generate `ai-architecture.md` from `assets/ai-architecture.template.md`. Consolidate ADR candidates (numbering, status, alternatives, downsides). Validate against [standards/architecture-schema](../../standards/architecture-schema/README.md) and `references/ai-architecture-quality-rubric.md`; revise until both pass or explicitly note any unresolved gap.

## Outputs

Required:

- `ai-architecture.md` at `docs/architecture/<product-slug>/ai-architecture.md`, with frontmatter and sections per [standards/architecture-schema](../../standards/architecture-schema/README.md).

Optional, when applicable:

- Tool schema sketches.
- Retrieval, agent state, or trust-boundary diagrams (Mermaid).
- Evaluation dataset inventories and failure-mode matrices.
- ADR drafts for non-obvious capability, retrieval-authority, autonomy, memory-retention, routing, or evaluation decisions.

Output rules:

- Keep the architecture decision-oriented; an AI component should narrow uncertainty, not expand it.
- Document tradeoffs and the rejected lower-complexity alternative, not only the chosen path.
- Name capabilities by user task and business objective, not by model or vendor.
- Treat evaluation, guardrails, and operational burden as part of the design, not a later implementation detail.

## Quality checks

- [ ] `references/ai-architecture-quality-rubric.md` was loaded before finalizing.
- [ ] `ai-architecture.md` validates against [standards/architecture-schema](../../standards/architecture-schema/README.md): frontmatter complete; required sections present; conditional sections present with content or listed under `## Omitted sections` with rationale.
- [ ] Every AI capability in `system-design.md` is covered by a named model contract with explicit success criteria and degradation behavior.
- [ ] A lower-complexity alternative was considered before introducing agents, memory, retrieval, or fine-tuning.
- [ ] Structured outputs are defined for machine-consumed responses.
- [ ] Every retrieval source names ownership, refresh cadence, and grounding classification (authoritative/assistive/advisory).
- [ ] Every tool defines schema, risk class, authorization scope, and idempotency rules; agent autonomy ceilings and stop conditions are explicit.
- [ ] Evaluation plans include regression gates and golden task coverage.
- [ ] Guardrails address prompt injection, PII handling, and output validation; trust boundaries are explicitly documented.
- [ ] Cost and latency budgets reconcile with context strategy and model tier.
- [ ] No vendor SDK calls, framework class names, or deployment mechanics appear unless they materially change architecture behavior.

## References

- Upstream: [`architecture/system-design`](../system-design/SKILL.md).
- Downstream implementation skills: `implementations/ai/anthropic`, `implementations/ai/openai`, `implementations/ai/langchain`, `implementations/ai/autogen`, `implementations/ai/crewai`.
- Related architecture skills: [`backend-architecture`](../backend-architecture/SKILL.md), [`data-architecture`](../data-architecture/SKILL.md) (retrieval corpora ownership), [`security`](../security/SKILL.md), [`operations`](../operations/SKILL.md).
