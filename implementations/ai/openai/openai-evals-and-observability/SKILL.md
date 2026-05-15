---
name: openai-evals-and-observability
description: Use when adding regression evaluation, prompt and model versioning, token and cost telemetry, latency tracking, tracing, dashboards, or operational monitoring for OpenAI-backed AI capabilities. Produces eval dataset structure, scoring harness, regression thresholds, prompt/model metadata, logs, metrics, traces, and runbook notes. Do not use for initial AI architecture, feature ideation, RAG implementation, tool implementation, or agent orchestration.
---

# OpenAI Evals And Observability

## When to use

Invoke when an OpenAI-backed capability needs measurable quality gates,
production telemetry, prompt/model versioning, or operational monitoring.

Do not use to define the model contract from scratch. The quality target should
come from `ai-architecture.md` or a quality-engineering handoff.

## Inputs

Required:

- Approved `ai-architecture.md` or existing OpenAI capability implementation.
- Capability name and success criteria.
- Evaluation examples or source for creating them.
- Target application language, framework, and telemetry stack.

Optional:

- Existing prompt registry or versioning scheme.
- Existing metrics and tracing conventions.
- Cost and latency budgets.
- Runbook or dashboard template.

## Operating rules

- Every shipping AI capability has at least one regression gate. No gate → block promotion and emit the gap explicitly.
- Eval datasets encode expected behavior and sensitive-data handling. Production user data is not used as eval data without an approved policy.
- Scoring method matches the claim. Deterministic checks for deterministic contracts; model-graded or human review only where justified, with documented rater criteria.
- Regression thresholds and promotion gates are explicit numbers tied to the architecture's success criteria, not subjective judgement.
- Prompt and model versions are first-class metadata on every runtime call and eval run. An unversioned call is unobservable and fails this skill.
- Telemetry never records unredacted secrets, credentials, or sensitive user payloads.
- Every alert names an owner, a condition, and a first response action, handed off to `operations` as a runbook input.

## Output contract

The implementation MUST conform to:

- [security-standards](../../../../standards/security-standards/README.md) — redaction in eval data, traces, and logs; approved handling for any real user data used in evaluation.
- [observability-standards](../../../../standards/observability-standards/README.md) — AI RED-equivalent (latency, tokens, cost, error/fallback rate), traces, structured logs, and mandatory model/prompt version metadata.
- [deployment-standards](../../../../standards/deployment-standards/README.md) — eval gates sit in the promotion ladder; prompt and model versions are deploy-time artifacts.
- [naming-conventions](../../../../standards/naming-conventions/README.md) — metric, eval-dataset, and gate names follow project rules.
- [architecture-schema](../../../../standards/architecture-schema/README.md) — capability tier drives regression-gate strictness and alert severity.

Upstream contract: `ai-architecture.md` (or a `quality-engineering` handoff) is the source of truth for success criteria, regression thresholds, and budgets; `operations` is the source of truth for alert ownership and runbook structure. If either is silent, this skill pauses and raises an ADR candidate rather than inventing the threshold.

## Process

1. Identify capability success criteria, failure modes, latency budget, cost budget, and model/prompt versions.
2. Define an eval dataset structure with expected outputs, scoring notes, and sensitive-data handling.
3. Implement or outline a scoring harness for deterministic checks, model-graded checks, or human review as appropriate.
4. Define regression thresholds and promotion gates.
5. Add prompt and model version metadata to runtime calls and eval runs.
6. Add metrics for latency, token use, estimated cost, validation failures, fallback rate, and model/provider errors.
7. Add tracing and structured logs that avoid unredacted sensitive payloads.
8. Produce dashboard and runbook notes for operational ownership.

## Outputs

- Eval dataset structure.
- Scoring harness or implementation plan.
- Regression thresholds and release gates.
- Prompt/model versioning metadata.
- Metrics, logs, and trace instrumentation notes.
- Dashboard and runbook notes.

## Quality checks

- [ ] Every production capability has at least one regression gate.
- [ ] Eval data records expected behavior and sensitive-data handling.
- [ ] Runtime telemetry includes model, prompt version, latency, token usage, fallback, and error outcome.
- [ ] Logs avoid unredacted secrets, credentials, and sensitive user payloads.
- [ ] Dashboard or runbook notes identify owner, alert condition, and first response action.

## References

- Upstream: [`architecture/ai-native-engineering`](../../../../architecture/ai-native-engineering/SKILL.md) — success criteria, evaluation plan, regression thresholds, budgets.
- Related architecture: [`architecture/quality-engineering`](../../../../architecture/quality-engineering/SKILL.md) (regression policy, acceptance criteria), [`architecture/operations`](../../../../architecture/operations/SKILL.md) (alert ownership, runbooks).
- Related implementation skills: gates and observes [`openai-structured-output-runtime`](../openai-structured-output-runtime/SKILL.md), [`openai-tool-calling-runtime`](../openai-tool-calling-runtime/SKILL.md), [`openai-rag-runtime`](../openai-rag-runtime/SKILL.md), and [`langchain-agent-runtime`](../../langchain/langchain-agent-runtime/SKILL.md) — every runtime job routes its regression gate here.
