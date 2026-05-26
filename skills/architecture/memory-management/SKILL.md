---
name: memory-management
description: Use when a project built with claude-full-stack-2.0 needs durable cross-session memory, hierarchical retrieval over a repo's code/docs/decisions, or task handoff between Claude sessions. Sets up the claude-mem MCP server in the target workspace and prescribes when to call recall, trace, expand, remember, forget, plan_task, tasks, handoff, resume, distill, and stats during architecture, implementation, and operations work.
---

# Memory Management

## When to use

Invoke at the start of any project that will span more than one Claude Code session, or any project where (a) the repo is large enough that grep+read costs context budget, (b) the team will accumulate decisions Claude needs to remember across sessions, or (c) work will be handed off between sessions or developers. Also invoke whenever a fresh session needs to continue a task started elsewhere.

Do not invoke for one-shot scripts, throwaway prototypes, or single-file changes where retrieval cost is negligible. Do not invoke before [`system-design`](../system-design/SKILL.md) has produced any artifacts worth indexing — claude-mem indexes what exists, and an empty repo has nothing to gain.

## Inputs

Required:

- Target repo path (the workspace where Claude will run).
- Python 3.11+ available on PATH.

Optional:

- `OPENAI_API_KEY` if hosted OpenAI embeddings (1536d) are preferred over local `bge-small` (384d).
- `VOYAGE_API_KEY` if Voyage embeddings (512d) are preferred.
- `ANTHROPIC_API_KEY` for the CLI `distill` command (transcript-to-memory extraction).

## Process

1. **Install claude-mem** (one-time per machine):
   ```bash
   pip install claude-mem
   ```
   Verify: `claude-mem --help` prints the subcommand list (`index`, `serve`, `doctor`, `distill`, `install-hooks`, `bench`).

2. **Drop the MCP config** into the target workspace:
   ```bash
   cp <this-skill-dir>/assets/.mcp.json <target-workspace>/.mcp.json
   ```
   The config tells Claude Code to launch `claude-mem serve --watch` over stdio whenever the workspace opens.

3. **Build the index**:
   ```bash
   cd <target-workspace>
   claude-mem index
   ```
   On first run this downloads the `bge-small` model (~90 MB) and embeds every code/docs unit. Subsequent runs are incremental.

4. **Verify health**:
   ```bash
   claude-mem doctor
   ```
   Output reports `units`, `by_layer`, `t2_coverage`, and `counters`. A healthy fresh repo shows non-zero `code` and `docs` counts.

5. **(Optional) Install the git post-commit hook** so the index stays warm without the watcher:
   ```bash
   claude-mem install-hooks
   ```

6. **(Optional) Pick a different embedder**:
   ```bash
   claude-mem index --embedder openai --reset
   # or
   claude-mem index --embedder voyage --reset
   ```
   `--reset` is required because the vector dimension is baked into the SQLite schema.

7. **Adopt the tool-use rules** in `references/usage-by-phase.md` for the remainder of the project. Treat these rules as default operating procedure during every subsequent skill invocation — they replace ad-hoc `Grep` and `Read` with budgeted, tier-aware retrieval.

## Outputs

- A populated `.claude-mem/` directory in the target workspace, containing:
  - `db.sqlite` — the index (gitignored).
  - `memory/<scope>/<slug>.md` — committed source-of-truth memory files.
  - `handoffs/<task_id>.md` — per-handoff snapshots (committed; resumable).
- A `.mcp.json` registering the `claude-mem` server (committed).
- An optional `.git/hooks/post-commit` hook.

## Quality checks

- `claude-mem doctor` reports `units > 0` and `by_layer` includes at least `code` for any repo containing supported source files.
- `claude-mem recall --query <known-symbol>` (via the MCP server or by running a test) returns at least one hit whose `t1_header` contains the symbol name.
- `claude-mem stats` reports a non-zero `counters.recall_calls` after any retrieval has happened in the session.
- A round-trip works: `remember(fact, scope)` writes a file under `.claude-mem/memory/<scope>/`, and a subsequent `recall(query=<fact substring>)` returns that memory's handle in the top results.

## References

- [`references/setup.md`](references/setup.md) — install + MCP-config walkthrough with Windows / macOS / Linux notes.
- [`references/usage-by-phase.md`](references/usage-by-phase.md) — mapping between claude-full-stack-2.0 workflow phases and claude-mem tools.
- [`assets/.mcp.json`](assets/.mcp.json) — drop-in MCP server config.
- claude-mem source and spec: <https://github.com/amritmalla/claude-mem>.
