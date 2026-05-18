# Anthropic Evals and Observability Quality Rubric

Load this before declaring the eval and observability surface complete. Revise until each check passes or the unresolved gap is explicitly documented as an ADR candidate against `ai-architecture.md`.

## Contract conformance

- [ ] The implementation consumes named success criteria and a numeric regression bar from `ai-architecture.md` or a `quality-engineering` handoff — not invented.
- [ ] Required metric set, cost/latency budget, and alert ownership are taken from the architecture / `operations`, not assumed.
- [ ] Every missing threshold, budget, metric, or ownership decision is recorded as an ADR candidate, not silently filled.

## Eval dataset and result schema

- [ ] The eval dataset structure defines case id, input reference, expected output or rubric, scoring method, and sensitive-data handling.
- [ ] The eval result schema is versioned and treated as an external contract surface under api-standards.
- [ ] No unredacted PII or secrets in the dataset; real user data is used only under an approved policy.

## Scoring and gates

- [ ] Scoring method matches the claim (deterministic for deterministic contracts; model-graded/human only where justified).
- [ ] Model-graded or human rater criteria are documented; the grader's own model id and prompt version are recorded.
- [ ] Regression thresholds and the promotion gate are explicit numbers tied to the architecture's success criteria.
- [ ] The eval gate runs in CI/CD before promotion, not by hand.

## Eval-run routing

- [ ] The synchronous-vs-Message-Batches routing decision is explicit with a stated rationale.
- [ ] Batch results feed the same scoring harness and the same regression gate as synchronous runs.
- [ ] Batch is not used for inline production gating given its minutes-to-hours latency.

## Telemetry

- [ ] Logs/metrics include model id, prompt version, latency, input/output tokens, cache-read tokens, cache-write tokens, estimated cost, validation failures, and fallback/error rate.
- [ ] Estimated cost applies uncached-input, cache-write, and cache-read rates distinctly — no single blended input rate.
- [ ] A cache miss is recorded on the cache-hit-ratio metric, never as a correctness or eval failure.
- [ ] Thinking tokens are surfaced as a distinct dimension, or extended thinking is explicitly marked N/A.
- [ ] No raw prompt, raw output, secret, or PII is logged unredacted; trace context propagates through the call.
- [ ] Anthropic API key, model id, and prompt version are deploy-time config, never committed or hardcoded.

## Dashboards and runbooks

- [ ] Dashboard exposes the AI RED-equivalent plus cache-hit ratio and regression-gate status.
- [ ] Every alert names an owner, a condition, and a first response action, handed to `operations` as a runbook input.

## Standards conformance

- [ ] [api-standards](../../../../../../standards/api-standards/README.md): the eval result schema is an external contract surface; versioning and breaking-change policy apply.
- [ ] [security-standards](../../../../../../standards/security-standards/README.md): no PII or secrets in eval data, traces, or logs without redaction; approved handling for any real user data; credentials injected at deploy time.
- [ ] [observability-standards](../../../../../../standards/observability-standards/README.md): structured logs and metrics for latency, tokens, cache outcome, cost, fallback/error, and model/prompt version; trace propagation; dashboards and alerting.
- [ ] [deployment-standards](../../../../../../standards/deployment-standards/README.md): model id and prompt version are deploy-time artifacts; the eval gate sits in the CI/CD promotion ladder.
- [ ] [naming-conventions](../../../../../../standards/naming-conventions/README.md): metric, eval-dataset, gate, and trace-span names follow project rules.

## Failure handling

If a check fails:

1. Identify the missing or incorrect implementation.
2. If the decision cannot be inferred from `ai-architecture.md` or a `quality-engineering` / `operations` handoff, raise an ADR candidate — do not guess the threshold, budget, or metric set.
3. Revise the eval, telemetry, or gate and re-run the regression gate.
4. Keep any unresolved gap explicit as an ADR candidate — do not hide it as an assumption.
