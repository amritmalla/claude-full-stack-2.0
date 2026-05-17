# Flutter App Scaffold — Layout Reference

Use this as the canonical directory-layout and entry-point reference when generating a Flutter app scaffold. Placeholder tokens use `<kebab-case>` or `<PascalCase>` style.

## Directory tree

```
<app-name>/
├── pubspec.yaml                          # all deps pinned — no ^
├── pubspec.lock                          # committed
├── analysis_options.yaml                 # strict lints
├── .gitignore                            # covers .env, signing artifacts, build/, .dart_tool/
├── .env.example                          # documents env vars; placeholder values only
├── lib/
│   ├── main_dev.dart                     # flutter run --flavor dev -t lib/main_dev.dart
│   ├── main_staging.dart                 # flutter run --flavor staging -t lib/main_staging.dart
│   ├── main_prod.dart                    # flutter run --flavor prod -t lib/main_prod.dart
│   ├── app/
│   │   ├── app.dart                      # root MaterialApp / CupertinoApp widget
│   │   └── app_config.dart               # Flavor enum + flavor-specific constants
│   ├── core/
│   │   ├── di/
│   │   │   └── injection.dart            # DI registration seam (<container> from mobile-architecture.md)
│   │   ├── error/
│   │   │   ├── error_handler.dart        # PlatformDispatcher + FlutterError overrides
│   │   │   └── fallback_widget.dart      # ErrorWidget.builder safe fallback
│   │   ├── logging/
│   │   │   └── app_logger.dart           # level- and flavor-aware structured logger
│   │   └── observability/
│   │       ├── crash_reporter.dart       # crash reporting seam (<vendor> from mobile-architecture.md)
│   │       └── perf_tracer.dart          # performance tracing seam
│   ├── features/
│   │   └── <feature-name>/               # one directory per feature
│   │       ├── data/
│   │       ├── domain/
│   │       └── presentation/
│   └── shared/
│       └── widgets/
├── test/
│   └── widget_test.dart
├── integration_test/
│   └── app_test.dart
├── android/
│   └── app/
│       └── build.gradle                  # productFlavors block: dev / staging / prod
├── ios/
│   └── Runner.xcodeproj/                 # scheme targets: Dev / Staging / Prod
└── fastlane/                             # or codemagic.yml at repo root
    ├── Appfile                           # app_identifier + team_id via ENV[]
    ├── Fastfile                          # flavor-aware lanes; signing via ENV[]
    ├── Gemfile                           # pins fastlane gem version
    └── README.md                         # lists all required ENV vars and purpose
```

## pubspec.yaml stub

```yaml
name: <app-name>
description: <description>
version: 1.0.0+1

environment:
  sdk: ">=3.3.0 <4.0.0"
  flutter: ">=3.19.0"

dependencies:
  flutter:
    sdk: flutter

  # --- Observability (<vendor> from mobile-architecture.md) ---
  # firebase_core: 2.27.0        # if Crashlytics
  # firebase_crashlytics: 3.4.9
  # sentry_flutter: 7.18.0       # if Sentry

  # --- Logging ---
  logger: 2.3.0

  # --- DI (<container> from mobile-architecture.md) ---
  # get_it: 7.6.7                # if GetIt
  # flutter_riverpod: 2.5.1      # if Riverpod

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: 4.0.0
  integration_test:
    sdk: flutter
```

All versions are pinned examples — replace with the exact current stable release at scaffold time. Never use `^`.

## Flavor entry-point pattern

```dart
// lib/main_dev.dart
import 'dart:async';
import 'package:<app_name>/app/app.dart';
import 'package:<app_name>/app/app_config.dart';
import 'package:<app_name>/core/di/injection.dart';
import 'package:<app_name>/core/error/error_handler.dart';
import 'package:<app_name>/core/observability/crash_reporter.dart';
import 'package:<app_name>/core/observability/perf_tracer.dart';
import 'package:flutter/material.dart';

void main() {
  AppConfig.setFlavor(Flavor.dev);
  runZonedGuarded(
    () async {
      WidgetsFlutterBinding.ensureInitialized();
      await CrashReporter.init(flavor: Flavor.dev);
      await PerfTracer.init(flavor: Flavor.dev);
      setupErrorHandlers(flavor: Flavor.dev);  // PlatformDispatcher + FlutterError
      setupDependencies();                      // DI registration seam
      runApp(const App());
    },
    (error, stack) => CrashReporter.recordError(error, stack, fatal: true),
  );
}
```

Repeat for `main_staging.dart` and `main_prod.dart` with the appropriate `Flavor` value.

## app_config.dart pattern

```dart
// lib/app/app_config.dart
enum Flavor { dev, staging, prod }

class AppConfig {
  static Flavor _flavor = Flavor.dev;

  static void setFlavor(Flavor flavor) => _flavor = flavor;
  static Flavor get flavor => _flavor;

  static bool get isDev => _flavor == Flavor.dev;
  static bool get isProd => _flavor == Flavor.prod;

  // Populate from dart-define or flavor-specific config files:
  static String get apiBaseUrl => const String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'https://api-dev.<app-name>.example',
  );
}
```

## Seams for downstream archetypes

Document these explicitly in the local-run README:

| Seam | File | Filled by |
|---|---|---|
| Navigation router | `app/app.dart` (router placeholder) | `flutter-navigation-and-routing` |
| Auth session provider | `core/di/injection.dart` (session shell) | `flutter-state-and-data-fetching` |
| Token storage and refresh | `core/di/injection.dart` (TODO comment) | `flutter-state-and-data-fetching` |
| Protected-route gates | `app/app.dart` (TODO comment) | `flutter-navigation-and-routing` |
| Design tokens and theming | `app/app.dart` (ThemeData placeholder) | `flutter-design-system-and-accessibility` |
| Performance budget CI gates | CI configuration | `flutter-performance-and-reliability` |

## .gitignore additions (signing and secrets)

```
# Secrets and environment
.env
.env.*
!.env.example

# Android signing
android/key.properties
*.jks
*.keystore

# iOS signing
*.mobileprovision
*.p12
*.cer

# Firebase / Google services (with real credentials)
google-services.json
GoogleService-Info.plist
firebase_options.dart   # if generated with real API keys — document in README instead

# Flutter build
build/
.dart_tool/
.flutter-plugins
.flutter-plugins-dependencies
```
