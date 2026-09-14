---
layout: post
title: "withContext"
date: 2026-09-14 12:00:00 +0000
categories: [en, glossary]
tags: [coroutines, threading]
lang: en
permalink: /en/glossary/with-context/
---

## The Theory (The What)

**`withContext(context) { }`** runs a block with a modified [`CoroutineContext`]({{ "/en/glossary/coroutine-context/" | relative_url }}) — almost always a different [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}) — and returns the block's value. It is a [suspend function]({{ "/en/glossary/suspend-functions/" | relative_url }}): the caller suspends, the block's [continuation]({{ "/en/glossary/continuation/" | relative_url }}) is scheduled on the target dispatcher, and when the block completes the caller resumes on its *original* dispatcher. No new coroutine is created; the block runs in the same [`Job`]({{ "/en/glossary/job/" | relative_url }}), so cancellation flows straight through.

```kotlin
// From FollowApp Suite — LegacyDataImporter.kt
val legacyTasks = withContext(Dispatchers.IO) { reader.readLegacyTasks() }
if (legacyTasks.isNotEmpty()) {
    taskDao.insertTasks(legacyTasks.mapIndexed { index, task -> task.toTaskEntity(index, now) })
}
```

Only the genuinely [blocking]({{ "/en/glossary/blocking-call/" | relative_url }}) call is wrapped; the Room insert that follows is already main-safe and stays on the caller's dispatcher.

## The Senior Nuance

- **It is what makes a suspend function main-safe.** Put it *inside* the function that blocks, so every caller — a ViewModel on Main, a test, a worker — gets correct behaviour without knowing. Wrapping at the call site instead means the next caller forgets.
- **`withContext` is sequential; `launch`/`async` are concurrent.** It returns the block's result and does not proceed until the block is done. If you find yourself needing the value, it is the right tool; if you need to fire and continue, it is the wrong one.
- **Cheap when the dispatcher does not actually change.** `IO` and `Default` share a pool, and the [Runtime]({{ "/en/glossary/runtime/" | relative_url }}) skips the thread hop when the target dispatcher is already the current one. Nested `withContext(IO)` inside `withContext(IO)` costs nearly nothing.
- **Do not use it to reach `Dispatchers.Main` from a repository.** A data-layer class that switches to Main has a UI dependency; return the value and let the caller decide where it lands.
- **`withContext(NonCancellable)`** is the escape hatch for cleanup that must finish even after cancellation — inside a `finally`, and nowhere else.
- See [Context & Dispatchers]({{ "/en/02-coroutines-flow/context-dispatchers/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
