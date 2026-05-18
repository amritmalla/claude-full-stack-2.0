# crewai

> Status: complete — 2 skills authored at mature tier; registered.

## Purpose

Implements approved AI architecture using the CrewAI framework: role-based agent crews, task decomposition, tool design, and operational control of agent execution.

Architecture decisions (whether a crew topology is warranted, the tool surface, task boundaries, stop conditions, eval bar) come from [`architecture/ai-native-engineering`](../../../architecture/ai-native-engineering/SKILL.md) and are taken as inputs here.

## Strategy

The un-deferral gate — a concrete agent workflow with a reference use case — is **satisfied**. Both skills are grounded in the shared **Research-and-synthesize** reference (Researcher / Critic-verifier / Writer; eval triplet: grounding score, citation correctness, answer correctness on a fixed eval set), so they teach a concrete realization rather than generic framework advice. The skills are authored at **mature tier** (`SKILL.md` + playbook + quality-rubric + asset template), intentionally diverging from the lean single-file `langchain-agent-runtime` framework precedent; the divergence is deliberate, not drift. The AutoGen stack mirrors the same reference and archetype boundaries so cross-framework skills stay swappable.

## Ecosystem (target)

- CrewAI (crews, agents, tasks, processes), Python
- Role/goal/backstory agent definitions, sequential and hierarchical processes
- Tool registration and execution adapters
- OpenTelemetry tracing for crew execution; token/cost telemetry
- Eval harness aligned with `evals-and-observability`

## Skills

### Authored

Both skills are authored at **mature tier** (`SKILL.md` + `references/<skill>-playbook.md` + `references/<skill>-quality-rubric.md` + `assets/<skill>.template.md`) and registered.

- [`crewai-agent-workflow`](crewai-agent-workflow/SKILL.md) — Research-and-synthesize as a CrewAI crew: role/goal/backstory agents over a sequential or hierarchical process per the approved topology, critic-gated termination, max-step budgets in code, loop-safety tests, tracing, and the gated eval triplet.
- [`crewai-task-and-tool-design`](crewai-task-and-tool-design/SKILL.md) — CrewAI task decomposition plus the closed tool registry and authorization-enforcing execution adapter for the Researcher's tools: tool schemas, idempotency, audit logging, and tool/task-failure tests.

### Archetype coverage

| Archetype | Skill | Status |
|---|---|---|
| agent-runtime | [`crewai-agent-workflow`](crewai-agent-workflow/SKILL.md) | authored (mature), registered |
| tool-calling-runtime | [`crewai-task-and-tool-design`](crewai-task-and-tool-design/SKILL.md) | authored (mature), registered |

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
- The un-deferral gate (a concrete reference agent workflow) is satisfied by the shared Research-and-synthesize reference.
