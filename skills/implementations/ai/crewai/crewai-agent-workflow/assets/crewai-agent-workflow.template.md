# CrewAI Agent Workflow — Integration Reference

Use this as the canonical shape when generating a CrewAI multi-agent workflow. Placeholder tokens use `<kebab-case>` or `<PascalCase>`. Language is illustrative (CrewAI, Python); port to the target stack. Every value marked `# from ai-architecture.md` is a contract input, not a default.

## Integration header (record the decision)

```
Workflow:        <workflow-name>                  # from ai-architecture.md
Process:         sequential | hierarchical        # from ai-architecture.md
Roles → agents:  Researcher→<Agent>, Critic→<Agent>, Writer→<Agent>
Termination:     <role> holds authority           # from ai-architecture.md
Max steps:       <n>   Per-agent steps: <n>   Wall-clock: <ms>   # from ai-architecture.md
Degradation:     <declared behavior on exhaustion> # from ai-architecture.md
Eval set:        <fixed eval set id>               # from ai-architecture.md
Thresholds:      grounding ≥ <x>, citation ≥ <x>, answer ≥ <x>   # from ai-architecture.md
Provider:        injected at deploy time           # not hardcoded
```

## Role-to-agent mapping (1:1, explicit)

```python
researcher = Agent(role="Researcher", goal=..., backstory=...,
                    tools=RESEARCH_TOOLS, allow_delegation=False)   # tools per topology
writer     = Agent(role="Writer",     goal=..., backstory=...,
                    tools=[],          allow_delegation=False)       # no tools granted
critic     = Agent(role="Critic",     goal=..., backstory=...,
                    tools=[],          allow_delegation=False)       # termination authority
# One agent per approved role. Do not merge or split roles.
# allow_delegation stays False unless the approved topology grants it.
```

## Termination as a code-checked condition (not a backstory)

```python
# Critic holds termination authority. The gate is a checked guardrail on the
# verification task, NOT "stop when grounded" in a backstory/task description.
def grounding_gate(output):                       # evaluates Critic's structured verdict
    verdict = parse_verdict(output)
    if verdict.grounded:
        return (True, output)                     # crew completes
    return (False, "REVISE")                      # route to revision task

verify_task = Task(description=..., agent=critic, guardrail=grounding_gate)
crew = Crew(agents=[researcher, writer, critic],
            tasks=[research_task, write_task, verify_task],
            process=Process.sequential,           # from ai-architecture.md
            max_rpm=MAX_RPM)
# On max-step hit: run the declared degradation path; never present truncation as success.
```

## Per-agent tool registration (closed set)

```python
RESEARCH_TOOLS = [retrieve_sources]      # approved surface only, Researcher only
# Tools are bound on the Agent, never globally on the Crew.
# Writer/Critic receive no tools they were not granted by the topology.
# Authorization is checked in the execution adapter (see crewai-task-and-tool-design),
# never delegated to the model.
```

## Loop / stall safety

```
- identical task-output repeat by one agent  -> terminate -> degradation
- two-agent ping-pong with no state change    -> terminate -> degradation
- critic grounding verdict not improving      -> terminate -> degradation
```

## Tracing (every step)

| Field | Source |
|---|---|
| `correlation_id` | per workflow run |
| `step_index`, `acting_role` | orchestrator |
| `tool_name`, `authz_outcome` | execution adapter |
| `termination_cause` | grounded \| budget \| loop-stall |
| metrics: steps, per-role actions, tool calls | orchestrator |

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
| Step/loop exhaustion | Budget/loop hit → declared degradation path runs |
| Eval-gate failure | Below-threshold run fails closed, not shipped |

## Configuration (deploy-time, never committed)

```
MODEL_PROVIDER / MODEL_ID    # ai-architecture.md input, injected
MAX_STEPS / STEP_BUDGET / WALL_CLOCK_MS / MAX_RPM
EVAL_SET_ID / G_THRESH / C_THRESH / A_THRESH
TRACING_TARGET
```
