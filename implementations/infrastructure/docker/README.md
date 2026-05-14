# docker

> Status: draft

## Purpose

Implements container packaging for services. Produces minimal, hardened images that conform to [deployment-standards](../../../standards/deployment-standards/README.md) (env-agnostic, immutable, signed) and [security-standards](../../../standards/security-standards/README.md) (no secrets baked, non-root, scanned).

## Skills

- [dockerfile-and-jvm-tuning](dockerfile-and-jvm-tuning/SKILL.md) — multi-stage Dockerfile for JVM services with distroless or jlink runtime, container-aware JVM tuning, layered jars, and image scanning.

## Architecture domains implemented

| Architecture domain | How |
|---|---|
| [infrastructure-platform](../../../architecture/infrastructure-platform/README.md) | Container packaging, JVM runtime tuning. |
| [security](../../../architecture/security/README.md) | Non-root, minimal base, scanned images. |
| [performance](../../../architecture/performance/README.md) | JVM heap and GC tuning for container memory limits. |

## Standards this implementation conforms to

- [deployment-standards](../../../standards/deployment-standards/README.md) — env-agnostic image, config at deploy time, signed artifacts.
- [security-standards](../../../standards/security-standards/README.md) — no baked secrets, container scan as a required gate.
- [naming-conventions](../../../standards/naming-conventions/README.md) — `kebab-case` image names, registry-prefixed.
