---
layout: post
title: "CoroutineExceptionHandler"
date: 2026-09-14 12:00:00 +0000
categories: [en, glossary]
tags: [coroutines, error-handling]
lang: en
permalink: /en/glossary/coroutine-exception-handler/
---

## The Theory (The What)

A **`CoroutineExceptionHandler`** is a [`CoroutineContext`]({{ "/en/glossary/coroutine-context/" | relative_url }}) element that receives exceptions no coroutine caught. It is invoked only for *root* coroutines — a `launch` directly in a scope, or a child of a [`SupervisorJob`]({{ "/en/glossary/supervisor-job/" | relative_url }}) — because everywhere else the exception propagates to the parent [`Job`]({{ "/en/glossary/job/" | relative_url }}) first. Without a handler, an uncaught exception reaches the thread's default handler and, on Android, crashes the process.

```kotlin
// Not found in FAS — standalone example
private val scope = CoroutineScope(
    SupervisorJob() + Dispatchers.IO +
        CoroutineExceptionHandler { _, e -> Log.e(TAG, "billing collector failed", e) }
)
```

The three elements each answer a different question: what fails independently (`SupervisorJob`), where it runs (`Dispatchers.IO`), and what happens when it fails anyway (the handler).

## The Senior Nuance

- **It never applies to `async`.** An exception inside `async` is stored in the `Deferred` and rethrown by `await()`; the handler is bypassed. Handle it at the `await` call.
- **It is not a `try/catch`.** By the time the handler runs the coroutine is already dead and its scope's children (unless supervised) already cancelled. It is for logging and reporting — [Crashlytics]({{ "/en/glossary/crashlytics/" | relative_url }}) `recordException` is the typical body — not for recovery.
- **`viewModelScope` has none by default.** An uncaught exception in a `launch` there crashes the app just like anywhere else. Handle errors inside each `launch`, or add a handler via `viewModelScope.launch(handler) { }` when the work is fire-and-forget.
- **[`CancellationException`]({{ "/en/glossary/cancellation-exception/" | relative_url }}) is never delivered to it.** Cancellation is normal completion from the framework's point of view.
- See [Context & Dispatchers]({{ "/en/02-coroutines-flow/context-dispatchers/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
