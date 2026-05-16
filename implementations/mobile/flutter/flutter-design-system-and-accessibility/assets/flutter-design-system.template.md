# Flutter Design System and Accessibility — Layout Reference

Use this as the canonical token, theming, and component-pattern reference. These files are **added to** the scaffold tree and fill the scaffold's ThemeData placeholder; they do not replace the app root. Placeholder tokens use `<kebab-case>` or `<PascalCase>`.

## Directory tree (added to the scaffold)

```
lib/
├── app/
│   └── app.dart                        # EXTEND the scaffold ThemeData placeholder here
├── design_system/
│   ├── tokens/
│   │   ├── color_tokens.dart           # semantic color (light + dark + brand)
│   │   ├── type_tokens.dart            # type scale
│   │   ├── spacing_tokens.dart         # spacing / radius / elevation
│   │   └── motion_tokens.dart          # durations + curves (reduced-motion aware)
│   ├── theme/
│   │   └── app_theme.dart              # ThemeData built from tokens
│   └── components/
│       ├── app_button.dart             # accessible primitive (semantics + ≥48dp)
│       └── app_text_field.dart         # masked-secret + autofill posture
├── l10n/
│   ├── app_en.arb                      # i18n seam (one locale ok to start)
│   └── l10n.dart                       # generated localization delegate
└── permissions/
    └── permission_request_ux.dart      # rationale / granted / denied / blocked UX
```

## Tokens are the only source of truth

```dart
// design_system/tokens/color_tokens.dart
abstract final class ColorTokens {
  static const surface      = Color(0xFF111317);
  static const onSurface    = Color(0xFFE6E8EB);   // AA-verified on `surface`
  static const accent       = Color(0xFF4C8DFF);
}

// Feature widgets reference ColorTokens.* / SpacingTokens.* — never raw hex
// or EdgeInsets.all(16). Raw values in feature code are a defect.
```

## Theme installed into the scaffold seam

```dart
// app/app.dart  (scaffold left: // TODO(flutter-design-system-and-accessibility))
MaterialApp.router(
  theme: AppTheme.light,                 // built from tokens
  darkTheme: AppTheme.dark,
  localizationsDelegates: AppLocalizations.localizationsDelegates,
  supportedLocales: AppLocalizations.supportedLocales,
  routerConfig: appRouter,               // owned by flutter-navigation-and-routing
);
```

## Accessible component pattern

```dart
class AppIconButton extends StatelessWidget {
  const AppIconButton({required this.icon, required this.label, required this.onTap});
  final IconData icon; final String label; final VoidCallback onTap;

  @override
  Widget build(BuildContext context) => Semantics(
    button: true,
    label: label,                                  // screen-reader reachable
    child: InkWell(
      onTap: onTap,
      child: ConstrainedBox(
        constraints: const BoxConstraints(minWidth: 48, minHeight: 48), // ≥48dp
        child: Icon(icon, color: ColorTokens.onSurface),
      ),
    ),
  );
}
```

## Font scale & reduced motion

```dart
// Reflow, don't clip, at large textScaleFactor:
Wrap(children: [...]);                              // not a fixed-height Row

// Honor reduced motion:
final reduceMotion = MediaQuery.of(context).disableAnimations;
final duration = reduceMotion ? Duration.zero : MotionTokens.standard;
```

## RTL-correct layout

```dart
// CORRECT — mirrors in RTL locales:
padding: const EdgeInsetsDirectional.only(start: 16, end: 8);
// WRONG in an RTL-supported app:
// padding: const EdgeInsets.only(left: 16, right: 8);
```

## Permission UX — own the experience, not the engine

```dart
// Explain BEFORE the OS prompt; handle blocked distinctly.
switch (status) {
  case PermissionStatus.notRequested:
    return RationaleSheet(onContinue: requestViaEngine);   // engine = state/scaffold
  case PermissionStatus.granted:
    return child;
  case PermissionStatus.denied:
    return DeniedInline(onRetry: requestViaEngine);
  case PermissionStatus.permanentlyBlocked:
    return BlockedCard(onOpenSettings: openAppSettings);   // no re-prompt loop
}
// This file renders the UX. It does NOT call the native permission API.
```

## Accessible, secret-safe auth field

```dart
AppTextField(
  label: l10n.password,
  obscureText: true,                       // masked
  autofillHints: const [AutofillHints.password],   // per architecture/security
  // value never logged, never in analytics, excluded from screenshots where supported
);
```

## Seams this skill fills and defers

| Seam | File | Status |
|---|---|---|
| Design tokens & theming | `app/app.dart` (scaffold ThemeData placeholder) | filled by this skill |
| i18n delegate | `l10n/l10n.dart` | filled by this skill |
| Permission-request UX | `permissions/permission_request_ux.dart` | filled by this skill |
| Native permission engine | n/a here | owned by `flutter-state-and-data-fetching` / scaffold |
| Layout placement / routing | n/a here | owned by `flutter-navigation-and-routing` |
| Auth state | n/a here | owned by `flutter-state-and-data-fetching` |
