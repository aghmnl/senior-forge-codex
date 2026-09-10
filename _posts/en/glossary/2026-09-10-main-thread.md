---
layout: post
title: "Main Thread"
date: 2026-09-10 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/main-thread/
---

## The Theory (The What)

The **main thread** (UI thread) is the single [thread]({{ "/en/glossary/thread/" | relative_url }}) on which Android dispatches input events, runs lifecycle callbacks, measures/lays out/draws views and composes [Compose]({{ "/en/glossary/jetpack-compose/" | relative_url }}) frames. Everything the user sees goes through it, at ~16 ms per frame at 60 Hz. A [blocking call]({{ "/en/glossary/blocking-call/" | relative_url }}) on it drops frames; five seconds of blocking triggers an ANR dialog and the system kills the app.

```kotlin
// From FollowApp Suite — TasksViewModel.kt
// Date math off the main thread: pattern scans over months/years
// must never stall input dispatching (popup ANR)
val suggested = withContext(Dispatchers.Default) {
    val settings = getRecurrenceSettingsUseCase().first()
    // ... RecurrenceCalculator.suggestPatternDueDate(...)
}
```

`Dispatchers.Main` is the [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}) that targets it. [viewModelScope]({{ "/en/glossary/viewmodel-scope/" | relative_url }}) defaults to `Main.immediate`, so suspend functions called from a ViewModel start on the main thread and must move their own heavy work away with `withContext`.

## The Senior Nuance

- **Suspending on Main is free; blocking on Main is the bug.** A [suspend function]({{ "/en/glossary/suspend-functions/" | relative_url }}) that hits a real [suspension point]({{ "/en/glossary/suspension-point/" | relative_url }}) releases the main thread to render. One that calls `File.readText()` does not.
- **CPU work counts too.** FAS moves recurrence date math to `Dispatchers.Default` even though it is not I/O — anything that takes more than a few milliseconds belongs off Main.
- **Some APIs *require* Main.** View mutations, `LiveData.setValue`, most Compose state writes from outside a composable. `withContext(Dispatchers.Main)` is how a background coroutine gets back to it.
- **Cold-start Main is the most contested thread in the app.** FAS's `restoreViewPreferences` comment documents the symptom: a fast DataStore read resumed on Main was queued behind first composition for hundreds of milliseconds.
- See [Suspend Functions]({{ "/en/02-coroutines-flow/suspend-functions/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
