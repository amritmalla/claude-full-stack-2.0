# AutoGen Multi-Agent Workflow Quality Rubric

Load this before declaring the workflow complete. Revise until each check passes or the unresolved gap is explicitly documented as an ADR candidate against `ai-architecture.md`.

## Topology conformance

- [ ] Roles, speaker/turn order or team structure, and delegation edges match `ai-architecture.md` exactly — none invented, merged, or split.
- [ ] Each approved role maps to exactly one AutoGen agent; the mapping is recorded.
- [ ] No manager/orchestrator or delegation authority exists beyond the approved topology.
- [ ] Every missing topology/tool/budget/degradation/eval decision is an ADR candidate, not silently filled.

## Termination and budgets

- [ ] The termination authority (Critic/verifier in the reference) is a code-checked condition, not a prompt instruction.
- [ ] Max turns, per-agent step bounds, and a wall-clock ceiling are enforced in orchestrator code.
- [ ] Budget exhaustion routes to the architecture's declared degradation path — never silent truncation presented as success.
- [ ] Loop/stall detection (repeated turns, ping-pong, no-progress rounds) terminates into degradation.

## Tools and security

- [ ] Only the approved tool surface is registered, and each tool only on the agents the topology permits.
- [ ] Tool authorization is checked on execution; a model-proposed call is never trusted.
- [ ] Prompt-injection posture across agent messages follows `architecture/security`.
- [ ] Memory/session policy (retention, scoping, redaction) is implemented as specified; no unbounded shared scratchpad.

## Eval triplet

- [ ] Grounding score is computed against the fixed eval set and gated at the architecture's threshold.
- [ ] Citation correctness (citations actually support the claim) is computed and gated.
- [ ] Answer correctness is graded against gold answers on the fixed question set and gated.
- [ ] The eval harness fails closed below threshold; results are not merely described.

## Observability

- [ ] Every turn, tool call, role transition, and the termination decision is traced with a correlation id and the deciding role.
- [ ] Multi-agent metrics (turns, per-role actions, tool calls, termination cause) are emitted.
- [ ] No secrets, raw tool payloads, or unredacted PII in traces or logs.

## Tests

- [ ] Successful completion.
- [ ] Critic-rejected-then-revised.
- [ ] Tool failure.
- [ ] Unsafe-action denial.
- [ ] Turn/loop exhaustion → degradation path.
- [ ] Eval-gate failure.

## Standards conformance

- [ ] [api-standards](../../../../../../standards/api-standards/README.md): when exposed as an external contract surface, request/response and versioning policy apply.
- [ ] [security-standards](../../../../../../standards/security-standards/README.md): per-agent tool authorization, injection posture, memory redaction, deploy-time credentials.
- [ ] [observability-standards](../../../../../../standards/observability-standards/README.md): per-turn tracing, multi-agent metrics, correlation id.
- [ ] [deployment-standards](../../../../../../standards/deployment-standards/README.md): model/prompt/topology/tool config injected at deploy time, not hardcoded.
- [ ] [naming-conventions](../../../../../../standards/naming-conventions/README.md): agent, role, tool, and metric names follow project rules.

## Failure handling

If a check fails:

1. Identify the missing or incorrect implementation.
2. If the decision cannot be inferred from `ai-architecture.md`, raise an ADR candidate — do not guess.
3. Revise the workflow and re-run the six required tests and the eval harness.
4. Keep any unresolved gap explicit as an ADR candidate — do not hide it as an assumption.
