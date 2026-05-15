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

- Upstream: [`architecture/ai-native-engineering`](../../../../architecture/ai-native-engineering/SKILL.md).
- Related: [`architecture/operations`](../../../../architecture/operations/SKILL.md), [`architecture/security`](../../../../architecture/security/SKILL.md).
