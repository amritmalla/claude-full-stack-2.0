# AutoGen Multi-Agent Workflow — Integration Reference

Use this as the canonical shape when generating an AutoGen multi-agent workflow. Placeholder tokens use `<kebab-case>` or `<PascalCase>`. Language is illustrative (AutoGen AgentChat, Python); port to the target stack. Every value marked `# from ai-architecture.md` is a contract input, not a default.

## Integration header (record the decision)

```
Workflow:        <workflow-name>                  # from ai-architecture.md
Topology:        group-chat | team                # from ai-architecture.md
Roles → agents:  Researcher→<Agent>, Critic→<Agent>, Writer→<Agent>
Termination:     <role> holds authority           # from ai-architecture.md
Max turns:       <n>   Per-agent steps: <n>   Wall-clock: <ms>   # from ai-architecture.md
Degradation:     <declared behavior on exhaustion> # from ai-architecture.md
Eval set:        <fixed eval set id>               # from ai-architecture.md
Thresholds:      grounding ≥ <x>, citation ≥ <x>, answer ≥ <x>   # from ai-architecture.md
Provider:        injected at deploy time           # not hardcoded
```

## Role-to-agent mapping (1:1, explicit)

```python
researcher = AssistantAgent("researcher", model_client=CLIENT, tools=RESEARCH_TOOLS)  # tools per topology
writer     = AssistantAgent("writer",     model_client=CLIENT)                        # no tools granted
critic     = AssistantAgent("critic",     model_client=CLIENT)                        # termination authority
# One agent per approved role. Do not merge or split roles.
```

## Termination as a code-checked condition (not a prompt)

```python
# Critic holds termination authority. The gate is a checked condition,
# NOT "say TERMINATE when grounded" in a system message.
grounded = TextMentionTermination("GROUNDED_OK")          # critic emits only when its check passes
budget   = MaxMessageTermination(MAX_TURNS)               # from ai-architecture.md
team = RoundRobinGroupChat(
    [researcher, writer, critic],
    termination_condition=grounded | budget,
)
# On budget-hit: run the declared degradation path; never present truncation as success.
```

## Per-agent tool registration (closed set)

```python
RESEARCH_TOOLS = [retrieve_sources]      # approved surface only, Researcher only
# Writer/Critic receive no tools they were not granted by the topology.
# Authorization is checked in the execution adapter (see autogen-tool-orchestration),
# never delegated to the model.
```

## Loop / stall safety

```
- identical-turn repeat by one agent      -> terminate -> degradation
- two-agent ping-pong with no state change -> terminate -> degradation
- critic grounding verdict not improving   -> terminate -> degradation
```

## Tracing (every turn)

| Field | Source |
|---|---|
| `correlation_id` | per workflow run |
| `turn_index`, `acting_role` | orchestrator |
| `tool_name`, `authz_outcome` | execution adapter |
| `termination_cause` | grounded \| budget \| loop-stall |
| metrics: turns, per-role actions, tool calls | orchestrator |

Never log: secrets, raw tool payloads, unredacted PII.

## Eval triplet wiring (computed + gated, not described)

```python
def evaluate(fixed_set):                  # fixed_set from ai-architecture.md
    g = grounding_score(runs)             # fraction of claims supported by sources
    c = citation_correctness(runs)        # citations actually support the claim
    a = answer_correctness(runs, gold)    # graded vs gold answers
    assert g >= G_THRESH and c >= C_THRESH and a >= A_THRESH   # fail closed
    emit_metrics(g, c, a)
```

## Required test matrix

| Test | Asserts |
|---|---|
| Success | Cited answer; Critic grounding gate passed within budget |
| Critic-gated revision | Ungrounded draft rejected, revised, then accepted |
| Tool failure | Researcher tool error handled; no false "done" |
| Unsafe-action denial | Unauthorized/ungranted tool call denied at execution |
| Turn/loop exhaustion | Budget/loop hit → declared degradation path runs |
| Eval-gate failure | Below-threshold run fails closed, not shipped |

## Configuration (deploy-time, never committed)

```
MODEL_PROVIDER / MODEL_ID    # ai-architecture.md input, injected
MAX_TURNS / STEP_BUDGET / WALL_CLOCK_MS
EVAL_SET_ID / G_THRESH / C_THRESH / A_THRESH
TRACING_TARGET
```
