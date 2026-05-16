# frontend-design + Google Stitch (official MCP) — design

> Status: approved
> Date: 2026-05-16
> Builds on: docs/superpowers/specs/2026-05-16-frontend-design-wrapper-skill-design.md

## Context

The `frontend-design` skill (at `implementations/frontend/frontend-design/`) is
today a thin, pure-delegation wrapper: it injects repo context and hard-delegates
all design work to the external superpowers `frontend-design` skill, owning no
artifact.

We want a second design generator: Google Stitch. Research established:

- Google ships an **official hosted Stitch MCP server** at
  `https://stitch.googleapis.com/mcp` (Streamable HTTP transport, API-key auth
  via the `X-Goog-Api-Key` header). It is added with a single command:
  `claude mcp add stitch --transport http --header "X-Goog-Api-Key: <YOUR_KEY>" https://stitch.googleapis.com/mcp`.
- The official `@google/stitch-sdk` and every third-party server
  (Kargatharaakash, davideast) are just clients/proxies over that same backend.
- **Claude Design (Anthropic Labs)** has no MCP/API — only a one-directional
  Claude Code handoff bundle — so it cannot be driven from Claude Code and is
  out of scope here.

Because the official direct MCP connection is one trivial command over the exact
same backend a custom wrapper would target, building a custom MCP server (an
earlier option) was rejected: no `mcp/servers/*` code is built. The skill simply
uses the official connection.

## Decisions

| Decision | Choice |
|---|---|
| Second generator | Google Stitch via the **official hosted MCP** (`https://stitch.googleapis.com/mcp`) |
| Custom MCP server | **Not built.** No `mcp/servers/*`, no `@google/stitch-sdk` wrapper, no third-party server |
| Claude Design | Deferred (no MCP/API) |
| Skill shape | `frontend-design` becomes a **generator-selecting router**: superpowers `frontend-design` vs Stitch |
| Generator selection | **Explicit user choice every run.** No silent default, no silent fallback |
| Stitch availability | Capability-declared: verify Stitch MCP tools are present in-session; if absent, give the setup command and stop/re-prompt |
| Handoff | **Ephemeral / symmetric** with the superpowers path. No persisted repo artifact, no new standard |
| Structure | `SKILL.md` (router) + `references/stitch-mcp.md` (Stitch setup + tool usage + failure handling, load-on-demand) |
| Auth | API key via `X-Goog-Api-Key` header (user-configured locally). **No key stored in the repo** |
| Transport | Streamable HTTP (official remote server) |

## File layout

```
implementations/frontend/frontend-design/
├── SKILL.md                 # rewritten as the router
└── references/
    └── stitch-mcp.md        # NEW; loaded on demand only for the Stitch path
```

No code. No changes under `mcp/`.

## SKILL.md (router)

### Frontmatter (load-bearing)

- `name: frontend-design` (unchanged; equals directory).
- `description:` starts with "Use when"; updated to state the skill routes a
  visual/UI/UX design request to a chosen generator — the external superpowers
  `frontend-design` skill or Google Stitch via its MCP. Same negative-scoping as
  today (not frontend application architecture; not framework token/component
  wiring). ≤ 1024 chars. Contains no links, keys, or secrets.

### Body sections

- **When to use** — unchanged intent: visual/UI/component/interaction/UX work
  after `architecture/frontend-architecture`, before the ecosystem
  design-system-and-accessibility archetype.
- **Generators** — the two options and each one's prerequisite:
  - superpowers `frontend-design` skill (hard dependency for this path).
  - Google Stitch (requires the official Stitch MCP configured in-session).
- **Lifecycle position** — unchanged: upstream `architecture/frontend-architecture`
  (consumes design-system seam, accessibility posture, performance budgets);
  downstream `implementations/frontend/<ecosystem>` design-system-and-accessibility
  archetype. Skill owns no artifact; produces only what the chosen generator
  produces.
- **Inputs** — Required: a design/UI request scoped to a repo project. Optional:
  the product's `frontend-architecture.md`.
- **Process** —
  1. Locate `frontend-architecture.md`; if present, extract design-system seam,
     accessibility posture, performance budgets, brand/IA inputs into a context
     block. If absent, note that explicitly and proceed.
  2. Present both generators and their prerequisites; **ask the user which to
     use**. No silent default.
  3a. superpowers chosen → confirm the external superpowers `frontend-design`
      skill is available; if not, state it is required and stop. Otherwise
      delegate, passing the context block (current behavior).
  3b. Stitch chosen → load `references/stitch-mcp.md` and follow it.
  4. If the chosen generator's prerequisites are not present in-session, state
     the exact requirement (for Stitch, point to the reference's setup command),
     then re-prompt or stop. **Never silently fall back to the other generator.**
  5. Produce no repository artifact of this skill's own.
- **Outputs** — none owned; whatever the chosen generator produces.
- **Quality checks** (binary) —
  - The user was presented the explicit generator choice.
  - The chosen generator's prerequisites were verified before proceeding.
  - If Stitch was chosen, `references/stitch-mcp.md` was loaded.
  - No repository artifact, schema, or template was fabricated by this skill.
- **References** — add `references/stitch-mcp.md`; keep upstream/downstream
  links; add a one-line note that Claude Design integration is deferred because
  it exposes no MCP/API.

## references/stitch-mcp.md

- **Setup (official, user-run).** Document the exact command shape:
  `claude mcp add stitch --transport http --header "X-Goog-Api-Key: <YOUR_KEY>" https://stitch.googleapis.com/mcp`
  with `<YOUR_KEY>` an explicit placeholder. State how to obtain the key from
  Stitch settings. **Secret rule:** the key is a secret; it is configured
  locally by the user and is never committed to or stored in this repository.
- **Availability check.** Confirm Stitch MCP tools are present in the current
  session (tool names surfaced by the configured `stitch` MCP server, e.g.
  `mcp__stitch__*`). If absent, output the setup command and stop or re-prompt
  per SKILL.md step 4.
- **Operational sequence.** Ensure or create a Stitch project → generate
  screen(s) from a brief composed out of the injected `frontend-architecture`
  context → retrieve the screen/design, code, and image via the Stitch tools the
  server advertises → surface results in-session for downstream consumption.
  Ephemeral: nothing is written to the repository.
- **Tool-name caveat.** Do not hardcode upstream tool names that may drift.
  Instruct Claude to read the live tool list the `stitch` server advertises and
  map the needed operations (create-project, generate-screen-from-text,
  get-screen, fetch-code, fetch-image, list) onto the actual advertised tools.
- **Failure handling.** Auth failure, missing/invalid key, API error, rate
  limit, or tool error → report the specific failure and stop. Never silently
  switch to the superpowers path.

## Out of scope

- Any custom MCP server, `@google/stitch-sdk` wrapper, or third-party server
  (`Kargatharaakash/stitch-mcp`, `@_davideast/stitch-mcp`).
- Claude Design integration (deferred; no MCP/API).
- Persisted Stitch artifacts and any new standard/schema.
- Tool-surface curation/filtering (not possible without a wrapper; the skill
  uses whatever the official server advertises).
- Mobile.
- Storing any API key in the repository.

## Quality bar (SKILL_SPEC.md)

- Valid frontmatter: `name` equals directory; `description` starts with "Use
  when"; ≤ 1024 chars; no links/keys/secrets in `description`.
- `SKILL.md` is an imperative recipe, sections present, ≤ ~400 lines; Stitch
  operational detail lives in `references/stitch-mcp.md` (loaded on demand).
- Quality-checks section is binary-verifiable.
- No secret/API key anywhere in the repository (verified at implementation).
- 3 "should match" and 2 "should NOT match" trigger prompts supplied at
  implementation time and verified.
