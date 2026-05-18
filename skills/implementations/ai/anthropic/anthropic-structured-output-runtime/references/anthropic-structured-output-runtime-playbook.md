# Anthropic Structured Output Runtime Playbook

Load this when implementing any owned area of `anthropic-structured-output-runtime` or checking the anti-pattern list. It expands the operating rules and process steps in `SKILL.md` with the Anthropic Messages API detail needed to produce a production-grade structured-output integration.

## Why this workflow exists

Structured output done wrong fails silently in production: a model returns prose where the contract expects JSON and a downstream parser stores a partial record; a schema field is widened "to be safe" and a consumer three services away breaks on the new shape; a cache breakpoint is placed on a per-request field and the cache never hits, doubling token cost without anyone noticing; extended thinking is enabled and the tool-use block the parser depends on never arrives because thinking and forced tool use were not reconciled.

The goal is a schema-bound, validation-closed, observable structured-output runtime whose mechanism is explicit and whose failure behavior is the architecture's declared degradation path — not a best-effort prompt that works in the demo and rots in production.

## Behavioral rules in depth

### 1. Consume the contract; do not reinterpret it

The capability, output schema, model tier, prompt-cache strategy, extended-thinking requirement, degradation behavior, and latency/cost budgets all come from `ai-architecture.md`. Read it before writing a request. Do not widen a field, relax a nullability decision, add an "extra" field, or narrow an enum because it is convenient. A schema gap is an ADR candidate, not an implementation decision.

### 2. The structured-output mechanism is a stated decision

Exactly one mechanism is chosen and recorded with its rationale:

| Mechanism | When to use | Cost |
|---|---|---|
| Forced single-tool call (`tool_choice: {type: "tool", name: ...}`), `input_schema` = the approved schema | Default. Strongest schema adherence. | One tool definition; tool-use block parsing. |
| Assistant-message prefill (start the assistant turn with `{`) | Lightweight objects, latency-sensitive, no tool overhead acceptable | Weaker guarantee than forced tool; still needs validation. |
| Strict prompt + post-hoc validation | Schema cannot be expressed as a tool input, or provider mechanism unavailable | Weakest; highest repair rate. |

The mechanism serves the contract. Never pick prefill because the tool definition is tedious; pick it because the contract's shape and latency budget justify it.

### 3. Validation fails closed

A response that does not satisfy the schema is an error. It is never returned downstream as a best-effort partial, never "mostly valid," never silently coerced. Parse → validate against the schema → on failure, enter the bounded repair path; on repair exhaustion, execute the architecture's declared degradation behavior (fallback value, surfaced error, queue for human review — whatever `ai-architecture.md` says).

### 4. Retries are bounded and explicit

Schema-repair retries have a maximum attempt count AND a deadline, both from the budget in `ai-architecture.md` (or an ADR candidate if absent). A repair attempt re-prompts with the validation error, it does not just resend. Exhaustion is not an exception swallowed in a catch block; it is the declared degradation path.

### 5. Caching is a decision, never an accident

`cache_control` breakpoints sit only on stable prefixes — system prompt, schema/tool definition, exemplars — per the architecture's cache strategy. Never on per-request variable content (the user input, retrieved data, timestamps). Cache placement must not change output semantics, and a cache miss is a cost event, never a correctness failure. Account for the 5-minute cache TTL: a breakpoint that is logically stable but practically re-warmed every request is still a cost bug.

### 6. Extended thinking is reconciled, not ignored

If the capability uses extended thinking: thinking blocks are preserved or stripped per the architecture's retention rule, and the interaction with forced tool use is handled explicitly (thinking precedes the tool-use block; the parser must skip thinking blocks, not choke on them). If the capability does not use extended thinking, state that it is N/A — do not leave it unaddressed.

### 7. Decoding is a decision

`temperature`, `top_p`, `max_tokens`, and `stop_sequences` are set explicitly wherever the contract requires determinism or bounded output. No magic numbers: every non-default value traces to a contract requirement, not a vibe.

### 8. Telemetry without leakage

Log model id, prompt version, latency, input/output tokens, cache-read and cache-write tokens, validation outcome, and which path executed (success / repair / degradation). Never log raw prompts, raw outputs, secrets, or PII unredacted. The Anthropic API key is injected at deploy time and never committed.

## Step detail

**Step 1 — Load the contract.** Open `ai-architecture.md`. Extract capability name, output schema, success criteria, declared failure modes, prompt-cache strategy, extended-thinking requirement, degradation behavior, latency/cost budget. Missing any decision the runtime needs → raise an ADR candidate before writing code.

**Step 2 — Verify completeness.** Confirm the model tier, prompt inputs, output shape, extended-thinking requirement, and degradation behavior are all named. A silent gap here becomes an invented decision later.

**Step 3 — Choose the mechanism.** Pick forced-tool (default), prefill, or strict-prompt-plus-validation using the table in rule 2. Record the choice and the contract reason in the integration's header comment or ADR.

**Step 4 — Build the request.** Compose the Messages API call: system prompt, messages, the chosen mechanism (tool definition + `tool_choice`, or prefill, or strict prompt), and explicit decoding settings from the contract.

**Step 5 — Place cache breakpoints.** Add `cache_control` only on stable prefixes per the architecture's strategy. Confirm by inspection that no breakpoint sits on per-request content and that placement does not change the produced object.

**Step 6 — Reconcile extended thinking.** If required, ensure thinking blocks are handled per the retention rule and the parser tolerates them ahead of the tool-use block. If not required, mark N/A explicitly.

**Step 7 — Validate and handle failure.** Implement parse → schema-validate → bounded repair → declared degradation. Validation failure must not return a partial.

**Step 8 — Tests.** Cover: valid output; malformed output (schema violation); refusal / degradation path; retry exhaustion; a cache-miss path. These five are the minimum.

**Step 9 — Telemetry.** Emit the metrics in rule 8 with redaction. Confirm a cache miss is visible as a cost metric, not an error.

**Step 10 — ADR candidates.** Write any unresolved schema/cache/thinking/budget/degradation gap as an ADR candidate against `ai-architecture.md`. Do not silently fill it.

## Anti-patterns to detect

Call these out explicitly when found:

- Schema widened, narrowed, or given an "extra" field relative to `ai-architecture.md`
- Mechanism left implicit ("the model usually returns JSON")
- Validation that returns a partial or coerced object instead of failing closed
- Unbounded retry loop, or retry with no deadline
- `cache_control` on per-request variable content, or a breakpoint that never hits due to TTL churn
- Extended thinking enabled but its interaction with forced tool use unaddressed
- Default `temperature`/`max_tokens` left implicit where the contract requires determinism
- Raw prompt/output, secrets, or PII in logs
- Anthropic API key or environment endpoint committed to source
- Cache miss treated as a correctness failure
- "Done" declared without the five required tests
