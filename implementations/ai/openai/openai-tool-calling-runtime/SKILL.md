---
name: openai-tool-calling-runtime
description: Use when implementing OpenAI tool or function calling from an approved ai-architecture.md tool surface. Produces tool schemas, provider SDK wiring, execution adapters, authorization checks, idempotency rules, audit logging, tool failure handling, and tests for allowed, denied, failed, and retried tool calls. Do not use for AI architecture, generic chat, RAG, structured extraction without tools, or agent framework orchestration.
---

# OpenAI Tool Calling Runtime

## When to use

Invoke when `ai-architecture.md` defines a tool surface and OpenAI is the chosen
provider for tool-calling behavior.

Do not use when the tool surface has not been approved, when actions have
unresolved side effects, or when the user is asking for framework-level agent
orchestration.

## Inputs

Required:

- Approved `ai-architecture.md`.
- Tool names, schemas, side-effect classes, and authorization scopes.
- Target application language and framework.
- Audit and logging requirements.

Optional:

- Existing service interfaces for tool execution.
- Idempotency keys or correlation-id strategy.
- Rate limits and retry budgets.
- Human-in-the-loop requirements.

## Process

1. Load `ai-architecture.md` and identify each approved tool, schema, side-effect class, and authorization scope.
2. Refuse to implement tools with undefined side effects, missing auth scope, or missing idempotency behavior.
3. Generate provider-specific tool schema definitions.
4. Implement a tool execution adapter that validates input before invoking application code.
5. Enforce authorization, idempotency, rate limits, and audit logging before side effects.
6. Handle tool failure, timeout, denied authorization, and model retry behavior explicitly.
7. Add tests for allowed tool calls, denied tool calls, malformed arguments, tool failure, and retry exhaustion.
8. Emit operational notes covering audit trails, side effects, and safe rollback.

## Outputs

- OpenAI tool schema definitions.
- Tool execution adapter.
- Authorization and idempotency checks.
- Audit logging hooks.
- Tests for success, denial, malformed input, failure, and retry paths.
- Operational notes for tool side effects.

## Quality checks

- [ ] Every implemented tool appears in `ai-architecture.md`.
- [ ] Every tool has a schema, side-effect class, idempotency rule, and authorization scope.
- [ ] Tool input is validated before any side effect occurs.
- [ ] Tests cover allowed, denied, malformed, failed, and retried tool calls.
- [ ] Audit logs identify tool name, actor, correlation id, outcome, and side-effect class.

## References

- Upstream: [`architecture/ai-native-engineering`](../../../../architecture/ai-native-engineering/SKILL.md).
- Related: [`architecture/security`](../../../../architecture/security/SKILL.md).
