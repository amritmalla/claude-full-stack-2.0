# claude-repo-mem tools by claude-full-stack-2.0 workflow phase

claude-repo-mem exposes 11 MCP tools. The right tool depends on what phase of the
workflow you're in. Use this table as default operating procedure — replace
`Grep`/`Read` with these tools whenever a match applies.

| Phase | Skill examples | Tool | When to call |
|---|---|---|---|
| Idea development | `idea-development` | — | The repo usually has nothing to index. Skip claude-repo-mem until system design produces artifacts. |
| System design | `system-design`, `backend-architecture`, `frontend-architecture`, `ai-native-engineering` | `recall(query, scopes=[<area>])` | Before writing an ADR, search for prior decisions in the same area. |
| System design | (any architecture skill) | `remember(fact, scope, kind="decision")` | After an ADR lands, store the rationale as a `decision` memory in scope `architecture/<area>`. |
| Implementation | `implementations/<category>/<ecosystem>/<skill>` | `recall(query)` | BEFORE any `Grep` — recall returns ranked, tier-aware results in one round-trip. |
| Implementation | (any impl skill) | `trace(seed_handle, depth=2)` | When you have a seed handle and need to see callers, callees, routes, hooks, or imports. Replaces N grep+read pairs. |
| Implementation | (any impl skill) | `expand(handle, tier)` | When you need one specific unit at a specific tier (T0 full source, T2 summary, T1 header). |
| Implementation | `quality-engineering`, `reliability` | `remember(fact, scope, kind="convention")` | When you discover a project-specific convention (testing style, naming, retry policy). |
| Implementation | `plan_task(intent)` | `plan_task` | Before any multi-step feature. Produces 2-6 independent sub-tasks with attached context bundles. |
| Implementation | `tasks()` | `tasks` | List in-flight or pending tasks; filter by scope/status. |
| Implementation | (end of session) | `handoff(task_id)` | Before context bloat or task switching. Snapshots intent + decisions + open questions + context handles to `.claude-repo-mem/handoffs/<id>.md`. |
| Resume work | (start of fresh session) | `resume(task_id, budget=4000)` | First call in any session continuing prior work. Returns snapshot markdown + budgeted hydrated bundle. |
| Operations | `operations` | `stats()` | Check index size, layer breakdown, T2 coverage, tool-call counters. |
| Operations | `operations` | `scopes()` | Inventory known scopes with unit counts. |
| Operations | (end of session, CLI) | `claude-repo-mem distill --yes` | Extract durable knowledge from the Claude Code transcript and write to `memory://` units. |

## Scope naming conventions

claude-repo-mem stores memory under `<repo>/.claude-repo-mem/memory/<scope>/<slug>.md`. Match scopes to your repo's logical structure:

- `architecture/<area>` — ADR-derived decisions. Examples: `architecture/auth`, `architecture/api-versioning`, `architecture/data-pipeline`.
- `tooling/<area>` — build / test / CI conventions. Examples: `tooling/testing`, `tooling/ci`, `tooling/lint`.
- `<repo-area>` — feature-area knowledge. Examples: `backend/auth`, `frontend/checkout`, `mobile/onboarding`.
- `ops/<area>` — operational runbooks. Examples: `ops/rollback`, `ops/incident-response`.

## Decision vs. fact vs. convention vs. preference

- **decision** — explicit "we chose X over Y because Z" with rationale.
- **fact** — something about the repo that's true and durable but not chosen (e.g., "the production DB is Postgres 15").
- **convention** — a recurring practice the team follows (e.g., "tests run with `pytest -q`").
- **preference** — a user/team preference that's reversible (e.g., "prefer tabs in Python files").

When in doubt, default to `decision` — they show up first in recall and are the most informative for future sessions.

## Budget hygiene

- `recall` default budget: 3000 tokens. Bump to 6000 for complex queries; rarely go above 8000.
- `trace` default budget: 8000 tokens (it hydrates connected nodes with full T0 source).
- `resume` default budget: 4000 tokens (matches "fresh session orientation").

Token usage is approximated as `len(text) // 4`. Overflow handles are always returned; if a critical handle was overflowed, call `expand(handle)` to pull it in explicitly.

## Verification rituals

After any non-trivial session, before closing it:

1. `claude-repo-mem stats` — confirm counters reflect activity.
2. `claude-repo-mem doctor` — confirm index health.
3. `handoff(active_task)` — snapshot for continuity.
4. (optional) `claude-repo-mem distill --yes` — extract any durable knowledge that wasn't `remember()`'d explicitly during the session.
