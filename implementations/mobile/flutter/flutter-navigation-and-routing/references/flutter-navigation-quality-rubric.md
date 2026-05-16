# Flutter Navigation and Routing Quality Rubric

Load this before declaring the navigation layer complete. Revise until each check passes or the unresolved gap is explicitly documented.

## Router & hierarchy

- [ ] Router matches the one named in `mobile-architecture.md`, or is documented as deferred with a pending ADR candidate.
- [ ] The router extends the scaffold `app/app.dart` placeholder — there is no second app root or parallel router.
- [ ] The route tree, nested/shell routes, and tab/shell architecture match the Navigation Architecture decisions and route ownership.
- [ ] The router re-evaluates redirects when the session shell changes (wired as a refresh listenable).

## Auth-gate routing

- [ ] The redirect predicate derives from the `flutter-state-and-data-fetching` session shell — no token reads, no JWT decode, no secure-storage access.
- [ ] An unauthenticated request to a protected route redirects before any protected content paints (no authenticated-UI flash).
- [ ] An authenticated user on an auth screen is redirected away from it.
- [ ] Post-login redirect returns the user to the originally requested route.

## Deep links & app links

- [ ] Universal-link / app-link domains are registered with association files (`apple-app-site-association`, `assetlinks.json`).
- [ ] Every deep-link path and query parameter is validated and sanitized before routing.
- [ ] Malformed or unknown links fall back to a safe default route.
- [ ] No deep-link parameter bypasses the auth gate or acts as an open redirect.

## Modal, back-stack & restoration

- [ ] Modal strategy matches `mobile-architecture.md`.
- [ ] System back, Android predictive back, and iOS interactive pop follow the document's back-navigation rules.
- [ ] Unsaved-changes interception is implemented where the document declares it.
- [ ] Route stack and in-progress flow state survive process death and restore to the screen the user left (not the home screen).

## Notifications

- [ ] Notification-payload-to-route resolution consumes the state-layer push seam.
- [ ] This layer does not parse the raw `RemoteMessage` or persist the payload (owned by `flutter-state-and-data-fetching`).

## Tests & verification

- [ ] Integration test: unauthenticated deep link into a protected route redirects without a content flash.
- [ ] Integration test: post-login redirect returns to the originally requested route.
- [ ] Integration test: route stack and flow state restore after simulated process death.
- [ ] `flutter analyze` reports zero issues (warnings included), or the skip is documented with reason.

## Standards conformance

- [ ] [security-standards](../../../../../standards/security-standards/README.md): deep-link input validation, no open redirect, no auth-gate bypass, no protected content painted before the gate resolves.
- [ ] [observability-standards](../../../../../standards/observability-standards/README.md): navigation and screen-view tracing wired through the scaffold seam.
- [ ] [naming-conventions](../../../../../standards/naming-conventions/README.md): route names, path segments, and file naming.

## Failure handling

If a check fails:

1. Identify the missing or incorrect implementation.
2. Ask the user for clarification if the decision cannot be inferred from `mobile-architecture.md` or `architecture/security`.
3. Revise the implementation, re-run the failure-path integration tests, and re-run `flutter analyze`.
4. Keep any unresolved gap explicit — do not hide it as an assumption.
