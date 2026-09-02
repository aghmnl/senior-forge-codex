---
layout: post
title: "Suspend Functions"
date: 2026-09-02 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/suspend-functions/
---

## The Theory (The What)

A **suspend function** is a function marked with the `suspend` modifier that can be paused and resumed without blocking the thread it runs on. Suspend functions are the fundamental building block of Kotlin [coroutines]({{ "/en/glossary/coroutines/" | relative_url }}): they let you write [async operations]({{ "/en/glossary/async-operations/" | relative_url }}) in a sequential, readable style while the [runtime]({{ "/en/glossary/runtime/" | relative_url }}) handles the suspension and continuation behind the scenes.

```kotlin
// From FollowApp Suite — LabelRepository.kt
interface LabelRepository {
    fun getLabelsWithOptions(): Flow<Map<Label, List<LabelOption>>>

    suspend fun getOrCreateLabel(name: String, type: LabelType): Label
    suspend fun upsertLabelOption(labelId: String, label: String, sortOrder: Int = 0): LabelOption
    suspend fun updateLabelOption(id: String, label: String): LabelOption
    suspend fun updateLabelOptionSortOrders(orderedIds: List<String>)
    suspend fun deleteLabelOption(labelOptionId: String)
    suspend fun renameLabel(labelId: String, name: String)
    suspend fun deleteLabel(labelId: String)
}
```

The `suspend` keyword signals that these operations may take time (database I/O, network calls) and must be called from a [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) or another suspend function — the compiler enforces this at [compile time]({{ "/en/glossary/compile-time/" | relative_url }}).

## The Senior Nuance

- **Thread safety by convention**: A suspend function suspends the coroutine, not the thread. This means one thread can run thousands of coroutines concurrently. Senior developers structure their repository interfaces with `suspend` for one-shot operations and `Flow` for observable streams — as the FAS example shows.
- **Structured concurrency**: Suspend functions inherit their caller's `CoroutineScope`, which means cancellation propagates automatically. When a ViewModel is cleared, its `viewModelScope` cancels, and all pending suspend calls are cancelled — no manual cleanup needed.
- **Under the hood**, the compiler transforms each suspend function into a state machine with a `Continuation` parameter. This is why suspend functions can only be called from coroutine context — they need a continuation to resume.
- **Bridge to [callbacks]({{ "/en/glossary/callbacks/" | relative_url }})**: `suspendCancellableCoroutine` wraps a [callback]({{ "/en/glossary/callbacks/" | relative_url }})-based API into a suspend function, converting [event-handler]({{ "/en/glossary/event-handlers/" | relative_url }}) style into sequential style. This is how many Android framework APIs (originally callback-based) are consumed in modern code.
- **`withContext`** switches the dispatcher within a suspend function without creating a new coroutine. Senior developers use it to ensure I/O-bound work runs on `Dispatchers.IO` while keeping the caller on `Dispatchers.Main` — a pattern visible throughout [lifecycle-aware]({{ "/en/glossary/lifecycle-aware/" | relative_url }}) Android code.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
