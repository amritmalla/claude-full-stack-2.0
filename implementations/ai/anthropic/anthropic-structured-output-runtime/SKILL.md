---
name: anthropic-structured-output-runtime
description: Use when implementing an Anthropic-backed AI capability that must return schema-bound JSON, typed objects, classifications, or extraction results from an approved ai-architecture.md. Produces Messages API wiring, tool-use or prefill-based structured output, schema validation, prompt-cache placement, extended-thinking handling, retry and failure handling, malformed-output tests, and telemetry for latency, tokens, cache hits, and validation failures. Do not use for generic model selection, AI architecture, RAG, free-form tool execution, or agent workflow design.
---

# Anthropic Structured Output Runtime

## When to use

Invoke when `ai-architecture.md` defines a model contract with a structured
output schema and the chosen provider is Anthropic (Claude via the Messages
API).

Do not use for free-form chat, retrieval topology design, multi-tool execution,
or agent control flow.

## Inputs

Required:

- Approved `ai-architecture.md`.
- Capability name and model contract.
- Output schema or typed object definition.
- Target application language and framework.

Optional:

- Existing prompt assets and few-shot examples.
- Existing validation library.
- Latency, cost, and retry budgets.
- Prompt-cache strategy from the architecture (cacheable system prompt, schema, exemplars).
- Whether extended thinking is required for the capability.
- Sample successful and failed outputs.

## Operating rules

- Preserve the model contract and output schema from `ai-architecture.md`. Do not widen, narrow, or reinterpret the schema. If the schema is missing a field, type, or nullability decision, raise an ADR candidate instead of inventing it.
- Structured output is produced through a deliberate mechanism, stated explicitly: a forced single-tool call whose `input_schema` is the approved schema (default), or assistant-message prefill, or strict prompt plus validation. Provider mechanics serve the contract, not the reverse.
- Validation fails closed. A response that does not satisfy the schema is an error, never a best-effort partial returned downstream.
- Retries are bounded and explicit. Schema-repair retries have a maximum attempt count and a deadline; exhaustion routes to the degradation behavior declared in the architecture.
- Prompt caching is a decision, not an accident. `cache_control` breakpoints are placed only on stable prefixes (system prompt, schema, exemplars) per the architecture's cache strategy; cache placement never changes output semantics, and a cache miss is never a correctness failure.
- Extended thinking is handled, not ignored. If the capability uses extended thinking, thinking blocks are preserved or stripped per the architecture, and tool-use-for-structured-output is reconciled with thinking-mode constraints explicitly.
- Decoding is a decision. `temperature`, `top_p`, `max_tokens`, and `stop_sequences` are set explicitly where the contract requires determinism, never left to defaults.
- No sensitive data in telemetry. Prompt and model version, cache outcome, and validation results are logged; raw payloads, secrets, and PII are redacted.

## Output contract

The implementation MUST conform to:

- [api-standards](../../../../standards/api-standards/README.md) — the output schema is an external contract surface; versioning and breaking-change policy apply.
- [security-standards](../../../../standards/security-standards/README.md) — no secrets or PII in prompts, logs, or stored outputs without redaction; Anthropic API credentials injected at deploy time, never committed.
- [observability-standards](../../../../standards/observability-standards/README.md) — structured logs and metrics for latency, input/output tokens, cache-read/write tokens, validation failures, and model/prompt version; trace propagation through the call.
- [deployment-standards](../../../../standards/deployment-standards/README.md) — model id, prompt version, and cache strategy are deploy-time configuration, not hardcoded.
- [naming-conventions](../../../../standards/naming-conventions/README.md) — capability, metric, and schema names follow project rules.

Upstream contract: `ai-architecture.md` is the source of truth for the capability, output schema, model tier, prompt-cache strategy, extended-thinking requirement, degradation behavior, and latency/cost budgets. If it is silent on any of these, this skill pauses and raises an ADR candidate rather than inventing the decision.

## Process

1. Load `ai-architecture.md` and identify the capability, output schema, success criteria, failure modes, and prompt-cache strategy.
2. Verify the architecture names the model tier, prompt inputs, output shape, extended-thinking requirement, and degradation behavior.
3. Choose the structured-output mechanism: forced single-tool call with the schema as `input_schema` (default), assistant prefill, or strict-prompt-plus-validation. Record the choice and why.
4. Implement the Messages API request: system prompt, messages, the chosen mechanism, and explicit decoding settings.
5. Place `cache_control` breakpoints on stable prefixes per the architecture's cache strategy; confirm cache placement does not alter output semantics.
6. If extended thinking is required, reconcile thinking blocks with the structured-output mechanism and the architecture's thinking-retention rule.
7. Add validation and explicit failure handling for malformed, partial, or low-confidence outputs.
8. Add tests for valid output, malformed output, refusal/degradation behavior, retry exhaustion, and a cache-miss path.
9. Add telemetry for model id, prompt version, latency, input/output tokens, cache-read/write tokens, validation failures, and fallback path.
10. Document unresolved architecture gaps as ADR candidates instead of silently filling them in.

## Outputs

- Anthropic Messages API integration for the structured-output capability.
- Prompt or message template files, with cache-breakpoint placement noted.
- Schema or validator definitions (and the tool definition when the tool-use mechanism is chosen).
- Typed response adapter.
- Tests for success, malformed output, refusal/fallback, retry exhaustion, and cache miss.
- Telemetry notes for tokens, cache outcomes, latency, validation failures, and model version.

Output rules:

- The structured-output mechanism is stated explicitly; it is never left implicit.
- No magic decoding values: every non-default `temperature`/`top_p`/`max_tokens` is tied to a contract requirement.
- `cache_control` appears only on stable prefixes; never on per-request variable content.
- No Anthropic API key or environment-specific endpoint committed to source.

## Quality checks

- [ ] The implementation consumes a named model contract from `ai-architecture.md`.
- [ ] The structured-output mechanism (forced tool, prefill, or strict-prompt) is explicit and justified.
- [ ] Output validation fails closed when the response does not match the schema.
- [ ] Tests cover valid output, malformed output, refusal or fallback, retry exhaustion, and a cache-miss path.
- [ ] `cache_control` breakpoints sit only on stable prefixes and do not change output semantics.
- [ ] Extended-thinking interaction is handled per the architecture (or explicitly N/A).
- [ ] Logs and metrics include prompt/model version and cache outcome without recording unredacted secrets or sensitive payloads.
- [ ] Any missing schema, cache, thinking, budget, or degradation decision is documented as an ADR candidate.

## References

- Upstream: [`architecture/ai-native-engineering`](../../../../architecture/ai-native-engineering/SKILL.md) — capability, model contract, output schema, cache strategy, degradation behavior, budgets.
- Related architecture: [`architecture/quality-engineering`](../../../../architecture/quality-engineering/SKILL.md) — malformed-output and contract coverage.
- Cross-provider counterpart: [`openai-structured-output-runtime`](../../openai/openai-structured-output-runtime/SKILL.md) — same archetype, OpenAI mechanics.
- Related implementation skills: [`openai-evals-and-observability`](../../openai/openai-evals-and-observability/SKILL.md) (regression gates for output quality), [`langchain-agent-runtime`](../../langchain/langchain-agent-runtime/SKILL.md) (when structured output is an agent step). Planned anthropic siblings are listed in the [anthropic stack README](../README.md).
