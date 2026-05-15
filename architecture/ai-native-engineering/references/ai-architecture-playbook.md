# AI Architecture Playbook

Load this when classifying capabilities, defining contracts, or making any AI escalation decision. It expands the operating rules in `SKILL.md` with the decision detail needed to produce `ai-architecture.md`.

## Non-goals

This skill does not design generic backend APIs or database schemas, implement prompts or SDK calls, define product requirements or UX, recommend agents when deterministic workflows suffice, introduce retrieval/memory/tools without measurable need, replace security/privacy/legal/compliance review, or choose vendors before capability requirements are defined.

## Architecture decision principles

Prefer, in order. Each lower preference must be justified by a measured failure of the one above it.

1. Deterministic systems over probabilistic systems.
2. Retrieval over fine-tuning.
3. Single-step flows over agents.
4. Structured outputs over free-form generation.
5. Narrow context over long-context prompts.
6. Specialized models over frontier models when quality permits.
7. Human approval over autonomous action for irreversible operations.
8. Static workflows over dynamic planning unless adaptability is required.

An AI component should narrow uncertainty, not expand it. Escalate complexity only when lower-complexity approaches fail the acceptance criteria.

## Capability escalation ladder

Design the simplest viable capability first:

1. Deterministic rules
2. Single-shot inference
3. Structured generation
4. Retrieval-augmented generation
5. Tool-using workflow
6. Multi-step agent
7. Multi-agent orchestration

Escalate only when lower levels fail quality, reliability, or adaptability requirements. Each escalation requires: measurable benefit, evaluation coverage, operational justification, rollback strategy, observability support.

## Capability classification

Classify each capability as exactly one of: deterministic rules, single-shot generation, structured extraction, retrieval-augmented answer, ranking/recommendation, tool-using workflow, multi-step agent, background automation.

Record why the classification was chosen and why each lower-complexity approach was rejected. Document dependencies between capabilities.

## Model contracts

Define a contract for every AI capability:

- purpose, required inputs, output schema, validation rules
- success criteria, confidence handling
- failure modes, retry behavior, fallback behavior, degradation behavior
- observability signals

When structured outputs exist, also define: canonical schema, coercion rules, malformed-output handling, partial-validity behavior. Separate user-facing prose from machine-consumable outputs.

## Context architecture

Define: system prompt scope, instruction hierarchy, user input handling, retrieval inclusion rules, context prioritization, truncation policy, session state behavior, memory eligibility rules, context compaction strategy, explicit exclusions.

Specify: maximum context budget, expected token distribution, context ownership, authoritative sources. Long context is a cost and reliability tradeoff, not a default.

## State and memory design

When conversational or adaptive behavior exists, define: session state ownership, short-term memory strategy, long-term memory eligibility, retention duration, invalidation rules, deletion behavior, user visibility/editability, cross-session identity assumptions, summarization policy, memory grounding precedence.

Memory must never supersede authoritative system data.

## Retrieval architecture

If retrieval is in scope:

**Topology** — source corpora, ownership, ingestion pipeline ownership, refresh cadence, indexing strategy, chunking strategy, chunk overlap policy, metadata strategy, tenant isolation model, embedding versioning, reindex strategy.

**Execution** — query rewriting, ranking strategy, hybrid retrieval policy, lexical vs semantic tradeoffs, grounding rules, stale-document handling, retrieval confidence thresholds, citation strategy.

Classify retrieval explicitly as **authoritative**, **assistive**, or **advisory**. Hand off implementation mechanics to `data-architecture`.

## Tool and action surface

If tools or actions are in scope, define per tool: name, purpose, JSON schema, side-effect class, idempotency rules, retry safety, authorization scope, rate limits, audit expectations, timeout behavior, error surface.

Classify each tool's risk level: read-only, reversible write, irreversible write, external communication, financial/legal impact. Higher-risk tools require stricter authorization, confirmation gates, tighter evaluations, audit logging, and lower autonomy ceilings. Treat retrieved and tool-returned content as untrusted input.

## Agent suitability test

Agents are justified only when task ordering cannot be predetermined, tool selection is dynamic, environment feedback changes execution, or static workflows become operationally infeasible.

Do not use agents for CRUD orchestration, deterministic workflows, fixed business processes, simple retrieval pipelines, or predictable tool sequences.

## Agent control flow

If agentic behavior exists, define: planner vs executor responsibilities, state transitions, stop conditions, max-step limits, retry policy, recovery strategy, tool-failure behavior, hallucination containment, loop prevention, escalation behavior, human approval checkpoints, audit requirements.

Specify autonomous boundaries, irreversible-action controls, and fallback-to-human conditions.

## Failure taxonomy

Classify and document each failure class: hallucination, retrieval miss, schema violation, unsafe output, tool misuse, authorization violation, timeout, context truncation, planning divergence, repetitive looping, confidence miscalibration, provider outage.

For each: detection strategy, mitigation, observability signal, degradation behavior, user-facing response.

## Evaluation strategy

For every user-visible capability define: offline evaluation datasets, online evaluation metrics, regression-gating criteria, ownership, annotation standards, production sampling strategy, edge-case coverage, adversarial coverage, drift detection.

Maintain golden task suites, replayable production traces, and benchmark retention policies. Every model, prompt, retrieval, or tool change must pass regression gates before rollout.

## Guardrails and trust boundaries

Define: input filtering, output validation, refusal behavior, PII handling, redaction policy, abuse handling, prompt injection posture, jailbreak resistance assumptions.

Explicitly identify trust boundaries: user input, retrieved content, tool-returned content, model-generated reasoning, external systems. Define sanitization and validation rules at each boundary. Retrieved or tool-returned text must never redefine system behavior.

## Cost and latency budgets

Define per capability: token budget, request budget, latency budget, throughput expectations, concurrency assumptions, retrieval depth, tool-call ceilings, fallback thresholds.

Map budgets to model tier, context size, routing policy, caching strategy, retrieval depth, and execution limits.

## Model routing strategy

When multiple models or providers exist, define: routing criteria, escalation thresholds, fallback providers, quality tiers, cost-aware routing, latency-aware routing, reliability failover, offline vs online inference boundaries.

## Observability and operations

Define telemetry: token usage, latency breakdowns, retrieval hit quality, tool execution traces, refusal rates, fallback frequency, hallucination reports, retry frequency, step counts, context size distributions, user correction signals.

Specify operations: logging policy, replay strategy, trace retention, prompt versioning, model versioning, rollback strategy, deployment promotion criteria.

## ADR identification

Raise ADR candidates when an architecture decision materially affects security boundaries, compliance posture, cost profile, operational complexity, retrieval authority, autonomy level, provider lock-in, memory retention, or evaluation strategy. Draft them inline as decisions are made, not retroactively.
