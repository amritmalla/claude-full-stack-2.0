---
name: anthropic-prompt-caching-and-context-runtime
description: Use when an Anthropic Claude capability from an approved ai-architecture.md must make cache_control, cache TTL, extended-thinking budget, or long-context packing deliberate against a cost/latency budget. Produces a cache/context plan plus telemetry. Not for RAG, tool, or agent design.
---

# Anthropic Prompt Caching and Context Runtime

## When to use

Invoke when `ai-architecture.md` defines a Claude capability with a cost or
latency budget and the caching and context behavior — `cache_control`
breakpoint placement, cache-hit economics, extended-thinking budget and
thinking-block retention, or long-context packing — must be made deliberate
rather than incidental.

Do not use to decide whether a feature should use AI, to pick a model tier, to
design output schemas, to execute tools, to design retrieval topology, or to
design agent control flow.

## Inputs

Required:

- Approved `ai-architecture.md`.
- Capability name and model contract.
- Cost and latency budgets (per-call token and latency targets).
- Target application language and framework.

Optional:

- Prompt-cache strategy from the architecture (which stable prefixes are cacheable).
- Extended-thinking requirement and thinking-token budget.
- Thinking-block retention rule across turns.
- Context budget and truncation policy for long inputs.
- Request-rate / traffic shape (informs whether the 5-minute TTL is realistically warm).
- Tenant or PII isolation requirements for shared prefixes.

## Operating rules

- Preserve the cache, thinking, and context strategy from `ai-architecture.md`. Do not invent a breakpoint plan, a thinking budget, or a context budget. If the architecture is silent on cache strategy, thinking budget, context budget, or the cost/latency target, raise an ADR candidate instead of choosing one.
- Cache breakpoints are a stated decision. `cache_control` is placed only on stable prefixes (system prompt, tool/schema definitions, exemplars, stable retrieved context), in a stated order, with a stated breakpoint count. Per-request variable content is never a breakpoint. Cache placement never changes output semantics.
- The 5-minute cache TTL is accounted for, not assumed. A prefix that is logically stable but practically re-warmed every request because traffic is sparser than the TTL is a cost bug; warm/cold accounting against the actual traffic shape is explicit. A cache miss is a cost event, never a correctness failure.
- Extended-thinking budget is a decision. The thinking-token budget and the thinking-block retention policy across turns come from `ai-architecture.md`; thinking budget is bounded and enforced, never left to defaults. Thinking-block retention or stripping is explicit.
- Context packing is disciplined. Input ordering (stable prefix first, volatile content last so breakpoints stay upstream of variance), the context budget, and the truncation policy when the budget is exceeded are explicit. Truncation fails toward the architecture's declared behavior, never a silent drop of grounding.
- Isolation before sharing. A cached prefix shared across requests or tenants must not carry one caller's PII into another's context; breakpoint placement respects tenant and data-isolation boundaries.
- No sensitive data in telemetry. Cache-read/write tokens, hit rate, thinking tokens, latency, model and prompt version are logged; raw prompts, retrieved content, secrets, and PII are redacted.

## Output contract

The implementation MUST conform to:

- [security-standards](../../../../../standards/security-standards/README.md) — a shared cached prefix never leaks PII across requests or tenants; Anthropic API credentials injected at deploy time, never committed.
- [observability-standards](../../../../../standards/observability-standards/README.md) — structured logs and metrics for cache-read/write tokens, cache hit rate, thinking tokens, latency, and model/prompt version; trace propagation through the call.
- [deployment-standards](../../../../../standards/deployment-standards/README.md) — cache strategy, thinking budget, and context budget are deploy-time configuration, not hardcoded.
- [naming-conventions](../../../../../standards/naming-conventions/README.md) — capability, metric, and config names follow project rules.

Upstream contract: `ai-architecture.md` is the source of truth for the prompt-cache strategy, breakpoint placement, extended-thinking budget, thinking-block retention rule, context budget, truncation policy, and cost/latency targets. If it is silent on any of these, this skill pauses and raises an ADR candidate rather than inventing the decision.

## Progressive references

- Read `references/anthropic-prompt-caching-and-context-runtime-playbook.md` when implementing any owned area or checking the anti-pattern list.
- Read `references/anthropic-prompt-caching-and-context-runtime-quality-rubric.md` before declaring the integration complete.
- Use `assets/anthropic-prompt-caching-and-context-runtime.template.md` as the breakpoint-layout, TTL-accounting, thinking-budget, context-packing, and telemetry reference.

## Process

1. Load `ai-architecture.md` and identify the capability, cost/latency budgets, prompt-cache strategy, extended-thinking requirement, thinking budget, thinking-retention rule, context budget, and truncation policy.
2. Verify the architecture names the cacheable stable prefixes, the breakpoint plan, the thinking budget, and the context budget. A silent gap is an ADR candidate, not an implementation choice.
3. Lay out the prompt: stable prefixes first (system, tool/schema definitions, exemplars, stable context), volatile content last, so breakpoints stay upstream of per-request variance.
4. Place `cache_control` breakpoints on the stated stable prefixes only, in the stated order and count; confirm by inspection no breakpoint sits on per-request content.
5. Perform warm/cold accounting against the real traffic shape and the 5-minute TTL; flag prefixes that will re-warm every request as a cost trap.
6. Enforce the extended-thinking budget and apply the thinking-block retention or stripping rule from the architecture.
7. Enforce the context budget and the declared truncation policy; truncation never silently drops grounding the contract requires.
8. Verify shared cached prefixes respect tenant and PII isolation boundaries.
9. Add telemetry for model/prompt version, latency, cache-read/write tokens, cache hit rate, and thinking tokens.
10. Add tests for a cache-warm hit, a cache-cold miss, a TTL re-warm path, thinking-budget enforcement, and context-budget truncation.
11. Document any unresolved cache/thinking/context/budget gap as an ADR candidate instead of silently filling it.

## Outputs

- Anthropic Messages API prompt layout with cache-breakpoint placement, order, and count noted.
- A warm/cold cache accounting note tied to the traffic shape and the 5-minute TTL.
- Extended-thinking budget and thinking-block retention policy.
- Context-packing and truncation discipline tied to the context budget.
- Tests for cache-warm hit, cache-cold miss, TTL re-warm, thinking-budget enforcement, and context-budget truncation.
- Telemetry notes for cache-read/write tokens, hit rate, thinking tokens, latency, and model/prompt version.

Output rules:

- Breakpoint placement, order, and count are stated explicitly; never implicit.
- `cache_control` appears only on stable prefixes; never on per-request variable content.
- The thinking budget and context budget are explicit values traced to the contract, never defaults or magic numbers.
- A cache miss is recorded as a cost metric, never an error.
- No Anthropic API key or environment-specific endpoint committed to source.

## Quality checks

- [ ] The implementation consumes a named capability and cost/latency budget from `ai-architecture.md`.
- [ ] `cache_control` breakpoints sit only on stable prefixes, in a stated order and count, never on per-request content.
- [ ] Warm/cold accounting against the 5-minute TTL and the real traffic shape is explicit; re-warm cost traps are flagged.
- [ ] The extended-thinking budget is enforced and the thinking-block retention rule is applied (or explicitly N/A).
- [ ] The context budget and truncation policy are explicit; truncation does not silently drop required grounding.
- [ ] Shared cached prefixes respect tenant and PII isolation boundaries.
- [ ] Tests cover cache-warm hit, cache-cold miss, TTL re-warm, thinking-budget enforcement, and context-budget truncation.
- [ ] Logs and metrics include cache outcome, thinking tokens, latency, and model/prompt version without recording unredacted secrets or sensitive payloads.
- [ ] Any missing cache, thinking, context, or budget decision is documented as an ADR candidate.

## References

- Upstream: [`architecture/ai-native-engineering`](../../../../architecture/ai-native-engineering/SKILL.md) — capability, model contract, prompt-cache strategy, extended-thinking requirement, context budget.
- Upstream: [`architecture/operations`](../../../../architecture/operations/SKILL.md) — cost/latency budgets and the operational burden of cache and context tuning.
- Cross-provider counterpart: none. This skill is Anthropic-specific (`cache_control`, the 5-minute cache TTL, and extended-thinking budget have no portable cross-provider equivalent); there is intentionally no `openai` mirror.
- Related architecture: [`architecture/operations`](../../../../architecture/operations/SKILL.md) — cost and latency budget ownership.
- Stack scope and where Anthropic-specific features are folded in: [anthropic stack README](../README.md).
- Standards: [`security-standards`](../../../../../standards/security-standards/README.md), [`observability-standards`](../../../../../standards/observability-standards/README.md), [`deployment-standards`](../../../../../standards/deployment-standards/README.md), [`naming-conventions`](../../../../../standards/naming-conventions/README.md).
