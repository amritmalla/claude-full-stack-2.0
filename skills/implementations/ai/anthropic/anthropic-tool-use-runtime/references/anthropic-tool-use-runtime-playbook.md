# Anthropic Tool Use Runtime Playbook

Load this when implementing any owned area of `anthropic-tool-use-runtime` or checking the anti-pattern list. It expands the operating rules and process steps in `SKILL.md` with the Anthropic Messages API tool-use detail needed to produce a production-grade tool-calling integration.

## Why this workflow exists

Tool use done wrong is a production incident, not a silent quality regression: the model proposes a `delete_account` call with arguments it inferred from a prompt-injected document and the adapter executes it because authorization was assumed to be the model's job; a retried `tool_use` re-charges a customer because the mutating tool had no idempotency key; a `tool_choice` left at default lets the model skip a mandatory verification tool; a `cache_control` breakpoint placed on `tool_result` means the cache never hits and token cost doubles unnoticed; an MCP connector tool reaches a system nobody approved because it was convenient.

The goal is a tool-use runtime where the model proposes and the adapter disposes: every side effect is authorized in code, idempotent, audited, and bounded — and the tool surface, `tool_choice`, and cache placement are the architecture's declared decisions, not conveniences invented at the keyboard.

## Behavioral rules in depth

### 1. Consume the tool surface; do not reinterpret it

The capability, the set of tools, each tool's `input_schema`, side-effect class, authorization model, idempotency policy, `tool_choice`/parallel policy, approved MCP connectors, cache strategy, extended-thinking requirement, degradation behavior, and budgets all come from `ai-architecture.md`. Read it before defining a tool. Do not add a "helper" tool, widen an argument type, rename a tool, or relax a required field because it is convenient. A tool-surface gap is an ADR candidate, not an implementation decision.

### 2. The model proposes; the adapter disposes

A `tool_use` block is untrusted model output that may be steered by prompt injection in any content the model saw. Authorization is enforced in the execution adapter, never by trusting the model to "only call tools it should." The adapter, before any side effect: resolves the caller/principal from the request context (not from model output), checks that principal is permitted to invoke that tool with those arguments, and validates arguments against the approved `input_schema`. Failing any check returns a structured error `tool_result`, not an executed side effect.

### 3. `tool_choice` is a stated decision

Exactly one policy is chosen per call and recorded with its rationale:

| `tool_choice` | When to use | Note |
|---|---|---|
| `{"type": "auto"}` | Model decides whether/which tool to call | Default behavior; still must be explicit in code, not implied by omission. |
| `{"type": "any"}` | The turn must result in some tool call | Use when a tool call is mandatory but which one is model-decided. |
| `{"type": "tool", "name": ...}` | Force exactly one named tool | Use for a mandatory step (e.g. a required lookup or verification). |
| `{"type": "none"}` | Suppress all tools this turn | Use to force a text-only turn while tools remain defined. |

The choice serves the contract. Never leave it implicit; never pick `auto` because deciding was tedious.

### 4. Parallel tool use is a decision

Claude may emit multiple `tool_use` blocks in one assistant turn. If the architecture allows it: the adapter executes each call with its own authorization and idempotency, with explicit ordering or bounded concurrency, and returns one `tool_result` per `tool_use` id in a single user turn. If the architecture disallows it: set `disable_parallel_tool_use` where supported by the chosen `tool_choice`, and assert in tests that only one `tool_use` is processed per turn. Unbounded fan-out of side-effecting calls is an incident.

### 5. Side-effecting tools are idempotent

Every mutating tool execution carries an idempotency key derived from a stable request property per the architecture's policy (e.g. a request id + tool name + argument hash). The adapter checks the key before applying the side effect so a replayed or retried `tool_use` does not double-apply. Read-only tools may skip this; classify each tool's side-effect class explicitly and do not guess.

### 6. MCP connector tools only where approved

An MCP connector tool is a remote, often third-party, side-effecting surface. Use it only where `ai-architecture.md` names the connector explicitly. The same authorization, argument validation, idempotency, audit, and redaction rules apply as for a local tool, plus: document the connector's trust boundary, never commit its credentials, and treat its responses as untrusted input. An unapproved MCP connector is an unauthorized integration, not a shortcut.

### 7. Caching is a decision, never an accident

`cache_control` is placed only on the stable tool-definition prefix — the system prompt and the `tools` array — per the architecture's cache strategy. Never on `tool_result`, user input, retrieved data, or anything that varies per request. The breakpoint goes on the last stable element of the prefix so the tool definitions are cached across the tool loop. Cache placement must not change tool semantics, and a cache miss is a cost event, never a correctness failure. Account for the 5-minute cache TTL: a tool-definition prefix that churns every request is still a cost bug.

### 8. Extended thinking is reconciled, not ignored

If the capability uses extended thinking: thinking blocks are preserved or stripped per the architecture's retention rule, and the tool-loop parser selects `tool_use` blocks while tolerating preceding `thinking` blocks rather than choking on them. When thinking is retained across tool turns, preserve the thinking block in the assistant message exactly as returned so signature verification holds. If the capability does not use extended thinking, state N/A — do not leave it unaddressed.

### 9. Decoding is a decision

`temperature`, `top_p`, `max_tokens`, and `stop_sequences` are set explicitly wherever the contract requires deterministic or bounded tool selection. No magic numbers: every non-default value traces to a contract requirement.

### 10. Audit and telemetry without leakage

Every tool execution emits an audit record: tool name, resolved principal, authorization outcome, idempotency key, result class (success / denied / failed), and correlation id. Telemetry logs model id, prompt version, latency, input/output tokens, cache-read and cache-write tokens, tool-call counts, authorization outcomes, and tool-failure counts. Never log raw tool arguments, raw results, secrets, or PII unredacted. The Anthropic API key and any MCP connector credential are injected at deploy time and never committed.

## Step detail

**Step 1 — Load the contract.** Open `ai-architecture.md`. Extract capability name, tool surface, each tool's `input_schema` / side-effect class / authorization model, idempotency policy, prompt-cache strategy. Missing any decision the runtime needs → raise an ADR candidate before writing code.

**Step 2 — Verify completeness.** Confirm the model tier, `tool_choice`/parallel policy, any approved MCP connector, extended-thinking requirement, and degradation behavior are all named. A silent gap here becomes an invented decision later.

**Step 3 — Define tools.** Build each tool from the approved name, description, and `input_schema` verbatim. Record the `tool_choice` decision and the contract reason in the integration header or ADR.

**Step 4 — Build the request.** Compose the Messages API call: system prompt, messages, `tools`, the chosen `tool_choice`, and explicit decoding settings from the contract.

**Step 5 — Place cache breakpoints.** Add `cache_control` only on the stable tool-definition prefix. Confirm by inspection that no breakpoint sits on `tool_result` or per-request content and that placement does not change tool behavior.

**Step 6 — Build the adapter.** Implement authorization (principal from request context) → argument validation against `input_schema` → idempotency-keyed execution → structured `tool_result`. A denied or failed call returns an error `tool_result`, never an executed side effect.

**Step 7 — Build the tool loop.** Feed each `tool_result` back as a user turn keyed by `tool_use` id; handle multiple/parallel `tool_use` blocks per the policy; bound the loop with a max-iteration limit and route exhaustion to the declared degradation behavior.

**Step 8 — Reconcile extended thinking.** If required, ensure the parser tolerates `thinking` blocks ahead of `tool_use` and retains/strips per the rule. If not required, mark N/A explicitly.

**Step 9 — Audit and telemetry.** Emit an audit record per tool execution and the metrics in rule 10 with redaction. Confirm a cache miss is visible as a cost metric, not an error.

**Step 10 — Tests.** Cover: valid tool call; unauthorized call (denied before side effect); tool execution failure; idempotent replay (no double-apply); loop-bound / retry exhaustion; a cache-miss path. These six are the minimum.

**Step 11 — ADR candidates.** Write any unresolved tool/authorization/idempotency/cache/`tool_choice`/degradation gap as an ADR candidate against `ai-architecture.md`. Do not silently fill it.

## Anti-patterns to detect

Call these out explicitly when found:

- A tool added, widened, renamed, or repurposed relative to `ai-architecture.md`
- Authorization delegated to the model ("the prompt tells it not to call that")
- A `tool_use` executed without resolving the principal from request context
- A mutating tool with no idempotency key, so replay double-applies
- `tool_choice` left implicit, or `auto` chosen because forcing was tedious
- Parallel tool use unbounded, or its allowance/suppression never decided
- An MCP connector tool used without explicit architecture approval
- `cache_control` on `tool_result` or per-request content, or a tool-prefix that churns under the 5-minute TTL
- Extended thinking enabled but its interaction with `tool_use` parsing unaddressed; or a retained thinking block mutated so its signature breaks
- Default `temperature`/`max_tokens` left implicit where the contract requires deterministic tool selection
- Raw tool arguments/results, secrets, or PII in logs or audit records
- Anthropic API key or MCP connector credential committed to source
- Cache miss treated as a correctness failure
- "Done" declared without the six required tests
