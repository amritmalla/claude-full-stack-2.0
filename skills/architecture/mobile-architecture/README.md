# mobile-architecture

> Status: draft

## Purpose

Defines mobile application architecture from an approved system design: platform strategy, application and navigation architecture, state and offline/sync design, device-capability integration, performance and battery budgets, accessibility and localization, notifications and background behavior, error handling and recovery, observability, testing strategy, and a failure taxonomy.

Technology-agnostic and framework-agnostic first. Covers native (iOS/Android) and cross-platform-native (React Native, Flutter, KMP). Mobile-web and PWA are out of scope and belong to [`frontend-architecture`](../frontend-architecture/README.md). Deep mobile security/privacy and store-release/signing are not owned here — they are raised as callouts and ADR candidates and owned by [`security`](../security/SKILL.md) and [`operations`](../operations/SKILL.md) / [`infrastructure-platform`](../infrastructure-platform/SKILL.md).

## Owns

- Platform-target strategy (native vs cross-platform-native vs hybrid) as an ADR
- Application architecture and module boundaries
- Navigation architecture and state restoration
- State management and cache ownership
- Offline-first and synchronization strategy
- Device-capability integration and permission posture
- Performance and battery budgets
- Accessibility and localization
- Notifications and background behavior
- Error handling, recovery, and the failure taxonomy
- Observability and analytics posture
- Testing strategy

Not owned (callouts only): mobile security/privacy design, store-release/signing/rollout.

## Produces

| Artifact | Conforms to |
|---|---|
| `mobile-architecture.md` | [architecture-schema](../../../standards/architecture-schema/README.md), [documentation-standards](../../../standards/documentation-standards/README.md) |
| ADR drafts (platform target, offline/sync, security callouts, release callouts) | [architecture-schema](../../../standards/architecture-schema/README.md) |

## Skills

- [mobile-architecture](SKILL.md) - turns an approved system design into mobile application architecture: platform strategy, app and navigation architecture, state, offline/sync, device capabilities, performance and battery, accessibility, notifications, error handling, observability, testing, failure taxonomy, and implementation handoffs.

## Standards this architecture domain conforms to

- [architecture-schema](../../../standards/architecture-schema/README.md) - `mobile-architecture.md` artifact structure and system-design traceability.
- [security-standards](../../../standards/security-standards/README.md) - mobile security/privacy callout posture.
- [observability-standards](../../../standards/observability-standards/README.md) - mobile telemetry and crash/latency signals.
- [deployment-standards](../../../standards/deployment-standards/README.md) - release/rollout callout posture.
- [documentation-standards](../../../standards/documentation-standards/README.md) - skill structure.

## Upstream inputs

Requires an approved `system-design.md` per [architecture-schema](../../../standards/architecture-schema/README.md) whose design includes a native or cross-platform-native mobile surface. Bounded contexts, component interfaces, API boundaries, and ADRs shape the mobile architecture produced here.

## Downstream consumers

Mobile architecture produced here is the source of truth for:

- Future `implementations/mobile/<ecosystem>` - iOS, Android, and cross-platform-native skills follow platform, navigation, state, offline, and performance decisions.
- [architecture/security](../security/SKILL.md) - owns the mobile security/privacy decisions raised here as callouts.
- [architecture/operations](../operations/SKILL.md) / [architecture/infrastructure-platform](../infrastructure-platform/SKILL.md) - own the release/signing/rollout decisions raised here as callouts.
- [architecture/performance](../performance/SKILL.md) - performance and battery budget enforcement.
