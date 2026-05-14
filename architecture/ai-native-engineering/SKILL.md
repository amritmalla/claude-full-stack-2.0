---
name: ai-native-engineering
description: Use when an approved system design exists and the product includes LLM, agent, or retrieval components that need architectural definition before implementation. Produces model and provider selection, prompt and context strategy, retrieval and grounding topology, tool and action surface, agent control flow, evaluation and guardrail plan, cost and latency budgets, and implementation handoff notes. Do not use for generic backend service design, data pipeline design, or vendor-specific SDK scaffolding; use backend-architecture, data-architecture, or implementations/ai/<vendor> instead.
---

# AI-Native Engineering

## When to use

Invoke after `system-design` has approved a design that includes LLM-powered features, retrieval-augmented generation, agentic workflows, or model-driven automation, and before implementation skills under `implementations/ai/*` generate vendor-specific code.

Do not use when the product has no AI surface, when only a single stateless prompt call is needed (treat as backend integration), or when the system design itself has not yet decided whether AI is in scope.

## Inputs

Required:

- Approved `system-design.md`.
- The AI capability in scope: assistant, agent, classifier, extractor, summarizer, search, or workflow automation.
- Primary user task and acceptance criteria for that task.

Optional:

- PRD sections covering quality bar, tolerance for hallucination, regulatory constraints, and human-in-the-loop expectations.
- Existing prompt assets, evaluation sets, or telemetry from prior iterations.
- Provider, model, or hosting constraints (self-hosted, regional, on-prem).
- Latency, cost, and throughput budgets.
- Data sensitivity classification for inputs and retrieval corpora.

## Operating rules

- Treat the model as a component with a contract, not as glue. Define inputs, outputs, failure modes, and degradation behavior the same way you would for any other dependency.
- Choose capabilities before vendors. Decide what the system must reason over, retrieve, call, or remember before naming a model family.
- Make context explicit. Define what enters the prompt, where it comes from, how it is shaped, and what is excluded. Long context is a design choice with cost.
- Treat tools and actions as a contract surface. Each tool has a name, schema, side-effect class, idempotency rule, and authorization scope.
- Plan for non-determinism. Every output path needs an evaluation strategy, a guardrail, and a fallback when the model is wrong, slow, or unavailable.
- Budget cost and latency at design time. Token, request, and wall-clock budgets per user-visible task drive model and retrieval choices, not the other way around.
- Do not introduce agents, multi-step planning, or fine-tuning without an evaluation plan that can detect regressions.
- When AI behavior changes a security or compliance boundary, raise it as an ADR candidate against the approved system design.

## Process

1. Load `system-design.md` and identify each AI-touched capability, its consumer, and the user task it supports.
2. Classify each capability: single-shot generation, structured extraction, retrieval-augmented answer, tool-using agent, or background automation. Record the classification and why.
3. Define the model contract per capability: required inputs, output shape and schema, success criteria, failure modes, and degradation behavior when the model is unavailable or low-confidence.
4. Decide the context strategy: system prompt scope, user input handling, retrieval inclusion rules, memory or session state, and explicit exclusions.
5. If retrieval is in scope, define the retrieval topology: source corpora, ingestion ownership, chunking and indexing strategy, query rewriting, ranking, and grounding rules. Hand off implementation details to `data-architecture`.
6. If tools or actions are in scope, define the tool surface: tool name, JSON schema, side-effect class, idempotency, authorization, rate limits, and audit expectations.
7. If agentic control flow is in scope, define the loop: planner vs executor split, stop conditions, max steps, recovery on tool failure, and human-in-the-loop checkpoints.
8. Define the evaluation plan: offline eval set composition, online metrics, regression-gating criteria, and ownership of the eval set.
9. Define guardrails: input filtering, output validation, refusal behavior, PII handling, prompt-injection posture, and logging redaction.
10. Define cost and latency budgets per capability and map them to model tier, context size, retrieval depth, and tool call limits.
11. Define operational concerns: telemetry signals, prompt and response logging policy, replay strategy, prompt and model versioning, and rollback path.
12. Produce `ai-architecture.md` describing the above with explicit handoffs to `implementations/ai/<vendor>`, `backend-architecture`, `data-architecture`, `security`, and `operations`.

## Outputs

Required:

- `ai-architecture.md` covering capabilities, model contracts, context strategy, retrieval topology if applicable, tool surface if applicable, agent control flow if applicable, evaluation plan, guardrails, budgets, and handoff notes.

Optional, when applicable:

- Tool schema sketches.
- Retrieval pipeline diagram or narrative.
- Evaluation set inventory.
- ADR drafts for non-obvious model, retrieval, or agent decisions.

## Quality checks

- [ ] Every AI-touched capability in `system-design.md` is covered by a named model contract.
- [ ] Each model contract names its inputs, output schema, success criteria, failure mode, and degradation behavior.
- [ ] Every retrieval source names its owner, refresh cadence, and grounding rule.
- [ ] Every tool names its schema, side-effect class, idempotency rule, and authorization scope.
- [ ] An evaluation plan exists for every capability that ships to users, with named metrics and a regression-gating criterion.
- [ ] Guardrails address input filtering, output validation, prompt-injection posture, and PII handling.
- [ ] Cost and latency budgets are stated per capability and reconcile with the chosen model tier and context strategy.
- [ ] No vendor SDK calls, framework class names, or deployment mechanics appear in the architecture unless they materially change behavior.

## References

- Upstream: [`architecture/system-design`](../system-design/SKILL.md).
- Downstream implementation skills: `implementations/ai/anthropic`, `implementations/ai/openai`, `implementations/ai/langchain`, `implementations/ai/autogen`, `implementations/ai/crewai`.
- Related architecture skills: [`backend-architecture`](../backend-architecture/SKILL.md), `data-architecture`, `security`, `operations`.
