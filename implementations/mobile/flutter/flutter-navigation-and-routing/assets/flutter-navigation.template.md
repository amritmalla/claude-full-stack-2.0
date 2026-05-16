# Flutter Navigation and Routing — Layout Reference

Use this as the canonical router-layout and code-pattern reference. These files are **added to** the scaffold tree and fill the scaffold's router placeholder; they do not replace the app root. Placeholder tokens use `<kebab-case>` or `<PascalCase>`. Dependency versions are pinned examples — replace with the exact current stable release; never use `^`.

## Directory tree (added to the scaffold)

```
lib/
├── app/
│   └── app.dart                        # EXTEND the scaffold router placeholder here
└── navigation/
    ├── app_router.dart                 # router (go_router/auto_route) + redirect
    ├── routes.dart                     # typed route names / paths (no magic strings)
    ├── auth_gate.dart                  # redirect predicate from the session shell
    ├── deep_link_parser.dart           # validates + sanitizes every parameter
    ├── shell/
    │   └── tab_shell.dart              # tab/shell architecture per mobile-architecture.md
    └── restoration/
        └── flow_restoration.dart       # RestorationMixin for in-progress flow state

ios/Runner/
└── apple-app-site-association          # universal-link association (no extension)
android/app/src/main/res/...
└── assetlinks.json                     # app-link association
```

## Router wired to the session shell (go_router example — use the router from mobile-architecture.md)

```dart
GoRouter buildRouter(SessionShell session) => GoRouter(
  refreshListenable: session,            // re-evaluates redirect on session change
  initialLocation: Routes.home,
  redirect: (context, state) {
    final loggingIn = state.matchedLocation == Routes.login;
    final authed = session.status == SessionStatus.authenticated;

    if (!authed && _isProtected(state.matchedLocation)) {
      // Synchronous redirect — protected screen never builds. No UI flash.
      return '${Routes.login}?from=${Uri.encodeComponent(state.matchedLocation)}';
    }
    if (authed && loggingIn) return Routes.home;
    return null;
  },
  routes: [ /* hierarchy + shell routes per mobile-architecture.md */ ],
);
```

## Auth gate reads session state — never tokens

```dart
// CORRECT: observes the flutter-state-and-data-fetching session shell.
bool _isProtected(String location) => Routes.protected.contains(location);

// WRONG (do not do this here):
//   final token = await secureStorage.read(key: 'access');   // token logic
//   if (JwtDecoder.isExpired(token)) ...                      // belongs to data layer
```

## Deep link as hostile input

```dart
Uri? resolveDeepLink(Uri incoming) {
  final route = Routes.match(incoming.path);
  if (route == null) return Uri.parse(Routes.home);          // unknown -> safe default

  final id = incoming.queryParameters['id'];
  if (id == null || !_isValidId(id)) return Uri.parse(route); // reject bad param

  final from = incoming.queryParameters['from'];
  if (from != null && !Routes.isInternal(from)) return null;  // no open redirect

  return Uri.parse('$route?id=$id');
}
```

## Post-login return-to-requested-route

```dart
// Login screen reads ?from= and returns there after auth succeeds.
final from = state.uri.queryParameters['from'];
onLoginSuccess: () => context.go(
  (from != null && Routes.isInternal(from)) ? from : Routes.home,
);
```

## State restoration across process death

```dart
class CheckoutFlow extends StatefulWidget { /* ... */ }

class _CheckoutFlowState extends State<CheckoutFlow> with RestorationMixin {
  final RestorableInt _step = RestorableInt(0);

  @override
  String? get restorationId => 'checkout_flow';

  @override
  void restoreState(RestorationBucket? oldBucket, bool initialRestore) {
    registerForRestoration(_step, 'step');   // survives OS kill; restores the step
  }
}
```

## Notification → route: consume the seam, do not own the payload

```dart
// flutter-state-and-data-fetching ingested + exposed the resolved intent.
// This skill only maps it to a route.
void onPushIntent(PushIntent intent) {        // from the state-layer seam
  final route = Routes.forPushKind(intent.kind);
  _router.go(route, extra: intent.refId);
}
// Do NOT parse RemoteMessage or persist anything here.
```

## Seams this skill fills and consumes

| Seam | File | Status |
|---|---|---|
| Navigation router | `app/app.dart` (scaffold placeholder) | filled by this skill |
| Protected-route gates | `navigation/auth_gate.dart` | filled by this skill |
| Session shell (auth state) | state layer | consumed (read-only) |
| Push payload → route | state-layer push seam | consumed by `navigation/...` |
| Navigation tracing | scaffold `perf_tracer.dart` seam | consumed by this skill |
| Token storage / refresh | n/a here | owned by `flutter-state-and-data-fetching` |
