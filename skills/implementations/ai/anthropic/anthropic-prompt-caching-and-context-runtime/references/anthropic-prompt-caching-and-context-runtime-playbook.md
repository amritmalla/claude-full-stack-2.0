# Anthropic Prompt Caching and Context Runtime Playbook

Load this when implementing any owned area of `anthropic-prompt-caching-and-context-runtime` or checking the anti-pattern list. It expands the operating rules and process steps in `SKILL.md` with the Anthropic Messages API detail needed to produce a production-grade caching and context runtime.

## Why this workflow exists

Caching and context done wrong is invisible until the bill arrives: a `cache_control` breakpoint is placed after the user input so the cacheable prefix changes every request and the cache never hits, silently doubling input-token cost; a prefix is genuinely stable but traffic is one request a minute, the 5-minute TTL expires between calls, and every request pays the cache-write premium with zero cache-read benefit; extended thinking is enabled with no budget and a single hard prompt burns tens of thousands of thinking tokens; a long retrieved context is packed ahead of the system prompt, pushing every breakpoint downstream of variance; thinking blocks are dropped between turns when the contract required them, degrading multi-turn reasoning with no error anywhere.

The goal is a deliberate, TTL-aware, budget-enforced caching and context runtime whose breakpoint plan, thinking budget, and packing discipline come from `ai-architecture.md` and whose cost behavior is measured — not a prompt that looks cached in the demo and burns money in production.

## Behavioral rules in depth

### 1. Consume the strategy; do not invent it

The prompt-cache strategy, breakpoint plan, extended-thinking budget, thinking-retention rule, context budget, truncation policy, and cost/latency targets all come from `ai-architecture.md`. Read it before laying out a prompt. A missing breakpoint plan, thinking budget, or context budget is an ADR candidate, not a number you pick because it seems reasonable.

### 2. Breakpoint placement is a stated decision

`cache_control` sits only on stable prefixes, with a stated order and a stated count:

| Prefix | Cacheable? | Notes |
|---|---|---|
| System prompt | Yes | Stable across requests; first breakpoint candidate. |
| Tool / schema definitions | Yes | Stable; cache with or after the system prefix. |
| Few-shot exemplars | Yes | Stable; cache as a contiguous block. |
| Stable retrieved context (session-scoped corpus) | Conditionally | Only if stable within the cache window; per the architecture. |
| User input / per-request variables / timestamps | Never | Variance here invalidates every breakpoint upstream-of-it placement is designed to protect. |

Anthropic supports a small number of breakpoints (typically up to four). Order matters: the cacheable region must be a contiguous prefix ending at the breakpoint, with all per-request variance after it. A breakpoint placed after volatile content caches nothing.

### 3. The 5-minute TTL is accounted for, not assumed

The Anthropic prompt cache entry lives ~5 minutes from last use. Logical stability is not enough — the prefix must be re-read within the TTL by real traffic for the cache to pay off. Do the warm/cold accounting explicitly against the request rate:

- Traffic dense enough that the prefix is re-read within 5 minutes → cache reads dominate; the strategy pays off.
- Traffic sparser than the TTL → every request is a cold write, paying the cache-write premium with no read benefit. This is a cost regression, flag it as one; the fix (longer TTL tier where the architecture approves it, request batching, or accepting no caching) is an architecture decision, not a silent code default.

A cache miss is always a cost event, never a correctness failure — output is identical warm or cold.

### 4. Extended-thinking budget is enforced

If the capability uses extended thinking, the thinking-token budget comes from `ai-architecture.md` and is enforced on the request (`thinking: {type: "enabled", budget_tokens: <from-contract>}`). No unbounded thinking. The thinking-block retention rule across turns — keep prior thinking in the conversation, or strip it — is explicit and applied. If the capability does not use extended thinking, state N/A; do not leave it unaddressed.

### 5. Context packing is disciplined

Pack stable-first, volatile-last so every breakpoint stays upstream of per-request variance. Enforce the context budget: if assembled input would exceed it, apply the architecture's declared truncation policy (drop oldest turns, drop lowest-rank retrieved chunks, summarize — whatever the contract says). Truncation never silently drops grounding the capability's correctness depends on; if the only way to fit is to drop required grounding, that is an ADR candidate.

### 6. Isolation before sharing

A cached prefix shared across requests or tenants is a data-isolation surface. Tenant-specific data, user PII, or per-caller secrets must never sit inside a prefix that another caller's request can read from cache. Keep shared prefixes free of caller-specific data; place the isolation boundary upstream of the breakpoint.

### 7. Telemetry without leakage

Log model id, prompt version, latency, input/output tokens, cache-read tokens, cache-write tokens, computed cache hit rate, and thinking tokens. Never log raw prompts, raw retrieved content, secrets, or PII unredacted. The Anthropic API key is injected at deploy time and never committed.

## Step detail

**Step 1 — Load the strategy.** Open `ai-architecture.md`. Extract capability, cost/latency budgets, prompt-cache strategy, cacheable prefixes, extended-thinking requirement, thinking budget, thinking-retention rule, context budget, truncation policy. Missing any → ADR candidate before writing code.

**Step 2 — Verify completeness.** Confirm the cacheable prefixes, breakpoint plan, thinking budget, and context budget are all named. A silent gap here becomes an invented number later.

**Step 3 — Lay out the prompt.** Order content stable-first (system, tools/schema, exemplars, stable context), volatile-last (user input, per-request variables). The cacheable region must be a contiguous prefix.

**Step 4 — Place breakpoints.** Add `cache_control` only on the stated stable prefixes, in the stated order and count. Confirm by inspection no breakpoint sits on or after per-request content.

**Step 5 — Warm/cold accounting.** Compare the real request rate to the 5-minute TTL. If the prefix re-warms every request, flag the cost trap explicitly and route the remedy as an architecture decision.

**Step 6 — Thinking budget.** Set `budget_tokens` from the contract. Apply the retention/stripping rule across turns. Mark N/A explicitly if thinking is not used.

**Step 7 — Context budget.** Enforce the budget; apply the declared truncation policy when exceeded. Required grounding is never silently dropped.

**Step 8 — Isolation check.** Verify no shared cached prefix carries one caller's PII or tenant data into another's context.

**Step 9 — Telemetry.** Emit the metrics in rule 7 with redaction. Confirm a cache miss surfaces as a cost metric, not an error.

**Step 10 — Tests.** Cover: cache-warm hit; cache-cold miss; TTL re-warm; thinking-budget enforcement; context-budget truncation. These five are the minimum.

**Step 11 — ADR candidates.** Write any unresolved cache/thinking/context/budget gap as an ADR candidate against `ai-architecture.md`. Do not silently fill it.

## Anti-patterns to detect

Call these out explicitly when found:

- `cache_control` placed on or after per-request variable content, so the cache never hits
- Breakpoint count or order left implicit ("just cache the system prompt somewhere")
- Logically stable prefix that re-warms every request because traffic is sparser than the 5-minute TTL, with no warm/cold accounting
- Cache miss treated as a correctness failure instead of a cost event
- Extended thinking enabled with no `budget_tokens`, or an invented budget not traced to the contract
- Thinking-block retention rule unaddressed across turns
- Context packed volatile-first, pushing breakpoints downstream of variance
- Context budget exceeded with silent truncation of grounding the capability needs
- Tenant data or PII inside a prefix shared across callers via cache
- Cache strategy, thinking budget, or context budget hardcoded instead of deploy-time config
- Raw prompt / retrieved content / secrets / PII in logs
- Anthropic API key or environment endpoint committed to source
- "Done" declared without the five required tests
