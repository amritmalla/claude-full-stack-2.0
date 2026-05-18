# autogen

> Status: complete — 2 skills authored at mature tier; registered.

## Purpose

Implements approved AI architecture using the AutoGen framework: multi-agent orchestration, conversation/group-chat topologies, tool orchestration, and operational control of agent loops.

Architecture decisions (whether to use a multi-agent topology at all, the tool surface, stop conditions, eval bar, operational control model) come from [`architecture/ai-native-engineering`](../../../architecture/ai-native-engineering/SKILL.md) and are taken as inputs here.

## Strategy

The un-deferral gate — a concrete multi-agent workflow with measurable eval criteria — is **satisfied**. Both skills are grounded in the shared **Research-and-synthesize** reference (Researcher / Critic-verifier / Writer; eval triplet: grounding score, citation correctness, answer correctness on a fixed eval set), so they teach a concrete realization rather than generic framework advice. The skills are authored at **mature tier** (`SKILL.md` + playbook + quality-rubric + asset template), intentionally diverging from the lean single-file `langchain-agent-runtime` framework precedent; the divergence is deliberate, not drift. The CrewAI stack mirrors the same reference and archetype boundaries so cross-framework skills stay swappable.

## Ecosystem (target)

- AutoGen (AgentChat / Core), Python
- Conversable agents, group chat / team topologies
- Tool/function registration and execution adapters
- OpenTelemetry tracing for agent loops; token/cost telemetry
- Eval harness aligned with `evals-and-observability`

## Skills

### Authored

Both skills are authored at **mature tier** (`SKILL.md` + `references/<skill>-playbook.md` + `references/<skill>-quality-rubric.md` + `assets/<skill>.template.md`) and registered.

- [`autogen-multi-agent-workflow`](autogen-multi-agent-workflow/SKILL.md) — Research-and-synthesize as AutoGen group-chat/teams: role-to-agent mapping, critic-gated termination, max-turn/step budgets in code, loop-safety tests, tracing, and the gated eval triplet. The pinned exemplar for the framework stacks.
- [`autogen-tool-orchestration`](autogen-tool-orchestration/SKILL.md) — AutoGen tool/function registration and execution adapter for the Researcher's tools: tool schemas, authorization enforced in the adapter, idempotency, audit logging, and tool-failure tests.

### Archetype coverage

| Archetype | Skill | Status |
|---|---|---|
| agent-runtime | [`autogen-multi-agent-workflow`](autogen-multi-agent-workflow/SKILL.md) | authored (mature), registered |
| tool-calling-runtime | [`autogen-tool-orchestration`](autogen-tool-orchestration/SKILL.md) | authored (mature), registered |

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
- The un-deferral gate (a concrete reference multi-agent workflow with measurable eval criteria) is satisfied by the shared Research-and-synthesize reference.
