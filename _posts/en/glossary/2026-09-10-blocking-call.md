---
layout: post
title: "Blocking Call"
date: 2026-09-10 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/blocking-call/
---

## The Theory (The What)

A **blocking call** is any operation that parks the calling [thread]({{ "/en/glossary/thread/" | relative_url }}) until it completes: `Thread.sleep`, synchronous file or socket I/O, `Object.wait`, a `synchronized` lock under contention, [runBlocking]({{ "/en/glossary/run-blocking/" | relative_url }}). While blocked, the thread does nothing else — it cannot run other [coroutines]({{ "/en/glossary/coroutines/" | relative_url }}), and if it is the [main thread]({{ "/en/glossary/main-thread/" | relative_url }}) the UI stops rendering.

```kotlin
// Not found in FAS — standalone example
suspend fun readConfig(): String = File("config.json").readText()   // still blocks the caller's thread

suspend fun readConfig(): String = withContext(Dispatchers.IO) {   // main-safe
    File("config.json").readText()
}
```

Marking a function `suspend` does **not** make its blocking calls non-blocking. Only genuine [suspension points]({{ "/en/glossary/suspension-point/" | relative_url }}) release the thread; a blocking call inside a [suspend function]({{ "/en/glossary/suspend-functions/" | relative_url }}) still blocks whoever called it.

## The Senior Nuance

- **Blocking on `Dispatchers.Main` is the ANR.** Five seconds of a blocked main thread and the system kills the app. Even 16 ms drops a frame.
- **`Dispatchers.IO` exists to absorb blocking calls.** It is a [thread pool]({{ "/en/glossary/thread-pool/" | relative_url }}) sized (64+ threads) precisely so that blocking file and network calls can park threads without starving CPU work. Wrap blocking code with `withContext(Dispatchers.IO)` *inside* the suspend function, so every caller gets a main-safe API.
- **Blocking inside a coroutine also blocks cancellation.** A parked thread cannot reach a suspension point, so `cancel()` has no effect until the blocking call returns. Prefer suspending equivalents (`delay` over `sleep`, Okio/Ktor suspending I/O over streams) where they exist.
- Contrast with suspension in [Suspend Functions]({{ "/en/02-coroutines-flow/suspend-functions/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
