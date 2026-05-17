# Flutter State and Data Fetching — Layout Reference

Use this as the canonical layer-layout and code-pattern reference. These directories are **added to** the scaffold tree; they do not replace it. Placeholder tokens use `<kebab-case>` or `<PascalCase>`. All dependency versions are pinned examples — replace with the exact current stable release; never use `^`.

## Directory tree (added to the scaffold)

```
lib/
├── core/
│   ├── di/
│   │   └── injection.dart              # EXTEND the scaffold seam — register the items below here
│   ├── network/
│   │   ├── api_client.dart             # typed client (dio/http) + flavor base URL
│   │   ├── interceptors/
│   │   │   ├── auth_interceptor.dart   # attaches token; single-flight refresh on 401
│   │   │   └── logging_interceptor.dart# routes to scaffold tracing seam; redacts auth/PII
│   │   └── failure.dart                # domain Failure type (no DioException leaks)
│   ├── auth/
│   │   ├── secure_token_store.dart     # flutter_secure_storage only
│   │   └── session_controller.dart     # flips the scaffold session shell
│   ├── cache/
│   │   └── cache_store.dart            # stale-while-revalidate + invalidation
│   └── offline/
│       ├── mutation_queue.dart         # persisted, idempotent, bounded retry
│       └── connectivity_listener.dart  # drains queue on reconnect
├── features/
│   └── <feature-name>/
│       ├── data/
│       │   ├── <feature>_repository.dart
│       │   └── models/<feature>_dto.dart
│       └── presentation/
│           └── <feature>_notifier.dart # one State Management Strategy row
└── notifications/
    └── push_delivery.dart              # payload → state; defers route to navigation seam
```

## State notifier pattern (Riverpod example — use the mechanism from mobile-architecture.md)

```dart
// One provider per State Management Strategy row. Ownership and invalidation
// lifecycle come from the table — do not invent them.
final <feature>Provider =
    StateNotifierProvider<<Feature>Notifier, AsyncValue<<Feature>State>>((ref) {
  return <Feature>Notifier(ref.read(<feature>RepositoryProvider));
});

class <Feature>Notifier extends StateNotifier<AsyncValue<<Feature>State>> {
  <Feature>Notifier(this._repo) : super(const AsyncValue.loading());
  final <Feature>Repository _repo;

  Future<void> load() async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(_repo.fetch);
  }
}
```

## Single-flight refresh (the race that matters)

```dart
class AuthInterceptor extends Interceptor {
  AuthInterceptor(this._store, this._session, this._refreshApi);
  final SecureTokenStore _store;
  final SessionController _session;
  final RefreshApi _refreshApi;

  Future<void>? _inFlightRefresh; // shared across concurrent 401s

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) async {
    if (err.response?.statusCode != 401) return handler.next(err);

    _inFlightRefresh ??= _refresh();          // exactly one refresh
    try {
      await _inFlightRefresh;                 // concurrent 401s await it
      final retried = await _retry(err.requestOptions);
      handler.resolve(retried);
    } catch (_) {
      await _store.clear();
      _session.markLoggedOut();               // flips the scaffold session shell
      handler.next(err);
    } finally {
      _inFlightRefresh = null;
    }
  }

  Future<void> _refresh() async {
    final next = await _refreshApi.refresh(await _store.refreshToken());
    await _store.save(next);
  }
}
```

## Durable, idempotent offline queue

```dart
class QueuedMutation {
  final String idempotencyKey; // client-generated; double-replay = no-op
  final String endpoint;
  final Map<String, dynamic> payload;
  int attempts;
}

// Persisted (Hive/Drift/SQLite per architecture) — NOT in-memory.
// Replay: skip if server already saw idempotencyKey.
// Retry: exponential backoff + jitter; park after `maxAttempts` (poison ceiling).
```

## Optimistic update with rollback

```dart
Future<void> toggleFavorite(Item item) async {
  final prior = state;                         // capture for rollback
  state = state.withFavorite(item.id, true);   // optimistic apply
  try {
    await _repo.setFavorite(item.id, true);
  } catch (e) {
    state = prior;                             // rollback
    _surfaceDegradedModeUx(e);                 // per mobile-architecture.md
  }
}
```

## Push delivery — payload only, no navigation

```dart
// Updates state and hands the payload to the navigation seam.
// Resolving payload -> route is flutter-navigation-and-routing's ownership.
void onMessage(RemoteMessage m) {
  _repo.ingestPushPayload(m.data);
  // TODO(flutter-navigation-and-routing): resolve m.data -> route
}
```

## Seams this skill fills and exposes

| Seam | File | Status |
|---|---|---|
| Auth session provider | `core/di/injection.dart` (scaffold shell) | filled by this skill |
| Token storage and refresh | `core/auth/secure_token_store.dart` + `auth_interceptor.dart` | filled by this skill |
| Push payload → route | `notifications/push_delivery.dart` (TODO marker) | deferred to `flutter-navigation-and-routing` |
| Protected-route gates | n/a here | owned by `flutter-navigation-and-routing` |
| Network tracing | scaffold `perf_tracer.dart` seam | consumed by this skill's logging interceptor |
