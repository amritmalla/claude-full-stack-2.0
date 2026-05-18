# Anthropic Evals and Observability — Integration Reference

Use this as the canonical shape when generating an Anthropic eval and observability surface. Placeholder tokens use `<kebab-case>` or `<PascalCase>`. Language is illustrative (Python SDK); port to the target stack. Every value marked `# from ai-architecture.md` is a contract input, not a default.

## Integration header (record the decision)

```
Capability:         <capability-name>             # from ai-architecture.md
Success criteria:   <measurable claim>            # from ai-architecture.md
Regression gate:    <metric> >= <number>          # from ai-architecture.md / quality-engineering
Required metrics:   <named metric set>            # from ai-architecture.md
Cost budget:        <max cost / 1k calls>         # from ai-architecture.md
Eval-run routing:   synchronous | message-batches # chosen; reason below
Reason:             <why this routing for this dataset>
Extended thinking:  used | N/A                    # from ai-architecture.md
Alert ownership:    <owner / escalation>          # from operations
```

## Eval dataset structure

```
case_id          <stable id>
input_ref        <pointer to sanitized/synthetic input — not raw PII>
expected         <expected output | rubric ref>
scoring_method   deterministic | model-graded | human
sensitivity      <none | redacted | approved-real-data-policy-ref>
```

## Versioned eval result schema (contract surface — api-standards)

```json
{
  "schema_version": "<semver>",
  "case_id": "<id>",
  "prompt_version": "<from deploy-time config>",
  "model_id": "<from deploy-time config>",
  "scoring_method": "deterministic | model-graded | human",
  "grader_model_id": "<set only when model-graded>",
  "grader_prompt_version": "<set only when model-graded>",
  "score": 0.0,
  "passed": true
}
```

## Scoring harness (method matches the claim)

```python
def score(case, output):
    if case.scoring_method == "deterministic":
        return deterministic_check(case.expected, output)     # exact/schema/numeric
    if case.scoring_method == "model-graded":
        # grader's own model_id + prompt_version recorded on the result
        return grade_with_claude(case.rubric, output)
    return queue_for_human_review(case, output)               # documented rater criteria
```

## Synchronous vs. Message Batches routing

```python
# Small / latency-bound regression run
resp = client.messages.create(model="<model-id>", max_tokens=<from-contract>,
                               messages=[{"role": "user", "content": case.input}])

# Large offline regression / bulk backfill — same gate, same harness, lower cost
batch = client.messages.batches.create(requests=[
    {"custom_id": c.case_id,
     "params": {"model": "<model-id>", "max_tokens": <from-contract>,
                "messages": [{"role": "user", "content": c.input}]}}
    for c in dataset
])
# poll batch until ended; read results; each result carries its own usage.
# Feed results into the SAME score() and the SAME regression gate.
```

Routing rule: batch latency is minutes-to-hours — use it for pre-promotion regression and bulk scoring, never for inline production gating. A batch run is held to the identical pass bar as a synchronous run.

## Cost accounting (cache rates applied distinctly)

```python
u = resp.usage
cost = (u.input_tokens                * RATE_INPUT
        + u.cache_creation_input_tokens * RATE_CACHE_WRITE   # premium over base input
        + u.cache_read_input_tokens     * RATE_CACHE_READ    # far below base input
        + u.output_tokens               * RATE_OUTPUT)
# NEVER: cost = (u.input_tokens + u.cache_read_input_tokens) * RATE_INPUT
```

## Telemetry fields (emit every call; redact payloads)

| Field | Source |
|---|---|
| `model_id`, `prompt_version` | deploy-time config |
| `latency_ms` | measured |
| `input_tokens`, `output_tokens` | `resp.usage` |
| `cache_read_tokens` | `resp.usage.cache_read_input_tokens` |
| `cache_write_tokens` | `resp.usage.cache_creation_input_tokens` |
| `thinking_tokens` | thinking block / configured budget (or N/A) |
| `estimated_cost` | three distinct rates above |
| `cache_hit_ratio` | cache_read / (cache_read + uncached input) |
| `fallback_rate`, `error_rate` | runtime outcome |
| `regression_gate` | pass / fail vs. `<number>` |

Never log: raw prompt, raw output, secrets, PII (unredacted).

## Dashboard and runbook notes

| Panel | Content |
|---|---|
| AI RED | latency, tokens, estimated cost, error/fallback rate |
| Cache | cache-hit ratio, cache-write vs. cache-read token split |
| Quality gate | current regression-gate status per capability |
| Alert | `<owner>` · `<condition: metric op number>` · `<first response action>` |

## Configuration (deploy-time, never committed)

```
ANTHROPIC_API_KEY        # secret store / env injection
MODEL_ID                 # e.g. claude-... — config, not hardcoded
PROMPT_VERSION           # config; first-class metadata on every call + eval case
REGRESSION_THRESHOLD     # from ai-architecture.md / quality-engineering
EVAL_RUN_ROUTING         # synchronous | message-batches
TOKEN_RATES              # input / cache-write / cache-read / output, applied distinctly
```
