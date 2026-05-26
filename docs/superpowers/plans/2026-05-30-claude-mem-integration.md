# claude-full-stack-2.0 ↔ claude-mem Integration Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Make claude-mem the recommended memory layer for projects built using claude-full-stack-2.0's 82 skills. Ship (a) an MCP server config so claude-mem runs alongside, and (b) a new companion skill `memory-management` documenting *when* skills should call `recall` / `remember` / `handoff` / `resume`.

**Architecture:** claude-mem ships separately (its own PyPI package + MCP stdio server). claude-full-stack-2.0 doesn't bundle it — instead, it provides a turnkey `.mcp.json`, bootstrap docs, and one new skill that other skills are *encouraged* (not required) to reference. No existing SKILL.md files are modified. The 4 WORKFLOW.md files are not modified in this pass either — they can adopt the skill later.

**Scope:** This integration is purely additive. We don't touch any of the 82 skills, the workflows, or `plugin.json`'s existing entries — we append one new skill path.

**Spec sources:**
- claude-mem: `D:/projects/claude-full-stack-mem/docs/specs/2026-05-25-claude-mem-design.md`
- claude-full-stack-2.0 SKILL spec: `D:/projects/claude-full-stack-2.0/SKILL_SPEC.md`

**Constraints:**
- claude-mem is invoked from outside this repo (the *user's* repo, where work happens).
- The MCP config shipped here is a *template* — users copy it into their workspace because claude-mem indexes a single repo at a time.
- The new skill must follow claude-full-stack-2.0's existing SKILL.md format (frontmatter `name` + `description`, then `## When to use` / `## Inputs` / `## Operating rules` / etc.).

---

## File Structure

**New files (all in claude-full-stack-2.0):**

- `skills/architecture/operations/memory-management/SKILL.md` — the new companion skill
- `skills/architecture/operations/memory-management/references/setup.md` — install + MCP-config walkthrough
- `skills/architecture/operations/memory-management/references/usage-by-phase.md` — when each tool helps (idea-development, system-design, implementation, etc.)
- `skills/architecture/operations/memory-management/assets/.mcp.json` — template MCP config users drop into their own repo
- `INTEGRATION.md` — top-level bootstrap pointer
- Modify: `.claude-plugin/plugin.json` — register the new skill

NOTE: `skills/architecture/operations/` already exists as a parent (it has `SKILL.md`, `assets/`, `references/`). The new skill lives as a sibling at `skills/architecture/operations/memory-management/`, NOT inside it.

Actually — re-read SKILL_SPEC: parent skill files live at `skills/architecture/<domain>/SKILL.md` with one SKILL per domain folder. `operations/` is the domain folder and already owns one SKILL.md. We have two options:

1. Put memory-management under a NEW top-level architecture domain: `skills/architecture/memory-management/SKILL.md`.
2. Put it under implementations: `skills/implementations/tooling/claude-mem/SKILL.md` (tooling category doesn't currently exist).

Option 1 is cleaner — memory IS an architecture concern (context strategy, durable knowledge, handoffs across sessions). Use option 1.

**Revised file list:**

- `skills/architecture/memory-management/SKILL.md`
- `skills/architecture/memory-management/references/setup.md`
- `skills/architecture/memory-management/references/usage-by-phase.md`
- `skills/architecture/memory-management/assets/.mcp.json`
- `INTEGRATION.md`
- Modify: `.claude-plugin/plugin.json`

---

## Cross-cutting design

### MCP config template

claude-mem's server runs over stdio. The template `.mcp.json` users drop in their workspace:

```json
{
  "mcpServers": {
    "claude-mem": {
      "command": "claude-mem",
      "args": ["serve", "--watch"]
    }
  }
}
```

If `claude-mem` isn't on PATH, users can swap `command` for the venv path. The setup reference covers both.

### Skill frontmatter

Per `SKILL_SPEC.md`, the `description` MUST start with `Use when …` and end with a one-sentence outcome. Trigger phrasing is critical because Claude's Skill tool routes by description matching.

The new skill's description:

> Use when a project built with claude-full-stack-2.0 needs durable cross-session memory, retrieval over a repo's code/docs/decisions, or task handoff between sessions. Defines how to install and configure the claude-mem MCP server and when to call its tools (recall, trace, remember, forget, plan_task, tasks, handoff, resume) during architecture, implementation, and operations work.

### What the skill body covers

Per `SKILL_SPEC.md` sections:

- **When to use** — at project bootstrap; when a multi-session task is in flight; when a fresh session needs to resume prior work; when decisions need to be captured for the future.
- **Inputs** — claude-mem version, OPENAI/VOYAGE keys if hosted embeddings desired, target repo path.
- **Operating rules** — call `recall` before `Grep`; `remember` decisions immediately (not at end of session); `handoff` before context bloat; `resume` at session start when continuing.
- **Steps** — install, configure MCP, run `claude-mem index`, verify with `doctor`, optionally `install-hooks`.
- **Outputs** — a working MCP server, a populated `.claude-mem/` directory in the user's workspace.
- **Definition of done** — `recall` returns ranked results for a known symbol; `remember` writes a markdown file under `.claude-mem/memory/<scope>/`.

---

## Task 1: Author the memory-management skill

**Files:**
- Create: `skills/architecture/memory-management/SKILL.md`
- Create: `skills/architecture/memory-management/references/setup.md`
- Create: `skills/architecture/memory-management/references/usage-by-phase.md`
- Create: `skills/architecture/memory-management/assets/.mcp.json`

- [ ] **Step 1: Write SKILL.md**

Frontmatter:
```yaml
name: memory-management
description: Use when a project built with claude-full-stack-2.0 needs durable cross-session memory, retrieval over a repo's code/docs/decisions, or task handoff between sessions. Sets up the claude-mem MCP server and prescribes when to call recall, trace, remember, forget, plan_task, tasks, handoff, and resume during architecture, implementation, and operations work.
```

Body sections per SKILL_SPEC (use `## When to use`, `## Inputs`, `## Operating rules`, `## Steps`, `## Outputs`, `## Definition of done`). Reference both reference files and the template `.mcp.json` asset.

- [ ] **Step 2: Write `references/setup.md`**

Walkthrough: install via pip, copy `.mcp.json` into user workspace, run `claude-mem index`, verify with `claude-mem doctor`, optional `claude-mem install-hooks`, switching embedders. Include Windows + macOS/Linux notes.

- [ ] **Step 3: Write `references/usage-by-phase.md`**

Maps claude-mem tools to claude-full-stack-2.0 workflow phases:

| Phase | Tool | When |
|---|---|---|
| Idea development | — | (nothing to index yet) |
| System design | `remember` | after each ADR is approved, store the rationale as a `decision` memory in scope `architecture/<area>` |
| Implementation | `recall`, `trace`, `expand` | before grepping for symbols; before reading a file; when exploring an unfamiliar handler chain |
| Implementation | `plan_task` | decompose multi-step features into independently-resumable sub-tasks |
| Implementation | `handoff` | end of session, or before opening a new task tree |
| Resume work | `resume` | start of a fresh session continuing prior task |
| Operations | `stats`, `scopes` | check index health; see which scopes have most coverage |
| Operations | `distill --yes` | end-of-session memory extraction from the Claude Code transcript |

- [ ] **Step 4: Write `assets/.mcp.json`**

```json
{
  "mcpServers": {
    "claude-mem": {
      "command": "claude-mem",
      "args": ["serve", "--watch"]
    }
  }
}
```

- [ ] **Step 5: Validate** — open each file, sanity-check that the frontmatter `name` matches the directory name (`memory-management`), and that `description` starts with `Use when`.

- [ ] **Step 6: Commit**

```
git add skills/architecture/memory-management/
git commit -m "feat(skills): memory-management — companion skill for claude-mem MCP integration"
```

---

## Task 2: Register skill in plugin.json

**Files:**
- Modify: `.claude-plugin/plugin.json`

- [ ] **Step 1: Insert path**

Insert `"./skills/architecture/memory-management"` into the `skills` array in alphabetical position (after `infrastructure-platform`, before `mobile-architecture`).

- [ ] **Step 2: Validate JSON**

```
python -c "import json; json.load(open('.claude-plugin/plugin.json'))"
```

- [ ] **Step 3: Commit**

```
git add .claude-plugin/plugin.json
git commit -m "chore(plugin): register memory-management skill"
```

---

## Task 3: INTEGRATION.md at repo root

**Files:**
- Create: `INTEGRATION.md`

- [ ] **Step 1: Write**

Top-level pointer doc:

```markdown
# Integrations

## claude-mem — durable cross-session memory

claude-mem is a local-first MCP server that gives Claude durable memory and
hierarchical retrieval over a single repo's code, docs, and decisions. It is
the recommended memory layer for projects built using claude-full-stack-2.0.

### Install (one-time, per machine)

```bash
pip install claude-mem
```

### Wire it into your workspace (per repo)

1. Copy `skills/architecture/memory-management/assets/.mcp.json` into your
   project root.
2. Build the index: `claude-mem index`.
3. Verify: `claude-mem doctor`.

The MCP server will auto-start when Claude Code loads the workspace.

### When to use which tool

See `skills/architecture/memory-management/SKILL.md` for the full mapping
between claude-full-stack-2.0 workflow phases and claude-mem tools.

### Status

Five phases shipped: substrate + retrieval, memory + tasks + distillation,
handoff + watcher, multilang + synthesizers, pluggable embedders + bench.
255 tests passing. Source: <https://github.com/amritmalla/claude-mem>.
```

- [ ] **Step 2: Commit**

```
git add INTEGRATION.md
git commit -m "docs: INTEGRATION.md — claude-mem setup pointer at repo root"
```

---

## Task 4: README mention

**Files:**
- Modify: `README.md` (top-level)

- [ ] **Step 1: Append a short paragraph**

Under a new `## Memory` section (or extend an existing companion-tools section if one exists), add:

```markdown
## Memory

For durable cross-session memory and hierarchical retrieval, install
[claude-mem](https://github.com/amritmalla/claude-mem) and follow
[`INTEGRATION.md`](./INTEGRATION.md). The `memory-management` skill defines
when each claude-mem tool is appropriate during architecture, implementation,
and operations work.
```

- [ ] **Step 2: Commit**

```
git add README.md
git commit -m "docs: README — point to claude-mem integration"
```

---

## Self-review

**1. Coverage:** Both selected items addressed:
- MCP server config + bootstrap → assets/.mcp.json + INTEGRATION.md + README mention.
- Companion skill → SKILL.md + two references + asset.

**2. Placeholder scan:** none. Every file body is concrete or has a worked example in the task steps.

**3. Type consistency:** skill name `memory-management` consistent across directory, frontmatter, and plugin.json registration.

**4. Non-goals (explicit):**
- The 82 existing skills are NOT modified.
- The 4 workflows are NOT modified.
- claude-mem is NOT bundled — users install separately via pip.
- Other potential integrations (e.g., embedded claude-mem in the marketplace, vendored Python package) are out of scope.

**5. Open questions:**
- Should `INTEGRATION.md` go at repo root, or under `docs/`? Plan picks repo root for discoverability; move if the repo has a convention against root-level integration docs.
- README structure varies across versions; if there's already a "Companion tools" section, append there instead of creating `## Memory`.

---

## Execution handoff

4 tasks, all pure file authoring. Execute inline with executing-plans.
