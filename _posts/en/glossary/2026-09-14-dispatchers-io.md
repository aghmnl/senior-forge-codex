---
layout: post
title: "Dispatchers.IO"
date: 2026-09-14 12:00:00 +0000
categories: [en, glossary]
tags: [coroutines, threading, performance]
lang: en
permalink: /en/glossary/dispatchers-io/
---

## The Theory (The What)

**`Dispatchers.IO`** is the [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}) designed for [blocking calls]({{ "/en/glossary/blocking-call/" | relative_url }}): file and socket I/O, synchronous SDKs, anything that parks a [thread]({{ "/en/glossary/thread/" | relative_url }}) while waiting. It is a view over the shared [thread pool]({{ "/en/glossary/thread-pool/" | relative_url }}) that allows up to 64 threads (or the core count, whichever is larger) to be blocked at once, so waiting threads do not starve CPU work.

```kotlin
// From FollowApp Suite — BackupManager.kt
suspend fun exportTo(uri: Uri): Result<Unit> = withContext(Dispatchers.IO) {
    // file write
}
```

The switch lives *inside* the suspend function, which is what makes it main-safe for every caller.

## The Senior Nuance

- **IO is for parking, not computing.** CPU-heavy loops here are wasteful but harmless; the real mistake is the reverse — blocking on [`Default`]({{ "/en/glossary/dispatchers-default/" | relative_url }}).
- **Room, Retrofit and DataStore already use it internally.** Wrapping their suspend calls in `withContext(IO)` is redundant; wrap your own file/JSON code.
- **`limitedParallelism(1)`** carves a single-threaded sub-dispatcher out of it — the way to confine a non-thread-safe SDK without creating a thread.
- **Hard-coding it is a testing smell.** Inject a `CoroutineDispatcher` (`@IoDispatcher`) so tests can substitute a [`TestDispatcher`]({{ "/en/glossary/test-dispatcher/" | relative_url }}).
- See [Context & Dispatchers]({{ "/en/02-coroutines-flow/context-dispatchers/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
