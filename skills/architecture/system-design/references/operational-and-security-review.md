# Operational and Security Review

Use this reference when evaluating failure behavior, operational maturity, security, compliance, and domain-specific system risks.

## Failure modes

For every major component, identify realistic failures:

- dependency outage,
- queue backlog,
- rate limiting,
- partial writes,
- cache inconsistency,
- worker crash,
- stale reads,
- model/provider failure,
- timeout cascade,
- webhook retry storm,
- data migration failure.

For each failure mode, define:

- What fails,
- User impact,
- Detection mechanism,
- Recovery behavior,
- Graceful degradation strategy.

The design must describe degraded behavior, not only ideal-path behavior.

## Operational maturity

Cover what the architecture requires from the team:

- observability,
- structured logs,
- metrics,
- tracing,
- alerting,
- dashboards,
- deployment strategy,
- rollback capability,
- incident response,
- audit logging,
- access control operations,
- secrets management,
- migration strategy,
- feature flags,
- data backfills.

If the design introduces operational burden, explain why it is necessary and what the minimum viable operating model is.

## Security and compliance

Document:

- authentication model,
- authorization boundaries,
- sensitive data handling,
- encryption expectations,
- tenant isolation,
- abuse prevention,
- rate limiting,
- auditability,
- retention and deletion,
- regulatory exposure,
- open compliance questions.

Do not hand-wave security. If the PRD is missing security or compliance requirements that shape architecture, ask for clarification or document an explicit assumption.

## Conditional checks

AI systems:

- model/provider failure path,
- hallucination impact,
- human review for high-impact outputs,
- prompt/data leakage risks,
- evaluation and monitoring approach,
- data retention by model providers.

B2B SaaS:

- tenant isolation,
- role-based access control,
- audit logs,
- billing boundaries,
- admin operations,
- data export and deletion.

Event-driven systems:

- idempotent consumers,
- retry policy,
- dead-letter handling,
- event ordering assumptions,
- replay behavior,
- schema evolution.

Internal tools:

- source-of-truth ownership,
- permission model,
- auditability,
- rollout authority,
- manual override path,
- operational support owner.
