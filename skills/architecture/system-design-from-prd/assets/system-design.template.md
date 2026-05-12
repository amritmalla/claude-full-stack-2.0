# System Design

> Section guide:
> - **Required:** Overview, Architecture Style, Bounded Contexts, Components, Data Flow, Failure Modes, ADR Index.
> - **Conditional:** Persistence Strategy (omit if a single store with an obvious mapping — fold one paragraph into Components instead), Security and Compliance (always include for external products and any system touching user data; may be omitted with one-line rationale for purely internal reference workloads), Operational Considerations (may merge into Failure Modes if the design has only one runtime topology and no durable operational decisions).
> - Note any omission under an "Omitted sections" heading at the bottom.

## Overview

[One-paragraph system summary. Include core workflows, primary actors, what the system optimizes for, and what it intentionally does not optimize for.]

## Architecture Style

[Chosen style, PRD-based justification, simpler alternatives considered, why alternatives were chosen or rejected, and operational tradeoffs accepted.]

## Bounded Contexts

[Table or structured list: Name, Responsibility, Owned Data, Dependencies, Upstream/Downstream Interactions.]

## Components

[One subsection per component: Responsibility, Interfaces, Dependencies, Inputs/Outputs, Persistence, Consistency, Scaling Expectations.]

## Data Flow

[Entry points, request paths, async boundaries, consistency model per entity, idempotency, retry behavior, and reconciliation needs.]

## Persistence Strategy

[Storage technology per bounded context, justification, write ownership, read patterns, caching behavior, migrations, and retention.]

## Failure Modes

[Table or structured list: Component, Failure Scenario, User Impact, Detection, Recovery, Degradation.]

## Security and Compliance

[Auth model, authorization boundaries, sensitive data, encryption, tenant isolation, abuse prevention, auditability, retention, deletion, and open compliance questions.]

## Operational Considerations

[Observability, deployment strategy, rollback capability, migrations, feature flags, incident response, secrets, backfills, and operational burden introduced.]

## ADR Index

[Table: ADR number, Title, Status, Summary.]
