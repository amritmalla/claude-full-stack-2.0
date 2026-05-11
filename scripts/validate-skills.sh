#!/usr/bin/env bash
# Validate frontmatter of every SKILL.md under skills/.
# Rules:
#   - YAML frontmatter present with name + description
#   - name matches parent directory
#   - description starts with "Use when"
#   - description <= 1024 characters
set -euo pipefail

fail=0

if [ ! -d skills ]; then
  echo "skills/ directory not found; nothing to validate"
  exit 0
fi

while IFS= read -r -d '' skill; do
  dir="$(dirname "$skill")"
  expected_name="$(basename "$dir")"

  fm="$(awk '/^---$/{f++; next} f==1{print} f==2{exit}' "$skill")"

  name="$(printf '%s\n' "$fm" | awk -F': *' '/^name:/{print $2; exit}')"
  desc="$(printf '%s\n' "$fm" | awk '/^description:/{sub(/^description: */,""); print; while(getline line) {if(line ~ /^[a-zA-Z_]+:/) exit; print line}}' | tr '\n' ' ' | sed 's/  */ /g;s/ $//')"

  if [ -z "$name" ] || [ -z "$desc" ]; then
    echo "FAIL $skill: missing name or description"
    fail=1
    continue
  fi

  if [ "$name" != "$expected_name" ]; then
    echo "FAIL $skill: name '$name' != directory '$expected_name'"
    fail=1
  fi

  if [ "${#desc}" -gt 1024 ]; then
    echo "FAIL $skill: description > 1024 chars (${#desc})"
    fail=1
  fi

  case "$desc" in
    "Use when"*) ;;
    *) echo "FAIL $skill: description must start with 'Use when'"; fail=1 ;;
  esac
done < <(find skills -name SKILL.md -print0 2>/dev/null)

if [ "$fail" -eq 0 ]; then
  echo "All skills valid."
fi

exit $fail
