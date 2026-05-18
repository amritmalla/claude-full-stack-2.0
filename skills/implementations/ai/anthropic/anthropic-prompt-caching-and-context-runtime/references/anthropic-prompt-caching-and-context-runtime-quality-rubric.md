# Anthropic Prompt Caching and Context Runtime Quality Rubric

Load this before declaring the caching and context integration complete. Revise until each check passes or the unresolved gap is explicitly documented as an ADR candidate against `ai-architecture.md`.

## Strategy conformance

- [ ] The implementation consumes a named capability, cost/latency budget, and prompt-cache strategy from `ai-architecture.md` — the breakpoint plan, thinking budget, and context budget are not invented.
- [ ] Cacheable prefixes, breakpoint plan, extended-thinking requirement, thinking budget, context budget, and truncation policy are taken from the architecture, not assumed.
- [ ] Every cache/thinking/context/budget gap is recorded as an ADR candidate, not silently filled.

## Cache breakpoints

- [ ] `cache_control` breakpoints sit only on stable prefixes (system prompt, tool/schema definitions, exemplars, stable context).
- [ ] Breakpoint order and count are explicit and the cacheable region is a contiguous prefix.
- [ ] No breakpoint sits on or after per-request variable content.
- [ ] Cache placement does not change output semantics; a cache miss is a cost metric, not an error.

## TTL and cost accounting

- [ ] Warm/cold accounting against the 5-minute cache TTL and the real traffic shape is explicit.
- [ ] Prefixes that re-warm every request because traffic is sparser than the TTL are flagged as a cost trap, with the remedy routed as an architecture decision.

## Thinking and context

- [ ] The extended-thinking budget is set from the contract and enforced; no unbounded thinking, no invented budget.
- [ ] The thinking-block retention/stripping rule across turns is applied, or extended thinking is explicitly marked N/A.
- [ ] The context budget is enforced and the declared truncation policy applies when exceeded.
- [ ] Truncation never silently drops grounding the capability's correctness depends on.

## Isolation

- [ ] No shared cached prefix carries one caller's PII or tenant data into another caller's context.
- [ ] The tenant / data-isolation boundary sits upstream of the cache breakpoint.

## Tests

- [ ] Cache-warm hit path.
- [ ] Cache-cold miss path.
- [ ] TTL re-warm path.
- [ ] Thinking-budget enforcement path.
- [ ] Context-budget truncation path.

## Telemetry

- [ ] Logs/metrics include model id, prompt version, latency, input/output tokens, cache-read/write tokens, cache hit rate, and thinking tokens.
- [ ] No raw prompt, raw retrieved content, secret, or PII is logged unredacted.
- [ ] Anthropic API key and environment endpoint are deploy-time config, never committed.

## Standards conformance

- [ ] [security-standards](../../../../../../standards/security-standards/README.md): no shared cached prefix leaks PII across requests or tenants; credentials injected at deploy time.
- [ ] [observability-standards](../../../../../../standards/observability-standards/README.md): structured logs and metrics for cache-read/write tokens, hit rate, thinking tokens, latency, model/prompt version; trace propagation.
- [ ] [deployment-standards](../../../../../../standards/deployment-standards/README.md): cache strategy, thinking budget, and context budget are deploy-time configuration, not hardcoded.
- [ ] [naming-conventions](../../../../../../standards/naming-conventions/README.md): capability, metric, and config names follow project rules.

## Failure handling

If a check fails:

1. Identify the missing or incorrect implementation.
2. If the decision cannot be inferred from `ai-architecture.md`, raise an ADR candidate — do not guess.
3. Revise the integration and re-run the five required tests.
4. Keep any unresolved gap explicit as an ADR candidate — do not hide it as an assumption.
