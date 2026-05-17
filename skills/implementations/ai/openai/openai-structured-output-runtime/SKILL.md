---
name: openai-structured-output-runtime
description: Use when implementing an OpenAI-backed AI capability that must return schema-bound JSON, typed objects, classifications, extraction results, or other machine-consumable responses from an approved ai-architecture.md. Produces provider SDK wiring, prompt structure, schema validation, retry and failure handling, malformed-output tests, and telemetry for latency, tokens, and validation failures. Do not use for generic model selection, AI architecture, RAG, tool calling, or agent workflow design.
---

# OpenAI Structured Output Runtime

## When to use

Invoke when `ai-architecture.md` defines a model contract with a structured
output schema and the chosen provider is OpenAI.

Do not use for free-form chat, retrieval topology design, tool execution, or
agent control flow.

## Inputs

Required:

- Approved `ai-architecture.md`.
- Capability name and model contract.
- Output schema or typed object definition.
- Target application language and framework.

Optional:

- Existing prompt assets.
- Existing validation library.
- Latency, cost, and retry budgets.
- Sample successful and failed outputs.

## Operating rules

- Preserve the model contract and output schema from `ai-architecture.md`. Do not widen, narrow, or reinterpret the schema. If the schema is missing a field, type, or nullability decision, raise an ADR candidate instead of inventing it.
- Validation fails closed. A response that does not satisfy the schema is an error, never a best-effort partial returned downstream.
- Retries are bounded and explicit. Schema-repair retries have a maximum attempt count and a deadline; exhaustion routes to the degradation behavior declared in the architecture.
- Provider features serve the contract, not the reverse. OpenAI structured-output / JSON-schema / response-format modes are a means to satisfy the approved schema, not a reason to change it.
- Decoding is a decision. Temperature, seed, and any determinism settings the contract requires are set explicitly, never left to provider defaults.
- No sensitive data in telemetry. Prompt and model version and validation outcomes are logged; raw payloads, secrets, and PII are redacted.

## Output contract

The implementation MUST conform to:

- [api-standards](../../../../../standards/api-standards/README.md) — the output schema is an external contract surface; versioning and breaking-change policy apply.
- [security-standards](../../../../../standards/security-standards/README.md) — no secrets or PII in prompts, logs, or stored outputs without redaction; provider credentials injected at deploy time, never committed.
- [observability-standards](../../../../../standards/observability-standards/README.md) — structured logs and metrics for latency, token usage, validation failures, and model/prompt version; trace propagation through the call.
- [deployment-standards](../../../../../standards/deployment-standards/README.md) — prompt and model versions are deploy-time configuration, not hardcoded.
- [naming-conventions](../../../../../standards/naming-conventions/README.md) — capability, metric, and schema names follow project rules.

Upstream contract: `ai-architecture.md` is the source of truth for the capability, output schema, model tier, degradation behavior, and latency/cost budgets. If it is silent on any of these, this skill pauses and raises an ADR candidate rather than inventing the decision.

## Process

1. Load `ai-architecture.md` and identify the capability, output schema, success criteria, and failure modes.
2. Verify that the architecture names the model tier, prompt inputs, output shape, and degradation behavior.
3. Choose the target SDK integration pattern for the application language and framework.
4. Implement schema-bound request and response handling.
5. Add validation and explicit failure handling for malformed, partial, or low-confidence outputs.
6. Add tests for valid output, malformed output, refusal/degradation behavior, and retry exhaustion.
7. Add telemetry for model name, prompt version, latency, token usage, validation failures, and fallback path.
8. Document unresolved architecture gaps as ADR candidates instead of silently filling them in.

## Outputs

- OpenAI SDK integration for the structured-output capability.
- Prompt or message template files.
- Schema or validator definitions.
- Typed response adapter.
- Tests for success and failure paths.
- Telemetry notes for tokens, latency, validation failures, and model version.

## Quality checks

- [ ] The implementation consumes a named model contract from `ai-architecture.md`.
- [ ] Output validation fails closed when the response does not match the schema.
- [ ] Tests cover valid output, malformed output, refusal or fallback, and retry exhaustion.
- [ ] Logs and metrics include prompt/model version without recording unredacted secrets or sensitive payloads.
- [ ] Any missing schema, budget, or degradation decision is documented as an ADR candidate.

## References

- Upstream: [`architecture/ai-native-engineering`](../../../../architecture/ai-native-engineering/SKILL.md) — capability, model contract, output schema, degradation behavior, budgets.
- Related architecture: [`architecture/quality-engineering`](../../../../architecture/quality-engineering/SKILL.md) — malformed-output and contract coverage.
- Related implementation skills: [`openai-tool-calling-runtime`](../openai-tool-calling-runtime/SKILL.md) (when the schema is a tool argument), [`openai-rag-runtime`](../openai-rag-runtime/SKILL.md) (when the grounded answer is schema-bound), [`openai-evals-and-observability`](../openai-evals-and-observability/SKILL.md) (regression gates for output quality), [`langchain-agent-runtime`](../../langchain/langchain-agent-runtime/SKILL.md) (when structured output is an agent step).
