# Anthropic Tool Use Runtime Quality Rubric

Load this before declaring the tool-use integration complete. Revise until each check passes or the unresolved gap is explicitly documented as an ADR candidate against `ai-architecture.md`.

## Contract conformance

- [ ] The implementation consumes a named capability and tool surface from `ai-architecture.md` — no tool is invented, added, widened, renamed, or repurposed.
- [ ] Each tool's `input_schema` matches the approved schema exactly; required fields and types are not relaxed.
- [ ] Model tier, `tool_choice`/parallel policy, any approved MCP connector, extended-thinking requirement, and degradation behavior are all taken from the architecture, not assumed.
- [ ] Every tool/authorization/idempotency/cache/`tool_choice`/degradation gap is recorded as an ADR candidate, not silently filled.

## Authorization and side effects

- [ ] Authorization is enforced in the execution adapter before any side effect; a model-proposed call is treated as untrusted input.
- [ ] The acting principal is resolved from request context, never from model output.
- [ ] Arguments are validated against the approved `input_schema` before execution; a denied or invalid call returns an error `tool_result`, not a side effect.
- [ ] Each tool's side-effect class (read-only vs mutating) is classified explicitly, not guessed.

## Idempotency

- [ ] Every mutating tool execution carries an idempotency key derived per the architecture's policy.
- [ ] A replayed or retried `tool_use` is proven not to double-apply.

## Tool-choice, parallelism, and MCP

- [ ] `tool_choice` (`auto` / `any` / `tool` / `none`) is explicit in code and justified against the contract.
- [ ] Parallel tool use is either bounded with per-call authorization and idempotency, or suppressed and asserted off, per the architecture.
- [ ] MCP connector tools appear only where the architecture explicitly approves the named connector, with the same authz/idempotency/audit rules and a documented trust boundary.
- [ ] Decoding settings (`temperature`, `top_p`, `max_tokens`, `stop_sequences`) are explicit where the contract requires deterministic tool selection; no unexplained magic values.

## Caching and thinking

- [ ] `cache_control` sits only on the stable tool-definition prefix (system prompt + `tools`).
- [ ] No breakpoint sits on `tool_result` or per-request variable content.
- [ ] Cache placement does not change tool semantics; a cache miss is a cost metric, not an error.
- [ ] Extended-thinking interaction with `tool_use` parsing is handled per the architecture, or explicitly marked N/A; retained thinking blocks are preserved unmutated.

## Tool loop and tests

- [ ] The tool loop is bounded by a max-iteration limit; exhaustion routes to the declared degradation behavior.
- [ ] Valid tool-call path.
- [ ] Unauthorized call path (denied before side effect).
- [ ] Tool execution failure path.
- [ ] Idempotent replay path (no double-apply).
- [ ] Loop-bound / retry exhaustion path.
- [ ] Cache-miss path.

## Telemetry and audit

- [ ] An audit record is emitted per tool execution: tool name, principal, authorization outcome, idempotency key, result class, correlation id.
- [ ] Logs/metrics include model id, prompt version, latency, input/output tokens, cache-read/write tokens, tool-call counts, authorization outcomes, and tool-failure counts.
- [ ] No raw tool argument, raw result, secret, or PII is logged or audited unredacted.
- [ ] Anthropic API key and MCP connector credentials are deploy-time config, never committed.

## Standards conformance

- [ ] [api-standards](../../../../../../standards/api-standards/README.md): each tool schema is an external contract surface; versioning and breaking-change policy apply.
- [ ] [security-standards](../../../../../../standards/security-standards/README.md): authorization enforced before side effects; no secrets or PII in prompts, tool arguments/results, logs, or audit records without redaction; credentials injected at deploy time.
- [ ] [observability-standards](../../../../../../standards/observability-standards/README.md): structured logs and metrics for latency, tokens, cache outcome, tool-call counts, authorization outcomes, tool failures, model/prompt version; trace propagation.
- [ ] [deployment-standards](../../../../../../standards/deployment-standards/README.md): model id, prompt version, tool-cache strategy, and `tool_choice` policy are deploy-time configuration, not hardcoded.
- [ ] [naming-conventions](../../../../../../standards/naming-conventions/README.md): capability, tool, metric, and audit-field names follow project rules.

## Failure handling

If a check fails:

1. Identify the missing or incorrect implementation.
2. If the decision cannot be inferred from `ai-architecture.md`, raise an ADR candidate — do not guess.
3. Revise the integration and re-run the six required tests.
4. Keep any unresolved gap explicit as an ADR candidate — do not hide it as an assumption.
