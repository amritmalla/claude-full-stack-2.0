# AutoGen Multi-Agent Workflow Playbook

Load this when implementing any owned area of `autogen-multi-agent-workflow` or checking the anti-pattern list. It expands the operating rules and process steps in `SKILL.md` with the AutoGen detail needed to produce a production-grade multi-agent runtime grounded in the Research-and-synthesize reference.

## Why this workflow exists

Multi-agent runtimes fail in production in ways single calls do not: two agents ping-pong until the token budget is exhausted; a "manager" agent silently gains delegation authority the architecture never granted; the workflow "completes" with a confident answer that no source supports because termination was a polite request in a system prompt rather than a checked condition; a tool the topology never authorized for the Writer gets called because the tool registry was global instead of per-agent.

The goal is an AutoGen workflow whose topology, termination authority, budgets, and eval gating are all code-enforced and traceable — and whose behavior is anchored to one concrete reference (Research-and-synthesize) with measurable evals, so the skill teaches a grounded realization rather than generic AutoGen tips.

## Behavioral rules in depth

### 1. Consume the topology; do not invent it

The roles, who may speak/act when, delegation edges, and the termination authority all come from `ai-architecture.md`. Read it before constructing a group chat or team. Do not add a manager/orchestrator agent, a planner/executor split, or agent-to-agent delegation that the approved topology does not contain. A missing topology decision is an ADR candidate, not an implementation choice.

### 2. One role, one agent, explicitly mapped

Each approved role maps to exactly one AutoGen agent. In Research-and-synthesize that is Researcher → one agent, Critic/verifier → one agent, Writer → one agent. Do not merge Critic into Writer "for efficiency" or split Researcher across two agents. The mapping is recorded so a reviewer can check it against the architecture without reading agent internals.

### 3. Termination is a checked condition, owned by a role

The Critic/verifier holds termination authority. Implement it as a termination condition on the group chat / team (an `is_termination_msg` predicate or an explicit team termination condition) that evaluates the Critic's verdict — not as "Critic, say TERMINATE when grounded" in a system message. A prompt request is not an enforcement mechanism: the model can ignore it, and then nothing stops the loop.

### 4. Budgets are enforced on the orchestrator

Max turns, per-agent step bounds, and a wall-clock ceiling are enforced in orchestrator code (max-round/max-turn settings plus an explicit guard), independent of any model's cooperation. Budget exhaustion routes to the architecture's degradation path — it is not an exception swallowed in a catch block, and it is not silent truncation presented as success.

### 5. Loop and stall safety is explicit

Detect: the same agent emitting near-identical turns, two agents alternating with no state change, and rounds where the Critic's grounding verdict does not improve. Any of these terminates into the degradation path. "It usually converges" is not loop safety.

### 6. Tools are per-agent and closed

Register only the approved tool surface, and register each tool only on the agents the topology permits. In the reference, the Researcher has retrieval tools; the Writer and Critic do not get write/retrieval tools they were never granted. A model-proposed tool call is untrusted: authorization is checked in the execution path, never delegated to the model. (Tool-execution mechanics are owned by `autogen-tool-orchestration`; this skill consumes them and enforces the per-agent registration boundary.)

### 7. The eval triplet is wired, not narrated

Grounding score, citation correctness, and answer correctness are computed against the fixed eval set and gated at the architecture's thresholds. A skill that says "evaluate grounding" without a computed metric and a gate is exactly the generic framework advice the deferral warned about. The eval harness runs the workflow over the fixed set and fails closed below threshold.

### 8. Provider-neutral orchestration

The model/provider is an `ai-architecture.md` input injected at deploy time. This skill owns orchestration topology, not provider SDK mechanics; do not hardcode a provider client or model id. Provider specifics belong to the provider skills.

## Step detail

**Step 1 — Load the topology.** From `ai-architecture.md` extract roles, speaker/turn order or team structure, termination authority, tool surface, memory policy, stop conditions, degradation behavior, eval plan. For Research-and-synthesize: Researcher/Critic/Writer, Critic terminates.

**Step 2 — Verify completeness.** Confirm max turns, per-agent bounds, termination authority, tool authorization, and eval thresholds are all named. Any gap → ADR candidate before code.

**Step 3 — Role-to-agent mapping.** Create one agent per role; record the mapping in the integration header.

**Step 4 — Topology.** Build the group chat (custom speaker selection matching the approved order) or team. The control flow matches the architecture; the Researcher → Writer → Critic → (revise|done) cycle is explicit, not emergent.

**Step 5 — Termination + degradation.** Implement the termination condition evaluating the Critic's grounding verdict. Wire the max-turn-exhaustion path to the architecture's declared degradation behavior.

**Step 6 — Tools per agent.** Register approved tools on permitted agents only, with authorization and input validation on execution.

**Step 7 — Memory/session.** Implement retention, scoping, redaction exactly as specified. No unbounded shared scratchpad.

**Step 8 — Budgets + loop safety.** Enforce max-turn/step/wall-clock and loop/stall detection in orchestrator code.

**Step 9 — Tracing.** Trace every turn, tool call, role transition, and the termination decision with a correlation id and deciding role.

**Step 10 — Eval wiring.** Run the workflow over the fixed eval set; compute grounding, citation correctness, answer correctness; gate at thresholds; emit metrics.

**Step 11 — Tests.** Success; critic-rejected-then-revised; tool failure; unsafe-action denial; turn exhaustion → degradation; eval-gate failure.

**Step 12 — ADR candidates.** Record any unresolved topology/tool/budget/degradation/eval gap rather than filling it silently.

## Anti-patterns to detect

Call these out explicitly when found:

- Roles invented, merged, or split relative to `ai-architecture.md`
- A manager/orchestrator or delegation edge the topology never approved
- Termination requested in a system prompt instead of a checked condition
- Max turns / wall-clock not enforced, or exhaustion presented as success
- No loop/stall detection ("it usually converges")
- A global tool registry instead of per-agent registration
- Authorization delegated to the model rather than checked on execution
- The eval triplet described but not computed or not gated (generic-advice smell)
- Provider SDK client or model id hardcoded in the orchestration
- Unbounded shared memory/scratchpad across agents
- "Done" declared without the six required tests
