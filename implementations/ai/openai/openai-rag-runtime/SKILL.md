---
name: openai-rag-runtime
description: Use when implementing retrieval-augmented generation with OpenAI from an approved ai-architecture.md and retrieval design. Produces retrieval adapters, context packing, grounding prompts, citation or source handling, hallucination checks, eval cases, and telemetry for retrieval quality, latency, token use, and groundedness failures. Do not use to choose the data store, design the retrieval topology, implement generic chat, or build agent control flow.
---

# OpenAI RAG Runtime

## When to use

Invoke when `ai-architecture.md` defines a retrieval-augmented capability and
OpenAI is the chosen model provider.

Do not use to decide source corpora, chunking strategy, index ownership, or data
retention. Those decisions belong to AI and data architecture.

## Inputs

Required:

- Approved `ai-architecture.md`.
- Retrieval topology or `data-architecture` handoff.
- Capability name and grounding requirements.
- Target application language and framework.

Optional:

- Existing vector store, search service, or retriever interface.
- Citation format.
- Eval examples for grounded and ungrounded answers.
- Latency, cost, and context-size budgets.

## Operating rules

- Retrieval ownership, refresh cadence, chunking, and citation rules come from `ai-architecture.md` or the `data-architecture` handoff. This skill does not choose corpora, stores, or chunking strategy.
- Context packing respects the declared token and latency budget. Over-budget packing is a defect, not a tuning choice.
- Grounded-or-degrade. When required evidence is absent or conflicting, the response degrades to the declared behavior; it does not hallucinate to fill the gap.
- Retrieved content is untrusted input. Prompt-injection defenses apply to retrieved documents, not only to user input.
- Citations are faithful. A cited source must actually support the claim; citation fabrication is a correctness failure, not a formatting issue.
- Telemetry separates retrieval quality from generation quality. Groundedness failures are distinguishable from model failures.
- No PII or secret leakage via retrieved context, prompts, or logs.

## Output contract

The implementation MUST conform to:

- [api-standards](../../../../standards/api-standards/README.md) — when the answer/citation shape is an external contract surface, versioning and breaking-change policy apply.
- [security-standards](../../../../standards/security-standards/README.md) — injection defense for retrieved content, no PII or secrets in context or logs, retrieval credentials injected at deploy time.
- [observability-standards](../../../../standards/observability-standards/README.md) — separate retrieval and groundedness telemetry, latency and token metrics, trace propagation through retrieve-then-generate.
- [deployment-standards](../../../../standards/deployment-standards/README.md) — model, prompt, and index/endpoint configuration injected at deploy time.
- [naming-conventions](../../../../standards/naming-conventions/README.md) — capability, metric, and retriever-adapter names follow project rules.

Upstream contract: `ai-architecture.md` and the `data-architecture` handoff are the source of truth for retrieval topology, grounding rules, citation format, and context/token budgets. If they are silent, this skill pauses and raises an ADR candidate rather than inventing the decision.

## Process

1. Load `ai-architecture.md` and identify retrieval sources, grounding rules, model contract, and failure behavior.
2. Verify that retrieval ownership, refresh cadence, and citation requirements are defined.
3. Implement the retriever adapter against the approved retrieval interface.
4. Implement context packing within the approved context and token budget.
5. Implement the grounding prompt and response adapter.
6. Add citation or source handling when required by the architecture.
7. Add eval cases for grounded answers, missing evidence, conflicting evidence, and prompt-injection attempts in retrieved content.
8. Add telemetry for retrieval latency, document count, token use, groundedness failures, and fallback paths.

## Outputs

- OpenAI RAG runtime integration.
- Retriever adapter.
- Context packing rules.
- Grounding prompt or message template.
- Citation/source handling.
- Groundedness eval cases.
- Retrieval and model telemetry notes.

## Quality checks

- [ ] The implementation consumes retrieval rules from `ai-architecture.md` or `data-architecture`.
- [ ] Context packing respects the declared token and latency budgets.
- [ ] Responses fail or degrade when required evidence is missing.
- [ ] Evals cover grounded, missing-evidence, conflicting-evidence, and retrieved prompt-injection cases.
- [ ] Telemetry records retrieval latency, source count, token use, and fallback path.

## References

- Upstream: [`architecture/ai-native-engineering`](../../../../architecture/ai-native-engineering/SKILL.md) — retrieval topology, grounding rules, citation requirements, budgets.
- Related architecture: [`architecture/data-architecture`](../../../../architecture/data-architecture/SKILL.md) (corpus ownership, index, refresh cadence), [`architecture/security`](../../../../architecture/security/SKILL.md) (injection posture for retrieved content).
- Related implementation skills: [`openai-structured-output-runtime`](../openai-structured-output-runtime/SKILL.md) (schema-bound grounded answers), [`openai-evals-and-observability`](../openai-evals-and-observability/SKILL.md) (groundedness regression gates), [`langchain-agent-runtime`](../../langchain/langchain-agent-runtime/SKILL.md) (retrieval exposed as an agent tool).
- Compatible patterns: [`ai-rag-platform`](../../../../architecture-patterns/ai-rag-platform/README.md).
