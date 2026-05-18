# Anthropic Structured Output Runtime — Integration Reference

Use this as the canonical shape when generating an Anthropic structured-output integration. Placeholder tokens use `<kebab-case>` or `<PascalCase>`. Language is illustrative (Python SDK); port to the target stack. Every value marked `# from ai-architecture.md` is a contract input, not a default.

## Integration header (record the decision)

```
Capability:        <capability-name>            # from ai-architecture.md
Mechanism:         forced-tool | prefill | strict-prompt   # chosen; reason below
Reason:            <why this mechanism for this contract>
Model tier:        <model-id>                    # from ai-architecture.md
Extended thinking: required | N/A                # from ai-architecture.md
Cache strategy:    <stable-prefixes cached>      # from ai-architecture.md
Degradation:       <declared fallback behavior>  # from ai-architecture.md
Budget:            <max repair attempts>, <deadline ms>  # from ai-architecture.md
```

## Forced single-tool call (default mechanism)

```python
TOOL = {
    "name": "<emit_result>",
    "description": "<one-line: what the structured result represents>",
    "input_schema": <APPROVED_SCHEMA>,  # verbatim from ai-architecture.md — do not edit
}

resp = client.messages.create(
    model="<model-id>",
    max_tokens=<from-contract>,
    temperature=<from-contract>,            # explicit where determinism required
    system=[
        {"type": "text", "text": SYSTEM_PROMPT,
         "cache_control": {"type": "ephemeral"}},   # stable prefix only
    ],
    tools=[TOOL],
    tool_choice={"type": "tool", "name": "<emit_result>"},
    messages=[{"role": "user", "content": user_input}],  # NEVER cache_control here
)
```

## Prefill mechanism (lightweight objects)

```python
messages=[
    {"role": "user", "content": user_input},
    {"role": "assistant", "content": "{"},   # prefill opens the JSON object
]
# Re-prepend "{" to the completion before parsing.
```

## Validate → bounded repair → declared degradation

```python
for attempt in range(MAX_REPAIR_ATTEMPTS + 1):     # bound from contract
    obj = parse(raw)
    ok, errors = validate(obj, APPROVED_SCHEMA)     # fail closed
    if ok:
        return obj
    if attempt == MAX_REPAIR_ATTEMPTS or deadline_exceeded():
        return run_declared_degradation()           # from ai-architecture.md
    raw = repair_call(raw, errors)                  # re-prompt WITH the errors
```

## Extended-thinking reconciliation (only if required)

```
- Thinking blocks precede the tool_use block in the response.
- Parser iterates content blocks, selects type == "tool_use", ignores "thinking".
- Retain or strip thinking per ai-architecture.md retention rule — do not invent it.
```

## Telemetry fields (emit every call; redact payloads)

| Field | Source |
|---|---|
| `model_id`, `prompt_version` | deploy-time config |
| `latency_ms` | measured |
| `input_tokens`, `output_tokens` | response usage |
| `cache_read_tokens`, `cache_write_tokens` | response usage |
| `validation_outcome` | pass / fail |
| `path` | success / repair / degradation |

Never log: raw prompt, raw output, secrets, PII (unredacted).

## Required test matrix

| Test | Asserts |
|---|---|
| Valid output | Conforming response parses, validates, returns the object |
| Malformed output | Schema violation triggers repair, not a partial return |
| Refusal / degradation | Declared degradation behavior executes |
| Retry exhaustion | Bound respected; degradation path taken at the limit |
| Cache miss | Correct output produced; miss recorded as cost metric, not error |

## Configuration (deploy-time, never committed)

```
ANTHROPIC_API_KEY        # secret store / env injection
MODEL_ID                 # e.g. claude-... — config, not hardcoded
PROMPT_VERSION           # config
CACHE_STRATEGY           # which prefixes carry cache_control
```
