---
name: langchain-agent-runtime
description: Use when implementing a LangChain-based agent runtime from an approved ai-architecture.md agent control-flow design. Produces graph or chain structure, tool registry, memory and session handling, stop conditions, max-step enforcement, failure recovery, tracing, and tests for tool loops, unsafe actions, and fallback behavior. Do not use for deciding whether an agent is needed, designing the tool surface, generic RAG, or direct provider SDK integration.
---

# LangChain Agent Runtime

## When to use

Invoke when `ai-architecture.md` approves an agentic capability and LangChain is
the chosen orchestration framework.

Do not use when the system only needs a single prompt call, structured
extraction, or plain RAG without multi-step control flow.

## Inputs

Required:

- Approved `ai-architecture.md`.
- Agent control flow, tool surface, stop conditions, and human checkpoints.
- Target application language and framework.
- Provider configuration and model contract.

Optional:

- Existing tool implementations.
- Memory or session storage.
- LangSmith, OpenTelemetry, or other tracing target.
- Eval cases for successful and unsafe agent behavior.

## Operating rules

- Implement only the approved agent control flow from `ai-architecture.md`. Do not invent planner/executor splits, delegation, or autonomy beyond the design.
- No agent without max steps, timeout, stop conditions, tool authorization, and an eval plan. Any missing → refuse and raise an ADR candidate.
- Only approved tools are registered. The tool registry is a closed set defined by the architecture's tool surface.
- Loop, step, and timeout budgets are enforced in code, not in prompts. A prompt instruction is not an enforcement mechanism.
- Human-in-the-loop checkpoints are honored exactly as specified; the agent cannot bypass a required checkpoint.
- Memory and session policy is implemented as specified — retention, scoping, and redaction included. No implicit unbounded memory.
- Every step (model call, tool call, state transition, terminal outcome) is traced with a correlation id.

## Output contract

The implementation MUST conform to:

- [api-standards](../../../../standards/api-standards/README.md) — when the agent is exposed as an external contract surface, request/response and versioning policy apply.
- [security-standards](../../../../standards/security-standards/README.md) — tool authorization, prompt-injection posture, memory redaction, and credentials injected at deploy time.
- [observability-standards](../../../../standards/observability-standards/README.md) — per-step tracing, agent metrics (steps, tool calls, terminal outcome), structured logs with correlation id.
- [deployment-standards](../../../../standards/deployment-standards/README.md) — model, prompt, and tool configuration injected at deploy time, never hardcoded.
- [naming-conventions](../../../../standards/naming-conventions/README.md) — agent, tool, and metric names follow project rules.

Upstream contract: `ai-architecture.md` is the source of truth for the agent control flow, tool surface, memory/session policy, stop conditions, and human checkpoints; `architecture/security` for tool authorization; `architecture/operations` for runbook handoff. If any is silent, this skill pauses and raises an ADR candidate rather than inventing the decision.

## Process

1. Load `ai-architecture.md` and identify the agent goal, planner/executor split, tools, memory, stop conditions, and failure behavior.
2. Refuse to implement an agent if the tool surface, max steps, stop condition, or eval plan is missing.
3. Implement the LangChain graph or chain structure with explicit state transitions.
4. Register only approved tools and enforce tool-level authorization and input validation.
5. Implement memory or session handling exactly as specified by the architecture.
6. Enforce max steps, timeout, loop detection, fallback behavior, and human-in-the-loop checkpoints.
7. Add tracing for agent steps, tool calls, model calls, and terminal outcome.
8. Add tests for successful completion, tool failure, unsafe action denial, loop/step exhaustion, and fallback.

## Outputs

- LangChain agent graph or chain.
- Tool registry wired to approved tools.
- Memory/session adapter when required.
- Stop-condition and max-step enforcement.
- Tracing instrumentation.
- Tests for success, failure, unsafe action denial, loop exhaustion, and fallback.

## Quality checks

- [ ] The agent maps to an approved agent control flow in `ai-architecture.md`.
- [ ] Only approved tools are registered.
- [ ] Max steps, timeout, and stop conditions are enforced in code.
- [ ] Tests cover tool failure, unsafe action denial, loop exhaustion, and fallback.
- [ ] Traces include model calls, tool calls, step count, terminal outcome, and correlation id.

## References

- Upstream: [`architecture/ai-native-engineering`](../../../../architecture/ai-native-engineering/SKILL.md) — agent control flow, tool surface, memory policy, stop conditions, checkpoints.
- Related architecture: [`architecture/operations`](../../../../architecture/operations/SKILL.md) (runbook handoff for agent incidents), [`architecture/security`](../../../../architecture/security/SKILL.md) (tool authorization, injection posture).
- Related implementation skills: [`openai-tool-calling-runtime`](../../openai/openai-tool-calling-runtime/SKILL.md) (provider tool mechanics the registry wraps), [`openai-rag-runtime`](../../openai/openai-rag-runtime/SKILL.md) (retrieval exposed as an agent tool), [`openai-evals-and-observability`](../../openai/openai-evals-and-observability/SKILL.md) (agent-behavior regression gates).
- Compatible patterns: [`ai-rag-platform`](../../../../patterns/ai-rag-platform/README.md) (retrieval-driven agents), [`event-driven`](../../../../patterns/event-driven/README.md) (tool side effects as domain events).
