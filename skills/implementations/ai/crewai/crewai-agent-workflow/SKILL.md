---
name: crewai-agent-workflow
description: Use when an approved ai-architecture.md defines a multi-agent workflow and CrewAI is the chosen framework. Produces the crew topology, role-to-agent mapping, critic-gated termination, budgets, and eval wiring. Not for single-agent runtimes, tool-surface design, or provider SDK work.
---

# CrewAI Agent Workflow

## When to use

Invoke when `ai-architecture.md` approves a multi-agent topology and CrewAI
(crews, agents, tasks, processes) is the chosen orchestration framework.

Do not use when the architecture approves only a single agent (use the
single-agent baseline), when the workflow needs no multi-agent control flow, or
to design the tool surface itself (that is an upstream architecture decision and
a `tool-calling-runtime` implementation concern).

## Inputs

Required:

- Approved `ai-architecture.md`.
- The approved multi-agent topology: roles, the process model
  (sequential / hierarchical), who acts when, and the termination authority.
- Tool surface and per-tool authorization model.
- Stop conditions, max-step budget, and degradation behavior.
- Eval plan: the fixed evaluation set and the pass thresholds.
- Target application language and framework; provider/model contract.

Optional:

- Existing tool implementations and retrieval surface.
- Memory or session storage policy.
- OpenTelemetry / tracing target.
- Sample successful and failed crew transcripts.

## Reference workflow

This skill is grounded in a concrete reference so it does not degrade into
generic framework advice: **Research-and-synthesize**. Three roles —
**Researcher** (retrieves source material for a question from the
architecture-defined retrieval surface), **Critic/verifier** (checks the draft's
claims against retrieved sources, flags ungrounded or mis-cited statements,
gates completion), **Writer** (produces the final answer with inline citations).
Input: a question. Output: a cited synthesized answer. The Critic holds
termination authority; the workflow is not done until grounding passes or the
max-step budget is hit, after which the architecture's degradation path runs.
The realization is CrewAI-specific — role/goal/backstory agents, a sequential or
hierarchical process per the approved topology, the Critic implemented as a
gating task — and the workflow contract and the eval triplet below are
framework-invariant.

## Operating rules

- Implement only the approved topology from `ai-architecture.md`. Do not invent
  roles, task edges, a manager agent, delegation, or agent-to-agent authority
  beyond the design.
- No multi-agent workflow without max steps, per-agent step bounds, a
  termination authority, tool authorization, and an eval plan. Any missing →
  pause and raise an ADR candidate; do not guess.
- Termination is code-enforced, not prompt-requested. The critic/verifier role's
  gate is implemented as a checked condition on the crew (a gating task callback
  / guardrail evaluating the Critic's verdict), not an instruction in a role
  backstory.
- The role-to-agent mapping is explicit and 1:1 with the approved topology. A
  role is not silently merged into another agent or split across agents.
- The process model (sequential vs hierarchical) matches the approved topology
  exactly. A hierarchical manager is used only when the architecture grants one;
  it is never added for convenience.
- Only approved tools are registered, and only on the agents the topology
  permits to use them. The tool set is a closed set from the architecture's tool
  surface; agent `allow_delegation` is off unless the topology grants it.
- Max-step, per-agent step, and wall-clock budgets are enforced in code on the
  crew/orchestrator, independent of any model's cooperation.
- Loop and stall safety is explicit: repeated identical task outputs, two agents
  ping-ponging, and no-progress rounds are detected and terminate into the
  degradation path.
- Memory and session policy is implemented exactly as specified — retention,
  scoping, redaction. No implicit unbounded crew memory or shared scratchpad.
- Every step (task execution, tool call, role transition, termination decision)
  is traced with a correlation id and the deciding role.
- The eval triplet is wired, not described: grounding score, citation
  correctness, and answer correctness are computed against the fixed eval set
  and gated at the architecture's thresholds.
- Provider-neutral: the model/provider is an `ai-architecture.md` input injected
  at deploy time; no provider SDK specifics are hardcoded here (those belong to
  the provider skills).

## Output contract

The implementation MUST conform to:

- [api-standards](../../../../../standards/api-standards/README.md) — when the workflow is exposed as an external contract surface, request/response and versioning policy apply.
- [security-standards](../../../../../standards/security-standards/README.md) — tool authorization per agent, prompt-injection posture across agent/task messages, memory redaction, credentials injected at deploy time.
- [observability-standards](../../../../../standards/observability-standards/README.md) — per-step tracing, multi-agent metrics (steps, per-role actions, tool calls, termination cause), structured logs with correlation id.
- [deployment-standards](../../../../../standards/deployment-standards/README.md) — model, prompt, topology, and tool configuration injected at deploy time, never hardcoded.
- [naming-conventions](../../../../../standards/naming-conventions/README.md) — agent, role, task, tool, and metric names follow project rules.

Upstream contract: `ai-architecture.md` is the source of truth for the
multi-agent topology, process model, tool surface, memory/session policy, stop
conditions, degradation behavior, and eval plan; `architecture/security` for
tool authorization and injection posture; `architecture/operations` for
runbook handoff. If any is silent, this skill pauses and raises an ADR
candidate rather than inventing the decision.

## Progressive references

- Read `references/crewai-agent-workflow-playbook.md` when implementing any owned area or checking the anti-pattern list.
- Read `references/crewai-agent-workflow-quality-rubric.md` before declaring the workflow complete.
- Use `assets/crewai-agent-workflow.template.md` as the topology, termination, tracing, and eval-wiring reference.

## Process

1. Load `ai-architecture.md` and identify the approved roles, the process model
   (sequential / hierarchical), the termination authority, the tool surface,
   memory policy, stop conditions, degradation behavior, and the eval plan.
2. Verify max steps, per-agent step bounds, termination authority, tool
   authorization, and eval thresholds are all present; if any is missing, raise
   an ADR candidate before writing code.
3. Map each approved role to exactly one CrewAI agent (role/goal/backstory);
   record the mapping.
4. Implement the crew with the approved process model and the task graph
   matching the approved control flow.
5. Implement the termination gate as a code-checked task guardrail/callback
   owned by the critic/verifier role; wire the degradation path for max-step
   exhaustion.
6. Register only approved tools, on only the permitted agents, with per-tool
   authorization and input validation; keep delegation off unless granted.
7. Implement memory/session handling exactly as specified (retention, scoping,
   redaction).
8. Enforce max-step, per-agent step, wall-clock, and loop/stall detection in
   crew/orchestrator code.
9. Add tracing for every task execution, tool call, role transition, and the
   termination decision with a correlation id.
10. Wire the eval triplet (grounding, citation correctness, answer correctness)
    against the fixed eval set and gate at the architecture's thresholds.
11. Add tests for successful completion, critic-rejected-then-revised, tool
    failure, unsafe-action denial, loop/step exhaustion → degradation, and an
    eval-gate failure.
12. Document unresolved architecture gaps as ADR candidates instead of silently
    filling them in.

## Outputs

- CrewAI crew realizing the approved topology and process model.
- Explicit role-to-agent mapping.
- Code-enforced termination gate owned by the critic/verifier role, plus the
  degradation path.
- Tool registry wired to approved tools on permitted agents only.
- Memory/session adapter when required.
- Max-step / step / wall-clock / loop-stall enforcement in crew code.
- Tracing instrumentation for task executions, tool calls, transitions,
  termination.
- Eval-triplet harness wired to the fixed eval set with gating thresholds.
- Tests for success, critic-gated revision, tool failure, unsafe-action denial,
  step exhaustion → degradation, and eval-gate failure.

Output rules:

- The termination authority and budgets are enforced in code, never left to a
  role backstory or task description.
- The role-to-agent mapping is explicit and matches the approved topology 1:1.
- The process model matches the approved topology; no unapproved manager.
- Only approved tools are registered, only on permitted agents.
- The eval triplet is computed and gated, not merely described.
- No provider SDK specifics or credentials are hardcoded.

## Quality checks

- [ ] The workflow maps 1:1 to an approved multi-agent topology in `ai-architecture.md`.
- [ ] The process model (sequential/hierarchical) matches the approved topology; no unapproved manager.
- [ ] Max steps, per-agent step bounds, and the termination authority are enforced in code.
- [ ] The critic/verifier termination gate is a checked condition, not a backstory/task instruction.
- [ ] Only approved tools are registered, only on permitted agents, with per-tool authorization; delegation off unless granted.
- [ ] Loop/stall detection terminates into the degradation path.
- [ ] Memory/session policy (retention, scoping, redaction) is implemented as specified.
- [ ] Traces include every task execution, tool call, role transition, termination cause, and correlation id.
- [ ] The eval triplet (grounding, citation correctness, answer correctness) is wired to the fixed eval set and gated at thresholds.
- [ ] Tests cover success, critic-gated revision, tool failure, unsafe-action denial, step exhaustion → degradation, and eval-gate failure.
- [ ] Any missing topology, process, tool, authorization, budget, degradation, or eval decision is documented as an ADR candidate.

## References

- Upstream: [`architecture/ai-native-engineering`](../../../../architecture/ai-native-engineering/SKILL.md) — multi-agent topology, process model, control flow, tool surface, stop conditions, eval plan.
- Related architecture: [`architecture/security`](../../../../architecture/security/SKILL.md) (tool authorization, injection posture), [`architecture/operations`](../../../../architecture/operations/SKILL.md) (loop-safety, runbook handoff for agent incidents).
- Cross-framework siblings: [`autogen-multi-agent-workflow`](../../autogen/autogen-multi-agent-workflow/SKILL.md) (same archetype, AutoGen mechanics), [`langchain-agent-runtime`](../../langchain/langchain-agent-runtime/SKILL.md) (single-agent baseline this builds beyond). Sibling crewai skills are listed in the [crewai stack README](../README.md).
- Related implementation skills: [`crewai-task-and-tool-design`](../crewai-task-and-tool-design/SKILL.md) (task/tool surface this workflow consumes), [`anthropic-evals-and-observability`](../../anthropic/anthropic-evals-and-observability/SKILL.md) (regression gates for the eval triplet).
- Standards: [`api-standards`](../../../../../standards/api-standards/README.md), [`security-standards`](../../../../../standards/security-standards/README.md), [`observability-standards`](../../../../../standards/observability-standards/README.md), [`deployment-standards`](../../../../../standards/deployment-standards/README.md), [`naming-conventions`](../../../../../standards/naming-conventions/README.md).
