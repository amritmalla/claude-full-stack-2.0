# Anthropic AI Implementation Stack — Mature-Tier Build-Out

- Date: 2026-05-18
- Status: approved (brainstorming complete)
- Area: `skills/implementations/ai/anthropic`

## Goal

Complete the anthropic AI implementation stack to full archetype coverage at
**mature tier**, and register all skills so they are invocable plugin skills.

Outcome: a uniformly mature 5-skill anthropic stack, both AI READMEs updated to
match the Anthropic-centric direction, and all 5 skills registered in
`.claude-plugin/marketplace.json`.

## Context and decisions

Resolved during brainstorming:

- **Provider scope is Anthropic-centric.** OpenAI stays as a frozen lean
  baseline (no expansion); anthropic is the depth/investment target.
- **Scope: all 4 planned skills, each self-contained.** No skill defers to
  another for cache/thinking discipline; each carries its own `cache_control`
  and extended-thinking operating rules inline. `anthropic-prompt-caching-and-context-runtime`
  is authored as a peer runtime job, not a foundation the others reference.
- **Tier: mature.** Each skill is a 4-file unit
  (`SKILL.md` + playbook + quality-rubric + asset template). This intentionally
  diverges from the lean openai mirror and the (previously lean) existing
  anthropic sibling; the divergence is recorded in the stack README.
- **Existing `anthropic-structured-output-runtime` is upgraded to mature** in
  the same effort, so the whole stack is uniformly mature (no mixed tier).
- **Done bar: authored + registered.** All 5 skills authored at mature tier AND
  registered in `.claude-plugin/marketplace.json`; both READMEs and the
  marketplace updated.
- **Execution approach: template-first (Approach A).** Upgrade the existing,
  already-validated structured-output skill first to pin the mature exemplar,
  then author the other 4 against it as a consistency exercise.
- **No separate implementation plan.** Per standing preference, implementation
  proceeds directly from this approved spec; the writing-plans step is skipped.

## Mature-tier artifact model

Each skill is a 4-file unit mirroring repo mature exemplars (`system-design`,
flutter scaffold):

```
<skill>/
  SKILL.md                          # gains a "Progressive references" section
  references/<skill>-playbook.md     # the how: Anthropic mechanics, decision points
  references/<skill>-quality-rubric.md  # validation checklist, loaded before finalizing
  assets/<skill>.template.md         # the deliverable scaffold the skill produces
```

`SKILL.md` keeps its current section model (When to use / Inputs / Operating
rules / Output contract / Process / Outputs / Quality checks / References) and
gains a **Progressive references** section (modeled on `system-design`
SKILL.md) stating when to read playbook vs rubric vs template. Existing
structured-output content is preserved and factored into the playbook, not
rewritten. Voice/section-model anchor = the upgraded structured-output skill,
cross-checked against `system-design`.

## Per-skill scope

| Skill | Archetype | Core deliverable | Anthropic surface folded in |
|---|---|---|---|
| `anthropic-structured-output-runtime` *(upgrade)* | structured-output | (content unchanged) schema-bound output, validation, repair | cache placement, extended-thinking reconciliation |
| `anthropic-tool-use-runtime` *(new)* | tool-calling | tool schemas, execution adapter, authz, idempotency, audit log, failure tests | parallel tool use, `tool_choice` control, MCP connector tools (when architecture approves), cache on tool-definition prefix |
| `anthropic-rag-runtime` *(new)* | rag | retrieval adapter, context packing, grounding prompt, hallucination checks, retrieval evals | Citations API, long-context discipline, cache on stable retrieved-context prefix |
| `anthropic-evals-and-observability` *(new)* | evals/obs | regression evals, prompt/model versioning, token+cost telemetry, traces, runbook notes | Message Batches API for offline/batch scoring; cache-read/write token accounting |
| `anthropic-prompt-caching-and-context-runtime` *(new)* | model-runtime | `cache_control` breakpoint strategy, cache-hit/TTL measurement, extended-thinking budget+retention, long-context packing | the skill *is* this surface; authored as a peer runtime job, not a referenced foundation |

Every skill keeps the hard upstream rule: requires approved
`ai-architecture.md`; pauses with an ADR candidate when the architecture is
silent on schema / tool surface / retrieval rules / cache strategy / eval gate.

## Execution order (Approach A)

1. **Upgrade `anthropic-structured-output-runtime` to mature tier.** Extract
   its depth into `references/anthropic-structured-output-runtime-playbook.md`;
   write `references/anthropic-structured-output-runtime-quality-rubric.md`;
   write `assets/anthropic-structured-output-runtime.template.md`; add a
   Progressive references section to its SKILL.md. This is the pinned exemplar.
2. **Author the 4 new skills** against the exemplar, in order:
   `anthropic-tool-use-runtime` → `anthropic-rag-runtime` →
   `anthropic-evals-and-observability` →
   `anthropic-prompt-caching-and-context-runtime`. Each is a full 4-file unit.
3. **Update `skills/implementations/ai/anthropic/README.md`**: status to 5/5
   authored + registered; archetype-coverage table; reword the
   "other anthropic skills reference rather than re-specify" line to
   "each skill self-specifies its cache/thinking discipline;
   `anthropic-prompt-caching-and-context-runtime` owns the deep
   context/caching runtime job"; add a note that the stack is mature-tier and
   this intentionally diverges from the lean openai mirror.
4. **Update `skills/implementations/ai/README.md`**: fix the five-vs-six prose
   drift; mark the anthropic stack complete; apply the Anthropic-centric
   reframing (anthropic = primary/mature, openai = frozen lean baseline);
   update the v0.2 table.
5. **Register all 5 in `.claude-plugin/marketplace.json`**: verify the existing
   structured-output entry; add the 4 new entries.

## Verification (before claiming done)

- File-set parity: every skill has exactly the 4 files; section model matches
  the pinned exemplar.
- `.claude-plugin/marketplace.json` parses as valid JSON; all 5 entries resolve
  to real on-disk paths.
- Each `SKILL.md` frontmatter `description` is well under ~300 chars; detail
  lives in the When-to-use body (standing guidance).
- Cross-reference links in each `SKILL.md` (upstream, cross-provider
  counterpart, siblings) resolve.
- Both READMEs internally consistent (no stale counts, no contradicted
  "reference rather than re-specify" claim).

## Out of scope

- No changes to the openai stack (frozen lean baseline).
- No new langchain skills.
- No changes to upstream `architecture/ai-native-engineering`.
- crewai / autogen scaffolds remain deferred.
