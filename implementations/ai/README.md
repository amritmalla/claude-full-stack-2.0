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
| [openai](openai/) | [`openai-structured-output-runtime`](openai/openai-structured-output-runtime/SKILL.md) | `structured-output-runtime` | authored, pre-promotion |
| [openai](openai/) | [`openai-tool-calling-runtime`](openai/openai-tool-calling-runtime/SKILL.md) | `tool-calling-runtime` | authored, pre-promotion |
| [openai](openai/) | [`openai-rag-runtime`](openai/openai-rag-runtime/SKILL.md) | `rag-runtime` | authored, pre-promotion |
| [openai](openai/) | [`openai-evals-and-observability`](openai/openai-evals-and-observability/SKILL.md) | `evals-and-observability` | authored, pre-promotion |
| [langchain](langchain/) | [`langchain-agent-runtime`](langchain/langchain-agent-runtime/SKILL.md) | `agent-runtime` | authored, pre-promotion |

### v0.2: likely next

| Ecosystem | Proposed skill | Archetype |
|---|---|---|
| anthropic | `anthropic-structured-output-runtime` | `structured-output-runtime` |
| anthropic | `anthropic-tool-use-runtime` | `tool-calling-runtime` |
| anthropic | `anthropic-rag-runtime` | `rag-runtime` |
| langchain | `langchain-rag-pipeline` | `rag-runtime` |
| langchain | `langchain-eval-harness` | `evals-and-observability` |

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

The v0.1 skills are **authored, pre-promotion**: the `SKILL.md` files are written
and upstream-correct, but they are deliberately not registered in
`.claude-plugin/marketplace.json`, so they are not yet invocable as plugin skills.

A skill is promoted (registered for invocation) when it reaches parity with the
canonical implementation template (e.g. `spring-kafka-event-integration`,
`spring-boot-performance-and-resilience`). The known parity gaps below are the
promotion checklist.

## Known follow-up (v0.2 hardening)

The five authored skills sit at a lower rigor tier than the canonical template.
These gaps are tracked, not accidental, and must close before promotion:

1. **No `## Output contract` section.** Canonical skills enumerate the standards
   the output MUST conform to (security, observability, deployment, naming) plus
   an explicit upstream-contract statement. The AI skills currently only carry a
   minimal `## References` line. This is the highest-priority gap.
2. **No `## Operating rules` section.** Canonical skills consolidate
   non-negotiables in a dedicated section; the AI skills scatter them into
   `## Process` steps ("Refuse to implement…"). Extract into a first-class
   section.
3. **Thin `## References`.** Add sibling-skill links (e.g. `openai-rag-runtime`
   ↔ `openai-structured-output-runtime`, all → `openai-evals-and-observability`)
   and compatible patterns, matching the canonical template.

Until these close, the AI layer is intentionally one tier below the backend and
infrastructure layers.

## Standards this implementation category conforms to

- [security-standards](../../standards/security-standards/README.md)
- [observability-standards](../../standards/observability-standards/README.md)
- [deployment-standards](../../standards/deployment-standards/README.md)
- [naming-conventions](../../standards/naming-conventions/README.md)
