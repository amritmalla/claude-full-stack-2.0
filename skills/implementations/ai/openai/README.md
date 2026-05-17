# openai

> Status: active — all 4 archetypes authored.

## Purpose

Implements approved AI architecture using the OpenAI ecosystem. This is the
provider-specific execution layer for model calls, structured outputs, tool
calling, RAG runtime behavior, evals, and observability.

Architecture decisions come from
[`architecture/ai-native-engineering`](../../../architecture/ai-native-engineering/SKILL.md)
and are taken as inputs here.

## Skills

- [`openai-structured-output-runtime`](openai-structured-output-runtime/SKILL.md) - implements schema-bound JSON, typed objects, extraction, classification, validation, retries, tests, and telemetry.
- [`openai-tool-calling-runtime`](openai-tool-calling-runtime/SKILL.md) - implements OpenAI tool/function calling with tool schemas, authorization, idempotency, audit logging, and failure tests.
- [`openai-rag-runtime`](openai-rag-runtime/SKILL.md) - implements OpenAI-backed retrieval-augmented generation with retriever adapters, context packing, grounding prompts, citations, evals, and telemetry.
- [`openai-evals-and-observability`](openai-evals-and-observability/SKILL.md) - adds regression evals, prompt/model versioning, token and cost telemetry, tracing, dashboards, and runbook notes.

## Upstream inputs

- Approved `ai-architecture.md`.
- Model contracts, prompt/context strategy, tool surface, retrieval rules, eval plan, guardrails, and cost/latency budgets.
- Related handoffs from `data-architecture`, `security`, `quality-engineering`, and `operations` when relevant.

## Design constraints

- Do not use OpenAI skills to decide whether a feature should use AI.
- Do not invent tool schemas, retrieval rules, or eval gates missing from `ai-architecture.md`.
- Keep direct provider integrations clear before adding framework abstractions.
