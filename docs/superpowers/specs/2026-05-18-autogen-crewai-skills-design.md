# AutoGen + CrewAI Skill Stacks — Mature-Tier Build-Out

- Date: 2026-05-18
- Status: approved (brainstorming complete)
- Area: `skills/implementations/ai/autogen`, `skills/implementations/ai/crewai`

## Goal

Un-defer the `autogen` and `crewai` scaffolds and author their planned skills at
**mature tier**, grounded in one shared concrete reference workflow so they do
not become generic framework advice, and register all skills so they are
invocable.

Outcome: 4 mature-tier skills (2 autogen, 2 crewai), both stack READMEs moved
from "deferred scaffold" to "complete", the `implementations/ai` README updated,
and all 4 registered in `.claude-plugin/marketplace.json`.

## Context and decisions

Resolved during brainstorming:

- **Deferral unblock: provide a concrete reference workflow.** Both stacks were
  deferred specifically because authoring without a reference use case "risks
  generic framework advice." The documented un-deferral gate — "a concrete
  reference [multi-]agent workflow with measurable eval criteria" — is satisfied
  by the reference workflow below.
- **Shared reference workflow: Research-and-synthesize.** One canonical workflow
  realized by *both* frameworks against the *same* eval criteria, mirroring how
  anthropic/openai mirror archetype boundaries.
- **Tier: mature.** Each skill is a 4-file unit
  (`SKILL.md` + playbook + quality-rubric + asset template), identical in shape
  to the pinned anthropic exemplar. Intentionally diverges from the lean
  single-file `langchain-agent-runtime` framework precedent; the divergence is
  recorded in the READMEs.
- **Provider-neutral.** Per the repo's decided design constraint ("provider
  skills own SDK mechanics; framework skills own orchestration"), these 4 skills
  are provider-neutral; model/provider config is an `ai-architecture.md` input,
  not baked in. `langchain-agent-runtime` sets the precedent.
- **Self-contained skills.** Consistent with the anthropic decision: no skill
  depends on another, no shared cross-skill reference file. Each skill restates
  the eval triplet and its own framework realization.
- **Done bar: authored + registered.** All 4 authored at mature tier AND
  registered; both stack READMEs and the `implementations/ai` README updated.
- **Execution approach: reference-anchored, exemplar-pinned (Approach A).** Pin
  `autogen-multi-agent-workflow` as the mature framework exemplar first, then
  author the other 3 against it in parallel.
- **No separate implementation plan.** Per standing preference, implementation
  proceeds directly from this approved spec; the writing-plans step is skipped.

## The shared reference workflow (grounding spine)

**Research-and-synthesize**, framework-invariant. Three roles:

- **Researcher** — takes a question, retrieves source material from the
  corpus/retrieval surface defined by `ai-architecture.md`.
- **Critic/verifier** — checks the draft's claims against retrieved sources;
  flags ungrounded or mis-cited statements; gates completion.
- **Writer** — produces the final synthesized answer with inline citations.

**Contracts.** Input: a question (+ architecture-defined retrieval surface).
Output: a synthesized answer with citations to sources. **Termination** is
bounded: max rounds/turns enforced in code; the Critic gates "done" — not final
until grounding passes or max-rounds is hit, then the architecture's degradation
path executes.

**Fixed eval set + 3 measurable metrics** (identical across both frameworks):

1. **Grounding score** — fraction of answer claims supported by retrieved
   sources.
2. **Citation correctness** — citations actually support the claim
   (precision/recall).
3. **Answer correctness** — graded against gold answers on a fixed question set.

The roles, I/O contract, eval set, and metrics are framework-invariant. autogen
vs crewai differ ONLY in topology realization and tool registration/orchestration
mechanics — never in what the workflow is or how it is scored. This spec is the
canonical statement of the reference; each skill restates the parts it needs.

## The 4 skills

| Skill | Archetype | Realizes (in its framework) |
|---|---|---|
| `autogen-multi-agent-workflow` | agent-runtime | Research-and-synthesize as AutoGen group-chat/teams: role→agent mapping, Critic-gated completion, max-turn/termination in code, loop-safety tests, tracing, eval wiring to the 3 metrics |
| `autogen-tool-orchestration` | tool-calling-runtime | Researcher retrieval + tools as AutoGen tool/function registration & execution adapter: authorization, idempotency, audit logging, tool-failure tests |
| `crewai-agent-workflow` | agent-runtime | Same topology as a CrewAI crew (role/goal agents; sequential or hierarchical process), Critic-as-task gate, max-step/termination, loop-safety tests, tracing, same eval wiring |
| `crewai-task-and-tool-design` | tool-calling-runtime | Task decomposition + CrewAI tool registry/execution adapter: authorization, idempotency, audit logging, failure tests |

Each skill is a mature 4-file unit:

```
<skill>/
  SKILL.md                          # same section model as the anthropic exemplar; has Progressive references
  references/<skill>-playbook.md     # the how: framework mechanics + the reference realization
  references/<skill>-quality-rubric.md  # validation checklist, loaded before finalizing
  assets/<skill>.template.md         # the deliverable scaffold the skill produces
```

SKILL.md section order: frontmatter (`name`, `description`) / `# Title` /
`## When to use` / `## Inputs` / `## Operating rules` / `## Output contract`
(+ "Upstream contract:" paragraph) / `## Progressive references` /
`## Process` / `## Outputs` (+ "Output rules:") / `## Quality checks` /
`## References`.

Every agent-runtime skill keeps the hard agent rule: no agent without max
steps, timeout, stop conditions, tool authorization, and an eval plan — missing
any → raise an ADR candidate. Every skill requires approved `ai-architecture.md`
and pauses with an ADR candidate when it is silent on a material decision.

## Execution order (Approach A)

1. **Pin the exemplar.** Author `autogen-multi-agent-workflow` fully at mature
   tier realizing the reference workflow. This pins section model, voice,
   depth, and eval-triplet wiring.
2. **Parallel-author the other 3** against the pinned exemplar + the reference:
   `autogen-tool-orchestration`, `crewai-agent-workflow`,
   `crewai-task-and-tool-design`. Each a full self-contained 4-file unit; the
   two tool-calling skills also cross-check the anthropic `anthropic-tool-use-runtime`
   mature exemplar for authz/idempotency/audit shape.
3. **Update `autogen/README.md` and `crewai/README.md`**: status
   "scaffold (deferred)" → "complete (mature), registered"; fill Authored
   sections; archetype-coverage tables to authored; replace
   "Planned skill scope (future work)" with realized scope; record the
   Research-and-synthesize reference as the satisfied un-deferral gate; add the
   mature-tier note (intentional divergence from lean `langchain-agent-runtime`).
4. **Update `implementations/ai/README.md`**: remove autogen/crewai from
   "Deferred until a reference workflow exists"; add the 4 skills to the
   Registered skills table at mature tier; note the shared reference workflow.
5. **Register all 4 in `.claude-plugin/marketplace.json`** (sorted insertion).

## Verification (before claiming done)

- File-set parity: each skill exactly 4 files; `name` matches directory;
  section model matches the pinned exemplar.
- `.claude-plugin/marketplace.json` parses as valid JSON; all entries resolve
  to real paths; list stays sorted.
- Each `SKILL.md` `description` is well under ~300 chars, starts "Use when",
  detail in the `## When to use` body. Subagents are briefed to write minimal
  descriptions, NOT to match exemplar length.
- All relative cross-reference links resolve.
- Anti-genericness check: every skill demonstrably ties to the
  Research-and-synthesize reference and the 3 eval metrics; no skill reads as
  generic framework advice.
- `autogen/README.md`, `crewai/README.md`, and `implementations/ai/README.md`
  internally consistent — no stale "deferred" or "scaffold" markers.

## Out of scope

- No changes to the anthropic or openai stacks.
- No new langchain skills; `langchain-agent-runtime` is not upgraded here.
- No changes to upstream `architecture/ai-native-engineering`.
- The reference workflow is a grounding device for the skills, not a shipped
  application; no runnable end-to-end app is built.
