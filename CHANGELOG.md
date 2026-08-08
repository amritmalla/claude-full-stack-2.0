# Changelog

All notable changes to this repository are documented here.

## [0.3.0] - 2026-08-08

- Add the `saas-idea-validation` skill and the `validation-brief-schema` standard: evidence-scored validation of a commercial SaaS idea, emitting a proceed / pivot / not-yet / kill verdict that gates `idea-development`.
- Register `rust-service-scaffold` in the plugin manifest and the architecture registry; it shipped unlisted. `validate_skills.py` now fails when a skill on disk is missing from an enumerated plugin manifest.
- **Breaking:** port the MCP server from the low-level `Server` to the high-level `MCPServer` API introduced in mcp 2.0. The requirement is now `mcp>=2,<3`; environments pinned to mcp 1.x cannot install this version.
- Add a weekly, non-blocking `mcp-canary` workflow that runs the test suite against the latest `mcp` release, so a breaking SDK major surfaces on a schedule rather than in an unrelated pull request.
- Align the Claude and Codex plugin manifests with the package version, and correct stale skill counts (84 skills + 4 workflows).

## [0.2.1] - 2026-05-27

- Configure FORCE_JAVASCRIPT_ACTIONS_TO_NODE24 and fix pytest pythonpath for stable CI runs.

## [0.2.0] - 2026-05-27

- Add repository conventions, security policy, cross-platform validation, and Codex plugin metadata.

