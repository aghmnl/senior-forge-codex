---
layout: post
title: "Application.onCreate()"
date: 2026-09-17 12:00:00 +0000
categories: [en, glossary]
tags: [android-framework, lifecycle, performance]
lang: en
permalink: /en/glossary/application-on-create/
---

## The Theory (The What)

**`Application.onCreate()`** is the first app code that runs when the process starts — before any `Activity`, `Service` or `BroadcastReceiver`, on the [main thread]({{ "/en/glossary/main-thread/" | relative_url }}), and *inside* the cold-start window the user experiences as the splash. Everything you put there is paid on every launch and delays the first frame. It is where DI graphs are built, where [`StrictMode`]({{ "/en/glossary/strict-mode/" | relative_url }}) is configured, and — too often — where [SDK]({{ "/en/glossary/sdk/" | relative_url }})s are initialised.

```kotlin
// From FollowApp Suite — MyTasksApplication.kt
override fun onCreate() {
    super.onCreate()
    // Read the persisted appearance settings BEFORE any Activity is
    // inflated so the OS picks the right locale + night mode from the
    // very first frame. [...] All three values live in the same
    // "settings" DataStore — reading them in a single runBlocking
    // triggers exactly one cold file open.
    val (language, themeMode, contrastLevel) = runBlocking {
        Triple(
            languagePreferences.getLanguage().first(),
            themePreferences.getThemeMode().first(),
            /* ... */
        )
    }
    // ...
}
```

## The Senior Nuance

- **Blocking here is sometimes a deliberate trade.** The example above runs [`runBlocking`]({{ "/en/glossary/run-blocking/" | relative_url }}) on Main on purpose: reading theme and locale *before* the first Activity avoids a visible flash on every launch. The comment documents the cost (one cold file open) and the reason. That is the difference between a decision and an accident.
- **Everything else should leave.** SDK bootstraps, analytics, crash reporters: move to a background dispatcher, or defer until after the first frame, or initialise lazily with `App Startup`.
- **It runs for every process, including non-UI ones.** A `WorkManager` job or a push message can start the process; do not assume a user is watching.
- See [Main-Safety]({{ "/en/02-coroutines-flow/main-safety/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
