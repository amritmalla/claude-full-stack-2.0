# ai-native-engineering

> Status: draft

## Purpose

Defines AI system architecture from an approved system design: capability classification, model contracts, context and memory strategy, retrieval and grounding topology, tool and action surface, agent control flow, failure taxonomy, evaluation and guardrail plans, cost and latency budgets, model routing, and observability requirements.

Technology-agnostic. Owns *what* AI capabilities the system exposes and *how* they behave, not the SDK or framework that runs them. Vendor-specific runtime scaffolding lives under [implementations/ai](../../implementations/ai/).

## Owns

- AI capability boundaries and escalation-ladder classification
- Model contracts (inputs, outputs, success criteria, degradation)
- Context architecture, state, and memory strategy
- Retrieval topology and grounding authority (mechanics handed to data-architecture)
- Tool and action contract surface and autonomy ceilings
- Agent suitability test and control flow
- Failure taxonomy, guardrails, and trust boundaries
- Evaluation strategy and regression gates
- Cost/latency budgets, model routing, and AI observability

## Produces

| Artifact | Conforms to |
|---|---|
| `ai-architecture.md` | [architecture-schema](../../../standards/architecture-schema/README.md), [documentation-standards](../../../standards/documentation-standards/README.md) |
| ADR drafts (capability, retrieval authority, autonomy, memory, routing) | [architecture-schema](../../../standards/architecture-schema/README.md) |

## Skills

- [ai-native-engineering](SKILL.md) - turns an approved system design with an AI surface into AI system architecture: capability classification, model contracts, context/memory, retrieval, tools, agent control flow, failure taxonomy, evaluation, guardrails, budgets, routing, observability, and implementation handoffs.

## Standards this architecture domain conforms to

- [architecture-schema](../../../standards/architecture-schema/README.md) - `ai-architecture.md` artifact structure and system-design traceability.
- [security-standards](../../../standards/security-standards/README.md) - guardrails, PII handling, trust boundaries.
- [observability-standards](../../../standards/observability-standards/README.md) - AI telemetry and operational signals.
- [deployment-standards](../../../standards/deployment-standards/README.md) - rollback and promotion criteria.
- [documentation-standards](../../../standards/documentation-standards/README.md) - skill structure.

## Upstream inputs

Requires an approved `system-design.md` per [architecture-schema](../../../standards/architecture-schema/README.md) whose design includes an AI surface. Bounded contexts, component interfaces, data ownership, and ADRs shape the AI architecture produced here.

## Downstream consumers

AI architecture produced here is the source of truth for:

- [implementations/ai/*](../../implementations/ai/) - vendor runtimes (Anthropic, OpenAI, LangChain, AutoGen, CrewAI) follow model contracts, tool surfaces, and evaluation gates.
- [architecture/backend-architecture](../backend-architecture/README.md) - orchestration ownership and request-path touchpoints.
- [architecture/data-architecture](../data-architecture/README.md) - retrieval corpora ownership, ingestion, indexing, and embedding lifecycle.
- [architecture/security](../security/SKILL.md) - trust boundaries, prompt-injection posture, and audit needs.
