# Anthropic Prompt Caching and Context Runtime — Integration Reference

Use this as the canonical shape when generating an Anthropic caching and context integration. Placeholder tokens use `<kebab-case>` or `<PascalCase>`. Language is illustrative (Python SDK); port to the target stack. Every value marked `# from ai-architecture.md` is a contract input, not a default.

## Integration header (record the decision)

```
Capability:          <capability-name>             # from ai-architecture.md
Cache strategy:      <stable prefixes, in order>   # from ai-architecture.md
Breakpoint count:    <n>                           # from ai-architecture.md
Cost/latency budget: <token target>, <latency ms>  # from ai-architecture.md
Traffic shape:       <req/min>                      # informs TTL warm/cold
Extended thinking:   required | N/A                 # from ai-architecture.md
Thinking budget:     <budget_tokens>                # from ai-architecture.md
Thinking retention:  keep | strip                   # from ai-architecture.md
Context budget:      <max input tokens>             # from ai-architecture.md
Truncation policy:   <declared behavior on overflow> # from ai-architecture.md
```

## Prompt layout — stable-first, volatile-last

```
[ system prompt            ]  <- cacheable, breakpoint candidate 1
[ tool / schema definitions]  <- cacheable, breakpoint candidate 2
[ few-shot exemplars       ]  <- cacheable, breakpoint candidate 3
[ stable session context   ]  <- cacheable IF stable in window (architecture)
---- cache breakpoint(s) end here; everything below is per-request ----
[ retrieved per-request ctx]  <- NEVER a breakpoint
[ user input / variables   ]  <- NEVER a breakpoint
```

## Breakpoint placement (stable prefixes only)

```python
resp = client.messages.create(
    model="<model-id>",                              # config, not hardcoded
    max_tokens=<from-contract>,
    system=[
        {"type": "text", "text": SYSTEM_PROMPT,
         "cache_control": {"type": "ephemeral"}},     # stable prefix only
    ],
    tools=TOOL_DEFS,                                  # stable; cache with prefix
    messages=[
        {"role": "user", "content": [
            {"type": "text", "text": STABLE_EXEMPLARS,
             "cache_control": {"type": "ephemeral"}},  # last stable breakpoint
            {"type": "text", "text": per_request_input},  # NO cache_control
        ]},
    ],
)
```

| Prefix | `cache_control`? |
|---|---|
| System prompt | Yes (stable) |
| Tool / schema definitions | Yes (stable) |
| Few-shot exemplars | Yes (stable) |
| Stable session context | Conditionally (per architecture) |
| Retrieved per-request context | Never |
| User input / variables / timestamps | Never |

## 5-minute TTL warm/cold accounting

```
TTL ≈ 5 min from last use of the cached prefix.

requests/min high enough that prefix is re-read within 5 min
    -> cache_read dominates; strategy pays off.

requests slower than 1 per 5 min
    -> every call is a cold cache_write (premium), zero read benefit
    -> COST TRAP: flag it; remedy (longer-TTL tier / batching /
       no caching) is an ADR candidate, not a silent default.

A cache miss is a cost event. Output is identical warm vs cold.
```

## Extended-thinking budget (only if required)

```python
thinking={"type": "enabled", "budget_tokens": <from-contract>}  # bounded
# Retention across turns: keep prior thinking blocks in the
# conversation, OR strip them — per ai-architecture.md. Do not invent.
```

## Context budget and truncation

```python
if assembled_tokens > CONTEXT_BUDGET:                 # from contract
    inputs = apply_declared_truncation(inputs)        # from ai-architecture.md
    # never silently drop grounding the capability requires;
    # if the only fit drops required grounding -> ADR candidate
```

## Telemetry fields (emit every call; redact payloads)

| Field | Source |
|---|---|
| `model_id`, `prompt_version` | deploy-time config |
| `latency_ms` | measured |
| `input_tokens`, `output_tokens` | response usage |
| `cache_read_tokens`, `cache_write_tokens` | response usage |
| `cache_hit_rate` | derived (read / (read + write)) |
| `thinking_tokens` | response usage (when thinking enabled) |

Never log: raw prompt, raw retrieved content, secrets, PII (unredacted).

## Required test matrix

| Test | Asserts |
|---|---|
| Cache-warm hit | Second call within TTL reads the cached prefix; cache_read_tokens > 0 |
| Cache-cold miss | First/expired call writes the prefix; output identical, miss is a cost metric |
| TTL re-warm | Call after TTL expiry re-writes; accounted as cost, not error |
| Thinking-budget enforcement | Thinking respects `budget_tokens`; no unbounded thinking |
| Context-budget truncation | Over-budget input truncated per declared policy; required grounding kept |

## Configuration (deploy-time, never committed)

```
ANTHROPIC_API_KEY        # secret store / env injection
MODEL_ID                 # e.g. claude-... — config, not hardcoded
PROMPT_VERSION           # config
CACHE_STRATEGY           # which prefixes carry cache_control, order, count
THINKING_BUDGET          # budget_tokens — config, not hardcoded
CONTEXT_BUDGET           # max input tokens — config, not hardcoded
```
