# anthropic

> Status: in progress — 1 of 5 archetypes authored.

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

- [`anthropic-structured-output-runtime`](anthropic-structured-output-runtime/SKILL.md) — schema-bound JSON / typed objects / extraction / classification via forced tool use, prefill, or strict prompt; validation, prompt-cache placement, extended-thinking handling, retries, tests, and telemetry. At canonical template parity; registered.

### Archetype coverage

| Archetype | Skill | Status |
|---|---|---|
| `structured-output-runtime` | [`anthropic-structured-output-runtime`](anthropic-structured-output-runtime/SKILL.md) | authored, registered |
| `tool-calling-runtime` | `anthropic-tool-use-runtime` | planned |
| `rag-runtime` | `anthropic-rag-runtime` | planned |
| `evals-and-observability` | `anthropic-evals-and-observability` | planned |
| `model-runtime` (context/caching) | `anthropic-prompt-caching-and-context-runtime` | planned |

### Planned skill scope (future work)

- **`anthropic-tool-use-runtime`** *(`tool-calling-runtime`)* — Anthropic tool-use wiring with tool schemas, execution adapter, authorization, idempotency, audit logging, and failure tests. Anthropic-specific surface folded into Operating rules: parallel tool use, `tool_choice` control, MCP connector tools where the architecture approves them, and prompt-cache placement on the tool-definition prefix.
- **`anthropic-rag-runtime`** *(`rag-runtime`)* — retrieval adapter, context packing, grounding prompt, citations, hallucination checks, retrieval evals. Anthropic-specific surface folded in: the **Citations API** for source-grounded answers, long-context window discipline, and cache placement on the retrieved-context prefix when the corpus is stable within a session.
- **`anthropic-evals-and-observability`** *(`evals-and-observability`)* — regression evals, prompt/model versioning, token and cost telemetry (including cache-read/write token accounting), tracing, dashboards, runbook notes. Anthropic-specific surface folded in: **Message Batches API** for offline eval runs and cost-efficient batch scoring.
- **`anthropic-prompt-caching-and-context-runtime`** *(`model-runtime`, Anthropic-specific)* — owns the cross-cutting context surface: `cache_control` breakpoint strategy, cache-hit measurement and TTL behavior, extended-thinking budget and thinking-block retention, long-context packing discipline, and prompt-structure conventions the other anthropic skills reference rather than re-specify.

## Anthropic-specific surface

Per the layer decision, most Anthropic-specific features are folded into the
relevant mirrored skills rather than split into their own skills:

| Feature | Home |
|---|---|
| Prompt caching (`cache_control`) | Operating rules of every anthropic skill; owned end-to-end by `anthropic-prompt-caching-and-context-runtime` |
| Extended thinking | Operating rules of the skill that uses it; budget/retention owned by `anthropic-prompt-caching-and-context-runtime` |
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

- [api-standards](../../../standards/api-standards/README.md)
- [security-standards](../../../standards/security-standards/README.md)
- [observability-standards](../../../standards/observability-standards/README.md)
- [deployment-standards](../../../standards/deployment-standards/README.md)
- [naming-conventions](../../../standards/naming-conventions/README.md)
