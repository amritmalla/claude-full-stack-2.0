# CrewAI Task and Tool Design Quality Rubric

Load this before declaring the task/tool layer complete. Revise until each check passes or the unresolved gap is explicitly documented as an ADR candidate against `ai-architecture.md`.

## Task decomposition conformance

- [ ] Task boundaries map 1:1 to the approved scope in `ai-architecture.md` — none invented, split, or merged.
- [ ] Each `Task` has an explicit input/output contract (`description`, `expected_output`) and exactly one owning agent.
- [ ] Tasks are not chained into autonomy or a loop the approved scope never granted.
- [ ] The decomposition is recorded so it can be checked against the architecture without reading agent internals.
- [ ] Every missing task-boundary/tool/authorization/side-effect/idempotency/audit/eval decision is an ADR candidate, not silently filled.

## Tool surface and schema

- [ ] Only the approved tool surface is registered; no tool added, widened, renamed, or repurposed.
- [ ] Each tool's input schema is exactly the approved schema; versioning and breaking-change policy apply as for any external API.
- [ ] Each tool's side-effect class (read-only / mutating) is classified explicitly, not guessed.
- [ ] Each tool is registered only on the agents/tasks the architecture permits; no crew-global registry.

## Authorization, idempotency, and side effects

- [ ] Authorization is enforced in the execution adapter before any side effect; a model-proposed call is never trusted.
- [ ] The principal is resolved from request context, never from model output.
- [ ] Arguments are validated against the approved input schema before execution.
- [ ] Every mutating tool execution carries an idempotency key from a stable request property; replay is proven not to double-apply.
- [ ] Tool fan-out is bounded with per-call authorization and idempotency, or explicitly disallowed and asserted off.

## Eval triplet

- [ ] Grounding score is computed against the fixed eval set and gated at the architecture's threshold.
- [ ] Citation correctness (citations actually support the claim) is computed and gated.
- [ ] Answer correctness is graded against gold answers on the fixed question set and gated.
- [ ] The harness exercises the tool/task layer (e.g. the Researcher's retrieve tool) and fails closed below threshold; results are not merely described.

## Observability

- [ ] Every tool execution emits an audit record: tool name, resolved principal, authorization outcome, idempotency key, result class, correlation id.
- [ ] Metrics (tool-call counts, authorization outcomes, idempotency hits, tool/task failures) are emitted with a correlation id propagated through the task and tool path.
- [ ] No secrets, raw tool payloads, or unredacted PII in traces, logs, or audit records; audit retention follows the declared rule.

## Tests

- [ ] Valid tool call.
- [ ] Unauthorized call (denied before side effect).
- [ ] Tool execution failure surfaced to its task.
- [ ] Idempotent replay (no double-apply).
- [ ] Fan-out ordering/bound (or fan-out suppression asserted).
- [ ] Eval-gate failure.

## Standards conformance

- [ ] [api-standards](../../../../../../standards/api-standards/README.md): each tool schema and task input/output contract is an external contract surface; versioning and breaking-change policy apply.
- [ ] [security-standards](../../../../../../standards/security-standards/README.md): authorization in the adapter before side effects, principal from request context, deploy-time credentials, no secrets or PII without redaction.
- [ ] [observability-standards](../../../../../../standards/observability-standards/README.md): per-execution audit records and metrics with a correlation id propagated through the task and tool path.
- [ ] [deployment-standards](../../../../../../standards/deployment-standards/README.md): model/prompt/tool/task config injected at deploy time, not hardcoded.
- [ ] [naming-conventions](../../../../../../standards/naming-conventions/README.md): task, tool, metric, and audit-field names follow project rules.

## Failure handling

If a check fails:

1. Identify the missing or incorrect implementation.
2. If the decision cannot be inferred from `ai-architecture.md`, raise an ADR candidate — do not guess.
3. Revise the task/tool layer and re-run the six required tests and the eval harness.
4. Keep any unresolved gap explicit as an ADR candidate — do not hide it as an assumption.
