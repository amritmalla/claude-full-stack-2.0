# Flutter Design System and Accessibility Playbook

Load this when implementing any owned area of `flutter-design-system-and-accessibility` or checking the anti-pattern list. It expands the operating rules and process steps in `SKILL.md` with the detail needed to produce a production-grade, accessible design system.

## Why this workflow exists

An inaccessible UI excludes real users and, in many markets, is a legal liability. The failures are invisible to a sighted developer on a default-font device: an icon button with no semantic label is a dead end for a screen-reader user; a hardcoded `16px` row clips at 200% font scale; a left-padded card looks broken in Arabic; a permission prompt that fires on launch with no rationale gets denied forever, breaking the feature it gates. None of this shows up in a quick visual check.

The goal is a token-driven, screen-reader-operable, font-scale-resilient, RTL-correct component library with permission UX that survives a double-denial — consuming architectural decisions instead of inventing them.

## Behavioral rules in depth

### 1. Consume architecture; do not invent it

Read the Accessibility & Localization section and the Device Capability Integration permission strategy in `mobile-architecture.md`, plus the auth-UI posture in `architecture/security`, before building a component. The contrast target, RTL decision, supported font-scale range, and permission strategy are architectural decisions. If a needed decision is missing, surface an ADR candidate.

### 2. Extend the scaffold ThemeData seam

The scaffold left a ThemeData placeholder in `app/app.dart` with a `// TODO(flutter-design-system-and-accessibility)` marker. Build the theme from tokens and install it there. A second `MaterialApp` or a competing theme source produces components that disagree about color and type.

### 3. Tokens are the only source of truth

Define semantic tokens — `colorSurface`, `textBody`, `spaceMd`, `radiusCard`, `motionStandard` — not raw values scattered through widgets. A feature widget using `Color(0xFF...)` or `EdgeInsets.all(16)` directly is a defect: it cannot be re-themed, dark-moded, or audited.

### 4. Accessibility is built in, never bolted on

Every interactive component, at creation time:

| Concern | Requirement |
|---|---|
| Screen reader | A meaningful `Semantics` label/hint; decorative elements excluded |
| Touch target | ≥48dp hit area even if the visual is smaller |
| Contrast | WCAG AA (4.5:1 text / 3:1 large text and UI) in light and dark |
| Focus order | Logical traversal order; no traps |
| State | Selected/disabled/error conveyed non-visually, not by color alone |

### 5. Text scales; layout must not break

Test every core screen at the maximum supported `textScaleFactor`. Use flexible layout (`Flexible`, `Wrap`, scrollable containers) so larger text reflows instead of clipping. Fixed-height rows holding scalable text are a defect.

### 6. Reduced motion is honored

Check `MediaQuery.disableAnimations` (or the platform reduced-motion signal). When set, transitions and decorative animation degrade to instant or minimal. Motion that conveys meaning gets a non-motion equivalent.

### 7. RTL is a direction, not an afterthought

When RTL is in scope, use `EdgeInsetsDirectional`, `AlignmentDirectional`, `start`/`end`, and directional icons. Verify the app under `Directionality(textDirection: TextDirection.rtl)`. Hardcoded `left`/`right` is a defect in an RTL-supported app.

### 8. The i18n seam exists from the start

All user-facing strings route through the localization delegate even if one locale ships first. Retrofitting i18n means re-touching every widget; the seam is cheap now and expensive later.

### 9. Permission UX owns the experience, not the engine

This skill builds the pre-permission rationale screen, the granted path, the denied state, and the distinct permanently-blocked state (with a deep link to system settings). It does **not** call the native permission API — that engine is `flutter-state-and-data-fetching` / the scaffold's platform-channel surface. Request the minimum scope, explain value before the OS prompt, and never re-prompt a permanently-blocked permission in a loop.

### 10. Auth UIs never leak secrets

Password/OTP fields are obscured, excluded from screenshots where the platform supports it, never logged, and follow the autofill/paste posture from `architecture/security`. An accessible auth screen is still a secure one.

### 11. A component library not tested with a screen reader is not done

Run TalkBack/VoiceOver (or the Flutter semantics debugger) through the core flows, render at max font scale, toggle reduced motion, and flip to RTL where in scope. These are the checks that catch the real defects.

## Step detail

**Step 1 — Gather context.** Load `mobile-architecture.md`; extract Accessibility & Localization and the Device Capability Integration permission strategy. Extract auth-UI posture from `architecture/security` where relevant. Confirm the scaffold ThemeData seam. Raise an ADR candidate for any missing decision.

**Step 2 — Token layer.** Define semantic color, type-scale, spacing, radius, elevation, and motion tokens with light/dark and brand variants. No raw values outside the token definitions.

**Step 3 — Theming.** Build `ThemeData` (and Cupertino theme where used) from tokens; install into the scaffold `app/app.dart` seam.

**Step 4 — Component library.** Compose primitives and components consuming tokens only; each declares semantics, a ≥48dp target, and AA contrast; state conveyed non-visually.

**Step 5 — Accessibility posture.** Implement screen-reader semantics, font-scale-resilient layout, reduced-motion handling, and AA contrast verification.

**Step 6 — RTL & i18n.** Install the localization delegate and i18n seam; use directional primitives; verify RTL mirroring where in scope.

**Step 7 — Permission-request UX.** Build rationale → request → granted, and distinct denied and permanently-blocked states with a settings deep link. Consume the permission strategy; do not call the native API.

**Step 8 — Accessible auth UIs.** Build login/MFA/recovery with masked input, screen-reader labels, font-scale resilience, and the `architecture/security` autofill/paste posture.

**Step 9 — Test and verify.** Screen-reader traversal of core flows, max-font-scale render, reduced-motion behavior, RTL mirroring. Run `flutter analyze`; fix every issue. Document skips.

**Step 10 — Standards validation.** Check security-standards (permission minimization, auth-secret handling), observability-standards (PII-free analytics), naming-conventions, WCAG AA mobile posture. Keep gaps explicit.

## Anti-patterns to detect

Call these out explicitly when found:

- A second `MaterialApp`/theme source instead of extending the scaffold ThemeData seam
- Raw hex, magic-number spacing, or ad-hoc `TextStyle` in feature widgets
- Icon/image buttons with no `Semantics` label
- Touch targets smaller than 48dp
- Fixed-height containers that clip text at large font scale
- Animations that ignore the reduced-motion setting
- Hardcoded `left`/`right` padding/alignment in an RTL-supported app
- Literal user-facing strings bypassing the i18n seam
- Permission prompt on launch with no rationale; re-prompting a permanently-blocked permission
- This layer calling the native permission API instead of consuming the engine
- Auth fields unobscured, logged, or screenshot-exposed
- Core flows never traversed with a screen reader or at max font scale
