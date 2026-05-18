# AutoGen Tool Orchestration — Integration Reference

Use this as the canonical shape when generating an AutoGen tool registry and execution adapter. Placeholder tokens use `<kebab-case>` or `<PascalCase>`. Language is illustrative (AutoGen AgentChat, Python); port to the target stack. Every value marked `# from ai-architecture.md` is a contract input, not a default.

## Integration header (record the decision)

```
Tool surface:    <tool-a>, <tool-b>                # from ai-architecture.md
Side-effect:     retrieve_sources=read-only, <tool-b>=<class>   # from ai-architecture.md
Authorization:   <per-tool model>, principal from <request-context source>  # from ai-architecture.md
Idempotency:     key = <stable property> for side-effecting tools   # from ai-architecture.md
Audit retention: <duration / policy>               # from ai-architecture.md
Eval set:        <fixed eval set id>               # from ai-architecture.md
Thresholds:      grounding ≥ <x>, citation ≥ <x>, answer ≥ <x>   # from ai-architecture.md
Provider:        injected at deploy time           # not hardcoded
```

## Tool schema (contract surface, verbatim from the architecture)

```python
# Researcher's retrieval tool — schema is the contract the Critic's
# grounding check depends on. Do not widen or rename.
def retrieve_sources(query: str, k: int) -> list[dict]:
    """<approved description from ai-architecture.md>"""
    # signature/schema == approved input_schema, field-for-field
```

## Per-agent registration (closed set, not global)

```python
RESEARCH_TOOLS = [guarded(retrieve_sources)]   # approved surface only
researcher = AssistantAgent("researcher", model_client=CLIENT, tools=RESEARCH_TOOLS)
writer     = AssistantAgent("writer",     model_client=CLIENT)   # no tools granted
critic     = AssistantAgent("critic",     model_client=CLIENT)   # no tools granted
# No global registry. A tool not granted to an agent is not callable by it.
```

## Execution adapter — model proposes, adapter disposes

```python
def guarded(fn):
    def adapter(**args):
        principal = resolve_principal_from_context()        # NOT from model output
        if not authorized(principal, fn.__name__, args):     # before any side effect
            audit(fn.__name__, principal, "denied", None, "denied")
            return error_result("unauthorized")              # structured, not an exception
        validate_against_schema(fn.__name__, args)           # approved input_schema
        key = idempotency_key(CORRELATION_ID, fn.__name__, args)  # side-effecting tools
        if (prior := idem_store.get(key)) is not None:
            audit(fn.__name__, principal, "allowed", key, "success")
            return prior                                     # replay: no double-apply
        try:
            result = fn(**args)
        except ToolError as e:
            audit(fn.__name__, principal, "allowed", key, "failed")
            return error_result(str(e))                      # failure into the loop
        idem_store.put(key, result)
        audit(fn.__name__, principal, "allowed", key, "success")
        return result
    return adapter
```

## Idempotency (side-effecting tools)

```
key = <stable property>            # e.g. correlation_id + tool_name + arg_hash
replay  -> return stored result    # never a second side effect
read-only tool -> skip ONLY if side-effect class is explicitly read-only
```

## Audit record (every execution)

| Field | Source |
|---|---|
| `tool_name` | adapter |
| `principal` | resolved from request context |
| `authz_outcome` | allowed \| denied |
| `idempotency_key` | side-effecting tools |
| `result_class` | success \| denied \| failed |
| `correlation_id` | per workflow run |

Never log: secrets, raw tool arguments, raw results, unredacted PII.

## Tool-failure wiring (Research-and-synthesize)

```
retrieval fails -> structured error result -> agent loop
Critic sees no sources -> grounding gate does NOT pass (never "grounded on nothing")
```

## Eval triplet wiring (computed + gated, through the real tool path)

```python
def evaluate(fixed_set):                  # fixed_set from ai-architecture.md
    runs = run_workflow(fixed_set)        # exercises the REGISTERED retrieve_sources
    g = grounding_score(runs)             # fraction of claims supported by sources
    c = citation_correctness(runs)        # citations actually support the claim
    a = answer_correctness(runs, gold)    # graded vs gold answers
    assert g >= G_THRESH and c >= C_THRESH and a >= A_THRESH   # fail closed
    emit_metrics(g, c, a)
```

## Required test matrix

| Test | Asserts |
|---|---|
| Valid call | Authorized, schema-valid call executes; result returned |
| Unauthorized call | Denied at execution before any side effect; error result |
| Tool failure | Tool error → structured error; Critic gate cannot pass on it |
| Idempotent replay | Replayed side-effecting call returns prior result, no double-apply |
| Out-of-surface / ungranted | Ungranted or unknown tool call denied |
| Eval-gate failure | Below-threshold run fails closed, not shipped |

## Configuration (deploy-time, never committed)

```
MODEL_PROVIDER / MODEL_ID              # ai-architecture.md input, injected
AUTHZ_POLICY / PRINCIPAL_SOURCE
IDEMPOTENCY_KEY_SOURCE
AUDIT_RETENTION
EVAL_SET_ID / G_THRESH / C_THRESH / A_THRESH
RETRIEVAL_BACKEND_CREDENTIALS          # injected, never committed
TRACING_TARGET
```
