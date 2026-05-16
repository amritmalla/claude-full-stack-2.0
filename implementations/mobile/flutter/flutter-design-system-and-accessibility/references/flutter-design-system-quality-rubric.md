# Flutter Design System and Accessibility Quality Rubric

Load this before declaring the design-system layer complete. Revise until each check passes or the unresolved gap is explicitly documented.

## Tokens & theming

- [ ] Semantic tokens (color, type scale, spacing, radius, elevation, motion) are defined as the single source of truth.
- [ ] Light, dark, and any brand variants are derived from tokens.
- [ ] The theme is installed into the scaffold `app/app.dart` ThemeData seam — there is no second theme source or parallel app root.
- [ ] No raw hex, magic-number spacing, or ad-hoc `TextStyle` appears in feature widgets.

## Component library & accessibility

- [ ] Components consume tokens only.
- [ ] Every interactive component declares a meaningful screen-reader semantics label/hint; decorative elements are excluded from semantics.
- [ ] Every interactive component has a ≥48dp touch target.
- [ ] Text and key UI meet WCAG AA contrast (4.5:1 / 3:1) in light and dark themes.
- [ ] Selected/disabled/error states are conveyed non-visually, not by color alone.
- [ ] Focus/traversal order is logical with no traps.

## Font scale, motion, RTL & i18n

- [ ] Core screens remain usable at the maximum supported font scale — no clipped, overlapped, or truncated critical content.
- [ ] Animations honor the platform reduced-motion setting and degrade gracefully.
- [ ] RTL uses directional primitives (`EdgeInsetsDirectional`, `start`/`end`) and mirrors correctly where RTL is in scope.
- [ ] User-facing strings route through the i18n seam where localization is in scope; the localization delegate is installed.

## Permission & auth UX

- [ ] Permission UX explains value before the OS prompt and requests the minimum scope.
- [ ] Denied and permanently-blocked states are handled distinctly; blocked offers a system-settings deep link.
- [ ] A permanently-blocked permission is never re-prompted in a loop.
- [ ] This layer does not call the native permission API (engine owned by `flutter-state-and-data-fetching` / scaffold).
- [ ] Auth UIs mask secrets, keep them out of logs and screenshots, and follow the `architecture/security` autofill/paste posture.

## Tests & verification

- [ ] Screen-reader traversal of core flows verified (TalkBack/VoiceOver or semantics debugger).
- [ ] Core screens rendered and verified at maximum font scale.
- [ ] Reduced-motion behavior verified.
- [ ] RTL mirroring verified where RTL is in scope.
- [ ] `flutter analyze` reports zero issues (warnings included), or the skip is documented with reason.

## Standards conformance

- [ ] [security-standards](../../../../../standards/security-standards/README.md): permission minimization; auth UIs mask secrets and keep them out of logs/screenshots.
- [ ] [observability-standards](../../../../../standards/observability-standards/README.md): permission-decision and accessibility analytics wired through the scaffold seam without PII or secrets.
- [ ] [naming-conventions](../../../../../standards/naming-conventions/README.md): token, component, and file naming.
- [ ] WCAG AA mobile posture (screen-reader operability, ≥48dp targets, AA contrast, font-scale resilience, reduced motion, RTL) is met as a non-optional part of the output.

## Failure handling

If a check fails:

1. Identify the missing or incorrect implementation.
2. Ask the user for clarification if the decision cannot be inferred from `mobile-architecture.md` or `architecture/security`.
3. Revise the implementation, re-run the accessibility verifications, and re-run `flutter analyze`.
4. Keep any unresolved gap explicit — do not hide it as an assumption.
