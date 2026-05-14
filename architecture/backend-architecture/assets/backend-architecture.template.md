# Backend Architecture: [Service or Context Name]

## Status

[draft | review | approved]

## Source Inputs

- System design: [path or title]
- ADRs: [list]
- PRD sections: [scope, non-goals, success metrics, acceptance criteria]

## Scope

### Owns

- [Backend responsibility owned here]

### Does Not Own

- [Responsibility explicitly outside this boundary]

### Open Decisions

- [Decision requiring stakeholder or architecture review]

## Backend Boundary

| Area | Decision |
|---|---|
| Service/module/context | [name] |
| Primary consumers | [consumers] |
| Upstream dependencies | [dependencies] |
| Downstream dependencies | [dependencies] |
| Runtime expectations | [latency, throughput, availability, cost] |

## Domain Model

### Core Concepts

| Concept | Responsibility | Key Invariants |
|---|---|---|
| [Concept] | [What it represents] | [Rules that must always hold] |

### Commands

| Command | Actor | Preconditions | Result |
|---|---|---|---|
| [Command] | [Actor/system] | [Required state] | [State change/event] |

### Queries

| Query | Consumer | Freshness | Notes |
|---|---|---|---|
| [Query] | [Consumer] | [Strong/eventual/cache] | [Notes] |

### Lifecycle States

| State | Meaning | Allowed Transitions |
|---|---|---|
| [State] | [Meaning] | [Next states] |

## Interface Strategy

| Interaction | Style | Consumer | Ownership | Compatibility |
|---|---|---|---|---|
| [Interaction] | [REST/event/job/etc.] | [Consumer] | [Producer/consumer] | [Compatibility rule] |

## Execution Flows

### [Flow Name]

1. [Step]
2. [Step]
3. [Step]

Failure handling:

- [Failure mode and behavior]

## Transactions and Consistency

| Workflow | Transaction Boundary | Consistency Model | Concurrency Control |
|---|---|---|---|
| [Workflow] | [Boundary] | [Strong/eventual/saga/etc.] | [Control] |

## Idempotency, Retries, and Timeouts

| Operation | Idempotency Key | Retry Behavior | Timeout Budget | Duplicate Handling |
|---|---|---|---|---|
| [Operation] | [Key] | [Retry rule] | [Budget] | [Behavior] |

## Data Ownership Expectations

| Data Area | Owner | Record of Truth | Retention/Migration Notes |
|---|---|---|---|
| [Data] | [Owner] | [System] | [Notes] |

## Security Touchpoints

| Surface | Authentication | Authorization | Sensitive Data | Audit Event |
|---|---|---|---|---|
| [Surface] | [Authn] | [Authz] | [Data] | [Event] |

## Operations

| Concern | Decision |
|---|---|
| Logs | [Structured log events] |
| Metrics | [Counters/gauges/histograms] |
| Traces | [Span boundaries] |
| Health/readiness | [Signals] |
| SLO-sensitive paths | [Paths] |
| Backpressure | [Behavior] |
| Runbook hooks | [Hooks] |

## Implementation Handoff

### Backend Scaffold

- [Controllers, modules, package boundaries, generated code expectations]

### Data Implementation

- [Schema and migration handoff notes]

### Security Review

- [Auth, authorization, secrets, tenant isolation notes]

### Testing

- [Contract, integration, E2E, and fixture expectations]

### Observability and Reliability

- [SLI/SLO, alert, runbook, and failure-mode notes]

## Deferred Decisions

- [Decision, owner, deadline]
