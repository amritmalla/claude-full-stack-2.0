#!/usr/bin/env node
import { spawnSync } from "node:child_process";

const npx = process.platform === "win32" ? "npx.cmd" : "npx";

function run(args) {
  const quotedArgs = args
    .map((arg) => `"${String(arg).replace(/"/g, '\\"')}"`)
    .join(" ");
  const command = `${npx} ${quotedArgs}`;
  const result = spawnSync(command, { shell: true, stdio: "inherit" });
  if (result.error) {
    console.error(result.error.message);
  }
  if (result.status !== 0) {
    process.exit(result.status ?? 1);
  }
}

run([
  "--yes",
  "markdownlint-cli",
  "**/*.md",
  "--ignore",
  "node_modules",
  "--ignore",
  "docs/superpowers",
  "--ignore",
  ".worktrees",
]);

for (const file of [
  "README.md",
  "SKILL_SPEC.md",
  "WORKFLOW_SPEC.md",
  "CONTRIBUTING.md",
  "CONVENTIONS.md",
  "SECURITY.md",
  "CHANGELOG.md",
]) {
  run(["--yes", "markdown-link-check", "-q", file]);
}
