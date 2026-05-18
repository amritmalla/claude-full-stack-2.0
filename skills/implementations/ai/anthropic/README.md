# anthropic

> Status: complete — 5 of 5 archetypes authored at mature tier; all registered.

## Purpose

Implements approved AI architecture using the Anthropic ecosystem (Claude via
the Messages API). This is the provider-specific execution layer for structured
output, tool use, RAG runtime behavior, evals and observability, and
prompt-cache/context discipline.

Architecture decisions come from
[`architecture/ai-native-engineering`](../../../architecture/ai-native-engineering/SKILL.md)
and are taken as inputs here.

## Skills

### Authored

All five skills are authored at **mature tier** (`SKILL.md` + `references/<skill>-playbook.md` + `references/<skill>-quality-rubric.md` + `assets/<skill>.template.md`) and registered.

- [`anthropic-structured-output-runtime`](anthropic-structured-output-runtime/SKILL.md) — schema-bound JSON / typed objects / extraction / classification via forced tool use, prefill, or strict prompt; validation, bounded repair, prompt-cache placement, extended-thinking handling, tests, telemetry.
- [`anthropic-tool-use-runtime`](anthropic-tool-use-runtime/SKILL.md) — tool schemas, an authorization-enforcing execution adapter, idempotency, audit logging, the bounded tool loop, parallel-tool and `tool_choice` control, tool-definition-prefix caching, and tool-failure tests.
- [`anthropic-rag-runtime`](anthropic-rag-runtime/SKILL.md) — retrieval adapter, long-context packing, grounding prompt, Citations-API source handling, hallucination/grounding gate, retrieved-context-prefix caching, and retrieval evals.
- [`anthropic-evals-and-observability`](anthropic-evals-and-observability/SKILL.md) — eval datasets, scoring harness, regression gates, prompt/model versioning, Message Batches routing for offline runs, token/cost and cache telemetry, traces, runbook notes.
- [`anthropic-prompt-caching-and-context-runtime`](anthropic-prompt-caching-and-context-runtime/SKILL.md) — `cache_control` breakpoint strategy, 5-minute-TTL warm/cold accounting, extended-thinking budget and retention, and long-context packing/truncation discipline.

### Archetype coverage

| Archetype | Skill | Status |
|---|---|---|
| `structured-output-runtime` | [`anthropic-structured-output-runtime`](anthropic-structured-output-runtime/SKILL.md) | authored (mature), registered |
| `tool-calling-runtime` | [`anthropic-tool-use-runtime`](anthropic-tool-use-runtime/SKILL.md) | authored (mature), registered |
| `rag-runtime` | [`anthropic-rag-runtime`](anthropic-rag-runtime/SKILL.md) | authored (mature), registered |
| `evals-and-observability` | [`anthropic-evals-and-observability`](anthropic-evals-and-observability/SKILL.md) | authored (mature), registered |
| `model-runtime` (context/caching) | [`anthropic-prompt-caching-and-context-runtime`](anthropic-prompt-caching-and-context-runtime/SKILL.md) | authored (mature), registered |

### Tier note

This stack is authored at **mature tier**, intentionally diverging from the lean single-file `openai` mirror. The cross-provider archetype boundaries still match `openai` so skills stay swappable; only the artifact depth differs. The divergence is deliberate, not drift.

### Self-contained design

Each skill is self-contained: it self-specifies its own `cache_control` and
extended-thinking discipline inline rather than deferring to a shared
foundation skill. `anthropic-prompt-caching-and-context-runtime` is the
specialist that owns the deep context/caching runtime job itself — it is a
peer, not a base the other skills reference. This keeps every skill swappable
against its `openai` counterpart without a hidden intra-stack dependency.

## Anthropic-specific surface

Per the layer decision, most Anthropic-specific features are folded into the
relevant mirrored skills rather than split into their own skills:

| Feature | Home |
|---|---|
| Prompt caching (`cache_control`) | Self-specified inline in every anthropic skill's Operating rules; `anthropic-prompt-caching-and-context-runtime` is the specialist for the deep caching job |
| Extended thinking | Self-specified inline in the Operating rules of each skill that uses it; `anthropic-prompt-caching-and-context-runtime` is the specialist for budget/retention |
| Citations API | `anthropic-rag-runtime` |
| Message Batches API | `anthropic-evals-and-observability` |
| MCP connector tools | `anthropic-tool-use-runtime` |

## Upstream inputs

- Approved `ai-architecture.md`.
- Model contracts, prompt/context strategy, prompt-cache strategy, tool surface, retrieval rules, eval plan, guardrails, and cost/latency budgets.
- Related handoffs from `data-architecture`, `security`, `quality-engineering`, and `operations` when relevant.

## Design constraints

- Do not use Anthropic skills to decide whether a feature should use AI.
- Do not invent output schemas, tool schemas, retrieval rules, cache strategy, or eval gates missing from `ai-architecture.md`.
- Keep provider mechanics (Messages API, tool use, caching) separate from framework orchestration; framework concerns belong to `implementations/ai/langchain`.
- Mirror the `openai` stack's archetype boundaries so cross-provider skills stay swappable.

## Standards this implementation conforms to

- [api-standards](../../../../standards/api-standards/README.md)
- [security-standards](../../../../standards/security-standards/README.md)
- [observability-standards](../../../../standards/observability-standards/README.md)
- [deployment-standards](../../../../standards/deployment-standards/README.md)
- [naming-conventions](../../../../standards/naming-conventions/README.md)
