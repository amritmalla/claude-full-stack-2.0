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

### Provider focus: Anthropic-centric

This is a Claude/Anthropic-first repository. The `anthropic` stack is the
primary, deepest stack; `openai` is a frozen lean baseline kept for
cross-provider reference and swappability, not active expansion.

### Registered skills

| Ecosystem | Skill | Archetype | Tier | Status |
|---|---|---|---|---|
| [anthropic](anthropic/) | [`anthropic-structured-output-runtime`](anthropic/anthropic-structured-output-runtime/SKILL.md) | `structured-output-runtime` | mature | registered |
| [anthropic](anthropic/) | [`anthropic-tool-use-runtime`](anthropic/anthropic-tool-use-runtime/SKILL.md) | `tool-calling-runtime` | mature | registered |
| [anthropic](anthropic/) | [`anthropic-rag-runtime`](anthropic/anthropic-rag-runtime/SKILL.md) | `rag-runtime` | mature | registered |
| [anthropic](anthropic/) | [`anthropic-evals-and-observability`](anthropic/anthropic-evals-and-observability/SKILL.md) | `evals-and-observability` | mature | registered |
| [anthropic](anthropic/) | [`anthropic-prompt-caching-and-context-runtime`](anthropic/anthropic-prompt-caching-and-context-runtime/SKILL.md) | `model-runtime` | mature | registered |
| [openai](openai/) | [`openai-structured-output-runtime`](openai/openai-structured-output-runtime/SKILL.md) | `structured-output-runtime` | lean | registered (frozen baseline) |
| [openai](openai/) | [`openai-tool-calling-runtime`](openai/openai-tool-calling-runtime/SKILL.md) | `tool-calling-runtime` | lean | registered (frozen baseline) |
| [openai](openai/) | [`openai-rag-runtime`](openai/openai-rag-runtime/SKILL.md) | `rag-runtime` | lean | registered (frozen baseline) |
| [openai](openai/) | [`openai-evals-and-observability`](openai/openai-evals-and-observability/SKILL.md) | `evals-and-observability` | lean | registered (frozen baseline) |
| [langchain](langchain/) | [`langchain-agent-runtime`](langchain/langchain-agent-runtime/SKILL.md) | `agent-runtime` | lean | registered |
| [autogen](autogen/) | [`autogen-multi-agent-workflow`](autogen/autogen-multi-agent-workflow/SKILL.md) | `agent-runtime` | mature | registered |
| [autogen](autogen/) | [`autogen-tool-orchestration`](autogen/autogen-tool-orchestration/SKILL.md) | `tool-calling-runtime` | mature | registered |
| [crewai](crewai/) | [`crewai-agent-workflow`](crewai/crewai-agent-workflow/SKILL.md) | `agent-runtime` | mature | registered |
| [crewai](crewai/) | [`crewai-task-and-tool-design`](crewai/crewai-task-and-tool-design/SKILL.md) | `tool-calling-runtime` | mature | registered |

The `anthropic` stack is **complete**: all five archetypes authored at mature
tier. It mirrors `openai`'s archetype boundaries so skills stay swappable; only
artifact depth differs. See the [anthropic stack README](anthropic/README.md)
for per-skill scope and where Anthropic-specific features (prompt caching,
extended thinking, Citations API, Message Batches, MCP connector tools) live.

The `autogen` and `crewai` framework stacks are **complete** at mature tier and
both grounded in one shared **Research-and-synthesize** reference workflow
(Researcher / Critic-verifier / Writer; eval triplet: grounding score, citation
correctness, answer correctness on a fixed eval set). They mirror each other's
archetype boundaries so cross-framework skills stay swappable, and diverge
intentionally from the lean single-file `langchain-agent-runtime` precedent.
`autogen-multi-agent-workflow` is the pinned mature exemplar for the framework
stacks.

### Roadmap

| Ecosystem | Proposed skill | Archetype |
|---|---|---|
| langchain | `langchain-rag-pipeline` | `rag-runtime` |
| langchain | `langchain-eval-harness` | `evals-and-observability` |

The `openai` stack is intentionally not on the roadmap — it is a frozen
baseline, not a growth area.

### Deferred until a reference workflow exists

Nothing is currently deferred. The autogen and crewai stacks — previously
deferred pending a concrete reference workflow — were un-deferred and authored
once the shared Research-and-synthesize reference (with measurable eval
criteria) satisfied the gate. New framework stacks that lack a concrete
reference workflow with measurable evals would be parked here rather than
authored as generic framework advice.

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

All ten skills above are **registered** in `.claude-plugin/marketplace.json`
and invocable: `SKILL.md` files written, upstream-correct, and at (or above)
canonical template parity.

The `anthropic` stack is authored at **mature tier** — each skill is a
four-file unit (`SKILL.md` + `references/<skill>-playbook.md` +
`references/<skill>-quality-rubric.md` + `assets/<skill>.template.md`). The
`openai` and `langchain` skills are lean single-file at canonical
implementation parity (e.g. `spring-kafka-event-integration`). The mixed tier
is intentional: Anthropic is the primary stack and gets the deeper artifacts;
`openai` is a frozen baseline and stays lean.

## Template parity

Every skill satisfies the canonical template:

1. **`## Output contract`.** Every skill enumerates the standards its output
   MUST conform to (api, security, observability, deployment, naming;
   architecture-schema where tiering applies) plus an explicit upstream-contract
   statement that pauses for an ADR candidate when the architecture is silent.
2. **`## Operating rules`.** Non-negotiables are consolidated in a first-class
   section in every skill, not scattered into `## Process`.
3. **`## References`.** Each skill links its upstream domain, related
   architecture domains, sibling AI implementation skills, and compatible
   patterns.

Mature-tier `anthropic` skills additionally carry a `## Progressive references`
section wiring the playbook, quality rubric, and asset template. The AI layer
is at the same rigor tier as the backend and infrastructure layers.

## Standards this implementation category conforms to

- [security-standards](../../../standards/security-standards/README.md)
- [observability-standards](../../../standards/observability-standards/README.md)
- [deployment-standards](../../../standards/deployment-standards/README.md)
- [naming-conventions](../../../standards/naming-conventions/README.md)
