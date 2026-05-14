# github-actions

> Status: draft

## Purpose

Implements CI/CD pipelines on GitHub Actions for any service in the repo. Pipelines enforce the gates declared in [deployment-standards](../../../standards/deployment-standards/README.md) and security scans declared in [security-standards](../../../standards/security-standards/README.md).

## Skills

- [github-actions-pipeline-hardened](github-actions-pipeline-hardened/SKILL.md) — produces build/test/scan/sign/push workflows with pinned action versions, dependency caching, SBOM generation, and provenance signing.

## Architecture domains implemented

| Architecture domain | How |
|---|---|
| [infrastructure-platform](../../../architecture/infrastructure-platform/README.md) | CI/CD pipeline definitions and runner topology. |
| [security](../../../architecture/security/README.md) | SAST, SCA, container scanning, secret scanning, image signing. |

## Standards this implementation conforms to

- [deployment-standards](../../../standards/deployment-standards/README.md) — CI gates (lint, test, build, scan, lint OpenAPI, migration plan review), env-ladder enforcement.
- [security-standards](../../../standards/security-standards/README.md) — SCA + SAST + container scan + secret scan as required gates; signed artifacts.
- [naming-conventions](../../../standards/naming-conventions/README.md) — workflow file names, environment variable casing.
