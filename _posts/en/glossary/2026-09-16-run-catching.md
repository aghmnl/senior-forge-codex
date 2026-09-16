---
layout: post
title: "runCatching"
date: 2026-09-16 12:00:00 +0000
categories: [en, glossary]
tags: [error-handling, functional, syntax]
lang: en
permalink: /en/glossary/run-catching/
---

## The Theory (The What)

**`runCatching { }`** runs a block and wraps the outcome in a [`Result<T>`]({{ "/en/glossary/result/" | relative_url }}): `Result.success(value)` if it returns, `Result.failure(e)` if it throws. It is the functional alternative to [`try/catch`]({{ "/en/glossary/try-catch/" | relative_url }}) when you want the error as a *value* you can map, recover from, or pass along — `getOrNull()`, `getOrDefault()`, `onFailure { }`, `getOrThrow()`.

```kotlin
// From FollowApp Suite — BackupManager.kt
suspend fun exportTo(uri: Uri): Result<Unit> = withContext(Dispatchers.IO) {
    runCatching {
        val json = BackupSerializer.serialize(bundle)
        context.contentResolver.openOutputStream(uri, "wt").use { /* ... */ }
    }.onSuccess {
        Log.d(TAG, "Backup exported")
    }.onFailure { Log.e(TAG, "Backup export failed", it) }
}
```

## The Senior Nuance

- **It catches `Throwable` — including [`CancellationException`]({{ "/en/glossary/cancellation-exception/" | relative_url }}).** Inside a coroutine, `runCatching { suspendCall() }` swallows cancellation and turns it into a `failure`. If the block suspends, rethrow it: `.onFailure { if (it is CancellationException) throw it }`, or use a narrower `try/catch`. This is the single most common `runCatching` bug in Android code.
- **Around [`await()`]({{ "/en/glossary/await/" | relative_url }}) inside [`supervisorScope`]({{ "/en/glossary/supervisor-scope/" | relative_url }}) it is the per-child recovery idiom.** `runCatching { header.await() }.getOrNull()` lets one optional part fail without the others.
- **Do not return `Result` from public APIs by default.** Kotlin's `Result` is meant for local handling; a sealed hierarchy communicates domain errors better across layers.
- See [Launch vs Async/Await]({{ "/en/02-coroutines-flow/launch-vs-async-await/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
