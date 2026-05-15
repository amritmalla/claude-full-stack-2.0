---
product: <kebab-case slug>          # matches the system-design / PRD slug
status: draft                       # draft | review | approved | superseded
owner: <name or role>
system_design: <relative path to source system-design.md>
prd: <relative path to source PRD, or null>
version: 0.1.0                      # semver
last_reviewed: YYYY-MM-DD
---

# AI Architecture: [Product or Capability Name]

## Overview

[One paragraph: which AI capabilities exist, the user tasks they serve, what this architecture optimizes for, and what it intentionally does not do. State the highest escalation level reached and why.]

## AI Capability Inventory

| Capability | Consumer | User Task | Business Objective | Acceptance Criteria | Risk Profile | Depends On |
|---|---|---|---|---|---|---|
| [name] | [who/what] | [task] | [objective] | [criteria] | [low/med/high] | [capabilities] |

## Capability Classification

| Capability | Level | Why This Level | Why Lower Levels Rejected |
|---|---|---|---|
| [name] | [deterministic / single-shot / structured extraction / RAG / ranking / tool-using / multi-step agent / background automation] | [reason] | [measured failure of simpler level] |

## Model Contracts

### [Capability Name]

| Field | Definition |
|---|---|
| Purpose | [what it does] |
| Required inputs | [inputs] |
| Output schema | [schema or link] |
| Validation rules | [rules] |
| Success criteria | [criteria] |
| Confidence handling | [behavior] |
| Failure modes | [modes] |
| Retry behavior | [policy] |
| Fallback behavior | [behavior] |
| Degradation behavior | [behavior when unavailable/low-confidence] |
| Observability signals | [signals] |

Structured output (if applicable): canonical schema [ref], coercion rules [rules], malformed-output handling [behavior], partial-validity behavior [behavior].

## Context Architecture

| Concern | Decision |
|---|---|
| System prompt scope | [scope] |
| Instruction hierarchy | [order of authority] |
| User input handling | [handling] |
| Retrieval inclusion rules | [rules] |
| Prioritization & truncation | [policy] |
| Maximum context budget | [tokens] |
| Authoritative sources | [sources] |
| Explicit exclusions | [what never enters context] |

## State & Memory Design

*Conditional — include when conversational or adaptive behavior exists; otherwise list under Omitted sections.*

| Concern | Decision |
|---|---|
| Session state ownership | [owner] |
| Short-term memory | [strategy] |
| Long-term memory eligibility | [rule] |
| Retention / invalidation / deletion | [rules] |
| User visibility / editability | [behavior] |
| Cross-session identity | [assumption] |
| Memory grounding precedence | [authoritative data wins] |

## Retrieval Architecture

*Conditional — include when retrieval is in scope; otherwise list under Omitted sections.*

**Classification:** [authoritative | assistive | advisory]

| Topology | Decision |  | Execution | Decision |
|---|---|---|---|---|
| Source corpora | [corpora] |  | Query rewriting | [strategy] |
| Ownership | [owner] |  | Ranking strategy | [strategy] |
| Ingestion & refresh cadence | [cadence] |  | Hybrid / lexical vs semantic | [policy] |
| Chunking & overlap | [strategy] |  | Grounding rules | [rules] |
| Metadata & tenant isolation | [model] |  | Stale-document handling | [behavior] |
| Embedding & reindex strategy | [strategy] |  | Confidence threshold & citation | [policy] |

Implementation mechanics handed off to `data-architecture`.

## Tool & Action Surface

*Conditional — include when tools or actions are in scope; otherwise list under Omitted sections.*

| Tool | Purpose | JSON Schema | Side-effect Class | Idempotency | Authz Scope | Rate Limit | Risk Level | Timeout / Error |
|---|---|---|---|---|---|---|---|---|
| [name] | [purpose] | [ref] | [read/write/external/...] | [rule] | [scope] | [limit] | [read-only / reversible / irreversible / external / financial-legal] | [behavior] |

## Agent Control Flow

*Conditional — include when the agent suitability test passes; otherwise list under Omitted sections with the suitability rationale.*

| Concern | Decision |
|---|---|
| Planner vs executor split | [responsibilities] |
| State transitions & stop conditions | [conditions] |
| Max-step limit & loop prevention | [limits] |
| Retry / recovery / tool-failure behavior | [behavior] |
| Escalation & human-approval checkpoints | [checkpoints] |
| Autonomous boundaries | [boundaries] |
| Irreversible-action controls | [controls] |

## Failure Taxonomy

| Failure Class | Detection | Mitigation | Observability Signal | Degradation | User-facing Response |
|---|---|---|---|---|---|
| [hallucination / retrieval miss / schema violation / unsafe output / tool misuse / authz violation / timeout / context truncation / planning divergence / looping / confidence miscalibration / provider outage] | [how detected] | [mitigation] | [signal] | [behavior] | [response] |

## Evaluation Strategy

| Capability | Offline Dataset | Online Metrics | Regression Gate | Owner | Edge/Adversarial Coverage | Drift Detection |
|---|---|---|---|---|---|---|
| [name] | [dataset] | [metrics] | [gating criterion] | [owner] | [coverage] | [method] |

Golden task suites: [location]. Replayable production traces: [policy]. No model/prompt/retrieval/tool change ships without passing regression gates.

## Guardrails & Trust Boundaries

| Boundary | Treatment | Sanitization / Validation |
|---|---|---|
| User input | [untrusted] | [rules] |
| Retrieved content | [untrusted] | [rules] |
| Tool-returned content | [untrusted] | [rules] |
| Model-generated reasoning | [treatment] | [rules] |
| External systems | [treatment] | [rules] |

Input filtering, output validation, refusal behavior, PII/redaction, prompt-injection posture, jailbreak-resistance assumptions: [decisions]. Retrieved or tool-returned text never redefines system behavior.

## Cost & Latency Budgets

| Capability | Token Budget | Request Budget | Latency Budget | Throughput / Concurrency | Retrieval Depth | Tool-call Ceiling | Fallback Threshold |
|---|---|---|---|---|---|---|---|
| [name] | [budget] | [budget] | [budget] | [expectation] | [depth] | [ceiling] | [threshold] |

Mapped to: model tier [tier], context size [size], caching [strategy], execution limits [limits].

## Model Routing Strategy

*Conditional — include when multiple models or providers exist; otherwise list under Omitted sections.*

| Concern | Decision |
|---|---|
| Routing criteria | [criteria] |
| Escalation thresholds | [thresholds] |
| Fallback providers | [providers] |
| Quality / cost / latency-aware routing | [policy] |
| Reliability failover | [behavior] |
| Offline vs online inference boundary | [boundary] |

## Observability & Operations

| Concern | Decision |
|---|---|
| Telemetry | [token usage, latency breakdown, retrieval hit quality, tool traces, refusal/fallback/retry rates, step counts, context size distribution, user-correction signals] |
| Logging & redaction policy | [policy] |
| Replay & trace retention | [policy] |
| Prompt & model versioning | [strategy] |
| Rollback strategy | [strategy] |
| Deployment promotion criteria | [criteria] |

## Implementation Handoffs

### implementations/ai/<vendor>

- [Capability-to-runtime mapping, contracts, schemas, expected behavior]

### backend-architecture

- [Orchestration ownership, request paths, transactional touchpoints]

### data-architecture

- [Retrieval corpora ownership, ingestion, indexing, embedding lifecycle]

### security

- [Trust boundaries, PII handling, prompt-injection posture, audit needs]

### operations

- [Telemetry, rollback, deployment promotion, runbook hooks]

## ADR Index

| ADR | Title | Status | Summary |
|---|---|---|---|
| NNNN | [title] | [proposed/accepted/...] | [summary] — links to `adrs/NNNN-<slug>.md` |

## Omitted sections

- [Conditional section name]: [one-line rationale for omission].

## Deferred Decisions

- [Decision, owner, deadline].
