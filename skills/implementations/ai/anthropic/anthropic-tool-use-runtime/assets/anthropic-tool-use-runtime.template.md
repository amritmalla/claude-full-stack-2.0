# Anthropic Tool Use Runtime — Integration Reference

Use this as the canonical shape when generating an Anthropic tool-use integration. Placeholder tokens use `<kebab-case>` or `<PascalCase>`. Language is illustrative (Python SDK); port to the target stack. Every value marked `# from ai-architecture.md` is a contract input, not a default.

## Integration header (record the decision)

```
Capability:        <capability-name>                  # from ai-architecture.md
Tool surface:      <tool-1>, <tool-2>, ...             # from ai-architecture.md
tool_choice:       auto | any | tool:<name> | none     # chosen; reason below
Reason:            <why this tool_choice for this contract>
Parallel tools:    allowed | suppressed                # from ai-architecture.md
MCP connectors:    <named connector> | none            # from ai-architecture.md
Model tier:        <model-id>                          # from ai-architecture.md
Extended thinking: required | N/A                      # from ai-architecture.md
Cache strategy:    <tool-definition prefix cached>     # from ai-architecture.md
Idempotency:       <key source per mutating tool>      # from ai-architecture.md
Degradation:       <declared fallback behavior>        # from ai-architecture.md
Budget:            <max loop iterations>, <deadline ms> # from ai-architecture.md
```

## Tool definitions + request (cache the stable prefix)

```python
TOOLS = [
    {
        "name": "<tool_name>",                  # verbatim from ai-architecture.md
        "description": "<one-line: what the tool does and its side-effect class>",
        "input_schema": <APPROVED_TOOL_SCHEMA>,  # verbatim — do not widen/relax
    },
    # ... one entry per approved tool
]

resp = client.messages.create(
    model="<model-id>",                          # from ai-architecture.md
    max_tokens=<from-contract>,
    temperature=<from-contract>,                 # explicit where determinism required
    system=[
        {"type": "text", "text": SYSTEM_PROMPT},
    ],
    tools=TOOLS,
    tool_choice=<TOOL_CHOICE>,                    # explicit decision; from header
    # cache_control goes on the LAST stable prefix element (tools/system),
    # NEVER on tool_result or user content:
    extra_headers={},                            # no per-request secrets here
    messages=conversation,                       # tool_result turns appended here
)
# To suppress parallel tool use when the contract disallows it:
#   tool_choice = {"type": "auto", "disable_parallel_tool_use": True}
```

Cache placement: attach `"cache_control": {"type": "ephemeral"}` to the final
tool definition (or the system block when tools are dynamic-but-stable). Never
attach it to a `tool_result` or user message.

## Execution adapter (model proposes, adapter disposes)

```python
def execute_tool_use(block, request_ctx):
    principal = resolve_principal(request_ctx)      # from context, NOT model output
    if not is_authorized(principal, block.name, block.input):   # fail closed
        return tool_result(block.id, error="unauthorized", is_error=True)

    ok, errs = validate(block.input, schema_for(block.name))    # vs input_schema
    if not ok:
        return tool_result(block.id, error=errs, is_error=True)

    if is_mutating(block.name):
        key = idempotency_key(request_ctx, block.name, block.input)  # contract policy
        if seen(key):
            return tool_result(block.id, content=cached_result(key))  # no double-apply

    result = run_tool(block.name, block.input)       # the only side effect
    audit(tool=block.name, principal=principal, outcome="success",
          key=locals().get("key"), corr=request_ctx.correlation_id)  # no raw args
    return tool_result(block.id, content=result)
```

## Bounded tool loop

```python
for step in range(MAX_LOOP_ITERATIONS):              # bound from contract
    if resp.stop_reason != "tool_use":
        return finalize(resp)
    tool_uses = [b for b in resp.content if b.type == "tool_use"]   # skip "thinking"
    results = [execute_tool_use(b, request_ctx) for b in tool_uses] # per-call authz
    conversation += [
        {"role": "assistant", "content": resp.content},  # retain blocks unmutated
        {"role": "user", "content": results},             # one result per tool_use id
    ]
    resp = client.messages.create(..., messages=conversation)
return run_declared_degradation()                    # loop exhausted; from contract
```

## Extended-thinking reconciliation (only if required)

```
- Thinking blocks precede tool_use blocks in the response.
- Loop selects type == "tool_use"; tolerates and does not choke on "thinking".
- When thinking is retained across tool turns, append the assistant content
  unmodified so the thinking-block signature stays valid.
- Retain or strip thinking per ai-architecture.md retention rule — do not invent it.
```

## Telemetry + audit fields (emit every call; redact payloads)

| Field | Source |
|---|---|
| `model_id`, `prompt_version` | deploy-time config |
| `latency_ms` | measured |
| `input_tokens`, `output_tokens` | response usage |
| `cache_read_tokens`, `cache_write_tokens` | response usage |
| `tool_calls`, `tool_failures` | adapter counters |
| `authz_outcome` | allowed / denied |
| `idempotency_key`, `correlation_id` | adapter / request context |
| `result_class` | success / denied / failed |

Never log: raw tool arguments, raw tool results, secrets, PII (unredacted).

## Required test matrix

| Test | Asserts |
|---|---|
| Valid tool call | Authorized call validates, executes, returns `tool_result` |
| Unauthorized call | Denied before any side effect; error `tool_result` returned |
| Tool failure | Tool error surfaced as `tool_result`, loop continues/degrades correctly |
| Idempotent replay | Replayed `tool_use` does not double-apply the side effect |
| Loop-bound exhaustion | Max iterations respected; declared degradation path taken |
| Cache miss | Correct tool behavior; miss recorded as cost metric, not error |

## Configuration (deploy-time, never committed)

```
ANTHROPIC_API_KEY        # secret store / env injection
MCP_CONNECTOR_TOKEN      # only if an MCP connector is approved; never committed
MODEL_ID                 # e.g. claude-... — config, not hardcoded
PROMPT_VERSION           # config
TOOL_CHOICE_POLICY       # auto | any | tool:<name> | none
CACHE_STRATEGY           # which prefix elements carry cache_control
```
