# autogen

> Status: scaffold (deferred — awaiting a reference multi-agent workflow).

## Purpose

Implements approved AI architecture using the AutoGen framework: multi-agent orchestration, conversation/group-chat topologies, tool orchestration, and operational control of agent loops.

Architecture decisions (whether to use a multi-agent topology at all, the tool surface, stop conditions, eval bar, operational control model) come from [`architecture/ai-native-engineering`](../../../architecture/ai-native-engineering/SKILL.md) and are taken as inputs here.

## Strategy

Per [`implementations/ai/README.md`](../README.md), AutoGen skills are **deferred until a concrete multi-agent workflow with measurable eval criteria exists**. Authoring them earlier risks generic framework advice. Direct provider skills (`openai`, `anthropic`) and the single-agent baseline (`langchain-agent-runtime`) are authored first to preserve a clear baseline.

## Ecosystem (target)

- AutoGen (AgentChat / Core), Python
- Conversable agents, group chat / team topologies
- Tool/function registration and execution adapters
- OpenTelemetry tracing for agent loops; token/cost telemetry
- Eval harness aligned with `evals-and-observability`

## Skills

### Authored

_None._

### Archetype coverage

| Archetype | Skill | Status |
|---|---|---|
| agent-runtime | `autogen-multi-agent-workflow` | deferred |
| tool-calling-runtime | `autogen-tool-orchestration` | deferred |

### Planned skill scope (future work)

- **`autogen-multi-agent-workflow`** *(`agent-runtime`)* — approved multi-agent topology (group chat / teams), role definitions, termination and max-turn enforcement, loop-safety tests, tracing. Deferred until a reference workflow with measurable eval criteria exists.
- **`autogen-tool-orchestration`** *(`tool-calling-runtime`)* — tool registry, execution adapter, authorization, idempotency, audit logging, tool-failure tests. Depends on an approved tool surface and operational control model.

## Architecture domains implemented

| Architecture domain | How |
|---|---|
| [ai-native-engineering](../../../architecture/ai-native-engineering/SKILL.md) | Multi-agent topology, control flow, eval wiring. |
| [security](../../../architecture/security/SKILL.md) | Tool authorization, prompt-injection posture. |
| [operations](../../../architecture/operations/SKILL.md) | Loop-safety, runbook inputs for agent failures. |

## Standards this implementation conforms to

- [security-standards](../../../../standards/security-standards/README.md)
- [observability-standards](../../../../standards/observability-standards/README.md)
- [deployment-standards](../../../../standards/deployment-standards/README.md)
- [naming-conventions](../../../../standards/naming-conventions/README.md)

## Upstream inputs

- Approved `ai-architecture.md` declaring agent topology, tool surface, memory/session policy, stop conditions, and eval plan.
- A concrete reference multi-agent workflow with measurable eval criteria (the gate for un-deferring these skills).
