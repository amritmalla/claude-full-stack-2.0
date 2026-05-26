# claude-repo-mem setup walkthrough

## Install

```bash
pip install claude-repo-mem
```

Requires Python 3.11+. On Windows, prefer a venv so the `claude-repo-mem` script lands somewhere predictable:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install claude-repo-mem
```

Confirm: `claude-repo-mem --help`.

## Wire MCP server into a workspace

Copy the template `.mcp.json` from this skill's `assets/` into your target workspace's root:

```bash
cp .../skills/architecture/memory-management/assets/.mcp.json ./.mcp.json
```

The template is:

```json
{
  "mcpServers": {
    "claude-repo-mem": {
      "command": "claude-repo-mem",
      "args": ["serve", "--watch"]
    }
  }
}
```

If `claude-repo-mem` is not on the global PATH (common when installed inside a workspace venv), point `command` at the venv binary:

- Windows: `".venv\\Scripts\\claude-repo-mem.exe"`
- macOS / Linux: `".venv/bin/claude-repo-mem"`

Commit `.mcp.json` so teammates inherit the config.

## Build the index

```bash
claude-repo-mem index
```

First run downloads `BAAI/bge-small-en-v1.5` (~90 MB) and embeds every supported file. Subsequent runs (via `--watch` or `claude-repo-mem install-hooks`) are incremental.

Supported languages: Python, JavaScript, TypeScript, Markdown, Java, Go, Rust. Synthesizers emit framework-aware edges for Flask / Django / Express routes, Python imports, and React `useState` hooks.

## Verify

```bash
claude-repo-mem doctor
```

Expected output (numbers vary):

```
repo_root: /path/to/repo
db: /path/to/repo/.claude-repo-mem/db.sqlite
units: 412
relations: 73
by_layer: {'code': 380, 'docs': 32}
t2_coverage: 0/412
counters: {...}
```

`t2_coverage` stays at 0 until you start using the LLM-driven summary backfill (it populates lazily once Claude calls `recall`/`trace` with an active LLM context).

## Keeping the index warm

Three options, pick one:

1. **Watcher** (recommended for active development): `.mcp.json` already includes `--watch`. The MCP server runs a file watcher; any change re-indexes the touched files in <1s.
2. **Git hook** (recommended for shared repos): `claude-repo-mem install-hooks`. Installs a `.git/hooks/post-commit` that re-indexes after every commit.
3. **Manual**: `claude-repo-mem index` whenever you remember to.

## Switching embedders

The default `bge-small` (384d, local CPU) is sufficient for most repos. Hosted alternatives:

```bash
# OpenAI text-embedding-3-small (1536d)
export OPENAI_API_KEY=sk-...
claude-repo-mem index --embedder openai --reset

# Voyage voyage-3-lite (512d)
export VOYAGE_API_KEY=vy-...
claude-repo-mem index --embedder voyage --reset
```

`--reset` is required because the vector dimension is baked into the SQLite schema. The embedder choice is persisted in `embedder_meta`; subsequent `index` calls without `--embedder` reuse it.

## End-of-session distillation

When wrapping up a session, run:

```bash
claude-repo-mem distill --yes
```

This reads the most recent Claude Code transcript JSONL from `~/.claude/projects/`, asks the LLM to extract durable decisions/conventions, and writes accepted ones as `memory://` units. Set `CLAUDE_REPO_MEM_LLM=anthropic` and `ANTHROPIC_API_KEY` to use the Anthropic API directly (the default MCP sampling path requires the LLM context to be available, which it isn't from the CLI).
