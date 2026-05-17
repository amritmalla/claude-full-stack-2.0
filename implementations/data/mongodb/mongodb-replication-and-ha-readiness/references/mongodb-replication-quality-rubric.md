# MongoDB Replication and HA Readiness Quality Rubric

Load this before declaring the topology complete. Revise until each check passes or the unresolved gap is explicitly documented in `replication-ha.md`.

## Context & boundary

- [ ] Availability targets and RPO/RTO are sourced from `architecture/reliability`; consistency posture from `data-architecture.md` (or an ADR candidate is raised).
- [ ] The per-operation read/write concerns are consumed from `mongodb-data-model-and-migration` — not redefined here.
- [ ] No host/VM/cluster provisioning is done here (infrastructure layer).

## Member topology & elections

- [ ] Voting-member count is odd; elections always resolve.
- [ ] No single failure domain (node/AZ/region per tier) removes the voting majority.
- [ ] Member priorities reflect intended primary placement.
- [ ] No arbiter for tier-0; any arbiter elsewhere has an ADR documenting the `w:"majority"` durability trade-off.

## Concern survivability

- [ ] The declared write concern is still honored after the planned failure (node/AZ/region per tier).
- [ ] The declared read concern is still honored after the planned failure.
- [ ] Any gap is a finding handed to `mongodb-data-model-and-migration` or a raised ADR candidate.

## Read preference & write concern

- [ ] Read preference is set per operation class; `primary` for read-after-write paths.
- [ ] Every secondary-read path names a staleness tolerance and sets `maxStalenessSeconds`.
- [ ] State-mutating writes use `w: "majority"` (+ `j: true` where loss of the last write is unacceptable).
- [ ] Any relaxed write concern names the exact data and the accepted loss window.

## Oplog, multi-region & change streams

- [ ] The oplog window exceeds the worst recovery/lag/maintenance interval; measured-vs-required is stated.
- [ ] Multi-region placement (if in scope) states the cross-region majority latency cost.
- [ ] Region-loss data survivability under the write concern is stated.
- [ ] Change-stream resumability (resume tokens) and failover behavior are specified where consumers exist.

## Verification & handoffs

- [ ] Failover was rehearsed (primary stepdown/kill): election timing vs RTO recorded, concerns still honored, no acknowledged-write loss — or the gap is documented.
- [ ] Internal member auth (keyfile/x.509) and member TLS are required and named to `mongodb-security-and-data-access-hardening`.
- [ ] Modeling, query tuning, backup/PITR, security/auth, and host provisioning are named handoffs — none implemented here.

## Standards conformance

- [ ] [observability-standards](../../../../../standards/observability-standards/README.md): replication lag, election/stepdown events, oplog window, member health exposed.
- [ ] [deployment-standards](../../../../../standards/deployment-standards/README.md): topology reproducible from config; member changes rolling.
- [ ] [architecture-schema](../../../../../standards/architecture-schema/README.md): tier drove member count, region spread, arbiter prohibition.
- [ ] [naming-conventions](../../../../../standards/naming-conventions/README.md): replica-set and member naming.
- [ ] [security-standards](../../../../../standards/security-standards/README.md): internal auth and member TLS required (mechanism named to the security skill).

## Failure handling

If a check fails:

1. Identify the unsurvivable concern, the deadlock-prone election, or the undersized oplog.
2. Ask the user for clarification if the decision cannot be inferred from `architecture/reliability` or `data-architecture.md`.
3. Revise the topology, re-rehearse the primary failover and re-capture timings.
4. Keep any unresolved gap explicit in `replication-ha.md` — do not hide it as an assumption.
