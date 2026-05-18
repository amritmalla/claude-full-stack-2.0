# CrewAI Task and Tool Design Playbook

Load this when implementing any owned area of `crewai-task-and-tool-design` or checking the anti-pattern list. It expands the operating rules and process steps in `SKILL.md` with the CrewAI task-and-tool detail needed to produce a production-grade task decomposition and tool execution adapter grounded in the Research-and-synthesize reference.

## Why this workflow exists

Task and tool design done wrong is a production incident, not a silent quality regression: a Researcher task is silently chained into a "fix the answer too" task the architecture never approved, so the crew acquires autonomy nobody signed off on; the model proposes a `delete_source` call with arguments inferred from a prompt-injected document and the adapter runs it because authorization was assumed to be the model's job; a retried retrieve-and-cache tool re-charges a metered search API because the mutating tool had no idempotency key; a tool registered globally on the crew lets the Writer call retrieval it was never granted; an audit log dumps raw tool payloads including the API key into the trace store.

The goal is a CrewAI task/tool layer where the model proposes and the adapter disposes: task boundaries map exactly to the approved scope, every side effect is authorized in code, idempotent, audited, and bounded — and the tool surface is the architecture's declared decision, not a convenience invented at the keyboard. The behavior is anchored to one concrete reference (Research-and-synthesize) with a measurable eval triplet, so the skill teaches a grounded realization rather than generic CrewAI tips.

## Behavioral rules in depth

### 1. Consume the task and tool surface; do not reinterpret it

The task boundaries, owning agent per task, the set of tools, each tool's input schema, side-effect class, authorization model, idempotency policy, fan-out policy, audit retention, and eval plan all come from `ai-architecture.md`. Read it before defining a `Task` or a tool. Do not add a task, split or merge an approved boundary, add a "helper" tool, widen an argument type, rename a tool, or relax a required field because it is convenient. A task-boundary or tool-surface gap is an ADR candidate, not an implementation decision.

### 2. Tasks map to the approved scope, one owning agent each

Each CrewAI `Task` realizes exactly one approved boundary, with an explicit input/output contract (`description` and `expected_output`) and exactly one owning agent. In Research-and-synthesize that is a retrieve task → Researcher, a synthesis task → Writer, a verification task → Critic. Do not fold "verify" into the synthesis task "for efficiency", do not split retrieval across two tasks, and do not chain tasks into a loop the design never granted. The decomposition is recorded so a reviewer can check it against the architecture without reading agent internals. (Crew topology, process selection, and the Critic's termination authority are owned by `crewai-agent-workflow`; this skill owns the task units and their tool dependencies, and enforces the boundary.)

### 3. The model proposes; the adapter disposes

A proposed tool call is untrusted model output that may be steered by prompt injection in any content the model saw. Authorization is enforced in the execution adapter, never by trusting the model to "only call tools it should." The adapter, before any side effect: resolves the caller/principal from the request context (not from model output), checks that principal is permitted to invoke that tool with those arguments, and validates arguments against the approved input schema. Failing any check returns a structured error result to the task, not an executed side effect.

### 4. Tools are a closed, per-agent/per-task set

Register only the approved tool surface, and register each tool only on the agents and tasks the architecture permits. In the reference, the retrieve-sources tool is on the Researcher's task only; the Writer and Critic tasks receive no retrieval or write tools they were never granted. A crew-global tool registry is the same defect as a global agent registry: it grants reach the topology never approved.

### 5. Side-effect class is explicit; mutating tools are idempotent

Classify every tool's side-effect class explicitly — read-only, or mutating — and do not guess. Every mutating tool execution carries an idempotency key derived from a stable request property per the architecture's policy (e.g. correlation id + tool name + argument hash). The adapter checks the key before applying the side effect so a replayed or retried call does not double-apply. A read-only retrieval may skip idempotency; a cache-write or external mutation may not.

### 6. Fan-out is a decision

If a task is permitted to issue multiple tool calls, the adapter executes each with its own authorization and idempotency, under explicit ordering or bounded concurrency. If the architecture disallows fan-out, suppress it and assert in tests that only one tool call is processed per step. Unbounded fan-out of side-effecting calls is an incident, not a throughput optimization.

### 7. Audit every execution without leakage

Every tool execution emits an audit record: tool name, resolved principal, authorization outcome, idempotency key, result class (success / denied / failed), and correlation id. Never log raw tool arguments, raw results, secrets, or PII unredacted. Credentials for any tool-backed system are injected at deploy time and never committed. Audit retention follows the architecture's declared rule, not a default.

### 8. The eval triplet is wired, not narrated

The tool/task layer this skill owns is exercised by the eval harness: grounding score, citation correctness, and answer correctness are computed against the fixed eval set and gated at the architecture's thresholds. A retrieve tool that returns nothing or returns the wrong sources shows up as a grounding-score drop, not as a passing run. A skill that says "evaluate retrieval quality" without a computed metric and a gate is exactly the generic framework advice the deferral warned about.

### 9. Provider-neutral tool design

The model/provider is an `ai-architecture.md` input injected at deploy time. This skill owns task decomposition and the tool execution adapter, not provider SDK mechanics; do not hardcode a provider client or model id. Provider specifics belong to the provider skills (`anthropic-tool-use-runtime` for Claude tool mechanics this adapter wraps).

## Step detail

**Step 1 — Load the contract.** Open `ai-architecture.md`. Extract task boundaries, owning agent per task, tool surface, each tool's input schema / side-effect class / authorization model, idempotency policy, fan-out policy, audit retention, eval plan. For Research-and-synthesize: retrieve/synthesis/verify tasks, retrieve-sources tool on the Researcher.

**Step 2 — Verify completeness.** Confirm task boundaries, per-tool authorization, side-effect class, idempotency-key source, fan-out policy, and audit retention are all named. Any gap → ADR candidate before code.

**Step 3 — Decompose tasks.** Create one `Task` per approved boundary with an explicit input/output contract and a single owning agent; record the decomposition in the integration header.

**Step 4 — Define tools.** Build each tool from the approved name, description, and input schema verbatim; classify each side-effect class.

**Step 5 — Register tools.** Register approved tools only on the permitted agents/tasks (retrieve-sources on the Researcher's task only). No crew-global registry.

**Step 6 — Build the adapter.** Implement principal resolution from request context → authorization → argument validation against the schema → idempotency-keyed execution for mutating tools → structured result. A denied or failed call returns an error result, never an executed side effect.

**Step 7 — Fan-out policy.** Bound or order multi-call tasks with per-call authorization and idempotency; suppress fan-out where disallowed.

**Step 8 — Audit.** Emit an audit record per tool execution with the fields in rule 7 and redaction; honor the declared retention rule.

**Step 9 — Eval wiring.** Wire the tool/task layer into the eval harness so grounding, citation correctness, and answer correctness are computed over the fixed eval set and gated at thresholds.

**Step 10 — Tests.** Cover: valid tool call; unauthorized call (denied before side effect); tool execution failure surfaced to its task; idempotent replay (no double-apply); fan-out ordering/bound; eval-gate failure. These six are the minimum.

**Step 11 — ADR candidates.** Write any unresolved task/tool/authorization/side-effect/idempotency/audit/eval gap as an ADR candidate against `ai-architecture.md`. Do not silently fill it.

## Anti-patterns to detect

Call these out explicitly when found:

- A task invented, split, or merged relative to `ai-architecture.md`
- Tasks chained into autonomy or a loop the approved scope never granted
- A task with no explicit input/output contract or more than one owning agent
- A tool added, widened, renamed, or repurposed relative to the contract
- Authorization delegated to the model ("the prompt tells it not to call that")
- A tool call executed without resolving the principal from request context
- A mutating tool with no idempotency key, so replay double-applies
- A tool's side-effect class unclassified or guessed
- A crew-global tool registry instead of per-agent/per-task registration
- Tool fan-out unbounded, or its allowance/suppression never decided
- Raw tool arguments/results, secrets, or PII in logs or audit records
- Audit retention left at a default instead of the declared rule
- The eval triplet described but not computed or not gated (generic-advice smell)
- Provider SDK client or model id hardcoded in the tool/task layer
- "Done" declared without the six required tests
