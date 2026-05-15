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

- Upstream: [`architecture/ai-native-engineering`](../../../../architecture/ai-native-engineering/SKILL.md).
