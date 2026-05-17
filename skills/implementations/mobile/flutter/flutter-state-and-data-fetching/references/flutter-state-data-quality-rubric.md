# Flutter State and Data Fetching Quality Rubric

Load this before declaring the data layer complete. Revise until each check passes or the unresolved gap is explicitly documented.

## State management

- [ ] State mechanism matches the one named in `mobile-architecture.md`, or is documented as deferred with a pending ADR candidate.
- [ ] The wiring extends the scaffold DI/session root — there is no second container or parallel `ProviderScope`.
- [ ] Each State Management Strategy row (local UI, session, cached-remote, persistent) maps to a concrete provider/notifier/bloc with the declared ownership scope.
- [ ] Each state's invalidation lifecycle matches the table (e.g. session cleared on logout, cached-remote invalidated on the declared trigger).

## Network layer

- [ ] The client uses the flavor base URL from `app_config.dart` — no hardcoded environment URLs.
- [ ] Request/response models are typed with explicit (de)serialization and honor the API contract.
- [ ] Transport and HTTP errors map to a single domain failure type; no `DioException`/`Map<String, dynamic>` leaks past the data layer.
- [ ] A logging interceptor routes through the scaffold tracing seam and redacts `Authorization` and PII.

## Auth-token plumbing

- [ ] Tokens are stored only via `flutter_secure_storage`; none appear in `SharedPreferences`, logs, crash custom keys, or analytics.
- [ ] Concurrent 401s trigger exactly one refresh (single-flight); in-flight requests queue and replay after it.
- [ ] A failed refresh clears tokens and flips the scaffold session shell to logged-out; queued requests fail cleanly.
- [ ] The scaffold's `// TODO(flutter-state-and-data-fetching)` token markers are replaced with the real implementation.

## Caching & offline

- [ ] The cache store implements stale-while-revalidate with the invalidation triggers from the State Management Strategy table.
- [ ] The offline mutation queue is persisted and survives process death (not in-memory).
- [ ] Replay is idempotent — each mutation carries an idempotency key and a double-replay is a no-op.
- [ ] Retry uses backoff with jitter and an explicit poison-message ceiling that parks and surfaces a stuck mutation.

## Optimistic updates & conflicts

- [ ] Every optimistic update captures prior state and has a rollback path on failure.
- [ ] Conflict resolution matches the rule in `mobile-architecture.md` — none is invented.
- [ ] Rollback surfaces failure per the degraded-mode UX in `mobile-architecture.md`.

## Push & background

- [ ] Push token registration and foreground/background/terminated handlers update state.
- [ ] Push handlers defer route resolution to `flutter-navigation-and-routing` — no `Navigator`/router calls in this layer.
- [ ] Background sync runs within the background-execution budget from the Performance & Battery / Notifications & Background sections.

## Tests & verification

- [ ] Unit test: single-flight refresh under concurrent 401s.
- [ ] Unit test: offline replay idempotency under double-replay.
- [ ] Unit test: optimistic rollback on mutation failure.
- [ ] `flutter analyze` reports zero issues (warnings included), or the skip is documented with reason.

## Standards conformance

- [ ] [api-standards](../../../../../../standards/api-standards/README.md): typed models honoring the REST/GraphQL/event contract; no ad-hoc shapes.
- [ ] [security-standards](../../../../../../standards/security-standards/README.md): tokens in secure storage only, never logged or persisted in plaintext; no secrets in the bundle.
- [ ] [observability-standards](../../../../../../standards/observability-standards/README.md): network tracing and request/response logging with token and PII redaction.
- [ ] [naming-conventions](../../../../../../standards/naming-conventions/README.md): repository, provider/notifier, model, and file naming.

## Failure handling

If a check fails:

1. Identify the missing or incorrect implementation.
2. Ask the user for clarification if the decision cannot be inferred from `mobile-architecture.md` or `architecture/security`.
3. Revise the implementation, re-run the failure-path unit tests, and re-run `flutter analyze`.
4. Keep any unresolved gap explicit — do not hide it as an assumption.
