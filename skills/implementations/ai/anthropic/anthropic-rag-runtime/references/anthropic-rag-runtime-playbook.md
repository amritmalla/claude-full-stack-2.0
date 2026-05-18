# Anthropic RAG Runtime Playbook

Load this when implementing any owned area of `anthropic-rag-runtime` or checking the anti-pattern list. It expands the operating rules and process steps in `SKILL.md` with the Anthropic Messages API and Citations API detail needed to produce a production-grade retrieval-augmented integration.

## Why this workflow exists

RAG done wrong fails plausibly in production: the model answers confidently from its parametric memory when retrieval returned nothing, and no gate catches it; citations are scraped from inline answer text with a regex and drift out of sync with the real sources; the retrieved-context block is packed in arbitrary order and the truncation silently drops the one chunk that held the answer; a `cache_control` breakpoint is placed on the per-query retrieval result so the cache never hits, doubling token cost while looking like it is configured; corpus access scoping is left to a prompt instruction and a user retrieves a document they were never authorized to see.

The goal is a grounded, citation-bearing, budget-disciplined, observable retrieval runtime whose unsupported-answer behavior is the architecture's declared degradation path and whose citations are first-class Citations API output — not a prompt-engineered demo that hallucinates under real corpora.

## Behavioral rules in depth

### 1. Consume the contract; do not reinterpret it

The capability, retrieval rules, corpus ownership, chunking, grounding requirement, citation policy, answer contract, packing budget, prompt-cache strategy, extended-thinking requirement, hallucination gate, degradation behavior, and budgets all come from `ai-architecture.md` and the `data-architecture` handoff. Read both before writing a retriever call. Retrieval topology, corpus ownership, and chunking are `data-architecture` decisions — do not re-chunk, re-rank, or swap the retriever because it is convenient. A gap is an ADR candidate, not an implementation decision.

### 2. Grounding is enforced, not hoped for

The answer is constrained to the retrieved context by the grounding system prompt AND a post-hoc grounding gate. When the retrieved context cannot support an answer, the declared behavior executes: abstain, return "not found in corpus", or escalate — whatever `ai-architecture.md` says. A confident free-form answer over empty or irrelevant retrieval is the canonical RAG failure; the gate exists to catch exactly that.

### 3. Citations are first-class Citations API output

Pass retrieved documents as document content blocks with `citations: {enabled: true}`. The model emits `cited_text` / source-location references bound to the document spans it used. The answer adapter carries these as structured fields on the answer contract. Never reconstruct citations by string-matching the answer against sources, and never instruct the model to "write [1], [2]" inline — that is prompt-engineered citation and it drifts. The Citations API binding is the contract surface.

### 4. Context packing is a budgeted decision

| Decision | Source | Rule |
|---|---|---|
| Packing budget (tokens / doc count) | `ai-architecture.md` | Pack up to the budget; do not exceed Claude's context window. |
| Document ordering | architecture (relevance, recency, declared) | Apply the declared order; do not reorder for convenience. |
| Truncation policy | architecture | Over-budget content truncated by the declared policy (drop lowest-rank, head/tail trim), never silent random drop. |

The long-context window is large but not free: every packed token is cost and latency. Pack deliberately to the budget; record the budget and ordering in the integration header.

### 5. Caching is a decision, never an accident

`cache_control` goes on the retrieved-context prefix ONLY when the corpus is stable within a session — a fixed document set reused across turns of one conversation, per the architecture's strategy. It is NEVER placed on a per-query variable prefix: the user question, or retrieval results that change every request. A breakpoint on per-query content never hits and is a pure cost bug. Account for the 5-minute cache TTL: a context prefix that is logically stable but re-warmed every request is still a cost bug. Cache placement must not change answer or citation semantics, and a cache miss is a cost event, never a correctness failure.

### 6. The hallucination/grounding gate fails closed

Retrieval evals run the declared dataset (grounding, citation coverage, refusal on out-of-corpus). At request time the grounding gate checks the answer against the retrieved context and citation coverage. A failing answer is not returned downstream — it enters the declared degradation path. Gate thresholds come from the architecture; absent, they are an ADR candidate.

### 7. Extended thinking is reconciled, not ignored

If the capability uses extended thinking for synthesis over retrieved context: thinking blocks are preserved or stripped per the architecture's retention rule, and the answer adapter selects citation-bearing text content blocks, not thinking blocks, when extracting the answer and citations. If the capability does not use extended thinking, state N/A — do not leave it unaddressed.

### 8. Decoding is a decision

`temperature`, `top_p`, `max_tokens`, and `stop_sequences` are set explicitly wherever the contract requires a deterministic or length-bounded grounded answer. No magic numbers: every non-default value traces to a contract requirement.

### 9. Telemetry and corpus security without leakage

Log model id, prompt version, retrieval latency, retrieved doc count, input/output tokens, cache-read and cache-write tokens, grounding outcome, citation coverage, and which path executed (answered / abstained / degradation). Never log raw documents, raw answers, secrets, or PII unredacted. Corpus access scoping is enforced by the retriever (filters, tenant scoping), never by a prompt instruction. The Anthropic API key and retriever credentials are injected at deploy time and never committed.

## Step detail

**Step 1 — Load the contract.** Open `ai-architecture.md` and the `data-architecture` handoff. Extract capability, retrieval rules, corpus ownership, chunking, grounding requirement, citation policy, answer contract, packing budget, cache strategy, extended-thinking requirement, hallucination gate, degradation behavior, budgets. Missing any decision the runtime needs → raise an ADR candidate before writing code.

**Step 2 — Verify completeness.** Confirm model tier, packing budget, context ordering and truncation policy, extended-thinking requirement, hallucination gate, and degradation behavior are all named. A silent gap here becomes an invented decision later.

**Step 3 — Retrieval adapter.** Implement against the declared retriever, preserving corpus access scoping (tenant/ACL filters at the retriever, not the prompt). Do not re-chunk or re-rank beyond the architecture's declaration.

**Step 4 — Pack context.** Pack retrieved documents up to the declared budget, in the declared order, applying the declared truncation policy. Confirm the packed prefix fits the context window.

**Step 5 — Build the request.** Compose the Messages API call: grounding system prompt, retrieved documents as document content blocks with `citations: {enabled: true}`, the user question, and explicit decoding settings from the contract.

**Step 6 — Place cache breakpoints.** Add `cache_control` to the retrieved-context prefix only if the corpus is stable within the session. Confirm by inspection that no breakpoint sits on the per-query variable prefix and that placement does not change the answer or its citations.

**Step 7 — Reconcile extended thinking.** If required, ensure thinking blocks are handled per the retention rule and the answer adapter ignores thinking blocks when selecting the cited answer text. If not required, mark N/A explicitly.

**Step 8 — Answer adapter and grounding gate.** Extract the answer and structured citations from the Citations API response. Run the grounding gate; on failure, execute the declared abstain/degradation behavior. An unsupported answer must not be returned.

**Step 9 — Evals and tests.** Build the retrieval eval suite (grounding, citation coverage, out-of-corpus refusal). Cover: grounded answer; ungrounded → abstain/degradation; citation-missing; empty retrieval; retry exhaustion; a cache-miss path. These six are the minimum.

**Step 10 — Telemetry.** Emit the metrics in rule 9 with redaction. Confirm a cache miss is visible as a cost metric, not an error, and grounding failures are visible as a quality metric.

**Step 11 — ADR candidates.** Write any unresolved retrieval/grounding/citation/packing/cache/thinking/gate/budget/degradation gap as an ADR candidate against `ai-architecture.md`. Do not silently fill it.

## Anti-patterns to detect

Call these out explicitly when found:

- Retriever, chunking, or re-ranking changed relative to the `data-architecture` handoff
- Grounding gate absent; model free to answer over empty or irrelevant retrieval
- Citations scraped from inline answer text or prompt-engineered (`write [1]`) instead of produced by the Citations API
- Retrieved context packed in arbitrary order, or over-budget content silently dropped
- `cache_control` on the per-query variable prefix (question or per-request retrieval), or a breakpoint that never hits due to TTL churn
- `cache_control` on the context prefix when the corpus is NOT stable within the session
- Corpus access scoping enforced by a prompt instruction instead of the retriever
- Extended thinking enabled but its interaction with citation extraction unaddressed
- Default `temperature`/`max_tokens` left implicit where the contract requires a bounded grounded answer
- Raw documents, raw answers, secrets, or PII in logs
- Anthropic API key, retriever endpoint, or corpus credential committed to source
- Cache miss treated as a correctness failure; grounding failure hidden instead of metered
- "Done" declared without the retrieval eval suite and the six required tests
