#!/usr/bin/env bash
# Validate every SKILL.md under architecture/ and implementations/.
set -euo pipefail

python3 scripts/validate_skills.py
