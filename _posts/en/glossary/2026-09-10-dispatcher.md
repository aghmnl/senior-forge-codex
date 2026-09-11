---
layout: post
title: "Dispatcher"
date: 2026-09-10 12:00:00 +0000
categories: [en, glossary]
tags: [coroutines, threading]
lang: en
permalink: /en/glossary/dispatcher/
---

## The Theory (The What)

A **Dispatcher** (`CoroutineDispatcher`) is the part of a coroutine's context that decides *which [thread]({{ "/en/glossary/thread/" | relative_url }}) or [thread pool]({{ "/en/glossary/thread-pool/" | relative_url }})* runs it. When a [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) resumes after a [suspension point]({{ "/en/glossary/suspension-point/" | relative_url }}), its [Continuation]({{ "/en/glossary/continuation/" | relative_url }}) is handed to the dispatcher, which schedules it. Android ships four: `Dispatchers.Main` (the [main thread]({{ "/en/glossary/main-thread/" | relative_url }})), `Main.immediate`, `Dispatchers.IO` (blocking I/O pool) and `Dispatchers.Default` (CPU-bound pool, sized to core count).

```kotlin
// From FollowApp Suite — TasksViewModel.kt
// Date math off the main thread: pattern scans over months/years
// must never stall input dispatching (popup ANR)
val suggested = withContext(Dispatchers.Default) {
    val settings = getRecurrenceSettingsUseCase().first()
    // ... RecurrenceCalculator.suggestPatternDueDate(...)
}
```

`withContext` swaps the dispatcher for the duration of its block and returns to the original one afterwards — no new coroutine, no `launch`.

## The Senior Nuance

- **The dispatcher is inherited, not chosen per call.** A [suspend function]({{ "/en/glossary/suspend-functions/" | relative_url }}) runs on whatever dispatcher its caller was on. That is why main-safety must be enforced *inside* the function with `withContext`, not assumed at the call site.
- **`IO` and `Default` share threads.** `Dispatchers.IO` is a view over the same pool as `Default` with a higher parallelism limit, so `withContext(IO)` from `Default` often does not switch threads at all — the runtime elides the hop.
- **`Main.immediate` skips the post if already on Main.** [viewModelScope]({{ "/en/glossary/viewmodel-scope/" | relative_url }}) uses it so that a `launch` from a click handler runs synchronously up to the first suspension, avoiding a frame of latency.
- **Never hard-code `Dispatchers.IO` in a class you want to unit test.** Inject the dispatcher so tests can substitute `StandardTestDispatcher`.
- See [Suspend Functions]({{ "/en/02-coroutines-flow/suspend-functions/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
