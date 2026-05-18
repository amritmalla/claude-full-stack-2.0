# Anthropic Evals and Observability Playbook

Load this when implementing any owned area of `anthropic-evals-and-observability` or checking the anti-pattern list. It expands the operating rules and process steps in `SKILL.md` with the Anthropic Messages API and Message Batches detail needed to produce a production-grade eval and observability surface.

## Why this workflow exists

Evals and observability done wrong let quality rot invisibly: a capability ships with no regression gate and a prompt edit silently halves accuracy three releases later; an eval set is built from raw production transcripts and leaks PII into the test repo; "cost" is reported as `input_tokens * rate` while 90% of those tokens were cache reads at a tenth of the price, so the cost dashboard is wrong by an order of magnitude and capacity planning is built on it; a thinking-budget bump triples output tokens and nobody notices because thinking tokens were never a distinct metric; an offline eval is rewritten as a "quick batch sanity check" with a looser pass bar and promotion is gated on the weaker number.

The goal is a versioned, redacted, numerically-gated eval surface and a telemetry surface that accounts for cache and thinking tokens honestly — not a notebook of ad-hoc spot checks and a cost number that is wrong on purpose.

## Behavioral rules in depth

### 1. Consume the regression bar; do not invent it

Success criteria, the regression threshold (as a number), the required metric set, and the cost/latency budget come from `ai-architecture.md` or a `quality-engineering` handoff. Alert ownership and runbook structure come from `operations`. Read them before building a dataset. A missing threshold, budget, or metric is an ADR candidate, not a number you choose.

### 2. The eval result schema is a contract surface

The result record — case id, input reference, expected/rubric, score, pass/fail, prompt version, model id, scoring method, grader version — is versioned and governed under api-standards. Downstream consumers (dashboards, gate logic, trend reports) depend on its shape. Do not add, rename, or retype a field without treating it as a breaking change.

### 3. No sensitive data in evals or telemetry

Eval datasets and traces carry no unredacted PII or secrets. Production user data is eval data only under an approved policy; otherwise use synthetic or sanitized cases. Telemetry records token counts, versions, and outcomes — never raw prompts or raw outputs unredacted. The Anthropic API key is deploy-time injected and never committed.

### 4. Scoring matches the claim

| Scoring method | When to use | Cost / caveat |
|---|---|---|
| Deterministic check (exact, schema, regex, numeric tolerance) | Contract is deterministic or schema-bound | Cheapest, strongest; preferred default |
| Model-graded (Claude judges output against a rubric) | Open-ended quality where deterministic checks cannot express the claim | Record the grader's own model id + prompt version; grader drift is a real regression source |
| Human review | High-stakes or rubric ambiguity the model grader cannot resolve | Documented rater criteria; slowest |

The method must justify the quality claim. Never use a permissive model grader to paper over a deterministic contract.

### 5. Versioning is mandatory metadata

Prompt version and model id are first-class fields on every runtime call and every eval case. An unversioned call cannot be attributed to a prompt change and is unobservable. Model id and prompt version are deploy-time configuration; the eval gate runs in CI/CD before promotion, not on a laptop.

### 6. Cost telemetry accounts for caching distinctly

The Anthropic `usage` object reports `input_tokens`, `output_tokens`, `cache_read_input_tokens`, and `cache_creation_input_tokens` separately. Record all four. Estimated cost applies three rates: uncached input, cache-write (creation, billed at a premium over base input), and cache-read (billed far below base input). Collapsing them into one blended input rate makes the cost dashboard wrong by the cache-hit ratio. A cache miss is a cost event surfaced on the cache-hit-ratio metric — never a correctness or eval failure.

### 7. Extended-thinking cost is a distinct dimension

When the capability uses extended thinking, thinking tokens are billed within `output_tokens`. Surface them as a separate telemetry dimension (derived from the thinking block, or from the configured thinking budget) so a thinking-budget regression — a prompt or config change that triples thinking — is visible on its own series, not buried in total output tokens. If extended thinking is not used, state N/A; do not leave it unaddressed.

### 8. Message Batches for offline eval runs

Route eval runs through the Message Batches API when latency is not required and the dataset is large enough that synchronous fan-out is wasteful or rate-limited. Batch jobs are submitted as a set of requests, polled to completion, and their results read back; each result still carries its own `usage`, so cache and token accounting is identical to synchronous runs. Batch results feed the **same scoring harness and the same regression gate** as synchronous runs. A batch run is a routing choice for cost and throughput, never a reason to relax the pass bar. Batch latency (minutes to hours) means batch is for pre-promotion regression and bulk backfill scoring, not for inline production gating.

### 9. Alerts are runbook inputs

Every alert names an owner, a condition (the metric and threshold), and a first response action. These are handed to `operations` as runbook content. Dashboards expose the AI RED-equivalent (latency, tokens, cost, error/fallback rate) plus cache-hit ratio and current regression-gate status.

## Step detail

**Step 1 — Load the contract.** Open `ai-architecture.md` and any `quality-engineering` / `operations` handoff. Extract success criteria, the numeric regression threshold, required metrics, cost/latency budget, alert ownership. Missing any → ADR candidate before building.

**Step 2 — Verify completeness.** Confirm the threshold is an explicit number, the required metric set is named, and alert ownership is defined. A silent gap becomes an invented gate later.

**Step 3 — Define the dataset.** Specify case id, input reference, expected output or rubric, scoring method, sensitive-data handling, and a versioned result schema. Sanitize or synthesize cases unless an approved policy permits real user data.

**Step 4 — Build the scoring harness.** Implement deterministic checks where the contract is deterministic; model-graded or human review only where justified, with documented rater criteria and recorded grader version.

**Step 5 — Define the gate.** Express regression thresholds and the promotion gate as explicit numbers tied to the architecture's success criteria. Wire the gate into CI/CD.

**Step 6 — Decide routing.** Small/latency-bound runs go synchronous; large offline runs and bulk scoring go through the Message Batches API. Wire batch results into the same harness and gate. Record the routing decision and its rationale.

**Step 7 — Add versioning metadata.** Attach prompt version and model id to runtime calls and every eval case as deploy-time config.

**Step 8 — Add metrics.** Emit latency, input/output tokens, `cache_read_input_tokens`, `cache_creation_input_tokens`, estimated cost (three distinct rates), thinking tokens where applicable, validation failures, fallback/error rate.

**Step 9 — Add tracing and logs.** Propagate trace context through the call; structure logs with redaction. No raw prompt/output, secret, or PII.

**Step 10 — Dashboard and runbook.** Produce owner / condition / first-response notes; expose cache-hit ratio and regression-gate status on the dashboard.

**Step 11 — ADR candidates.** Write any unresolved threshold/budget/metric/ownership gap as an ADR candidate against the architecture. Do not silently fill it.

## Anti-patterns to detect

Call these out explicitly when found:

- A shipping capability with no regression gate, or a gate with no number behind it
- Regression threshold, cost budget, or required metric invented instead of taken from the architecture / quality-engineering handoff
- Eval result schema changed in shape without treating it as a contract break
- Raw production transcripts used as eval data without an approved policy; PII or secrets in the eval repo or traces
- Permissive model grader masking a deterministic contract; grader's own version unrecorded
- Runtime call or eval case with no prompt version / model id
- Cost computed with a single blended input rate, ignoring `cache_read_input_tokens` / `cache_creation_input_tokens`
- Cache miss treated as a correctness or eval failure
- Extended thinking used but thinking tokens not surfaced as a distinct dimension
- Offline eval run through Message Batches held to a looser pass bar than synchronous runs
- Batch used for inline production gating despite its minutes-to-hours latency
- Alert with no named owner, condition, or first response action
- Model id or prompt version hardcoded instead of deploy-time config; eval gate run by hand instead of in CI/CD
