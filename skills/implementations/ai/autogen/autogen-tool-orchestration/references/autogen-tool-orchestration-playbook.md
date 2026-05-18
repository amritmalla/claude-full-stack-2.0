# AutoGen Tool Orchestration Playbook

Load this when implementing any owned area of `autogen-tool-orchestration` or checking the anti-pattern list. It expands the operating rules and process steps in `SKILL.md` with the AutoGen tool-registration and execution-adapter detail needed to produce a production-grade tool runtime grounded in the Research-and-synthesize reference.

## Why this workflow exists

Tool execution done wrong is a production incident, not a silent quality regression: the Researcher proposes a `fetch_document` call with arguments steered by prompt injection in a retrieved snippet and the adapter executes it because authorization was assumed to be the model's job; a retried retrieval that also writes a cache row double-applies because the tool had no idempotency key; a write tool gets registered on the Writer agent because the registry was global instead of per-agent; a failed retrieval returns an empty string the Critic reads as "no contradicting sources" and grounding passes on nothing.

The goal is an AutoGen tool runtime where the model proposes and the adapter disposes: every side effect is authorized in code, idempotent, audited, and bounded — and the tool surface, side-effect classes, and authorization model are the architecture's declared decisions, not conveniences invented at the keyboard. Behavior is anchored to one concrete reference (Research-and-synthesize) with measurable evals, so the skill teaches a grounded realization rather than generic AutoGen tips.

## Behavioral rules in depth

### 1. Consume the tool surface; do not reinterpret it

The set of tools, each tool's input schema, side-effect class, authorization model, principal source, idempotency policy, audit retention, and budgets all come from `ai-architecture.md`. Read it before registering a tool. Do not add a "helper" tool, widen an argument type, rename a tool, or relax a required field because it is convenient. In Research-and-synthesize the Researcher's retrieval tool is the load-bearing case: its schema is the contract the Critic's grounding check depends on. A tool-surface gap is an ADR candidate, not an implementation decision.

### 2. The model proposes; the adapter disposes

An AutoGen `FunctionCall` emitted by an agent is untrusted model output that may be steered by prompt injection in any content the model saw (a retrieved document, a prior agent message). Authorization is enforced in the execution adapter, never by trusting the model to "only call tools it should." The adapter, before any side effect: resolves the caller/principal from the request context (not from model output), checks that principal is permitted to invoke that tool with those arguments, and validates arguments against the approved input schema. Failing any check returns a structured error result, not an executed side effect.

### 3. Tools are per-agent and a closed set

Register only the approved tool surface, and register each tool only on the agents the topology permits. In the reference, the Researcher holds the retrieval tool; the Writer and Critic receive no tools they were not granted. Registration is not global. The per-agent boundary is a registration-time fact a reviewer can check without reading agent internals. (The topology that grants tools to agents is owned by `autogen-multi-agent-workflow`; this skill owns the registration and execution mechanics and enforces the per-agent boundary.)

### 4. Side-effect class is explicit

Classify every tool's side-effect class from `ai-architecture.md` — read-only, idempotent-write, or non-idempotent-write — and never guess. The retrieval tool is typically read-only; a tool that records a query, writes a cache, or mutates external state is side-effecting and falls under the idempotency rule. A tool whose class is unstated is an ADR candidate, not a default.

### 5. Side-effecting tools are idempotent

Every mutating tool execution carries an idempotency key derived from a stable request property per the architecture's policy (e.g. correlation id + tool name + argument hash). The adapter checks the key before applying the side effect, so a replayed or retried tool call returns the prior result rather than double-applying. The agent loop retries tool calls; idempotency is what makes that safe. Read-only tools may skip this only because their class is explicitly read-only.

### 6. Tool failure is a handled path

A denied or failed tool call returns a structured error result into the agent loop — not a swallowed exception, not an empty string the Critic misreads as "no contradicting evidence". In Research-and-synthesize a failed retrieval must prevent the Critic's grounding gate from passing: no sources means not grounded, never silently grounded. Failure is observable, attributable, and routed, not absorbed.

### 7. The eval triplet is wired, not narrated

Grounding score, citation correctness, and answer correctness are computed against the fixed eval set and gated at the architecture's thresholds, exercising the registered retrieval tool end to end. A skill that says "evaluate grounding" without a computed metric and a gate, run through the real tool path, is exactly the generic framework advice the deferral warned about. The eval harness runs the workflow over the fixed set and fails closed below threshold.

### 8. Audit and telemetry without leakage

Every tool execution emits an audit record: tool name, resolved principal, authorization outcome, idempotency key, result class (success / denied / failed), and correlation id. Telemetry logs tool-call counts, authorization outcomes, idempotency outcomes (fresh / replayed), tool-failure counts, and latency. Never log raw tool arguments, raw results, secrets, or PII unredacted. Credentials for any retrieval backend are injected at deploy time and never committed.

### 9. Provider-neutral execution

The model/provider is an `ai-architecture.md` input injected at deploy time. This skill owns tool registration and the execution adapter, not provider SDK mechanics; do not hardcode a provider client or model id. Provider specifics belong to the provider skills.

## Step detail

**Step 1 — Load the contract.** From `ai-architecture.md` extract the tool surface, each tool's input schema / side-effect class / authorization model / principal source, idempotency policy and key source, audit retention, eval plan. Missing any decision the runtime needs → ADR candidate before code.

**Step 2 — Verify completeness.** Confirm each tool's side-effect class, authorization model, idempotency policy, and audit retention are named. A silent gap here becomes an invented decision later.

**Step 3 — Define tools.** Build each tool from the approved name, description, and input schema verbatim. Classify the side-effect class explicitly. For the reference: the Researcher's `retrieve_sources` schema is the contract the grounding check depends on.

**Step 4 — Register per agent.** Register each tool only on the permitted agents (retrieval on the Researcher only). Keep the set closed; no global registry.

**Step 5 — Build the adapter.** Resolve principal from request context → authorization check → argument validation against the input schema → idempotency-keyed execution → structured result. A denied or failed call returns an error result, never an executed side effect.

**Step 6 — Idempotency.** For each side-effecting tool derive the key from the stable property per policy; a replay returns the prior result. Prove no double-apply.

**Step 7 — Audit.** Emit an audit record per execution (tool, principal, authz outcome, idempotency key, result class, correlation id) with redaction.

**Step 8 — Failure wiring.** Route denied/failed calls as structured errors into the agent loop; ensure the Critic's grounding gate cannot pass on a failed retrieval.

**Step 9 — Telemetry.** Emit tool-call counts, authorization/idempotency outcomes, failure counts, latency with a correlation id.

**Step 10 — Eval wiring.** Run the workflow over the fixed eval set through the registered retrieval tool; compute grounding, citation correctness, answer correctness; gate at thresholds; emit metrics.

**Step 11 — Tests.** Valid call; unauthorized call denied at execution; tool failure; idempotent replay (no double-apply); out-of-surface/ungranted tool call denial; eval-gate failure.

**Step 12 — ADR candidates.** Record any unresolved tool/side-effect/authorization/idempotency/audit/eval gap rather than filling it silently.

## Anti-patterns to detect

Call these out explicitly when found:

- A tool added, widened, renamed, or repurposed relative to `ai-architecture.md`
- Authorization delegated to the model ("the prompt tells it not to call that")
- A tool call executed without resolving the principal from request context
- A global tool registry instead of per-agent registration
- A side-effecting tool with no idempotency key, so replay double-applies
- Side-effect class guessed instead of taken from the contract
- A failed retrieval returned as an empty result the Critic reads as "grounded"
- The eval triplet described but not computed or not run through the real tool path (generic-advice smell)
- Raw tool arguments/results, secrets, or PII in logs or audit records
- Retrieval-backend credentials committed to source
- Provider SDK client or model id hardcoded in the adapter
- "Done" declared without the six required tests
