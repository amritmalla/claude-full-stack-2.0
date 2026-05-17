# crewai

> Status: scaffold (deferred — awaiting a reference agent workflow).

## Purpose

Implements approved AI architecture using the CrewAI framework: role-based agent crews, task decomposition, tool design, and operational control of agent execution.

Architecture decisions (whether a crew topology is warranted, the tool surface, task boundaries, stop conditions, eval bar) come from [`architecture/ai-native-engineering`](../../../architecture/ai-native-engineering/SKILL.md) and are taken as inputs here.

## Strategy

Per [`implementations/ai/README.md`](../README.md), CrewAI skills are **deferred until a concrete agent workflow exists** — without a reference use case the skills risk becoming generic framework advice. Direct provider skills (`openai`, `anthropic`) and the single-agent baseline (`langchain-agent-runtime`) are authored first to preserve a clear baseline.

## Ecosystem (target)

- CrewAI (crews, agents, tasks, processes), Python
- Role/goal/backstory agent definitions, sequential and hierarchical processes
- Tool registration and execution adapters
- OpenTelemetry tracing for crew execution; token/cost telemetry
- Eval harness aligned with `evals-and-observability`

## Skills

### Authored

_None._

### Archetype coverage

| Archetype | Skill | Status |
|---|---|---|
| agent-runtime | `crewai-agent-workflow` | deferred |
| tool-calling-runtime | `crewai-task-and-tool-design` | deferred |

### Planned skill scope (future work)

- **`crewai-agent-workflow`** *(`agent-runtime`)* — approved crew topology, role/task definitions, process selection (sequential/hierarchical), termination and max-step enforcement, loop-safety tests, tracing. Deferred until a concrete agent workflow example exists.
- **`crewai-task-and-tool-design`** *(`tool-calling-runtime`)* — task decomposition, tool registry, execution adapter, authorization, idempotency, audit logging, failure tests. Deferred to avoid generic framework advice without a reference use case.

## Architecture domains implemented

| Architecture domain | How |
|---|---|
| [ai-native-engineering](../../../architecture/ai-native-engineering/SKILL.md) | Crew topology, task decomposition, eval wiring. |
| [security](../../../architecture/security/SKILL.md) | Tool authorization, prompt-injection posture. |
| [operations](../../../architecture/operations/SKILL.md) | Loop-safety, runbook inputs for agent failures. |

## Standards this implementation conforms to

- [security-standards](../../../../standards/security-standards/README.md)
- [observability-standards](../../../../standards/observability-standards/README.md)
- [deployment-standards](../../../../standards/deployment-standards/README.md)
- [naming-conventions](../../../../standards/naming-conventions/README.md)

## Upstream inputs

- Approved `ai-architecture.md` declaring crew topology, tool surface, task boundaries, stop conditions, and eval plan.
- A concrete reference agent workflow (the gate for un-deferring these skills).
