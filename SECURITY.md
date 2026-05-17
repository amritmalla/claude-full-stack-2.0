# Security Policy

## Supported Versions

Security fixes target the default branch and the latest published plugin version.

## Reporting A Vulnerability

Please report suspected vulnerabilities privately to the maintainer listed in `.claude-plugin/plugin.json`.

Include:

- Affected file or skill.
- Reproduction steps.
- Expected impact.
- Whether secrets, credentials, generated artifacts, or user data are involved.

Do not open a public issue for exploitable vulnerabilities, leaked secrets, or supply-chain concerns.

## Security Expectations

- Skills must not instruct agents to expose secrets, disable authentication, or bypass policy gates.
- Templates must not include real credentials, tokens, hostnames, or private account identifiers.
- Validation scripts must be deterministic and must not call external LLM APIs.
- CI/CD examples should prefer pinned actions, least-privilege permissions, and explicit environment promotion gates.

