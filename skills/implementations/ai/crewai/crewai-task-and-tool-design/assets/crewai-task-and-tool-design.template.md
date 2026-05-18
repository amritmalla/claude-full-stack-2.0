# CrewAI Task and Tool Design — Integration Reference

Use this as the canonical shape when generating a CrewAI task decomposition and tool execution adapter. Placeholder tokens use `<kebab-case>` or `<PascalCase>`. Language is illustrative (CrewAI, Python); port to the target stack. Every value marked `# from ai-architecture.md` is a contract input, not a default.

## Integration header (record the decision)

```
Capability:      <capability-name>                 # from ai-architecture.md
Tasks → agents:  retrieve→Researcher, synthesize→Writer, verify→Critic   # from ai-architecture.md
Tool surface:    [retrieve_sources, ...]           # closed set, from ai-architecture.md
Side-effect:     retrieve_sources = read-only      # classified per tool, from ai-architecture.md
Authorization:   per-tool principal model          # from architecture/security
Idempotency:     key = corr_id+tool+arg_hash       # mutating tools only, from ai-architecture.md
Fan-out:         allowed | disallowed (bound: <n>) # from ai-architecture.md
Audit retention: <duration / policy>               # from ai-architecture.md
Eval set:        <fixed eval set id>               # from ai-architecture.md
Thresholds:      grounding ≥ <x>, citation ≥ <x>, answer ≥ <x>   # from ai-architecture.md
Provider:        injected at deploy time           # not hardcoded
```

## Task decomposition (1:1 with approved boundaries)

```python
retrieve_task = Task(
    description="Retrieve source material for <question>",   # explicit input contract
    expected_output="Ranked sources with ids",                # explicit output contract
    agent=researcher,                                          # one owning agent
    tools=[retrieve_sources],                                  # only the granted tool
)
synthesize_task = Task(
    description="Draft a cited answer from retrieved sources",
    expected_output="Draft answer with inline citations",
    agent=writer,                                              # no tools granted
)
verify_task = Task(
    description="Check every claim against retrieved sources",
    expected_output="GROUNDED_OK or a list of ungrounded claims",
    agent=critic,                                              # no tools granted
)
# One Task per approved boundary. Do not invent, split, merge, or chain into
# autonomy the design never granted. Crew topology / termination is owned by
# crewai-agent-workflow.
```

## Tool definition (schema verbatim from the contract)

```python
class RetrieveSourcesInput(BaseModel):
    query: str                       # exactly the approved schema; no widening
    k: int                           # required field not relaxed

retrieve_sources = StructuredTool(
    name="retrieve_sources",         # approved name, not renamed
    description="<approved description>",
    args_schema=RetrieveSourcesInput,
    func=adapter.run,                # all calls go through the execution adapter
)
# side-effect class: read-only (classified, not guessed)
```

## Execution adapter (model proposes, adapter disposes)

```python
def run(tool_name, args, ctx):
    principal = resolve_principal(ctx)            # from request context, NOT model output
    if not authorized(principal, tool_name, args):# enforced here, never in the prompt
        return error_result("denied")             # no side effect on denial
    validate(args, schema_for(tool_name))         # against the approved schema
    if side_effecting(tool_name):
        key = idempotency_key(ctx, tool_name, args)   # stable property, from ai-architecture.md
        if seen(key):
            return prior_result(key)              # replay does not double-apply
    result = execute(tool_name, args)
    audit(tool_name, principal, "allowed", key, classify(result), ctx.correlation_id)
    return result
```

## Fan-out policy

```
- fan-out disallowed        -> one tool call per step; assert in tests
- fan-out allowed, bound <n> -> per-call authz + idempotency, explicit order/concurrency
- unbounded side-effecting fan-out -> incident, not a throughput optimization
```

## Audit (every execution)

| Field | Source |
|---|---|
| `correlation_id` | per request, propagated through task + tool path |
| `tool_name`, `principal` | adapter (principal from request context) |
| `authz_outcome` | allowed \| denied |
| `idempotency_key` | mutating tools only |
| `result_class` | success \| denied \| failed |

Never log: secrets, raw tool arguments/results, unredacted PII. Retention follows the declared rule.

## Eval triplet wiring (computed + gated, exercises the tool/task layer)

```python
def evaluate(fixed_set):                  # fixed_set from ai-architecture.md
    runs = run_tasks(fixed_set)           # exercises retrieve_sources via the adapter
    g = grounding_score(runs)             # fraction of claims supported by retrieved sources
    c = citation_correctness(runs)        # citations actually support the claim
    a = answer_correctness(runs, gold)    # graded vs gold answers
    assert g >= G_THRESH and c >= C_THRESH and a >= A_THRESH   # fail closed
    emit_metrics(g, c, a)
```

## Required test matrix

| Test | Asserts |
|---|---|
| Valid tool call | Authorized, schema-valid call executes; result returned to its task |
| Unauthorized call | Denied before any side effect; error result, no execution |
| Tool failure | Tool error surfaced to its task; no false "done" |
| Idempotent replay | Replayed mutating call returns prior result; no double-apply |
| Fan-out bound | Multi-call task respects order/bound, or fan-out suppressed |
| Eval-gate failure | Below-threshold run fails closed, not shipped |

## Configuration (deploy-time, never committed)

```
MODEL_PROVIDER / MODEL_ID    # ai-architecture.md input, injected
TOOL_REGISTRY / AUTHZ_POLICY
IDEMPOTENCY_KEY_SOURCE / FANOUT_BOUND
EVAL_SET_ID / G_THRESH / C_THRESH / A_THRESH
AUDIT_RETENTION / TRACING_TARGET
```
