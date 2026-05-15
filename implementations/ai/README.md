# implementations/ai

Technology-specific execution skills for AI systems.

## Philosophy

AI implementation skills consume the architecture produced by
[`architecture/ai-native-engineering`](../../architecture/ai-native-engineering/SKILL.md).
They implement, harden, test, and observe an approved AI design in a specific
provider or framework.

They do not decide whether a feature should use AI, what the model contract is,
what tools are allowed, what retrieval topology is acceptable, or what evaluation
bar is sufficient. Those decisions belong upstream in `ai-architecture.md`.

If `ai-architecture.md` is silent on a material decision such as output schema,
tool side effects, retrieval grounding rules, prompt-injection posture, latency
budget, or regression gate, the implementation skill pauses and raises an ADR
candidate against the AI architecture instead of guessing.

## Archetypes

AI implementation skills are organized around repeatable runtime jobs, not broad
vendor buckets.

| Archetype | What the skill produces | Primary upstream |
|---|---|---|
| `model-runtime` | Provider SDK wiring, prompt layout, streaming, retry policy, fallback behavior, and basic telemetry. | `ai-native-engineering` |
| `structured-output-runtime` | Schema-bound outputs, validation, repair/failure handling, typed adapters, and malformed-output tests. | `ai-native-engineering` + `quality-engineering` |
| `tool-calling-runtime` | Tool schemas, execution adapter, authorization checks, idempotency, audit logging, and tool failure tests. | `ai-native-engineering` + `security` |
| `rag-runtime` | Retrieval adapter, context packing, grounding prompt, citation/source handling, hallucination checks, and retrieval evals. | `ai-native-engineering` + `data-architecture` |
| `agent-runtime` | Agent control flow, tool registry, memory/session policy, stop conditions, max-step enforcement, and loop-safety tests. | `ai-native-engineering` + `operations` |
| `evals-and-observability` | Eval dataset structure, prompt/model versioning, regression gates, token/cost metrics, traces, and dashboard/runbook notes. | `ai-native-engineering` + `quality-engineering` + `operations` |
| `safety-and-guardrails-review` | Prompt-injection review, PII handling, output validation, refusal behavior, redaction, and security handoff notes. | `ai-native-engineering` + `security` |

## Initial skill plan

The first AI implementation slice should focus on production primitives that
show up across many AI-backed products.

### v0.1: authored first

| Ecosystem | Skill | Archetype | Status |
|---|---|---|---|
| [openai](openai/) | [`openai-structured-output-runtime`](openai/openai-structured-output-runtime/SKILL.md) | `structured-output-runtime` | registered |
| [openai](openai/) | [`openai-tool-calling-runtime`](openai/openai-tool-calling-runtime/SKILL.md) | `tool-calling-runtime` | registered |
| [openai](openai/) | [`openai-rag-runtime`](openai/openai-rag-runtime/SKILL.md) | `rag-runtime` | registered |
| [openai](openai/) | [`openai-evals-and-observability`](openai/openai-evals-and-observability/SKILL.md) | `evals-and-observability` | registered |
| [langchain](langchain/) | [`langchain-agent-runtime`](langchain/langchain-agent-runtime/SKILL.md) | `agent-runtime` | registered |
| [anthropic](anthropic/) | [`anthropic-structured-output-runtime`](anthropic/anthropic-structured-output-runtime/SKILL.md) | `structured-output-runtime` | registered |

### v0.2: likely next

| Ecosystem | Proposed skill | Archetype |
|---|---|---|
| anthropic | `anthropic-tool-use-runtime` | `tool-calling-runtime` |
| anthropic | `anthropic-rag-runtime` | `rag-runtime` |
| anthropic | `anthropic-evals-and-observability` | `evals-and-observability` |
| anthropic | `anthropic-prompt-caching-and-context-runtime` | `model-runtime` |
| langchain | `langchain-rag-pipeline` | `rag-runtime` |
| langchain | `langchain-eval-harness` | `evals-and-observability` |

The `anthropic` stack mirrors `openai`'s archetype boundaries; see the
[anthropic stack README](anthropic/README.md) for per-skill scope and where
Anthropic-specific features (prompt caching, extended thinking, Citations API,
Message Batches, MCP connector tools) are folded in.

### Deferred until a reference workflow exists

| Ecosystem | Proposed skill | Reason deferred |
|---|---|---|
| crewai | `crewai-agent-workflow` | Needs a concrete agent workflow example before authoring. |
| crewai | `crewai-task-and-tool-design` | Risk of becoming generic framework advice without a reference use case. |
| autogen | `autogen-multi-agent-workflow` | Needs a multi-agent workflow with measurable eval criteria. |
| autogen | `autogen-tool-orchestration` | Depends on an approved tool surface and operational control model. |

## Decided design constraints

- AI implementation skills require `ai-architecture.md` unless they are being
  used only to review an existing implementation.
- Skills are job-specific. Do not create a broad `openai` or `langchain` skill
  that mixes chat, RAG, agents, evals, and safety into one recipe.
- Provider skills own SDK mechanics and provider-specific behavior. Framework
  skills own orchestration patterns such as chains, graphs, memory, and agent
  control flow.
- Direct provider skills should be authored before framework abstractions when
  both are plausible, so the repository preserves a clear baseline.
- Every shipping AI capability needs an eval story. If no eval gate exists, the
  implementation skill must emit the gap and route to `evals-and-observability`.

## Status and promotion criteria

The v0.1 skills are **registered**: the `SKILL.md` files are written,
upstream-correct, at canonical template parity, and registered in
`.claude-plugin/marketplace.json`, so they are invocable as plugin skills.

A skill is eligible for promotion (registration for invocation) once it reaches
parity with the canonical implementation template (e.g.
`spring-kafka-event-integration`, `spring-boot-performance-and-resilience`).
The v0.1 set met this bar and was registered together.

## Template parity (closed)

The five authored skills now match the canonical template. The gaps tracked
during v0.1 are closed:

1. **`## Output contract` — closed.** Every skill enumerates the standards its
   output MUST conform to (api, security, observability, deployment, naming;
   architecture-schema where tiering applies) plus an explicit upstream-contract
   statement that pauses for an ADR candidate when the architecture is silent.
2. **`## Operating rules` — closed.** Non-negotiables are consolidated in a
   first-class section in every skill, no longer scattered into `## Process`.
3. **`## References` — closed.** Each skill links its upstream domain, related
   architecture domains, sibling AI implementation skills, and compatible
   patterns, matching the canonical template.

The AI layer is now at the same rigor tier as the backend and infrastructure
layers. The only remaining step before these skills become invocable is
marketplace registration.

## Standards this implementation category conforms to

- [security-standards](../../standards/security-standards/README.md)
- [observability-standards](../../standards/observability-standards/README.md)
- [deployment-standards](../../standards/deployment-standards/README.md)
- [naming-conventions](../../standards/naming-conventions/README.md)
