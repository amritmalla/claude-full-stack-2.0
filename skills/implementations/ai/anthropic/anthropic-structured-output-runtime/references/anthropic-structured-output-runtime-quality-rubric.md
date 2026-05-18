# Anthropic Structured Output Runtime Quality Rubric

Load this before declaring the structured-output integration complete. Revise until each check passes or the unresolved gap is explicitly documented as an ADR candidate against `ai-architecture.md`.

## Contract conformance

- [ ] The implementation consumes a named capability and output schema from `ai-architecture.md` — the schema is not invented, widened, narrowed, or given extra fields.
- [ ] Model tier, prompt inputs, output shape, extended-thinking requirement, and degradation behavior are all taken from the architecture, not assumed.
- [ ] Every schema/cache/thinking/budget/degradation gap is recorded as an ADR candidate, not silently filled.

## Mechanism

- [ ] The structured-output mechanism (forced single-tool call, prefill, or strict-prompt-plus-validation) is explicit in code and justified against the contract.
- [ ] Forced tool use, when chosen, uses the approved schema as `input_schema` and `tool_choice` pins the tool.
- [ ] Decoding settings (`temperature`, `top_p`, `max_tokens`, `stop_sequences`) are explicit where the contract requires determinism; no unexplained magic values.

## Validation and failure

- [ ] Output is parsed and validated against the schema before any downstream use.
- [ ] Validation fails closed — a non-conforming response is an error, never a partial or coerced object.
- [ ] Repair retries are bounded by both a max attempt count and a deadline from the budget.
- [ ] Retry exhaustion executes the architecture's declared degradation behavior.

## Caching and thinking

- [ ] `cache_control` breakpoints sit only on stable prefixes (system prompt, schema/tool definition, exemplars).
- [ ] No breakpoint sits on per-request variable content.
- [ ] Cache placement does not change output semantics; a cache miss is a cost metric, not an error.
- [ ] Extended-thinking interaction with the chosen mechanism is handled per the architecture, or explicitly marked N/A.

## Tests

- [ ] Valid output path.
- [ ] Malformed output (schema violation) path.
- [ ] Refusal / degradation path.
- [ ] Retry exhaustion path.
- [ ] Cache-miss path.

## Telemetry

- [ ] Logs/metrics include model id, prompt version, latency, input/output tokens, cache-read/write tokens, validation outcome, and executed path.
- [ ] No raw prompt, raw output, secret, or PII is logged unredacted.
- [ ] Anthropic API key and environment endpoint are deploy-time config, never committed.

## Standards conformance

- [ ] [api-standards](../../../../../../standards/api-standards/README.md): the output schema is treated as an external contract surface; versioning and breaking-change policy apply.
- [ ] [security-standards](../../../../../../standards/security-standards/README.md): no secrets or PII in prompts, logs, or stored outputs without redaction; credentials injected at deploy time.
- [ ] [observability-standards](../../../../../../standards/observability-standards/README.md): structured logs and metrics for latency, tokens, cache outcome, validation failures, model/prompt version; trace propagation.
- [ ] [deployment-standards](../../../../../../standards/deployment-standards/README.md): model id, prompt version, and cache strategy are deploy-time configuration, not hardcoded.
- [ ] [naming-conventions](../../../../../../standards/naming-conventions/README.md): capability, metric, and schema names follow project rules.

## Failure handling

If a check fails:

1. Identify the missing or incorrect implementation.
2. If the decision cannot be inferred from `ai-architecture.md`, raise an ADR candidate — do not guess.
3. Revise the integration and re-run the five required tests.
4. Keep any unresolved gap explicit as an ADR candidate — do not hide it as an assumption.
