---
layout: post
title: "coroutineScope (builder)"
date: 2026-09-10 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/coroutine-scope-builder/
---

## The Theory (The What)

**`coroutineScope { }`** is a [suspend function]({{ "/en/glossary/suspend-functions/" | relative_url }}) that creates a child scope, runs its block, and *suspends until every coroutine launched inside it has completed*. If any child fails, the others are cancelled and the exception is rethrown to the caller. It is how you introduce parallelism inside sequential suspend code without leaking work.

```kotlin
// From FollowApp Suite — TasksViewModel.kt
try {
    coroutineScope {
        ids.forEach { launch { quickCompleteTaskUseCase(taskId = it, isCompleted = isCompleted) } }
    }
} finally {
    isBulkWriteInFlight = false
}
```

The `finally` runs exactly once, after all twenty `launch`es have finished — `coroutineScope` turns a fan-out into a single suspension point.

## The Senior Nuance

- **It is a suspend function, not a scope you store.** Unlike `CoroutineScope(...)`, which creates a long-lived scope you must cancel yourself, `coroutineScope` lives only for the duration of the call. Nothing leaks.
- **Failure is all-or-nothing.** One failing child cancels its siblings and propagates. Use `supervisorScope` when independent children should not take each other down.
- **It is the correct way to do "parallel decomposition" in a use case.** `coroutineScope { val a = async { .. }; val b = async { .. }; a.await() + b.await() }` — the function is still a plain `suspend fun` to its caller.
- **Cancellation flows through.** If the outer job is cancelled ([viewModelScope]({{ "/en/glossary/viewmodel-scope/" | relative_url }}) cleared), every child launched here receives [CancellationException]({{ "/en/glossary/cancellation-exception/" | relative_url }}).
- See [Suspend Functions]({{ "/en/02-coroutines-flow/suspend-functions/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
