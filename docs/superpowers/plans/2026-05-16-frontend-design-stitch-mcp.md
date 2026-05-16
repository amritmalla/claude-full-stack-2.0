# frontend-design Stitch MCP Router Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the `frontend-design` skill into a generator-selecting router (superpowers `frontend-design` vs Google Stitch via Google's official hosted MCP), with Stitch operational detail in a load-on-demand reference.

**Architecture:** Rewrite `implementations/frontend/frontend-design/SKILL.md` as a router that injects repo context, asks the user which generator to use, verifies that generator's prerequisites, and dispatches — never silently defaulting or falling back. Add `references/stitch-mcp.md` carrying the official `claude mcp add stitch …` setup, availability check, operational sequence, tool-name-drift caveat, and failure handling. No code, no custom MCP server, no stored secrets, no persisted artifact.

**Tech Stack:** Markdown only. Validation = SKILL_SPEC.md quality bar (frontmatter `name`==dir, `description` starts "Use when" and ≤1024 chars and link/secret-free, SKILL.md ≤~400 lines, repo-relative links resolve) + a repo-wide secret scan + manual trigger-prompt invocation check.

**Spec:** [docs/superpowers/specs/2026-05-16-frontend-design-stitch-mcp-design.md](../specs/2026-05-16-frontend-design-stitch-mcp-design.md)

**Execution environment:** Work directly in the main checkout `D:\projects\claude-full-stack-2.0` on branch `master` (user has opted out of worktrees). Commit directly to `master`.

---

## File Structure

- **Modify (full rewrite):** `implementations/frontend/frontend-design/SKILL.md` — the router. One responsibility: assemble repo context, present the generator choice, verify the chosen generator's prerequisites, dispatch, persist nothing.
- **Create:** `implementations/frontend/frontend-design/references/stitch-mcp.md` — Stitch path operational detail, loaded on demand only when the user picks Stitch.

No other files change. No `mcp/` changes. The `architecture/frontend-architecture` repointed links from the previous effort stay as-is.

---

### Task 1: Rewrite SKILL.md as the generator-selecting router

**Files:**
- Modify (full rewrite): `implementations/frontend/frontend-design/SKILL.md`

- [ ] **Step 1: Overwrite the file with exactly this content**

Write `implementations/frontend/frontend-design/SKILL.md` with EXACTLY the following (file begins at the YAML `---`, ends after the final References bullet; UTF-8 no BOM; every `—` is a literal em dash U+2014):

```markdown
---
name: frontend-design
description: Use when a claude-full-stack-2.0 project needs visual, UI, component, interaction, or UX design work — turning an approved frontend architecture into concrete visual and interaction design. This skill is a router that injects repository context and asks which design generator to use: the external superpowers frontend-design skill, or Google Stitch via its official MCP. Do not use for frontend application architecture, routing, rendering, state, or data-flow decisions (use architecture/frontend-architecture); do not use for wiring design tokens or components into framework code (use the implementations/frontend/<ecosystem> design-system-and-accessibility archetype, for example react-design-system-and-accessibility).
---

# Frontend Design

## When to use

Invoke when a project needs visual, UI, component, interaction, or UX design — after `architecture/frontend-architecture` has produced a `frontend-architecture.md`, and before the `implementations/frontend/<ecosystem>` design-system-and-accessibility archetype wires the design into framework code.

Do not use for frontend application architecture, routing, rendering, state, or data-flow decisions (use [`architecture/frontend-architecture`](../../../architecture/frontend-architecture/SKILL.md)). Do not use for wiring design tokens or components into a specific framework (use that ecosystem's design-system-and-accessibility archetype).

## Generators

This skill does not perform design itself. It routes to one of two generators, chosen by the user each run:

- superpowers `frontend-design` — the external superpowers skill. Prerequisite: that skill is available in the session. Hard dependency for this path.
- Google Stitch — Google's official hosted Stitch MCP. Prerequisite: the Stitch MCP is configured in the session. Setup and operation live in `references/stitch-mcp.md`.

## Lifecycle position

Upstream is [`architecture/frontend-architecture`](../../../architecture/frontend-architecture/SKILL.md): this skill consumes its design-system seam, accessibility posture, and performance budgets. Downstream is the `implementations/frontend/<ecosystem>` design-system-and-accessibility archetype, which wires the resulting design into framework code. This skill owns no artifact and produces only what the chosen generator produces.

## Inputs

Required:

- A design or UI request scoped to a project in this repository.

Optional:

- The product's `frontend-architecture.md` (design-system seam, accessibility posture, performance budgets, brand and information-architecture inputs).

## Process

- [ ] Step 1: Locate the product's `frontend-architecture.md`. If present, extract the design-system seam, accessibility posture, performance budgets, and brand / information-architecture inputs into a context block. If absent, note that explicitly and proceed.
- [ ] Step 2: Present both generators and their prerequisites, and ask the user which generator to use for this design task. Do not pick a default.
- [ ] Step 3a: If the user chose superpowers `frontend-design`: confirm the external superpowers `frontend-design` skill is available. If it is not, state that it is required and stop. Otherwise invoke it, passing the assembled repo context block.
- [ ] Step 3b: If the user chose Google Stitch: load `references/stitch-mcp.md` and follow it, passing the assembled repo context block as the design brief source.
- [ ] Step 4: If the chosen generator's prerequisites are not present in the session, state the exact requirement (for Stitch, the setup command in `references/stitch-mcp.md`), then re-ask the generator choice or stop. Never silently fall back to the other generator.
- [ ] Step 5: Do not produce any repository artifact of this skill's own.

## Outputs

None owned. The output is whatever the chosen generator produces.

## Quality checks

- [ ] The user was presented the explicit choice between the two generators.
- [ ] The chosen generator's prerequisites were verified before proceeding.
- [ ] If Google Stitch was chosen, `references/stitch-mcp.md` was loaded.
- [ ] No repository artifact, schema, or template was fabricated by this skill.

## References

- Upstream: [`architecture/frontend-architecture`](../../../architecture/frontend-architecture/SKILL.md).
- Downstream: `implementations/frontend/<ecosystem>` design-system-and-accessibility archetype (e.g. [`react-design-system-and-accessibility`](../react/react-design-system-and-accessibility/SKILL.md)).
- Google Stitch path detail: [`references/stitch-mcp.md`](references/stitch-mcp.md).
- Delegated execution (superpowers path): the external superpowers `frontend-design` skill.
- Claude Design (Anthropic Labs) integration is deferred: it exposes no MCP or public API, only a one-directional Claude Code handoff bundle, so it cannot be driven from this skill.
```

- [ ] **Step 2: Verify frontmatter validity, "Use when", length, line cap**

Run (PowerShell tool):
```
$f='implementations/frontend/frontend-design/SKILL.md'
Get-Content $f | Select-String '^name:'
$d=(Get-Content $f | Select-String '^description: ').ToString()
"starts-ok=$($d -like 'description: Use when*') desc-len=$($d.Length) lines=$((Get-Content $f).Count) dir=$(Split-Path (Split-Path $f -Parent) -Leaf)"
```
Expected: `name: frontend-design`; `starts-ok=True`; `desc-len` a value < 1024 (≈ 760–820); `lines` < 400 (≈ 70); `dir=frontend-design`.

- [ ] **Step 3: Verify the description carries no markdown link and no secret**

Run (PowerShell tool):
```
$d=(Get-Content implementations/frontend/frontend-design/SKILL.md | Select-String '^description:').ToString()
"no-link=$(-not ($d -match '\]\('))  no-key=$(-not ($d -match 'X-Goog-Api-Key|AQ\.'))"
```
Expected: `no-link=True  no-key=True`.

- [ ] **Step 4: Verify every repo-relative link resolves**

Run (PowerShell tool):
```
Push-Location implementations/frontend/frontend-design
foreach ($p in '../../../architecture/frontend-architecture/SKILL.md','../react/react-design-system-and-accessibility/SKILL.md','references/stitch-mcp.md') { "$p => $(Test-Path $p)" }
Pop-Location
```
Expected: first two `=> True`; `references/stitch-mcp.md => False` for now (created in Task 2 — this is expected and rechecked in Task 2 Step 5). Note this expected-False explicitly in the task report.

- [ ] **Step 5: Verify required sections are present**

Run (PowerShell tool):
```
$h=(Get-Content implementations/frontend/frontend-design/SKILL.md | Select-String '^## ').Line
$h
"count=$($h.Count)"
```
Expected lines, in order: `## When to use`, `## Generators`, `## Lifecycle position`, `## Inputs`, `## Process`, `## Outputs`, `## Quality checks`, `## References`; `count=8`.

- [ ] **Step 6: Commit**

```
git add implementations/frontend/frontend-design/SKILL.md
git commit -m "feat(frontend): make frontend-design a generator-selecting router

frontend-design now routes a design request to a user-chosen generator:
the external superpowers frontend-design skill, or Google Stitch via its
official MCP. Explicit choice each run, no silent default or fallback.
Stitch detail deferred to references/stitch-mcp.md (next task).

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 2: Add references/stitch-mcp.md

**Files:**
- Create: `implementations/frontend/frontend-design/references/stitch-mcp.md`

- [ ] **Step 1: Create the directory and file with exactly this content**

Create `implementations/frontend/frontend-design/references/stitch-mcp.md` with EXACTLY the following (UTF-8 no BOM; `<YOUR_KEY>` is a literal placeholder and MUST NOT be replaced with a real key):

```markdown
# Google Stitch MCP — path detail

Loaded on demand by `../SKILL.md` Process Step 3b when the user chooses the
Google Stitch generator. Stitch is reached through Google's official hosted MCP
server; this repository builds no MCP server and stores no credentials.

## Setup (user-run, local)

The user configures the official Stitch MCP once, locally:

`claude mcp add stitch --transport http --header "X-Goog-Api-Key: <YOUR_KEY>" https://stitch.googleapis.com/mcp`

- Transport is Streamable HTTP; the server is remote and Google-hosted.
- `<YOUR_KEY>` is a Stitch API key the user generates in Stitch settings
  (Stitch web app → settings → API key).
- Secret rule: the API key is a secret. It is configured locally by the user
  and is never committed to, written into, or echoed by this repository. Do not
  add it to any file here.

## Availability check

Confirm the Stitch MCP is connected in the current session: the configured
`stitch` server advertises tools (surfaced as `mcp__stitch__*`). If no such
tools are present, the prerequisite is not met: output the setup command above,
then return to `../SKILL.md` Process Step 4 (re-ask the generator choice or
stop). Do not switch to the superpowers path on the user's behalf.

## Operational sequence

Use the repo context block passed from `../SKILL.md` (design-system seam,
accessibility posture, performance budgets, brand / information-architecture
inputs) as the design brief source.

1. Ensure a Stitch project exists: list projects; if none suitable, create one.
2. Generate screen(s) from a text brief composed out of the repo context block.
3. Retrieve the generated screen plus its code and image.
4. Surface the design, code, and image in-session for the user and for
   downstream consumption by the `implementations/frontend/<ecosystem>`
   design-system-and-accessibility archetype.

Ephemeral: write nothing to the repository. This skill owns no artifact.

## Tool-name caveat

Do not hardcode upstream tool names; Google's advertised tool set can drift.
Read the live tool list the `stitch` server advertises this session and map the
operations above onto the actual tools:

- create / list projects
- generate a screen from a text prompt
- get a screen
- fetch screen code
- fetch screen image
- list screens

If a needed operation has no advertised tool, report that specifically and stop;
do not improvise an equivalent.

## Failure handling

On authentication failure, missing or invalid key, API error, rate limit, or
any tool error: report the specific failure to the user and stop. Never silently
switch to the superpowers `frontend-design` path.
```

- [ ] **Step 2: Verify the file contains the exact setup command and no real key**

Run (PowerShell tool):
```
$f='implementations/frontend/frontend-design/references/stitch-mcp.md'
"has-cmd=$([bool](Select-String -Path $f -Pattern 'claude mcp add stitch --transport http'))"
"has-endpoint=$([bool](Select-String -Path $f -Pattern 'https://stitch\.googleapis\.com/mcp'))"
"has-placeholder=$([bool](Select-String -Path $f -Pattern '<YOUR_KEY>'))"
"no-real-key=$(-not [bool](Select-String -Path $f -Pattern 'AQ\.[A-Za-z0-9_\-]{8,}'))"
```
Expected: `has-cmd=True`, `has-endpoint=True`, `has-placeholder=True`, `no-real-key=True`.

- [ ] **Step 3: Repo-wide secret scan (no leaked key anywhere)**

Run (PowerShell tool):
```
$hits = Get-ChildItem -Recurse -File -Include *.md,*.json,*.txt | Where-Object { $_.FullName -notmatch '\\\.git\\' } | Select-String -Pattern 'AQ\.Ab8RN6|X-Goog-Api-Key:\s*AQ\.' 
"leak-hits=$(@($hits).Count)"
```
Expected: `leak-hits=0`.

- [ ] **Step 4: Verify the reference resolves from SKILL.md and back**

Run (PowerShell tool):
```
Push-Location implementations/frontend/frontend-design
"skill->ref=$(Test-Path 'references/stitch-mcp.md')"
Push-Location references
"ref->skill=$(Test-Path '../SKILL.md')"
Pop-Location; Pop-Location
```
Expected: `skill->ref=True`, `ref->skill=True`.

- [ ] **Step 5: Re-run the Task 1 Step 4 link check (now fully green)**

Run (PowerShell tool):
```
Push-Location implementations/frontend/frontend-design
foreach ($p in '../../../architecture/frontend-architecture/SKILL.md','../react/react-design-system-and-accessibility/SKILL.md','references/stitch-mcp.md') { "$p => $(Test-Path $p)" }
Pop-Location
```
Expected: all three `=> True`.

- [ ] **Step 6: Commit**

```
git add implementations/frontend/frontend-design/references/stitch-mcp.md
git commit -m "feat(frontend): add Stitch MCP path reference for frontend-design

Load-on-demand detail for the Google Stitch generator: official
claude mcp add setup, availability check, operational sequence,
tool-name-drift caveat, and failure handling. Placeholder key only;
no secret stored in the repo.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 3: Trigger-prompt and no-secret final verification

**Files:** none modified — verification only; results recorded in the commit/PR notes.

- [ ] **Step 1: Confirm the 3 "should match" prompts route to `frontend-design`**

For a claude-full-stack-2.0 project, each of these should invoke `frontend-design`:
1. "We have an approved frontend-architecture.md — design the dashboard's visual look and interaction patterns."
2. "Do the UI/UX design for the onboarding flow before we wire it into React."
3. "Generate the screens for our settings page with Google Stitch."

Expected: all three match `frontend-design`. (Prompt 3 still matches this skill — Stitch is one of its generators, selected inside the skill, not a separate skill.)

- [ ] **Step 2: Confirm the 2 "should NOT match" prompts**

1. "Decide our routing model, rendering strategy, and state tiers." → `frontend-architecture`, NOT `frontend-design`.
2. "Wire the design tokens and accessible primitives into our React components." → `react-design-system-and-accessibility`, NOT `frontend-design`.

Expected: neither matches `frontend-design`.

- [ ] **Step 3: Final repo-wide secret scan**

Run (PowerShell tool):
```
$hits = Get-ChildItem -Recurse -File | Where-Object { $_.FullName -notmatch '\\\.git\\' } | Select-String -Pattern 'AQ\.Ab8RN6|X-Goog-Api-Key:\s*AQ\.'
"leak-hits=$(@($hits).Count)"
```
Expected: `leak-hits=0`.

- [ ] **Step 4: Record results**

Record the 3+2 prompt outcomes and `leak-hits=0` in the PR description (or as a note alongside the commits if no PR). No file change, no commit.

---

## Self-Review

**1. Spec coverage:**
- Router skill (superpowers vs Stitch), explicit choice each run, no silent default/fallback → Task 1 SKILL.md Process Steps 2/3a/3b/4 + Quality checks.
- Frontmatter updated, "Use when", ≤1024, link/secret-free → Task 1 Steps 2–3.
- Lifecycle/ephemeral/no-artifact unchanged → Task 1 SKILL.md Lifecycle + Process Step 5 + Quality checks.
- Structure SKILL.md + references/stitch-mcp.md (load-on-demand) → Task 1 + Task 2; Process Step 3b loads it.
- Official Stitch setup command, key obtention, secret rule → Task 2 file content + Steps 2–3.
- Availability check, operational sequence, tool-name caveat, failure handling, no silent fallback → Task 2 file content.
- Claude Design deferred note → Task 1 SKILL.md References bullet.
- No custom server / no mcp/ changes / no stored key → no task touches `mcp/`; Task 2 Step 3 + Task 3 Step 3 secret scans.
- SKILL_SPEC quality bar incl. 3+2 trigger prompts → Task 1 Steps 2–5 + Task 3. ✓ No gaps.

**2. Placeholder scan:** `<YOUR_KEY>` is an intentional, spec-mandated placeholder explicitly protected by Task 2 Step 2 (`has-placeholder=True`) and the secret scans — not a plan placeholder. No "TBD"/"TODO"/"handle errors"-style omissions; full file contents inline. ✓

**3. Type/identifier consistency:** Skill `name` = directory = `frontend-design` throughout; reference path `references/stitch-mcp.md` is consistent in SKILL.md (Process 3b, Process 4, References) and Task 2; link depths (`../../../architecture/...`, `../react/...`) match the file's actual location and the previous effort's working links; endpoint `https://stitch.googleapis.com/mcp` and header `X-Goog-Api-Key` consistent between spec and Task 2. ✓
