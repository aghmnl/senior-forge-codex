---
layout: post
title: "viewModelScope"
date: 2026-09-10 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/viewmodel-scope/
---

## The Theory (The What)

**`viewModelScope`** is a `CoroutineScope` extension property on `ViewModel` (from `lifecycle-viewmodel-ktx`) bound to `SupervisorJob() + Dispatchers.Main.immediate`. Every [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) launched in it is cancelled automatically in `onCleared()`, which makes it the default place for a [ViewModel]({{ "/en/glossary/viewmodel-store/" | relative_url }}) to call [suspend functions]({{ "/en/glossary/suspend-functions/" | relative_url }}).

```kotlin
// From FollowApp Suite — TasksViewModel.kt
// Dispatchers.IO because viewModelScope defaults to Main.immediate,
// and Main is saturated by Compose's first composition on cold start.
viewModelScope.launch(Dispatchers.IO) {
    val snapshot = runCatching { tasksViewPreferences.read() }
        .onFailure { Log.e(TAG, "Error restoring TasksView prefs — falling back to defaults", it) }
        .getOrNull()
    // ...
}
```

The default [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}) is Main, so anything launched here runs on the [main thread]({{ "/en/glossary/main-thread/" | relative_url }}) until the first [suspension point]({{ "/en/glossary/suspension-point/" | relative_url }}) — which is why the suspend functions it calls must be main-safe.

## The Senior Nuance

- **`Main.immediate` runs synchronously until the first suspension.** A `launch` from a click handler executes its first lines before the handler returns — no extra frame of latency, but also no chance to "escape" a busy main thread. FAS's `restoreViewPreferences` overrides to `Dispatchers.IO` precisely because Main was saturated during cold start.
- **`SupervisorJob` isolates failures.** One crashing coroutine does not cancel its siblings in the scope — but an uncaught exception still crashes the app. Handle errors inside each `launch`.
- **Cancellation is cooperative.** `onCleared()` cancels the job; each coroutine stops at its next suspension point. Work with no suspension points keeps running — see [cooperative cancellation]({{ "/en/glossary/cooperative-cancellation/" | relative_url }}).
- **Do not pass it down.** A repository or use case that receives `viewModelScope` couples itself to the UI lifecycle. Expose suspend functions instead and let the caller own the scope.
- See [Suspend Functions]({{ "/en/02-coroutines-flow/suspend-functions/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
