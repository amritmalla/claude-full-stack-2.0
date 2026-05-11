#!/usr/bin/env bash
# Lint repository markdown.
# Requires Node (uses npx to invoke markdownlint-cli and markdown-link-check).
set -euo pipefail

npx --yes markdownlint-cli "**/*.md" \
  --ignore node_modules \
  --ignore docs/superpowers \
  --ignore .worktrees

# Link-check only the top-level public-facing docs to avoid slow runs.
for f in README.md SKILL_SPEC.md WORKFLOW_SPEC.md ROADMAP.md CONTRIBUTING.md; do
  if [ -f "$f" ]; then
    npx --yes markdown-link-check -q "$f"
  fi
done
