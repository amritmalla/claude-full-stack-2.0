---
name: spring-kafka-event-integration
description: Use when adding, reviewing, or hardening Kafka producers, consumers, or event-driven flows in a Spring Boot service after backend architecture has defined the event contracts. Produces Spring Kafka producer and consumer configuration, serialization and schema-registry posture, idempotency and exactly-once delivery decisions, retry and dead-letter topology, transactional outbox wiring, consumer group and rebalance behavior, error and poison-pill handling, observability for event flows, and integration test scaffolding with embedded or Testcontainers Kafka. Do not use for event contract design, broker provisioning, non-Kafka brokers (RabbitMQ, Pulsar, SQS), or general async/scheduled work; use backend-architecture, infrastructure-platform, or spring-boot-service-scaffold instead.
---

# Spring Kafka Event Integration

## When to use

Invoke when a Spring Boot service must produce or consume Kafka events and the event contracts (topic names, message shape, idempotency keys, ordering expectations, delivery semantics) have been decided by `backend-architecture`. Use it for new producers and consumers, for reviewing an existing Kafka integration before production, or for adding the transactional outbox pattern.

Do not use for designing the event contract itself (use `backend-architecture`), for choosing the messaging substrate (use `backend-architecture` or `system-design`), for non-Kafka brokers, for broker or cluster provisioning (use `infrastructure-platform` and `implementations/infrastructure/*`), for in-process async (`@Async`, scheduling), or for the initial service scaffold (use `spring-boot-service-scaffold`).

## Inputs

Required:

- Spring Boot service source tree (or scaffold output) targeting Kafka.
- Approved `backend-architecture.md` with event contracts: topic names, message shape, idempotency keys, ordering rule, delivery semantics, retry expectation, and DLQ policy.
- Broker connectivity details (bootstrap servers, security protocol) or the assumption that those land via configuration.

Optional:

- Schema registry posture (Confluent Schema Registry, Apicurio, none) and serialization choice (Avro, Protobuf, JSON Schema).
- Existing Kafka topology: partition counts, replication factor, retention.
- Tenant or PII constraints affecting key design or payload redaction.
- Transactional source-of-truth requirements (outbox vs direct produce).
- Throughput and latency targets per topic.

## Operating rules

- Preserve the event contract. Do not silently change topic names, key strategy, message shape, ordering rule, or delivery semantics. If the contract is missing a needed decision (idempotency key, retry budget, DLQ behavior), raise it as an ADR candidate against `backend-architecture`.
- Choose delivery semantics explicitly per flow: at-most-once, at-least-once, or effectively-once (idempotent producer + transactional consumer + idempotent sink). State the trade-off.
- Idempotency is a property of the consumer or the sink, not the broker. Every at-least-once consumer needs an idempotency key and a deduplication mechanism.
- Producers that mutate state must use the transactional outbox pattern unless an ADR justifies direct produce. Dual-write to DB and Kafka without outbox is a defect.
- Serialization is a contract. If a schema registry is in use, prefer Avro or Protobuf with subject-naming and compatibility rules; if not, JSON with explicit schema validation.
- Consumers handle poison pills explicitly: classify retryable vs non-retryable errors, define the retry topology (in-memory retries, retry topics, blocking vs non-blocking), and define the DLQ shape.
- Consumer group, partition assignment, and concurrency are tuned to the ordering rule. Per-key ordering requires single-consumer-per-partition discipline; global ordering is rarely justified.
- Manual offset acknowledgement is the default for at-least-once flows. Auto-commit hides bugs.
- Observability is mandatory: producer success/failure rate, consumer lag, retry counts, DLQ rate, end-to-end latency, and trace propagation across the broker.
- A Kafka integration that has no integration test against an embedded or Testcontainers broker is not done.

## Output contract

The integration MUST conform to:

- [api-standards](../../../../standards/api-standards/README.md) where event payloads are part of the external contract surface (versioning, breaking-change policy, idempotency-key shape).
- [security-standards](../../../../standards/security-standards/README.md) — SASL/SSL configuration, secret handling for broker credentials, no PII logged in payloads or keys without redaction, ACL or topic-level authorization respected.
- [observability-standards](../../../../standards/observability-standards/README.md) — Kafka-specific Micrometer metrics, consumer-lag exposure, trace propagation via headers, structured logs with correlation IDs on consume and produce paths.
- [deployment-standards](../../../../standards/deployment-standards/README.md) — broker connection details and credentials injected at deploy time, never baked into the image.
- [naming-conventions](../../../../standards/naming-conventions/README.md) — topic names, consumer group IDs, and DLQ topics follow the project's naming rules.

Upstream contract: `backend-architecture.md` is the source of truth for topic names, message shape, idempotency key, ordering rule, delivery semantics, retry budget, and DLQ policy. If the contract is silent on any of these, this skill pauses and raises an ADR candidate rather than inventing the decision.

## Process

1. Read `backend-architecture.md` and extract the event contract per flow: topic, key strategy, message shape, ordering rule, delivery semantics, idempotency key, retry budget, DLQ policy, retention assumption.
2. Identify each producer and consumer surface in the service. Classify each as: mutating producer (needs outbox), pure event emission, idempotent consumer, non-idempotent consumer-with-dedupe, or stream processor.
3. Choose serialization and schema-registry posture. If Avro/Protobuf with a registry, decide subject-naming strategy and compatibility mode. If JSON, decide schema validation surface.
4. Configure the producer: `acks=all`, `enable.idempotence=true`, retries and delivery timeout aligned with the contract's retry budget, compression, batching, and transactional ID when transactional.
5. For mutating producers, wire the transactional outbox: outbox table owned by the service, polling or change-data-capture mechanism, atomic write with the domain change, and the producer reading from outbox. Hand off outbox table DDL to `postgres-schema-and-migration`.
6. Configure the consumer container: `enable.auto.commit=false`, manual ack, concurrency aligned with partition count and ordering rule, max-poll-interval and session-timeout aligned with processing time, and `isolation.level=read_committed` when consuming transactional producers.
7. Define error handling: classify retryable vs non-retryable exceptions, configure the error handler (`DefaultErrorHandler` with `DeadLetterPublishingRecoverer`, or non-blocking retry topics with `RetryTopicConfigurer`), and define the DLQ topic shape and headers.
8. Implement consumer-side idempotency for at-least-once flows: dedupe table or distributed cache keyed by the idempotency key, with a documented retention window aligned to retry budget and consumer lag tolerance.
9. Generate observability wiring: producer metrics, consumer lag exposure, retry and DLQ counters, structured logs with correlation IDs, and trace propagation through Kafka headers (`b3` or `traceparent`).
10. Generate integration tests using `spring-kafka-test` `@EmbeddedKafka` or Testcontainers Kafka. Cover at minimum: produce-and-consume happy path, retry-then-DLQ for a non-retryable error, idempotency on duplicate delivery, and ordering preservation per key where required.
11. Define operational runbooks inputs for `operations`: consumer-lag thresholds, DLQ alerting threshold, replay procedure from DLQ, and offset-reset procedure.
12. Validate against [observability-standards](../../../../standards/observability-standards/README.md), [security-standards](../../../../standards/security-standards/README.md), and the contract in `backend-architecture.md`. Fix any divergence before declaring done.

## Outputs

Required:

- Spring Kafka producer and consumer configuration (Java/Kotlin `@Configuration`, `application*.yml` keys, or both).
- Error handler and DLQ wiring per consumer flow.
- Idempotency mechanism per at-least-once consumer.
- Observability wiring: metrics, structured logs, and trace propagation across producer and consumer paths.
- Integration tests against embedded or Testcontainers Kafka.
- Operational notes covering consumer-lag thresholds, DLQ replay, and offset-reset procedure.

Optional, when applicable:

- Transactional outbox wiring (table, polling or CDC component, transactional producer).
- Schema registry client configuration and subject-naming rules.
- Retry-topic topology generated via `RetryTopicConfigurer`.
- ADR drafts for delivery-semantics, outbox-vs-direct, or schema-registry decisions.

Output rules:

- Topic names, group IDs, and DLQ topics follow project naming conventions.
- No broker credentials, secrets, or environment-specific bootstrap servers committed to source.
- Auto-commit must not appear in any consumer configuration without an ADR.
- Every retry and DLQ decision matches the retry budget and DLQ policy stated in `backend-architecture.md`.

## Quality checks

- [ ] Every producer and consumer in the service traces back to a flow in `backend-architecture.md`.
- [ ] Delivery semantics are explicit per flow and match the contract.
- [ ] Mutating producers use the transactional outbox unless an ADR justifies direct produce.
- [ ] Producer config sets `acks=all` and `enable.idempotence=true`; transactional producers set a stable `transactional.id`.
- [ ] Consumer config disables auto-commit and configures concurrency consistent with the ordering rule.
- [ ] Every at-least-once consumer has an idempotency mechanism keyed by the contract's idempotency key.
- [ ] Error handling classifies retryable vs non-retryable failures and routes non-retryables to a named DLQ topic with documented headers.
- [ ] Integration tests cover happy path, retry-then-DLQ, idempotent duplicate delivery, and per-key ordering where required.
- [ ] Observability emits producer success/failure, consumer lag, retry count, DLQ rate, and propagates trace context through Kafka headers.
- [ ] No broker credentials or environment-specific bootstrap servers are committed.

## References

- Upstream: [`architecture/backend-architecture`](../../../../architecture/backend-architecture/SKILL.md) — event contracts and delivery semantics.
- Related implementation skills: [`spring-boot-service-scaffold`](../spring-boot-service-scaffold/SKILL.md) (baseline this skill builds on), [`observability-readiness`](../observability-readiness/SKILL.md) (extends observability for event flows), [`postgres-schema-and-migration`](../../../data/postgres/postgres-schema-and-migration/SKILL.md) (outbox table DDL).
- Compatible patterns: [`event-driven`](../../../../patterns/event-driven/README.md), [`cqrs`](../../../../patterns/cqrs/README.md).
