# Flutter State and Data Fetching Playbook

Load this when implementing any owned area of `flutter-state-and-data-fetching` or checking the anti-pattern list. It expands the operating rules and process steps in `SKILL.md` with the detail needed to produce a production-grade data layer.

## Why this workflow exists

A data layer done wrong fails in production in ways that are invisible in development: a token refresh race logs ten users out at once under a flaky network; an in-memory offline queue silently drops a user's mutations when the OS kills the app; an optimistic update with no rollback leaves the UI showing data the server rejected; a cache with no invalidation serves a deleted record for the rest of the session. None of these reproduce on a fast simulator with a fresh token.

The goal is a data layer that survives concurrency, process death, and degraded networks — and that consumes architectural decisions instead of inventing them.

## Behavioral rules in depth

### 1. Consume architecture; do not invent it

Read the State Management Strategy table, Offline & Synchronization Design, and Notifications & Background Behavior in `mobile-architecture.md`, plus the token strategy in `architecture/security`, before writing a single provider. The state mechanism, conflict-resolution rule, and refresh strategy are architectural decisions. If any needed decision is missing, surface an ADR candidate before proceeding.

### 2. Extend the scaffold seam — never duplicate the container

The scaffold installed the DI root and a typed session-provider shell with `// TODO(flutter-state-and-data-fetching)` markers. Fill those markers. Registering a second `ProviderScope`, a parallel GetIt instance, or a competing session object splits the source of truth and produces bugs where one half of the app sees a logged-in user and the other half does not.

### 3. Tokens never touch plaintext

Access and refresh tokens live only in `flutter_secure_storage` (Keychain on iOS, Keystore-backed on Android). Never `SharedPreferences`, never a plain file, never a log line, never a crash-report custom key, never an analytics property. Redact `Authorization` headers in the network logging interceptor.

### 4. Single-flight refresh — the most common production race

When the access token expires, every in-flight request 401s near-simultaneously. The wrong design fires N refreshes, races them, and the losers write a stale token over the winner. The correct design:

| Step | Behavior |
|---|---|
| First 401 | Acquire a refresh lock; start exactly one refresh |
| Concurrent 401s | Do not refresh; await the in-flight refresh future |
| Refresh succeeds | Replay all queued requests with the new token |
| Refresh fails | Clear tokens, flip the scaffold session shell to logged-out, fail queued requests cleanly |

### 5. The offline queue must survive process death

A mutation queue that lives only in memory loses the user's work the moment the OS reclaims the app — which it does aggressively on mobile. The queue is persisted (Hive/Drift/SQLite per architecture), replayed idempotently (each mutation carries a client-generated idempotency key so a double-replay is a no-op), and bounded: exponential backoff with jitter and an explicit poison-message ceiling after which the mutation is parked and surfaced, not retried forever.

### 6. Every optimistic update has a rollback

Apply the optimistic value, record the prior state, fire the mutation. On failure, restore the prior state and surface the failure per the degraded-mode UX in `mobile-architecture.md`. Conflict resolution (last-write-wins, server-authoritative, merge) is taken from the architecture document, not chosen here.

### 7. Honor the API contract

Every request and response is a typed model with explicit `fromJson`/`toJson` (or codegen). No `Map<String, dynamic>` leaking past the data layer. Transport and HTTP errors map to a single domain failure type so the presentation layer never switches on `DioException`.

### 8. Push delivers payload; navigation owns the destination

Register the push token, handle foreground/background/terminated messages, update the relevant state. Then hand the payload to the navigation seam. This skill never calls `Navigator` or a router — resolving a payload to a route is `flutter-navigation-and-routing`'s ownership, and crossing that boundary couples two archetypes that must stay independently testable.

### 9. A data layer not tested under failure is not done

The tests that matter are the ones that do not pass by accident: concurrent-401 single-flight refresh, offline replay idempotency under double-replay, and optimistic rollback on mutation failure. Unit-test these explicitly before declaring completion.

## Step detail

**Step 1 — Gather context.** Load `mobile-architecture.md`. Extract the four State Management Strategy rows, the Offline & Synchronization Design, the Notifications & Background Behavior section, and Application Architecture (state ownership, side-effect handling, concurrency). Extract token strategy, session model, and secure-storage posture from `architecture/security`. Confirm the scaffold DI/session seam exists. Raise an ADR candidate for any missing decision.

**Step 2 — State management wiring.** Install the architecture-named mechanism extending the scaffold root. For each State Management Strategy row, create a concrete provider/notifier/bloc with the declared ownership scope and an invalidation hook matching the declared lifecycle (e.g. session state cleared on logout, cached-remote invalidated on the declared trigger).

**Step 3 — Network layer.** Create the typed client with the flavor base URL from `app_config.dart`. Add a logging interceptor (redacting `Authorization` and PII) routed through the scaffold tracing seam, and an error interceptor mapping transport/HTTP errors to a domain `Failure`. Generate typed request/response models honoring the API contract.

**Step 4 — Auth-token plumbing.** Implement a `SecureTokenStore` over `flutter_secure_storage`. Add an auth interceptor that attaches the access token and, on 401, runs the single-flight refresh from rule 4. On refresh failure, clear tokens and flip the scaffold session shell. Replace the scaffold's token TODO markers with the real implementation.

**Step 5 — Caching & revalidation.** Implement the cache store for the chosen mechanism with stale-while-revalidate read behavior and the invalidation triggers from the State Management Strategy table.

**Step 6 — Offline queue.** Implement a persisted queue with idempotency keys, a connectivity listener (`connectivity_plus` or platform channel) that drains on reconnect, idempotent replay, exponential backoff with jitter, and a poison ceiling that parks and surfaces a stuck mutation.

**Step 7 — Optimistic updates.** Implement apply/rollback wrappers capturing prior state, and conflict resolution exactly as specified in `mobile-architecture.md`.

**Step 8 — Push delivery wiring.** Register the push token (store/refresh per provider). Implement foreground, background, and terminated handlers that update state and forward the payload to the navigation seam. No `Navigator` usage.

**Step 9 — Background sync.** Wire `workmanager` or platform background fetch to drain the offline queue and refresh declared data, within the background-execution budget.

**Step 10 — Test and verify.** Unit-test single-flight refresh under concurrent 401s, offline replay idempotency under double-replay, and optimistic rollback. Run `flutter analyze` and fix every issue. Document any skipped check.

**Step 11 — Standards validation.** Check api-standards (contract fidelity), security-standards (token storage and redaction), observability-standards (network tracing), naming-conventions. Keep any unresolved gap explicit.

## Anti-patterns to detect

Call these out explicitly when found:

- A second `ProviderScope` / parallel DI container instead of extending the scaffold seam
- Tokens in `SharedPreferences`, a plain file, log lines, crash custom keys, or analytics properties
- One refresh per 401 instead of single-flight with a replay queue
- An in-memory offline queue that does not survive process death
- Offline replay with no idempotency key (double-applies on reconnect)
- Unbounded retry with no backoff or poison ceiling
- Optimistic update with no captured prior state / no rollback path
- Invented conflict-resolution rule instead of the one in `mobile-architecture.md`
- `Map<String, dynamic>` or `DioException` leaking past the data layer
- Push handler calling `Navigator` / a router instead of deferring to `flutter-navigation-and-routing`
- Network layer not routed through the scaffold tracing seam
- Failure-path tests (refresh race, replay idempotency, rollback) missing
