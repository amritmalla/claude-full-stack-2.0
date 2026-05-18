---
name: anthropic-rag-runtime
description: Use when an approved ai-architecture.md defines an Anthropic Claude retrieval-augmented capability. Produces a retrieval adapter, context packing, grounding prompt, Citations-API sourcing, a hallucination gate, and retrieval evals. Not for tool execution, schema-only output, or agent design.
---

# Anthropic RAG Runtime

## When to use

Invoke when `ai-architecture.md` defines a retrieval-augmented capability with a
grounding requirement and the chosen provider is Anthropic (Claude via the
Messages API and the Citations API).

Do not use to design retrieval topology, choose the corpus or chunking strategy,
decide whether a feature should use RAG, or build agent control flow. Those are
upstream decisions from `ai-architecture.md` and `data-architecture`.

## Inputs

Required:

- Approved `ai-architecture.md`.
- Capability name and model contract.
- Retrieval topology, corpus ownership, and chunking decision (from `data-architecture` via the AI architecture).
- Grounding requirement and citation policy.
- Answer contract (the shape of the answer plus its citation/source fields).
- Target application language and framework.

Optional:

- Existing retriever or vector store client.
- Existing prompt assets and grounding exemplars.
- Long-context packing budget, context ordering rule, and truncation policy.
- Prompt-cache strategy from the architecture (when the corpus is stable within a session).
- Hallucination/grounding gate thresholds and the retrieval eval dataset.
- Latency, cost, and retry budgets.

## Operating rules

- Preserve the retrieval rules, corpus ownership, chunking, grounding requirement, citation policy, and answer contract from `ai-architecture.md` and the `data-architecture` handoff. Do not invent a retriever, a chunking scheme, a grounding threshold, or a citation format. A missing decision is an ADR candidate, not an implementation choice.
- Grounding is enforced, not hoped for. The answer is constrained to the retrieved context; an answer that cannot be supported by the retrieved context follows the architecture's declared behavior (abstain, surface "not in corpus", or escalate), never a free-form guess.
- Citations are first-class, produced through the Anthropic **Citations API** (`citations: {enabled: true}` on retrieved document blocks), not prompt-engineered. The model emits citation references bound to source spans; the answer adapter carries them as structured fields, never as scraped inline text.
- Context packing is a budgeted decision. The packing budget, document ordering, and truncation policy come from the architecture. Retrieved content is packed up to the budget within Claude's long-context window in the declared order; over-budget content is truncated by the declared policy, never silently dropped at random.
- Prompt caching is a decision, not an accident. `cache_control` is placed on the retrieved-context prefix ONLY when the corpus is stable within a session (e.g. a fixed document set reused across turns); it is never placed on a per-query variable prefix (the question, per-request retrieval results). Cache placement never changes answer or citation semantics, and a cache miss is never a correctness failure.
- The hallucination/grounding gate fails closed. Retrieval evals run the declared dataset; an answer that fails the grounding check is a failure to be handled by the declared degradation path, not a result returned downstream.
- Extended thinking is handled, not ignored. If the capability uses extended thinking for synthesis over retrieved context, thinking blocks are preserved or stripped per the architecture, and their interaction with citation extraction is reconciled explicitly (the adapter selects citation-bearing text blocks, not thinking blocks). If not used, state N/A.
- Decoding is a decision. `temperature`, `top_p`, `max_tokens`, and `stop_sequences` are set explicitly where the contract requires deterministic or bounded grounded answers, never left to defaults.
- No sensitive data leakage. Retrieved context can carry secrets or PII; it is never logged unredacted, and access scoping on the corpus is enforced by the retriever, not the prompt. Prompt and model version, cache outcome, retrieval and grounding metrics are logged; raw documents, raw answers, secrets, and PII are redacted.

## Output contract

The implementation MUST conform to:

- [api-standards](../../../../../standards/api-standards/README.md) — the answer-plus-citation shape is an external contract surface; versioning and breaking-change policy apply.
- [security-standards](../../../../../standards/security-standards/README.md) — no secrets or PII leaked via retrieved context, prompts, logs, or stored answers without redaction; corpus access scoping enforced at retrieval; Anthropic API credentials injected at deploy time, never committed.
- [observability-standards](../../../../../standards/observability-standards/README.md) — structured logs and metrics for retrieval latency, input/output tokens, cache-read/write tokens, grounding/hallucination outcomes, citation coverage, and model/prompt version; trace propagation through retrieval and generation.
- [deployment-standards](../../../../../standards/deployment-standards/README.md) — model id, prompt version, cache strategy, and retriever endpoint are deploy-time configuration, not hardcoded.
- [naming-conventions](../../../../../standards/naming-conventions/README.md) — capability, metric, retriever, and answer-schema names follow project rules.

Upstream contract: `ai-architecture.md` (with the `data-architecture` handoff) is the source of truth for the capability, retrieval rules, corpus ownership, chunking, grounding requirement, citation policy, answer contract, context-packing budget, prompt-cache strategy, extended-thinking requirement, hallucination gate, degradation behavior, and latency/cost budgets. If it is silent on any of these, this skill pauses and raises an ADR candidate rather than inventing the decision.

## Progressive references

- Read `references/anthropic-rag-runtime-playbook.md` when implementing any owned area or checking the anti-pattern list.
- Read `references/anthropic-rag-runtime-quality-rubric.md` before declaring the integration complete.
- Use `assets/anthropic-rag-runtime.template.md` as the retrieval-adapter, context-packing, Citations-API request, grounding-gate, telemetry, and eval-matrix reference.

## Process

1. Load `ai-architecture.md` and the `data-architecture` handoff; identify the capability, retrieval rules, corpus ownership, chunking, grounding requirement, citation policy, answer contract, and prompt-cache strategy.
2. Verify the architecture names the model tier, packing budget, context ordering and truncation policy, extended-thinking requirement, hallucination gate, and degradation behavior.
3. Implement the retrieval adapter against the declared retriever, preserving corpus access scoping; do not re-chunk or re-rank beyond what the architecture declares.
4. Pack retrieved documents into the long-context window up to the declared budget, in the declared order, applying the declared truncation policy.
5. Build the Messages API request with the grounding system prompt and retrieved documents as document content blocks with the Citations API enabled.
6. Place `cache_control` on the retrieved-context prefix only when the corpus is stable within the session; confirm it is never on the per-query variable prefix and does not alter answer or citation semantics.
7. If extended thinking is required, reconcile thinking blocks with citation extraction per the architecture's retention rule.
8. Build the answer adapter that carries structured citations from the Citations API response; enforce the grounding gate and the declared abstain/degradation behavior.
9. Add the retrieval eval suite (grounding, citation coverage, refusal on out-of-corpus) and tests for grounded answer, ungrounded/abstain, citation-missing, retrieval-empty, retry exhaustion, and a cache-miss path.
10. Add telemetry for model id, prompt version, retrieval latency, input/output tokens, cache-read/write tokens, grounding outcome, citation coverage, and degradation path.
11. Document unresolved architecture gaps as ADR candidates instead of silently filling them in.

## Outputs

- Anthropic Messages API + Citations API integration for the retrieval-augmented capability.
- Retrieval adapter against the declared retriever, with corpus access scoping preserved.
- Context-packing module honoring the budget, ordering, and truncation policy, with cache-breakpoint placement noted.
- Grounding system prompt and exemplar files.
- Answer adapter carrying structured citations/source spans.
- Grounding/hallucination gate and the retrieval eval suite.
- Tests for grounded answer, ungrounded/abstain, citation-missing, empty retrieval, retry exhaustion, and cache miss.
- Telemetry notes for retrieval latency, tokens, cache outcomes, grounding, citation coverage, and model version.

Output rules:

- Citations are produced by the Citations API and carried as structured fields; they are never scraped from inline answer text.
- The grounding behavior is explicit; an unsupported answer is never returned in place of the declared abstain/degradation path.
- `cache_control` appears on the retrieved-context prefix only when the corpus is stable within a session; never on the per-query variable prefix.
- No magic decoding or packing values: every non-default `temperature`/`top_p`/`max_tokens` and every budget/truncation number traces to the contract.
- No Anthropic API key, retriever endpoint, or corpus credential committed to source.

## Quality checks

- [ ] The implementation consumes a named capability, retrieval rules, grounding requirement, citation policy, and answer contract from `ai-architecture.md` / `data-architecture`.
- [ ] Citations come from the Citations API as structured fields, not prompt-engineered or scraped.
- [ ] Context packing honors the declared budget, ordering, and truncation policy within the long-context window.
- [ ] The grounding/hallucination gate fails closed; an unsupported answer routes to the declared degradation behavior.
- [ ] `cache_control` sits on the retrieved-context prefix only when the corpus is stable within a session, never on the per-query variable prefix, and does not change answer/citation semantics.
- [ ] Extended-thinking interaction with citation extraction is handled per the architecture (or explicitly N/A).
- [ ] Retrieval evals plus tests cover grounded answer, ungrounded/abstain, citation-missing, empty retrieval, retry exhaustion, and a cache-miss path.
- [ ] Logs and metrics include prompt/model version, retrieval and grounding outcomes, and cache outcome without recording unredacted documents, secrets, or PII.
- [ ] Any missing retrieval, grounding, citation, packing, cache, thinking, gate, budget, or degradation decision is documented as an ADR candidate.

## References

- Upstream: [`architecture/ai-native-engineering`](../../../../architecture/ai-native-engineering/SKILL.md) — capability, model contract, grounding requirement, citation policy, answer contract, cache strategy, degradation behavior, budgets.
- Upstream: [`architecture/data-architecture`](../../../../architecture/data-architecture/SKILL.md) — retrieval topology, corpus ownership, chunking, and access scoping.
- Cross-provider counterpart: [`openai-rag-runtime`](../../openai/openai-rag-runtime/SKILL.md) — same archetype, OpenAI mechanics.
- Related implementation skills: sibling anthropic skills are listed in the [anthropic stack README](../README.md).
- Standards: [`api-standards`](../../../../../standards/api-standards/README.md), [`security-standards`](../../../../../standards/security-standards/README.md), [`observability-standards`](../../../../../standards/observability-standards/README.md), [`deployment-standards`](../../../../../standards/deployment-standards/README.md), [`naming-conventions`](../../../../../standards/naming-conventions/README.md).
