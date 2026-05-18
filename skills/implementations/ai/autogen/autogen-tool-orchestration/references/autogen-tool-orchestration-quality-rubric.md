# AutoGen Tool Orchestration Quality Rubric

Load this before declaring the integration complete. Revise until each check passes or the unresolved gap is explicitly documented as an ADR candidate against `ai-architecture.md`.

## Tool surface conformance

- [ ] Every registered tool exists in the approved tool surface — none added, widened, renamed, or repurposed.
- [ ] Each tool's input schema matches the approved schema exactly; no required field relaxed.
- [ ] Each tool's side-effect class is explicitly classified from the contract, not guessed.
- [ ] Every missing tool/side-effect/authorization/idempotency/audit/eval decision is an ADR candidate, not silently filled.

## Authorization and registration

- [ ] Authorization is enforced in the execution adapter before any side effect; a model-proposed call is never trusted.
- [ ] The principal is resolved from request context, not from model output.
- [ ] Each tool is registered only on the agents the topology permits (Researcher holds retrieval; Writer/Critic do not).
- [ ] There is no global tool registry; registration is per-agent and a closed set.

## Idempotency and failure

- [ ] Every side-effecting tool carries an idempotency key derived from the architecture's stable property.
- [ ] A replayed or retried tool call returns the prior result and does not double-apply (proven by test).
- [ ] A denied or failed tool call returns a structured error into the agent loop, not a swallowed exception.
- [ ] A failed retrieval prevents the Critic's grounding gate from passing; failure is never read as "grounded".

## Eval triplet

- [ ] Grounding score is computed against the fixed eval set, through the registered retrieval tool, and gated at the architecture's threshold.
- [ ] Citation correctness (citations actually support the claim) is computed and gated.
- [ ] Answer correctness is graded against gold answers on the fixed question set and gated.
- [ ] The eval harness fails closed below threshold; results are not merely described.

## Observability

- [ ] Every tool execution is audited (tool name, resolved principal, authz outcome, idempotency key, result class, correlation id).
- [ ] Metrics for tool-call counts, authorization outcomes, idempotency outcomes, tool failures, and latency are emitted.
- [ ] No secrets, raw tool arguments/results, or unredacted PII in traces, logs, or audit records.

## Tests

- [ ] Valid tool call.
- [ ] Unauthorized call denied at execution before any side effect.
- [ ] Tool execution failure handled as a structured error.
- [ ] Idempotent replay (no double-apply).
- [ ] Out-of-surface / ungranted tool call denied.
- [ ] Eval-gate failure.

## Standards conformance

- [ ] [api-standards](../../../../../../standards/api-standards/README.md): each tool schema is an external contract surface; versioning and breaking-change policy apply.
- [ ] [security-standards](../../../../../../standards/security-standards/README.md): authorization before side effects, principal from request context, redaction in logs/audit, deploy-time credentials.
- [ ] [observability-standards](../../../../../../standards/observability-standards/README.md): per-execution audit record, tool/authz/idempotency/failure metrics, correlation id.
- [ ] [deployment-standards](../../../../../../standards/deployment-standards/README.md): model, tool config, and authorization policy injected at deploy time, not hardcoded.
- [ ] [naming-conventions](../../../../../../standards/naming-conventions/README.md): tool, principal, metric, and audit-field names follow project rules.

## Failure handling

If a check fails:

1. Identify the missing or incorrect implementation.
2. If the decision cannot be inferred from `ai-architecture.md`, raise an ADR candidate — do not guess.
3. Revise the adapter and re-run the six required tests and the eval harness.
4. Keep any unresolved gap explicit as an ADR candidate — do not hide it as an assumption.
