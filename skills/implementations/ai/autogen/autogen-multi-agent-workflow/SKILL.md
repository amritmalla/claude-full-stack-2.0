---
name: autogen-multi-agent-workflow
description: Use when an approved ai-architecture.md defines a multi-agent workflow and AutoGen is the chosen framework. Produces the group-chat/team topology, role-to-agent mapping, critic-gated termination, budgets, and eval wiring. Not for single-agent runtimes, tool-surface design, or provider SDK work.
---

# AutoGen Multi-Agent Workflow

## When to use

Invoke when `ai-architecture.md` approves a multi-agent topology and AutoGen
(AgentChat / Core) is the chosen orchestration framework.

Do not use when the architecture approves only a single agent (use the
single-agent baseline), when the workflow needs no multi-agent control flow, or
to design the tool surface itself (that is an upstream architecture decision and
a `tool-calling-runtime` implementation concern).

## Inputs

Required:

- Approved `ai-architecture.md`.
- The approved multi-agent topology: roles, who speaks/acts when, and the
  termination authority.
- Tool surface and per-tool authorization model.
- Stop conditions, max-turn budget, and degradation behavior.
- Eval plan: the fixed evaluation set and the pass thresholds.
- Target application language and framework; provider/model contract.

Optional:

- Existing tool implementations and retrieval surface.
- Memory or session storage policy.
- OpenTelemetry / tracing target.
- Sample successful and failed multi-agent transcripts.

## Reference workflow

This skill is grounded in a concrete reference so it does not degrade into
generic framework advice: **Research-and-synthesize**. Three roles —
**Researcher** (retrieves source material for a question from the
architecture-defined retrieval surface), **Critic/verifier** (checks the draft's
claims against retrieved sources, flags ungrounded or mis-cited statements,
gates completion), **Writer** (produces the final answer with inline citations).
Input: a question. Output: a cited synthesized answer. The Critic holds
termination authority; the workflow is not done until grounding passes or the
max-turn budget is hit, after which the architecture's degradation path runs.
The realization is AutoGen-specific; the workflow contract and the eval triplet
below are framework-invariant.

## Operating rules

- Implement only the approved topology from `ai-architecture.md`. Do not invent
  roles, delegation edges, autonomy, or agent-to-agent authority beyond the
  design.
- No multi-agent workflow without max turns, per-agent step bounds, a
  termination authority, tool authorization, and an eval plan. Any missing →
  pause and raise an ADR candidate; do not guess.
- Termination is code-enforced, not prompt-requested. The critic/verifier role's
  gate is implemented as a checked condition on the group chat / team, not an
  instruction in a system message.
- The role-to-agent mapping is explicit and 1:1 with the approved topology. A
  role is not silently merged into another agent or split across agents.
- Only approved tools are registered, and only on the agents the topology
  permits to use them. The tool set is a closed set from the architecture's tool
  surface.
- Max-turn, per-agent step, and wall-clock budgets are enforced in code on the
  orchestrator (group chat / team), independent of any model's cooperation.
- Loop and stall safety is explicit: repeated identical turns, two agents
  ping-ponging, and no-progress rounds are detected and terminate into the
  degradation path.
- Memory and session policy is implemented exactly as specified — retention,
  scoping, redaction. No implicit unbounded shared scratchpad.
- Every turn (agent message, tool call, role transition, termination decision)
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
- [security-standards](../../../../../standards/security-standards/README.md) — tool authorization per agent, prompt-injection posture across agent messages, memory redaction, credentials injected at deploy time.
- [observability-standards](../../../../../standards/observability-standards/README.md) — per-turn tracing, multi-agent metrics (turns, per-role actions, tool calls, termination cause), structured logs with correlation id.
- [deployment-standards](../../../../../standards/deployment-standards/README.md) — model, prompt, topology, and tool configuration injected at deploy time, never hardcoded.
- [naming-conventions](../../../../../standards/naming-conventions/README.md) — agent, role, tool, and metric names follow project rules.

Upstream contract: `ai-architecture.md` is the source of truth for the
multi-agent topology, tool surface, memory/session policy, stop conditions,
degradation behavior, and eval plan; `architecture/security` for tool
authorization and injection posture; `architecture/operations` for runbook
handoff. If any is silent, this skill pauses and raises an ADR candidate rather
than inventing the decision.

## Progressive references

- Read `references/autogen-multi-agent-workflow-playbook.md` when implementing any owned area or checking the anti-pattern list.
- Read `references/autogen-multi-agent-workflow-quality-rubric.md` before declaring the workflow complete.
- Use `assets/autogen-multi-agent-workflow.template.md` as the topology, termination, tracing, and eval-wiring reference.

## Process

1. Load `ai-architecture.md` and identify the approved roles, the topology
   (group chat / team), the termination authority, the tool surface, memory
   policy, stop conditions, degradation behavior, and the eval plan.
2. Verify max turns, per-agent step bounds, termination authority, tool
   authorization, and eval thresholds are all present; if any is missing, raise
   an ADR candidate before writing code.
3. Map each approved role to exactly one AutoGen agent; record the mapping.
4. Implement the group chat / team with explicit speaker-selection or team
   topology matching the approved control flow.
5. Implement the termination gate as a code-checked condition owned by the
   critic/verifier role; wire the degradation path for max-turn exhaustion.
6. Register only approved tools, on only the permitted agents, with per-tool
   authorization and input validation.
7. Implement memory/session handling exactly as specified (retention, scoping,
   redaction).
8. Enforce max-turn, per-agent step, wall-clock, and loop/stall detection in
   orchestrator code.
9. Add tracing for every turn, tool call, role transition, and the termination
   decision with a correlation id.
10. Wire the eval triplet (grounding, citation correctness, answer correctness)
    against the fixed eval set and gate at the architecture's thresholds.
11. Add tests for successful completion, critic-rejected-then-revised, tool
    failure, unsafe-action denial, loop/turn exhaustion → degradation, and an
    eval-gate failure.
12. Document unresolved architecture gaps as ADR candidates instead of silently
    filling them in.

## Outputs

- AutoGen group chat / team realizing the approved topology.
- Explicit role-to-agent mapping.
- Code-enforced termination gate owned by the critic/verifier role, plus the
  degradation path.
- Tool registry wired to approved tools on permitted agents only.
- Memory/session adapter when required.
- Max-turn / step / wall-clock / loop-stall enforcement in orchestrator code.
- Tracing instrumentation for turns, tool calls, transitions, termination.
- Eval-triplet harness wired to the fixed eval set with gating thresholds.
- Tests for success, critic-gated revision, tool failure, unsafe-action denial,
  turn exhaustion → degradation, and eval-gate failure.

Output rules:

- The termination authority and budgets are enforced in code, never left to a
  prompt instruction.
- The role-to-agent mapping is explicit and matches the approved topology 1:1.
- Only approved tools are registered, only on permitted agents.
- The eval triplet is computed and gated, not merely described.
- No provider SDK specifics or credentials are hardcoded.

## Quality checks

- [ ] The workflow maps 1:1 to an approved multi-agent topology in `ai-architecture.md`.
- [ ] Max turns, per-agent step bounds, and the termination authority are enforced in code.
- [ ] The critic/verifier termination gate is a checked condition, not a prompt instruction.
- [ ] Only approved tools are registered, only on permitted agents, with per-tool authorization.
- [ ] Loop/stall detection terminates into the degradation path.
- [ ] Memory/session policy (retention, scoping, redaction) is implemented as specified.
- [ ] Traces include every turn, tool call, role transition, termination cause, and correlation id.
- [ ] The eval triplet (grounding, citation correctness, answer correctness) is wired to the fixed eval set and gated at thresholds.
- [ ] Tests cover success, critic-gated revision, tool failure, unsafe-action denial, turn exhaustion → degradation, and eval-gate failure.
- [ ] Any missing topology, tool, authorization, budget, degradation, or eval decision is documented as an ADR candidate.

## References

- Upstream: [`architecture/ai-native-engineering`](../../../../architecture/ai-native-engineering/SKILL.md) — multi-agent topology, control flow, tool surface, stop conditions, eval plan.
- Related architecture: [`architecture/security`](../../../../architecture/security/SKILL.md) (tool authorization, injection posture), [`architecture/operations`](../../../../architecture/operations/SKILL.md) (loop-safety, runbook handoff for agent incidents).
- Cross-framework siblings: [`langchain-agent-runtime`](../../langchain/langchain-agent-runtime/SKILL.md) (single-agent baseline this builds beyond), [`crewai-agent-workflow`](../../crewai/crewai-agent-workflow/SKILL.md) (same archetype, CrewAI mechanics). Sibling autogen skills are listed in the [autogen stack README](../README.md).
- Related implementation skills: [`autogen-tool-orchestration`](../autogen-tool-orchestration/SKILL.md) (tool registration/execution this workflow consumes), [`anthropic-evals-and-observability`](../../anthropic/anthropic-evals-and-observability/SKILL.md) (regression gates for the eval triplet).
- Standards: [`api-standards`](../../../../../standards/api-standards/README.md), [`security-standards`](../../../../../standards/security-standards/README.md), [`observability-standards`](../../../../../standards/observability-standards/README.md), [`deployment-standards`](../../../../../standards/deployment-standards/README.md), [`naming-conventions`](../../../../../standards/naming-conventions/README.md).
