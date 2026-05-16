# Flutter Navigation and Routing Playbook

Load this when implementing any owned area of `flutter-navigation-and-routing` or checking the anti-pattern list. It expands the operating rules and process steps in `SKILL.md` with the detail needed to produce a production-grade navigation layer.

## Why this workflow exists

Navigation bugs are the ones users hit first and report worst. A protected screen that paints for a frame before redirecting leaks data and looks broken. A deep link that trusts its parameters becomes an auth-gate bypass or an open redirect. An app with no state restoration drops the user back at the home screen every time the OS reclaims memory mid-task — which on a low-end Android happens constantly. None of these reproduce in a foreground demo with a logged-in user.

The goal is a navigation graph that treats deep links as hostile input, derives auth gating from session state without owning tokens, and survives process death — consuming architectural decisions instead of inventing them.

## Behavioral rules in depth

### 1. Consume architecture; do not invent it

Read the Navigation Architecture section of `mobile-architecture.md` and the auth-transition policy in `architecture/security` before defining a single route. Hierarchy, route ownership, modal strategy, tab/shell shape, and back/restoration behavior are architectural decisions. If a needed decision is missing, surface an ADR candidate before proceeding.

### 2. Extend the scaffold router placeholder

The scaffold left a router placeholder in `app/app.dart` and `// TODO(flutter-navigation-and-routing)` markers. Fill them. A second app root or a parallel router produces two navigation states that disagree about where the user is — back buttons go nowhere, deep links land on a dead tree.

### 3. Auth gating reads session state — never tokens

The redirect predicate observes the `flutter-state-and-data-fetching` session shell (logged-in / logged-out / unknown). This layer never reads secure storage, never refreshes a token, never decodes a JWT. Token lifecycle is the data layer's ownership; crossing that line couples two archetypes and duplicates the source of truth for "is the user authenticated."

### 4. Every deep link is hostile input

A deep link arrives from an email, an SMS, a QR code, another app — none trusted. Before routing:

| Check | Behavior on failure |
|---|---|
| Path matches a known route | Fall back to a safe default route |
| Path/query params are well-formed and in range | Reject the param; do not route with it |
| Target is not auth-gated for an unauthenticated user | Route through the auth gate, not around it |
| Redirect target (if any) is an allow-listed internal route | Refuse — never an open redirect |

A deep link must not reach a protected screen without passing the same auth gate as in-app navigation.

### 5. No flash of authenticated UI

The redirect must resolve before the protected screen's first build. With `go_router` this is the `redirect` callback returning the login location synchronously from session state — not a `build`-time check that renders the protected widget and then navigates away. A one-frame leak of authenticated content is a security finding, not a cosmetic bug.

### 6. State restoration is mandatory on mobile

The OS kills backgrounded apps to reclaim memory — routinely on low-end Android. Without restoration the user loses their place and any in-progress flow (a half-filled form, a multi-step checkout). Assign restoration IDs, use `RestorationMixin` for in-progress flow state, and restore the route stack to the screen the user left — not the home screen.

### 7. Back-stack behavior is explicit, not default

System back, Android predictive back, and the iOS interactive pop each follow the back-navigation rules in `mobile-architecture.md`. Where the document declares unsaved-changes interception, a `PopScope` (or equivalent) confirms before discarding. Default framework back behavior is acceptable only where the document says so.

### 8. Notification-to-route resolution consumes the seam — it does not own the payload

`flutter-state-and-data-fetching` ingests, persists, and exposes the push payload. This skill maps that payload to a route. It does not parse the raw `RemoteMessage`, does not persist anything, does not decide whether the payload was already handled. It receives a resolved intent from the seam and navigates.

### 9. A navigation graph not tested under failure is not done

The tests that matter: an unauthenticated deep link into a protected route (must redirect, must not flash), post-login redirect returning to the originally requested route, and restoration after simulated process death. Integration-test these explicitly.

## Step detail

**Step 1 — Gather context.** Load `mobile-architecture.md`; extract the full Navigation Architecture section and the routing/deep-link behavior under Notifications & Background Behavior. Extract auth-transition policy from `architecture/security`. Confirm the scaffold router placeholder and the state-layer session shell exist. Raise an ADR candidate for any missing decision.

**Step 2 — Router installation.** Install the architecture-named router in the scaffold `app/app.dart` placeholder. Wire `refreshListenable` (or equivalent) to the session shell so a session change re-evaluates redirects.

**Step 3 — Route hierarchy.** Build the route tree, nested/shell routes, and tab/shell architecture with route ownership exactly as the document specifies.

**Step 4 — Auth-gate routing.** Implement the redirect predicate from session state: unauthenticated → declared destination; authenticated on an auth screen → home; capture the requested location and return to it after login.

**Step 5 — Deep-link / app-link handling.** Register universal-link/app-link domains and association files (`apple-app-site-association`, `assetlinks.json`). Parse, validate, and sanitize every parameter per rule 4. Route valid links through the auth gate; fall back safely on invalid ones.

**Step 6 — Modal & back-stack.** Implement the modal strategy and system/predictive/interactive back behavior, including unsaved-changes interception where declared.

**Step 7 — State restoration.** Assign restoration IDs; use `RestorationMixin` for in-progress flow state; restore the route stack to the screen the user left.

**Step 8 — Notification-to-route resolution.** Consume the state-layer push seam and map the resolved payload to a route. No raw payload parsing or persistence here.

**Step 9 — Test and verify.** Integration-test unauthenticated-deep-link redirect (no flash), post-login redirect to requested route, and restoration after simulated process death. Run `flutter analyze`; fix every issue. Document any skipped check.

**Step 10 — Standards validation.** Check security-standards (deep-link validation, no bypass, no flash), observability-standards (navigation tracing), naming-conventions. Keep any unresolved gap explicit.

## Anti-patterns to detect

Call these out explicitly when found:

- A second app root or parallel router instead of extending the scaffold placeholder
- Auth gating that reads secure storage / decodes a token instead of observing the session shell
- A `build`-time auth check that renders the protected widget then navigates away (UI flash)
- Deep-link parameters used unvalidated, as an open redirect, or to bypass the auth gate
- No universal-link / app-link association files
- No state restoration — user dropped at home after process death
- Default back behavior where the architecture declares unsaved-changes interception
- This layer parsing or persisting the raw push `RemoteMessage` instead of consuming the state-layer seam
- Navigation/screen-view events not traced through the scaffold seam
- Failure-path tests (unauth deep link, post-login redirect, restoration) missing
