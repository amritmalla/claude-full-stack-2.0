# ai-rag-platform

## Summary

A RAG (retrieval-augmented generation) platform grounds an LLM's responses in a curated knowledge corpus: relevant content is retrieved at query time and supplied as context, reducing hallucination and enabling fresh, source-attributed answers.

## Problem & forces

A base LLM cannot answer over private, current, or large proprietary knowledge, and fine-tuning is slow and stale. The forces — grounded/attributable answers, freshness without retraining, and access control over knowledge — justify a retrieval layer in front of generation.

## When to use / When not to use

**Use when**

- Answers must be grounded in a private or frequently-changing corpus.
- Source attribution and freshness matter more than creative generation.
- Knowledge is too large or dynamic to fit in a prompt or fine-tune.

**Avoid when**

- The task needs no external knowledge (pure reasoning, transformation, chat).
- The corpus is tiny and static enough to fit directly in the prompt.
- Strict determinism is required — generation remains probabilistic.

## Structure

An ingestion pipeline chunks, embeds, and indexes sources; a query path retrieves top-k context and composes the grounded prompt.

```text
sources → chunk → embed → vector index          (ingestion, event-driven)
query → embed → retrieve top-k → prompt + context → LLM → answer + citations
```

## Key tradeoffs

Gain: grounded, attributable, fresh answers without retraining; access-controllable knowledge. Pay: retrieval quality dominates output quality, ingestion/index operational cost, chunking/embedding tuning, latency of the retrieve+generate path, evaluation difficulty.

## Failure modes & mitigations

- **Irrelevant retrieval** — wrong chunks poison the answer. Tune chunking, use hybrid (keyword+vector) retrieval and re-ranking; evaluate retrieval separately from generation.
- **Stale index** — corpus changed, index did not. Drive re-indexing from change events ([`event-driven`](../event-driven/README.md)).
- **Context overflow** — too much retrieved text. Cap and re-rank; compress context.
- **Unattributed claims** — answers without sources. Require citations and ground checks in evaluation.

## Related skills & patterns

- Skills: [`ai-native-engineering`](../../skills/architecture/ai-native-engineering/SKILL.md), [`data-architecture`](../../skills/architecture/data-architecture/SKILL.md), [`security`](../../skills/architecture/security/SKILL.md)
- Patterns: [`event-driven`](../event-driven/README.md) (ingestion/re-index pipeline), [`microservices`](../microservices/README.md), [`serverless-platform`](../serverless-platform/README.md)
