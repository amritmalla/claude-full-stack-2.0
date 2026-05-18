---
name: anthropic-evals-and-observability
description: Use when an approved ai-architecture.md needs eval or observability coverage for an Anthropic Claude capability. Produces eval datasets, regression gates, prompt/model versioning, token/cost and cache telemetry, and traces. Not for model selection, RAG topology, or tool/agent design.
---

# Anthropic Evals and Observability

## When to use

Invoke when an Anthropic-backed capability (Claude via the Messages API) needs
measurable regression gates, production telemetry, prompt/model versioning, or
operational monitoring, and the success criteria and regression bar come from
`ai-architecture.md` or a quality-engineering handoff.

Do not use to define the model contract, success criteria, or eval bar from
scratch, nor for RAG, tool, or agent implementation.

## Inputs

Required:

- Approved `ai-architecture.md` (or an existing Anthropic capability under review).
- Capability name and success criteria.
- Regression bar and quality gate from `quality-engineering` (or the architecture).
- Dashboard, alerting, and runbook expectations from `operations`.
- Target application language, framework, and telemetry stack.

Optional:

- Evaluation examples or an approved source for creating them.
- Existing prompt registry or versioning scheme.
- Existing metrics, trace, and dashboard conventions.
- Cost and latency budgets, including a per-capability token budget.
- Prompt-cache strategy from the architecture (which prefixes are cached).
- Whether the capability uses extended thinking.
- Whether eval runs are eligible for the Message Batches API.

## Operating rules

- Every shipping Anthropic capability has at least one regression gate tied to a number from `ai-architecture.md` or a `quality-engineering` handoff. No gate, or no number → block promotion and emit the gap as an ADR candidate; never invent the threshold, cost budget, or required-metric set.
- The eval dataset is a contract surface. Its result schema (case id, input ref, expected, score, pass/fail, prompt/model version) is versioned and treated under api-standards; consumers of eval results are not broken by silent shape changes.
- No PII or secrets in eval datasets, traces, or logs without approved redaction. Production user data is not used as eval data unless an approved policy says so; raw prompts and raw model outputs are redacted in telemetry.
- Scoring method matches the claim. Deterministic checks for deterministic contracts; model-graded or human review only where justified, with documented rater criteria and the grader's own model/prompt version recorded.
- Prompt version and model id are first-class metadata on every runtime call and every eval case. An unversioned call is unobservable and fails this skill. Model id and prompt version are deploy-time configuration, never hardcoded; the eval gate runs in CI/CD before promotion.
- Token and cost telemetry accounts for caching explicitly. `input_tokens`, `output_tokens`, `cache_read_input_tokens`, and `cache_creation_input_tokens` are recorded separately from `usage`; estimated cost applies the cache-read and cache-write rates distinctly, not a single blended input rate. A cache miss is a cost event, never a correctness or eval failure.
- Extended-thinking cost is measured, not hidden. When the capability uses extended thinking, thinking tokens are counted within `output_tokens` and surfaced as a distinct telemetry dimension so a thinking-budget regression is visible; if extended thinking is not used, state N/A.
- Offline eval runs and bulk batch scoring route through the Message Batches API when latency is not required and the dataset is large enough to justify it. Batch results feed the same scoring harness and the same regression gate as synchronous runs; a batch run is not a weaker gate.
- Every alert names an owner, a condition, and a first response action, handed to `operations` as a runbook input. Dashboards expose the AI RED-equivalent (latency, tokens, cost, error/fallback rate) plus cache-hit ratio and regression-gate status.

## Output contract

The implementation MUST conform to:

- [api-standards](../../../../../standards/api-standards/README.md) — the eval result schema is an external contract surface; versioning and breaking-change policy apply.
- [security-standards](../../../../../standards/security-standards/README.md) — no PII or secrets in eval datasets, traces, or logs without redaction; approved policy for any real user data used in evaluation; Anthropic API credentials injected at deploy time, never committed.
- [observability-standards](../../../../../standards/observability-standards/README.md) — structured logs and metrics for latency, input/output tokens, cache-read/write tokens, estimated cost, fallback/error rate, and mandatory model/prompt version metadata; trace propagation; dashboards and alerting.
- [deployment-standards](../../../../../standards/deployment-standards/README.md) — model id and prompt version are deploy-time artifacts; the eval gate sits in the CI/CD promotion ladder, not run by hand.
- [naming-conventions](../../../../../standards/naming-conventions/README.md) — metric, eval-dataset, gate, and trace-span names follow project rules.

Upstream contract: `ai-architecture.md` (or a `quality-engineering` handoff) is the source of truth for capability success criteria, regression thresholds, required metrics, and cost/latency budgets; `operations` is the source of truth for alert ownership, dashboard layout, and runbook structure. If any of these is silent on a material decision — eval gate, regression threshold, cost budget, or required metric set — this skill pauses and raises an ADR candidate rather than inventing it.

## Progressive references

- Read `references/anthropic-evals-and-observability-playbook.md` when implementing any owned area or checking the anti-pattern list.
- Read `references/anthropic-evals-and-observability-quality-rubric.md` before declaring the eval and observability surface complete.
- Use `assets/anthropic-evals-and-observability.template.md` as the eval-dataset, scoring, batch-routing, telemetry, and dashboard reference.

## Process

1. Load `ai-architecture.md` (and any `quality-engineering` / `operations` handoff) and identify the capability, success criteria, regression bar, required metrics, and cost/latency budgets.
2. Verify the architecture names the success criteria, the regression threshold as an explicit number, the required metric set, and the alert ownership model. A silent gap here is an ADR candidate, not an assumption.
3. Define the eval dataset structure: case id, input reference, expected output or rubric, scoring method, sensitive-data handling, and a versioned result schema.
4. Implement or outline the scoring harness: deterministic checks for deterministic contracts, model-graded or human review where justified with documented rater criteria.
5. Define regression thresholds and the CI/CD promotion gate as explicit numbers tied to the architecture's success criteria.
6. Decide eval-run routing: synchronous for small/latency-bound runs, the Message Batches API for large offline runs and bulk scoring; wire batch results into the same harness and gate.
7. Add prompt version and model id metadata to runtime calls and every eval case.
8. Add metrics for latency, input/output tokens, cache-read and cache-write tokens, estimated cost (cache rates applied distinctly), thinking tokens where applicable, validation failures, and fallback/error rate.
9. Add tracing and structured logs with redaction; never record unredacted prompts, outputs, secrets, or PII.
10. Produce dashboard and runbook notes: owner, alert condition, first response action; expose cache-hit ratio and regression-gate status.
11. Document any unresolved threshold, budget, metric, or ownership gap as an ADR candidate instead of silently filling it in.

## Outputs

- Eval dataset structure with a versioned result schema.
- Scoring harness or implementation plan (deterministic, model-graded, or human).
- Regression thresholds and the CI/CD promotion gate.
- Eval-run routing decision (synchronous vs. Message Batches) with the rationale.
- Prompt/model versioning metadata on runtime calls and eval cases.
- Metrics, logs, and trace instrumentation notes, including cache and thinking token accounting.
- Dashboard and runbook notes for operational ownership.

Output rules:

- Every regression gate is an explicit number traced to a contract requirement; no subjective "looks good".
- Token and cost telemetry separates cache-read and cache-write tokens; estimated cost never uses a single blended input rate.
- The eval-run routing decision (synchronous vs. batch) is stated explicitly; a batch run is held to the same gate as a synchronous run.
- No Anthropic API key, environment endpoint, or unredacted prompt/output/PII committed to source or logs.

## Quality checks

- [ ] The implementation consumes named success criteria and a numeric regression bar from `ai-architecture.md` or a `quality-engineering` handoff.
- [ ] Every production capability has at least one regression gate that runs in CI/CD before promotion.
- [ ] The eval result schema is versioned and treated as a contract surface.
- [ ] Scoring method matches the claim; model-graded/human criteria are documented and the grader version is recorded.
- [ ] Telemetry records model id, prompt version, latency, input/output tokens, cache-read/write tokens, estimated cost, and fallback/error outcome.
- [ ] Estimated cost applies cache-read and cache-write rates distinctly; thinking tokens are surfaced or marked N/A.
- [ ] Eval-run routing (synchronous vs. Message Batches) is explicit and batch results feed the same gate.
- [ ] Eval datasets, traces, and logs carry no unredacted PII, secrets, or raw payloads; credentials are deploy-time only.
- [ ] Dashboard/runbook notes name an owner, an alert condition, and a first response action.
- [ ] Any missing threshold, budget, metric, or ownership decision is documented as an ADR candidate.

## References

- Upstream: [`architecture/ai-native-engineering`](../../../../architecture/ai-native-engineering/SKILL.md) — capability, success criteria, evaluation plan, required metrics, budgets.
- Related architecture: [`architecture/quality-engineering`](../../../../architecture/quality-engineering/SKILL.md) — regression bar, acceptance criteria, gate policy; [`architecture/operations`](../../../../architecture/operations/SKILL.md) — dashboards, alerting, runbook ownership.
- Cross-provider counterpart: [`openai-evals-and-observability`](../../openai/openai-evals-and-observability/SKILL.md) — same archetype, OpenAI mechanics.
- Related implementation skills: gates and observes the sibling anthropic runtime skills; every Anthropic runtime job routes its regression gate here. Sibling anthropic skills are listed in the [anthropic stack README](../README.md).
- Standards: [`api-standards`](../../../../../standards/api-standards/README.md), [`security-standards`](../../../../../standards/security-standards/README.md), [`observability-standards`](../../../../../standards/observability-standards/README.md), [`deployment-standards`](../../../../../standards/deployment-standards/README.md), [`naming-conventions`](../../../../../standards/naming-conventions/README.md).
