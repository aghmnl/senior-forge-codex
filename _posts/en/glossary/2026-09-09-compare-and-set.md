---
layout: post
title: "Compare-and-Set (CAS)"
date: 2026-09-09 12:00:00 +0000
categories: [en, glossary]
tags: [concurrency, threading, state-management]
lang: en
permalink: /en/glossary/compare-and-set/
---

## The Theory (The What)

**Compare-and-set** (CAS) is a hardware-level primitive: "write this new value, but only if the current value is still the one I read". It returns `true` on success and `false` if someone else won the race, in which case the caller retries with the fresh value. It is the foundation of lock-free concurrency.

```kotlin
// The retry loop that MutableStateFlow.update is built on
public inline fun <T> MutableStateFlow<T>.update(function: (T) -> T) {
    while (true) {
        val prevValue = value
        val nextValue = function(prevValue)
        if (compareAndSet(prevValue, nextValue)) return
    }
}
```

## The Senior Nuance

- CAS trades blocking for retrying. A [synchronized block]({{ "/en/glossary/synchronized-block/" | relative_url }}) parks a thread until the lock frees; CAS never parks, it just recomputes. Under low contention — which is what a [ViewModel]({{ "/en/glossary/viewmodel-store/" | relative_url }}) state holder sees — that is dramatically cheaper, with no deadlock risk.
- The retry means **the lambda must be pure**. It can run more than once, so a `update { it.copy(...) ; analytics.log() }` will double-log under contention. Side effects belong outside the block.
- CAS compares by *reference identity*, not [`equals`]({{ "/en/glossary/equals/" | relative_url }}). That is why the state object must be [immutable]({{ "/en/glossary/immutability/" | relative_url }}): a mutable object edited in place keeps its identity, so CAS cannot detect that anything changed — the classic ABA problem in its everyday Android form.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
