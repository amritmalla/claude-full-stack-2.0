# MongoDB Replication and HA Readiness Playbook

Load this when designing any owned area of `mongodb-replication-and-ha-readiness` or checking the anti-pattern list. It expands the operating rules and process steps in `SKILL.md` with the detail needed to produce a survivable replica-set topology.

## Why this workflow exists

Replication defects are discovered during the outage they were supposed to prevent. An even voting count deadlocks the election when one member is lost. An arbiter plus `w: "majority"` acknowledges writes that are not actually durable, so the failover loses committed data. An oplog sized for a quiet day rolls over while a secondary is catching up, forcing a full multi-hour resync at the worst moment. A `secondaryPreferred` read on a path that just wrote returns stale data and the bug looks impossible. A cross-region `w: "majority"` quietly adds inter-region latency to every write. None of this fails a functional test — it fails when a node, an AZ, or a region goes away.

The goal is a topology that keeps the declared write/read concerns honored through the planned failure, with elections that always resolve and an oplog that outlasts recovery — consuming the reliability targets instead of inventing them.

## Behavioral rules in depth

### 1. The topology must survive the concerns the model declared

`mongodb-data-model-and-migration` declared, per operation, a write concern and read concern. This skill's primary job: prove the member layout still honors them after the planned failure (one node for tier-2, one AZ for tier-1, one region for tier-0, per the reliability tier). If `w: "majority"` cannot be met after losing an AZ, the topology is wrong — or the concern is, which is a finding handed back.

### 2. Consume reliability and data-architecture; do not invent it

Availability targets, RPO/RTO, and consistency posture are upstream. The member count and region spread *implement* them. If a needed decision is missing, raise an ADR candidate.

### 3. Design the topology, not the model

Per-operation concern is the model skill's ownership. A concern that is too weak for the durability requirement is reported as a finding, not silently "fixed" here — that keeps one owner for the durability contract.

### 4. Odd votes; elections must always resolve

A replica set elects a primary by majority of voting members. An even count can split; a partition-prone layout can leave no majority. Keep voting members odd, place them so a single failure domain cannot remove the majority, and set priorities so the intended member becomes primary.

### 5. Arbiters are a trap with `w: "majority"`

An arbiter votes but holds no data. With a 2-data + 1-arbiter set and `w: "majority"`, losing a data member means a write "acknowledged by majority" exists on only one data node — a subsequent failure loses it. Arbiters are prohibited for tier-0 and require an explicit ADR (documenting the durability trade-off) anywhere else.

### 6. Read preference is a consistency decision

| Preference | Use when |
|---|---|
| `primary` | Read-after-write; any consistency-sensitive read |
| `primaryPreferred` | Prefer fresh, tolerate brief primary loss |
| `secondaryPreferred` / `nearest` | Staleness explicitly acceptable; set `maxStalenessSeconds` |

Every secondary-read path states its staleness tolerance. A silent `secondaryPreferred` on a read-after-write path is a defect.

### 7. Write concern is sized to durability

State mutations default to `w: "majority"`; add `j: true` where losing the last write is unacceptable (journaled to disk, not just acknowledged in memory). A relaxed concern (`w: 1`, `w: 0`) names exactly the data it applies to and the accepted loss window — it is a deliberate, documented trade.

### 8. The oplog must outlast the worst recovery

The oplog is a capped collection; a secondary that falls behind the oplog window cannot catch up incrementally and needs a full resync. Size the window to exceed the worst of: secondary recovery time, maintenance window, network-partition duration, and backup-induced lag. State measured window vs requirement — "it's the default" is not sizing.

### 9. Multi-region is explicit about latency and loss

Cross-region `w: "majority"` pays inter-region round-trip on every write. State that cost. State whether losing a whole region loses data given the write concern and member placement. Tier-0 cross-region posture is a deliberate, documented choice.

### 10. Change streams depend on the oplog and survive failover only if designed

Consumers must persist resume tokens and handle `ChangeStreamHistoryLost` (oplog rolled past the token). The oplog window must cover the maximum consumer downtime. Failover behavior for in-flight streams is specified, not assumed.

### 11. Internal member auth is required — named to security

Members authenticate to each other via keyfile or x.509, and member traffic is TLS. This skill *requires* it and names the mechanism handoff to `mongodb-security-and-data-access-hardening`; an unauthenticated replica set is rejected.

### 12. An un-rehearsed failover is not HA

Step down or kill the primary on a representative deployment. Confirm: a timely election (vs the RTO), the declared concerns still honored, no acknowledged-write loss. Documentation without a rehearsal is a hypothesis.

## Step detail

**Step 1 — Gather context.** Load `architecture/reliability` (availability, RPO/RTO) and `data-architecture.md` (consistency, region intent). Pull per-operation concerns from `mongodb-data-model-and-migration`. Resolve tier from `architecture-schema`. Raise an ADR candidate for any missing decision.

**Step 2 — Member topology.** Odd voting count; data members across the required AZ/region spread; priorities for primary placement; hidden/delayed members if the posture calls for them.

**Step 3 — Concern survivability.** Prove declared `w`/`readConcern` holds through node/AZ/region loss per tier; gap → finding or ADR.

**Step 4 — Arbiter posture.** Prohibit for tier-0; ADR-only elsewhere with the `w:"majority"` trade-off documented.

**Step 5 — Read preference.** Per operation class; `maxStalenessSeconds` on every secondary path.

**Step 6 — Write concern.** `w:"majority"` (+`j:true` where required) for mutations; relaxed concerns name data + loss window.

**Step 7 — Oplog sizing.** Worst recovery/lag/maintenance interval vs configured window; state measured-vs-required.

**Step 8 — Multi-region.** Roles per region; cross-region majority latency cost; region-loss survivability.

**Step 9 — Change streams.** Resume-token handling; oplog window vs max consumer downtime; failover behavior.

**Step 10 — Rehearse failover.** Stepdown/kill primary; election timing vs RTO; concerns honored; no acknowledged-write loss. Document any check that cannot run.

**Step 11 — Emit & validate.** `replication-ha.md` (member/priority/region map, concern-survivability matrix, read-preference table, oplog sizing, change-stream posture, rehearsed-failover results), handoff list. Validate against observability-, deployment-, security-standards, architecture-schema, naming-conventions.

## Anti-patterns to detect

Call these out explicitly when found:

- A topology that cannot honor the model's declared `w`/`readConcern` after the planned failure
- Even voting-member count, or a layout where one failure domain removes the majority
- An arbiter on tier-0, or anywhere with `w:"majority"` and no ADR documenting the trade-off
- `secondaryPreferred`/`nearest` on a read-after-write path; no `maxStalenessSeconds`
- State mutations on `w: 1`/`w: 0` with no named data scope and accepted loss window
- Oplog left at default with no measured-vs-required window
- Cross-region majority with the write-latency cost unstated, or unstated region-loss data risk
- Change-stream consumers with no resume-token handling or oplog-window guarantee
- Unauthenticated/non-TLS member traffic (internal auth not named to security)
- Model/concern *redesign* done here instead of handed to `mongodb-data-model-and-migration`
- HA declared done with no rehearsed primary failover
- Host/VM/cluster provisioning authored here (infrastructure layer)
