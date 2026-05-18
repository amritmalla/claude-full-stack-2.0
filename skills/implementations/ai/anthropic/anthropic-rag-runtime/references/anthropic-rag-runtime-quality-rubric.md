# Anthropic RAG Runtime Quality Rubric

Load this before declaring the retrieval-augmented integration complete. Revise until each check passes or the unresolved gap is explicitly documented as an ADR candidate against `ai-architecture.md`.

## Contract conformance

- [ ] The implementation consumes a named capability, retrieval rules, corpus ownership, chunking, grounding requirement, citation policy, and answer contract from `ai-architecture.md` and the `data-architecture` handoff — none invented or reinterpreted.
- [ ] Model tier, packing budget, context ordering and truncation policy, extended-thinking requirement, hallucination gate, and degradation behavior are all taken from the architecture, not assumed.
- [ ] Every retrieval/grounding/citation/packing/cache/thinking/gate/budget/degradation gap is recorded as an ADR candidate, not silently filled.

## Retrieval and packing

- [ ] The retrieval adapter uses the declared retriever; chunking and re-ranking are not changed beyond the architecture's declaration.
- [ ] Corpus access scoping is enforced by the retriever (filters/ACL/tenant), never by a prompt instruction.
- [ ] Context is packed up to the declared budget, in the declared order, within Claude's long-context window.
- [ ] Over-budget content is truncated by the declared policy; nothing is silently or randomly dropped.

## Grounding and citations

- [ ] Retrieved documents are sent as document content blocks with the Citations API enabled.
- [ ] Citations are carried as structured fields from the Citations API response, not scraped from inline answer text or prompt-engineered.
- [ ] The grounding gate fails closed — an unsupported answer is never returned; it routes to the declared degradation behavior.
- [ ] Decoding settings (`temperature`, `top_p`, `max_tokens`, `stop_sequences`) are explicit where the contract requires a bounded grounded answer; no unexplained magic values.

## Caching and thinking

- [ ] `cache_control` sits on the retrieved-context prefix only when the corpus is stable within the session.
- [ ] No breakpoint sits on the per-query variable prefix (question or per-request retrieval results).
- [ ] Cache placement does not change answer or citation semantics; a cache miss is a cost metric, not an error.
- [ ] Extended-thinking interaction with citation extraction is handled per the architecture, or explicitly marked N/A.

## Tests and evals

- [ ] Retrieval eval suite covers grounding, citation coverage, and out-of-corpus refusal on the declared dataset.
- [ ] Grounded answer path.
- [ ] Ungrounded → abstain / degradation path.
- [ ] Citation-missing path.
- [ ] Empty retrieval path.
- [ ] Retry exhaustion path.
- [ ] Cache-miss path.

## Telemetry

- [ ] Logs/metrics include model id, prompt version, retrieval latency, retrieved doc count, input/output tokens, cache-read/write tokens, grounding outcome, citation coverage, and executed path.
- [ ] No raw document, raw answer, secret, or PII is logged unredacted.
- [ ] Anthropic API key, retriever endpoint, and corpus credentials are deploy-time config, never committed.

## Standards conformance

- [ ] [api-standards](../../../../../../standards/api-standards/README.md): the answer-plus-citation shape is treated as an external contract surface; versioning and breaking-change policy apply.
- [ ] [security-standards](../../../../../../standards/security-standards/README.md): no secrets or PII leaked via retrieved context, prompts, logs, or stored answers without redaction; corpus access scoping at retrieval; credentials injected at deploy time.
- [ ] [observability-standards](../../../../../../standards/observability-standards/README.md): structured logs and metrics for retrieval latency, tokens, cache outcome, grounding/citation outcomes, model/prompt version; trace propagation through retrieval and generation.
- [ ] [deployment-standards](../../../../../../standards/deployment-standards/README.md): model id, prompt version, cache strategy, and retriever endpoint are deploy-time configuration, not hardcoded.
- [ ] [naming-conventions](../../../../../../standards/naming-conventions/README.md): capability, metric, retriever, and answer-schema names follow project rules.

## Failure handling

If a check fails:

1. Identify the missing or incorrect implementation.
2. If the decision cannot be inferred from `ai-architecture.md` or the `data-architecture` handoff, raise an ADR candidate — do not guess.
3. Revise the integration and re-run the retrieval eval suite and the six required tests.
4. Keep any unresolved gap explicit as an ADR candidate — do not hide it as an assumption.
