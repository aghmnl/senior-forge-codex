---
layout: post
title: "Suspension Point"
date: 2026-09-10 12:00:00 +0000
categories: [en, glossary]
tags: [coroutines, cancellation, threading]
lang: en
permalink: /en/glossary/suspension-point/
---

## The Theory (The What)

A **suspension point** is a call inside a [suspend function]({{ "/en/glossary/suspend-functions/" | relative_url }}) where the [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) *may* pause and hand its [thread]({{ "/en/glossary/thread/" | relative_url }}) back to the [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}). Every call to another suspend function is a candidate; the IDE marks them with a gutter icon. Whether the coroutine actually suspends depends on the callee — a Room [DAO]({{ "/en/glossary/dao/" | relative_url }}) query will, an `if` will not.

```kotlin
// From FollowApp Suite — QuickCompleteTaskUseCase.kt
suspend operator fun invoke(taskId: String, isCompleted: Boolean, cascade: Boolean = false) {
    taskRepository.updateTaskCompletion(taskId = taskId, isCompleted = isCompleted)
    if (cascade) {
        taskRepository.updateDescendantsCompletion(taskId = taskId, isCompleted = isCompleted)
    }
    if (isCompleted) {
        spawnNextOccurrence(taskId)
    }
}
```

Three suspension points, one per line. Between them the code runs synchronously on whatever thread resumed it.

## The Senior Nuance

- **Suspension points are where cancellation is checked.** Every suspending call from `kotlinx.coroutines` checks the job before and after suspending and throws [CancellationException]({{ "/en/glossary/cancellation-exception/" | relative_url }}) if it was cancelled. Code with no suspension points is uncancellable — see [cooperative cancellation]({{ "/en/glossary/cooperative-cancellation/" | relative_url }}).
- **Suspension points are where the thread can change.** After `withContext(Dispatchers.IO)` returns, you are back on the caller's dispatcher but not necessarily the same physical thread. Never rely on thread identity across a suspension point (`ThreadLocal`, non-reentrant locks).
- **Not every `suspend` call suspends.** A [suspend function]({{ "/en/glossary/suspend-functions/" | relative_url }}) whose fast path returns a cached value completes synchronously and never returns `COROUTINE_SUSPENDED`. The point is *potential*, not guaranteed.
- Detailed in [Suspend Functions]({{ "/en/02-coroutines-flow/suspend-functions/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
