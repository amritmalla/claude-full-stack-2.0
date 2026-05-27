# Integrations

## Use claude-full-stack-2.0 in Claude Desktop

Claude Desktop loads MCP servers from `claude_desktop_config.json` but doesn't
read the Claude Code plugin manifest. To make the 83 skills + 4 workflows
available in Claude Desktop (or any MCP host), install the companion package:

```bash
pip install claude-full-stack-skills
```

Add to your Claude Desktop config:

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "claude-full-stack-skills": {
      "command": "claude-full-stack-skills"
    }
  }
}
```

Restart Claude Desktop. Each skill and workflow now appears as an MCP tool
whose `description` ("Use when …") drives Claude's routing. You can also call:

- `list_skills(kind?, contains?)` — browse the catalog.
- `get_skill_reference(skill, reference)` — fetch a `references/*.md` on demand.

The skills are bundled inside the wheel — no separate clone needed. To point
at a local development checkout instead, set
`CLAUDE_FULL_STACK_SKILLS_ROOT=/path/to/claude-full-stack-2.0`.

The same MCP server works in Claude Code (drop the config in `.mcp.json`),
the Anthropic API, and any other MCP host.

---

## claude-repo-mem — durable cross-session memory

[claude-repo-mem](https://github.com/amritmalla/claude-repo-mem) is a local-first MCP server
that gives Claude durable memory and hierarchical retrieval over a single repo's
code, docs, and decisions. It is the recommended memory layer for projects built
using claude-full-stack-2.0.

### Install (one-time, per machine)

```bash
pip install claude-repo-mem
```

Requires Python 3.11+. See
[`skills/architecture/memory-management/references/setup.md`](skills/architecture/memory-management/references/setup.md)
for Windows / macOS / Linux notes and venv-scoped installs.

### Wire it into your workspace (per repo)

1. Copy `skills/architecture/memory-management/assets/.mcp.json` into your
   project root.
2. Build the index: `claude-repo-mem index`.
3. Verify: `claude-repo-mem doctor`.

The MCP server auto-starts when Claude Code loads the workspace and runs an
incremental file watcher; changes are re-indexed within ~750ms.

### Optional: post-commit git hook

If you don't want the watcher process running, install a post-commit hook
instead:

```bash
claude-repo-mem install-hooks
```

### Hosted embedders

Default is the local `bge-small` (384d, CPU). Swap with:

```bash
export OPENAI_API_KEY=sk-...
claude-repo-mem index --embedder openai --reset    # 1536d

export VOYAGE_API_KEY=vy-...
claude-repo-mem index --embedder voyage --reset    # 512d
```

`--reset` is required when changing embedders because the vector dimension is
baked into the SQLite schema.

### When to use which tool

The full mapping between claude-full-stack-2.0 workflow phases and claude-repo-mem
tools lives in
[`skills/architecture/memory-management/references/usage-by-phase.md`](skills/architecture/memory-management/references/usage-by-phase.md).

Headline rules:

- Before any `Grep`, call `recall(query)`.
- After any decision, call `remember(fact, scope, kind="decision")`.
- Before a multi-step feature, call `plan_task(intent)`.
- End of session: `handoff(task_id)`. Start of next session: `resume(task_id)`.

### Status (claude-repo-mem)

Five phases shipped: substrate + retrieval; memory + tasks + distillation;
handoff + watcher + skills; multilang (Python / JS-TS / Markdown / Java / Go /
Rust) + framework synthesizers (Flask, Django, Express, React); pluggable
embedders + benchmark harness + distill UX. 255 tests passing.
