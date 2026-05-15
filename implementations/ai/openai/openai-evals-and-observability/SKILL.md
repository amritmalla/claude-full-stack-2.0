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

- Upstream: [`architecture/ai-native-engineering`](../../../../architecture/ai-native-engineering/SKILL.md).
- Related: [`architecture/quality-engineering`](../../../../architecture/quality-engineering/SKILL.md), [`architecture/operations`](../../../../architecture/operations/SKILL.md).
