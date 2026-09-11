---
layout: post
title: "Cooperative Cancellation"
date: 2026-09-10 12:00:00 +0000
categories: [en, glossary]
tags: [cancellation, coroutines]
lang: en
permalink: /en/glossary/cooperative-cancellation/
---

## The Theory (The What)

**Cooperative cancellation** is the rule that a [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) is never killed from outside — it must *reach a point where it checks* whether it has been cancelled. Those points are every [suspension point]({{ "/en/glossary/suspension-point/" | relative_url }}) from `kotlinx.coroutines` (`delay`, `withContext`, `yield`, a Room [DAO]({{ "/en/glossary/dao/" | relative_url }}) call, `Flow.collect`) plus explicit checks: `isActive`, `ensureActive()`. At such a point, a cancelled coroutine throws [CancellationException]({{ "/en/glossary/cancellation-exception/" | relative_url }}).

```kotlin
// From FollowApp Suite — DragToReorder.kt
} catch (e: CancellationException) {
    // Gesture coroutine disposed mid-drag (e.g. composition change)
    state.endDrag(cancelled = true)
    throw e
}
```

Because the coroutine chooses *where* it can be interrupted, it is never stopped halfway through a database write or with a file handle open.

## The Senior Nuance

- **CPU loops are uncancellable unless you make them cancellable.** A `while` that never suspends will run to completion after [viewModelScope]({{ "/en/glossary/viewmodel-scope/" | relative_url }}) is cleared. Add `ensureActive()` or `yield()` inside long loops.
- **[Blocking calls]({{ "/en/glossary/blocking-call/" | relative_url }}) defeat cancellation.** A thread parked in `InputStream.read` cannot check anything. Prefer suspending I/O, or accept that cancellation takes effect after the call returns.
- **`NonCancellable` is the escape hatch for cleanup.** `withContext(NonCancellable) { db.commit() }` inside a `finally` guarantees the cleanup itself is not cancelled mid-way.
- **The design trade-off:** cooperative cancellation costs discipline (rethrow, don't swallow) and buys safety — no torn writes, no leaked resources, deterministic `finally`.
- See [Suspend Functions]({{ "/en/02-coroutines-flow/suspend-functions/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
