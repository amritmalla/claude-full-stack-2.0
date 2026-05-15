# langchain

> Status: scaffold

## Purpose

Implements approved AI architecture using the LangChain ecosystem. This layer
owns framework orchestration such as chains, graphs, tools, memory, agent
control flow, tracing, and framework-specific eval wiring.

Architecture decisions come from
[`architecture/ai-native-engineering`](../../../architecture/ai-native-engineering/SKILL.md)
and are taken as inputs here.

## Skills

- [`langchain-agent-runtime`](langchain-agent-runtime/SKILL.md) - implements an approved agent control flow with graph or chain structure, tool registry, memory/session handling, stop conditions, max-step enforcement, tracing, and safety tests.

## Planned skills

- `langchain-rag-pipeline` - RAG chain and retriever orchestration once a reference RAG workflow exists.
- `langchain-eval-harness` - framework-specific eval wiring once the OpenAI eval baseline is stable.

## Upstream inputs

- Approved `ai-architecture.md`.
- Agent control flow, tool surface, memory/session policy, stop conditions, eval plan, and operational constraints.

## Design constraints

- Do not introduce LangChain just because an AI feature exists.
- Use direct provider skills when the capability does not need framework-level orchestration.
- Refuse to implement agents without max steps, stop conditions, tool authorization, and eval criteria.
