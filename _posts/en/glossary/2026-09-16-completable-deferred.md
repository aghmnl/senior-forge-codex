---
layout: post
title: "CompletableDeferred"
date: 2026-09-16 12:00:00 +0000
categories: [en, glossary]
tags: [coroutines, testing, callbacks]
lang: en
permalink: /en/glossary/completable-deferred/
---

## The Theory (The What)

**`CompletableDeferred<T>`** is a [`Deferred`]({{ "/en/glossary/deferred/" | relative_url }}) with no [`async`]({{ "/en/glossary/async/" | relative_url }}) block behind it: you create it empty and complete it by hand with `complete(value)` or `completeExceptionally(e)`. Anyone calling [`await()`]({{ "/en/glossary/await/" | relative_url }}) on it suspends until one of those happens. It is the coroutine-native one-shot promise — the [`CountDownLatch(1)`]({{ "/en/glossary/count-down-latch/" | relative_url }}) that suspends instead of blocking and carries a value.

```kotlin
// From FollowApp Suite — FakeLabelRepository.kt
/** When set, getLabelsWithOptions suspends until completed — lets tests observe in-flight reloads. */
var loadGate: CompletableDeferred<Unit>? = null

override fun getLabelsWithOptions(): Flow<Map<Label, List<LabelOption>>> =
    flow.map {
        loadGate?.await()
        // ...
    }
```

```kotlin
// From FollowApp Suite — LabelsListViewModelTest.kt
labelRepo.loadGate = CompletableDeferred()      // hold the next read in flight
vm.onConfirmScaleOptionRename(option.id)
advanceUntilIdle()
assertFalse(vm.uiState.value.isLoading)          // assert the intermediate state
labelRepo.loadGate!!.complete(Unit)              // release it
```

## The Senior Nuance

- **Its two jobs: test gates and callback bridges.** In tests it freezes a coroutine at a chosen point so an intermediate state can be asserted deterministically. In production it turns a one-shot [callback]({{ "/en/glossary/callbacks/" | relative_url }}) into a suspend call — though [`suspendCancellableCoroutine`]({{ "/en/glossary/suspend-cancellable-coroutine/" | relative_url }}) is usually the better tool for that, because it wires cancellation back to the callback.
- **It is still a [`Job`]({{ "/en/glossary/job/" | relative_url }}).** Pass a parent (`CompletableDeferred(parent = job)`) if it should be cancelled with a scope; otherwise it is unowned.
- **`complete()` returns `Boolean`.** `false` means it was already completed — a cheap "first one wins" without a lock.
- See [Launch vs Async/Await]({{ "/en/02-coroutines-flow/launch-vs-async-await/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
