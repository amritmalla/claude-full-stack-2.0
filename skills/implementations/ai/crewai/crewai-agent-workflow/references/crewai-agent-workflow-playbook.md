# CrewAI Agent Workflow Playbook

Load this when implementing any owned area of `crewai-agent-workflow` or checking the anti-pattern list. It expands the operating rules and process steps in `SKILL.md` with the CrewAI detail needed to produce a production-grade multi-agent runtime grounded in the Research-and-synthesize reference.

## Why this workflow exists

Multi-agent runtimes fail in production in ways single calls do not: two agents ping-pong until the token budget is exhausted; a hierarchical manager agent silently gains delegation authority the architecture never granted; the crew "completes" with a confident answer that no source supports because termination was a polite request in a role backstory rather than a checked condition; a tool the topology never authorized for the Writer gets called because tools were attached at the crew level instead of per-agent.

The goal is a CrewAI workflow whose topology, process model, termination authority, budgets, and eval gating are all code-enforced and traceable — and whose behavior is anchored to one concrete reference (Research-and-synthesize) with measurable evals, so the skill teaches a grounded realization rather than generic CrewAI tips.

## Behavioral rules in depth

### 1. Consume the topology; do not invent it

The roles, the process model (sequential / hierarchical), the task edges, delegation, and the termination authority all come from `ai-architecture.md`. Read it before constructing a crew. Do not add a manager/orchestrator agent, a `Process.hierarchical` topology, a planner/executor split, or `allow_delegation=True` that the approved topology does not contain. A missing topology decision is an ADR candidate, not an implementation choice.

### 2. One role, one agent, explicitly mapped

Each approved role maps to exactly one CrewAI agent with its own role/goal/backstory. In Research-and-synthesize that is Researcher → one agent, Critic/verifier → one agent, Writer → one agent. Do not merge Critic into Writer "for efficiency" or split Researcher across two agents. The mapping is recorded so a reviewer can check it against the architecture without reading agent internals.

### 3. Termination is a checked condition, owned by a role

The Critic/verifier holds termination authority. Implement it as a guardrail / task callback on the Critic's verification task that evaluates the Critic's structured verdict — not as "stop when the answer is grounded" in a role backstory or task description. A backstory request is not an enforcement mechanism: the model can ignore it, and then nothing stops the crew. The crew continues into a revision task only when the gate rejects; it completes only when the gate passes or the budget is hit.

### 4. Budgets are enforced on the crew

Max steps, per-agent step bounds, and a wall-clock ceiling are enforced in crew/orchestrator code (`max_iter` / `max_rpm` plus an explicit step counter and guard), independent of any model's cooperation. Budget exhaustion routes to the architecture's degradation path — it is not an exception swallowed in a catch block, and it is not silent truncation presented as success.

### 5. Loop and stall safety is explicit

Detect: the same agent emitting near-identical task outputs, two agents alternating with no state change, and rounds where the Critic's grounding verdict does not improve. Any of these terminates into the degradation path. "It usually converges" is not loop safety.

### 6. Tools are per-agent and closed

Register only the approved tool surface, and attach each tool only to the agents the topology permits — tools are bound on the `Agent`, never globally on the `Crew`. In the reference, the Researcher has retrieval tools; the Writer and Critic do not get write/retrieval tools they were never granted. A model-proposed tool call is untrusted: authorization is checked in the execution path, never delegated to the model or to a role backstory. (Task decomposition and tool-execution mechanics are owned by `crewai-task-and-tool-design`; this skill consumes them and enforces the per-agent registration boundary.)

### 7. The eval triplet is wired, not narrated

Grounding score, citation correctness, and answer correctness are computed against the fixed eval set and gated at the architecture's thresholds. A skill that says "evaluate grounding" without a computed metric and a gate is exactly the generic framework advice the deferral warned about. The eval harness runs the crew over the fixed set and fails closed below threshold.

### 8. Provider-neutral orchestration

The model/provider is an `ai-architecture.md` input injected at deploy time. This skill owns crew topology and process model, not provider SDK mechanics; do not hardcode a provider client, model id, or `llm=` literal. Provider specifics belong to the provider skills.

## Step detail

**Step 1 — Load the topology.** From `ai-architecture.md` extract roles, process model (sequential / hierarchical), task order, termination authority, tool surface, memory policy, stop conditions, degradation behavior, eval plan. For Research-and-synthesize: Researcher/Critic/Writer, Critic terminates.

**Step 2 — Verify completeness.** Confirm max steps, per-agent bounds, termination authority, tool authorization, and eval thresholds are all named. Any gap → ADR candidate before code.

**Step 3 — Role-to-agent mapping.** Create one agent per role with explicit role/goal/backstory; record the mapping in the integration header.

**Step 4 — Topology.** Build the crew with the approved process. Sequential: the Research → Write → Verify task chain is explicit. Hierarchical: only if the architecture grants a manager; the manager is not invented. The control flow matches the architecture; the cycle is explicit, not emergent.

**Step 5 — Termination + degradation.** Implement the gate as a guardrail/callback on the Critic's task evaluating its grounding verdict. Wire the max-step-exhaustion path to the architecture's declared degradation behavior.

**Step 6 — Tools per agent.** Attach approved tools to permitted agents only, with authorization and input validation on execution; `allow_delegation` off unless granted.

**Step 7 — Memory/session.** Implement retention, scoping, redaction exactly as specified. No unbounded crew memory or shared scratchpad.

**Step 8 — Budgets + loop safety.** Enforce max-step/per-agent/wall-clock and loop/stall detection in crew code.

**Step 9 — Tracing.** Trace every task execution, tool call, role transition, and the termination decision with a correlation id and deciding role.

**Step 10 — Eval wiring.** Run the crew over the fixed eval set; compute grounding, citation correctness, answer correctness; gate at thresholds; emit metrics.

**Step 11 — Tests.** Success; critic-rejected-then-revised; tool failure; unsafe-action denial; step exhaustion → degradation; eval-gate failure.

**Step 12 — ADR candidates.** Record any unresolved topology/process/tool/budget/degradation/eval gap rather than filling it silently.

## Anti-patterns to detect

Call these out explicitly when found:

- Roles invented, merged, or split relative to `ai-architecture.md`
- A hierarchical manager, delegation edge, or `allow_delegation=True` the topology never approved
- Termination requested in a role backstory or task description instead of a checked condition
- Max steps / wall-clock not enforced, or exhaustion presented as success
- No loop/stall detection ("it usually converges")
- Tools attached on the crew globally instead of per-agent
- Authorization delegated to the model rather than checked on execution
- The eval triplet described but not computed or not gated (generic-advice smell)
- Provider SDK client, model id, or `llm=` literal hardcoded in the crew
- Unbounded crew memory or shared scratchpad across agents
- "Done" declared without the six required tests
