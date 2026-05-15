# Reliability Architecture Quality Rubric

Load this before emitting `reliability-architecture.md`. Revise until each check passes or the unresolved gap is explicitly documented.

## SLOs and error budgets

- [ ] Every user-facing journey or externally observable workflow names an SLI, SLO target, time window, and owner.
- [ ] SLOs map to user experience, not infrastructure vanity metrics.
- [ ] Every SLO has an error-budget policy with burn-rate thresholds and a defined operational action on burn.
- [ ] No SLO is tracked without an operational consequence.

## Dependencies and failure modes

- [ ] Every dependency in scope has a criticality class (critical / degradable / optional).
- [ ] Each dependency states outage impact, fallback posture, and detection signal; no hidden hard dependencies.
- [ ] Failure modes name a real component, a failure shape, the trigger, blast radius, detection, mitigation, and recovery.
- [ ] No generic failure-mode placeholders survive.

## Degradation and isolation

- [ ] Every critical journey defines graceful-degradation behavior for each degradable dependency, with a user-visible signal and recovery path.
- [ ] No critical workflow catastrophically fails from optional-dependency loss.
- [ ] Isolation strategy names the containment unit, what it contains, and trip/recovery thresholds where applicable.
- [ ] No shared dependency saturation across all tenants or workloads.

## Redundancy and disaster recovery

- [ ] Every redundancy decision names the failure mode it mitigates, the failover trigger, and the failover time.
- [ ] Consistency tradeoffs of active-active / replication are addressed, not ignored.
- [ ] DR plan states RTO and RPO per data class, restore tooling, rehearsal cadence, and last validated date.
- [ ] No backup strategy without restore validation; replicas are not treated as backups.

## Validation and release safety

- [ ] Chaos/game-day exercises name cadence and success criterion, or the section is omitted with rationale.
- [ ] Incident-posture inputs are defined, or omitted with rationale because `operations` owns the model.
- [ ] Release safety names the rollback path, deploy-gating signals, and automatic-rollback triggers.
- [ ] Release gating aligns with the `dev → staging → production` promotion flow ([deployment-standards](../../../standards/deployment-standards/README.md)).

## Linkage and decisions

- [ ] `reliability-architecture.md` conforms to [architecture-schema](../../../standards/architecture-schema/README.md): frontmatter complete, required sections present, conditional sections present or omitted with rationale under `## Omitted sections`.
- [ ] Frontmatter links the source `system-design.md`; bounded contexts, components, and data flow are consumed, not redefined.
- [ ] Every ADR candidate has Context, Decision, Consequences (including downsides), and Alternatives considered; ADRs share the system's monotonic numbering.
- [ ] Reliability tradeoffs with security, cost, or performance are surfaced explicitly.
- [ ] No telemetry-pipeline configuration, runbook prose, or vendor SDK code leaked into the architecture.
- [ ] At least one weak-reliability risk was surfaced, or the design's intentional simplicity was explained.

## Failure handling

If a check fails:

1. Identify the missing or weak reliability decision and the failure it leaves uncontained.
2. Ask the architecture or product owner for clarification if it cannot be inferred from `system-design.md` or the PRD.
3. Revise `reliability-architecture.md` or the relevant ADR.
4. Keep unresolved questions explicit as open decisions with owners; do not hide them as assumptions or claim untested recovery capability.
