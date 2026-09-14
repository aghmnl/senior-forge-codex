---
layout: post
title: "Crashlytics"
date: 2026-09-13 12:00:00 +0000
categories: [en, glossary]
tags: [error-handling, android-framework, build-tools]
lang: en
permalink: /en/glossary/crashlytics/
---

## The Theory (The What)

**Firebase Crashlytics** is the crash-reporting service most Android apps ship with. The SDK installs an uncaught-exception handler, captures the [stack trace]({{ "/en/glossary/stack-trace/" | relative_url }}), device state and breadcrumbs, and uploads them on the next launch; the console groups reports by root cause and tracks crash-free users per version.

```xml
<!-- From FollowApp Suite — AndroidManifest.xml -->
<!-- Crashlytics collection: false in debug, true in release. -->
<meta-data
    android:name="firebase_crashlytics_collection_enabled"
    android:value="${crashlyticsCollectionEnabled}" />
```

FAS disables collection in debug builds through a manifest placeholder, so development crashes never pollute the production dashboard, and turns it on only in `release`.

## The Senior Nuance

- **The mapping upload is the feature that matters.** Release builds are [obfuscated]({{ "/en/glossary/obfuscation/" | relative_url }}) by [R8]({{ "/en/glossary/r8/" | relative_url }}); the Crashlytics Gradle plugin uploads `mapping.txt` at build time so the console shows real class and method names. Without it every crash reads `a.b.c` and grouping breaks.
- **[NullPointerException]({{ "/en/glossary/null-pointer-exception/" | relative_url }}) is consistently the top category.** Most originate at Java/Kotlin interop boundaries — [platform types]({{ "/en/glossary/platform-types/" | relative_url }}) — or from `!!`. The report tells you *where*; only a meaningful exception message tells you *which* [invariant]({{ "/en/glossary/invariant/" | relative_url }}) broke.
- **Non-fatal reports are for handled failures you still want to see.** `recordException(e)` in a `catch` sends the trace without crashing. Use it for "should never happen" branches; do not use it as logging.
- **Custom keys and logs give context the trace lacks.** Setting the current screen, user tier or feature flag before the crash turns "NPE in `TasksViewModel`" into "NPE in `TasksViewModel` on the archive flow with grouping enabled".

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
