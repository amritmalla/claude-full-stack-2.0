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
