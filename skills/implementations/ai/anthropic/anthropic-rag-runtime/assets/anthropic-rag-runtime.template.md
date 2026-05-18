# Anthropic RAG Runtime — Integration Reference

Use this as the canonical shape when generating an Anthropic retrieval-augmented integration. Placeholder tokens use `<kebab-case>` or `<PascalCase>`. Language is illustrative (Python SDK); port to the target stack. Every value marked `# from ai-architecture.md` is a contract input, not a default.

## Integration header (record the decision)

```
Capability:         <capability-name>             # from ai-architecture.md
Retriever:          <retriever-id / store>        # from data-architecture
Chunking:           <declared scheme>             # from data-architecture
Corpus scoping:     <tenant/ACL filter>           # from data-architecture
Model tier:         <model-id>                    # from ai-architecture.md
Grounding:          abstain | not-in-corpus | escalate   # from ai-architecture.md
Citation policy:    Citations API (structured)    # from ai-architecture.md
Answer contract:    <answer + citation fields>    # from ai-architecture.md
Packing budget:     <tokens / doc count>          # from ai-architecture.md
Ordering:           relevance | recency | <declared>     # from ai-architecture.md
Truncation:         <declared policy>             # from ai-architecture.md
Cache strategy:     context-prefix IFF corpus stable in session  # from ai-architecture.md
Extended thinking:  required | N/A                # from ai-architecture.md
Grounding gate:     <thresholds>                  # from ai-architecture.md
Degradation:        <declared fallback behavior>  # from ai-architecture.md
Budget:             <max repair attempts>, <deadline ms>  # from ai-architecture.md
```

## Retrieval adapter (scoping enforced at the retriever)

```python
def retrieve(query: str, scope: Scope) -> list[Doc]:
    # access scoping is a retriever filter, NEVER a prompt instruction
    return retriever.search(
        query,
        filter=scope.acl_filter,        # from data-architecture
        top_k=<from-contract>,          # from ai-architecture.md
    )
```

## Context packing (budget, order, truncation are contract inputs)

```python
docs = order(retrieve(q, scope), by="<declared-order>")   # from ai-architecture.md
packed, dropped = pack(
    docs,
    budget_tokens=<PACKING_BUDGET>,     # from ai-architecture.md
    truncation="<declared-policy>",     # from ai-architecture.md — never random
)
emit_metric("retrieved_docs", len(docs))
emit_metric("packed_docs", len(packed))   # dropped is metered, not silent
```

## Messages API request with Citations API + cache placement

```python
resp = client.messages.create(
    model="<model-id>",                  # from ai-architecture.md
    max_tokens=<from-contract>,
    temperature=<from-contract>,         # explicit where determinism required
    system=[
        {"type": "text", "text": GROUNDING_PROMPT,
         "cache_control": {"type": "ephemeral"}},   # stable instruction prefix
    ],
    messages=[{
        "role": "user",
        "content": [
            # Retrieved context as document blocks with citations ENABLED.
            # cache_control here ONLY if the corpus is stable within the session.
            *[
                {"type": "document",
                 "source": {"type": "text", "media_type": "text/plain",
                            "data": d.text},
                 "title": d.title,
                 "citations": {"enabled": True},
                 # "cache_control": {"type": "ephemeral"}  # IFF corpus stable in session
                }
                for d in packed
            ],
            {"type": "text", "text": user_question},   # per-query — NEVER cache_control
        ],
    }],
)
```

## Answer adapter — structured citations, fail-closed grounding

```python
answer_text, citations = [], []
for block in resp.content:
    if block.type == "thinking":
        continue                          # ignore thinking; never the answer source
    if block.type == "text":
        answer_text.append(block.text)
        for c in getattr(block, "citations", []) or []:
            citations.append(Citation(    # structured, from Citations API
                cited_text=c.cited_text,
                doc_title=c.document_title,
                location=c.location,
            ))

if not grounding_gate(answer_text, citations, packed):   # fail closed
    return run_declared_degradation()      # abstain / not-in-corpus / escalate
return Answer(text="".join(answer_text), citations=citations)
```

## Bounded repair → declared degradation

```python
for attempt in range(MAX_REPAIR_ATTEMPTS + 1):   # bound from contract
    ok, reason = grounding_gate(ans.text, ans.citations, packed)
    if ok:
        return ans
    if attempt == MAX_REPAIR_ATTEMPTS or deadline_exceeded():
        return run_declared_degradation()          # from ai-architecture.md
    ans = regenerate_with_grounding_feedback(reason)
```

## Extended-thinking reconciliation (only if required)

```
- Thinking blocks precede the answer text blocks in the response.
- Adapter skips type == "thinking"; citations are read off "text" blocks only.
- Retain or strip thinking per ai-architecture.md retention rule — do not invent it.
```

## Telemetry fields (emit every call; redact payloads)

| Field | Source |
|---|---|
| `model_id`, `prompt_version` | deploy-time config |
| `retrieval_latency_ms`, `generation_latency_ms` | measured |
| `retrieved_docs`, `packed_docs` | retrieval/packing |
| `input_tokens`, `output_tokens` | response usage |
| `cache_read_tokens`, `cache_write_tokens` | response usage |
| `grounding_outcome` | pass / fail |
| `citation_coverage` | cited spans / claims |
| `path` | answered / abstained / degradation |

Never log: raw documents, raw answer, secrets, PII (unredacted).

## Required test + eval matrix

| Test / eval | Asserts |
|---|---|
| Grounded answer | Supported question returns answer with structured citations |
| Ungrounded / abstain | Out-of-corpus question triggers declared degradation, not a guess |
| Citation missing | Answer without required citation fails the gate |
| Empty retrieval | No documents → declared degradation, never parametric answer |
| Retry exhaustion | Bound respected; degradation path taken at the limit |
| Cache miss | Correct grounded answer; miss recorded as cost metric, not error |
| Retrieval eval suite | Grounding, citation coverage, out-of-corpus refusal on declared dataset |

## Configuration (deploy-time, never committed)

```
ANTHROPIC_API_KEY        # secret store / env injection
RETRIEVER_ENDPOINT       # config, not hardcoded
RETRIEVER_CREDENTIALS    # secret store / env injection
MODEL_ID                 # e.g. claude-... — config, not hardcoded
PROMPT_VERSION           # config
CACHE_STRATEGY           # context-prefix IFF corpus stable in session
PACKING_BUDGET           # tokens / doc count — config
```
