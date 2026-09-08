---
layout: post
title: "Concurrency"
date: 2026-09-08 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/concurrency/
---

## The Theory (The What)

**Concurrency** is multiple flows of execution making progress over the same period, interleaving on one thread or running in parallel on several. On Android that means the main thread plus whatever [coroutines]({{ "/en/glossary/coroutines/" | relative_url }}) run on `Dispatchers.IO`/`Default` — and every piece of state reachable from more than one of them.

```kotlin
// From FollowApp Suite — TasksViewModel.kt
// State is replaced, never mutated in place: safe under concurrent updates
_uiState.update { it.copy(selectedTaskIds = setOf(taskId)) }
```

## The Senior Nuance

- Concurrency is what makes [mutability]({{ "/en/glossary/mutation/" | relative_url }}) dangerous rather than merely untidy. A [`MutableList`]({{ "/en/glossary/mutable-list/" | relative_url }}) read by one coroutine while another writes it throws `ConcurrentModificationException` at best, and silently renders stale data at worst.
- [Immutability]({{ "/en/glossary/immutability/" | relative_url }}) is the cheapest answer: a value nobody can change needs no [synchronized block]({{ "/en/glossary/synchronized-block/" | relative_url }}) and no lock ordering. `MutableStateFlow.update { }` composes an atomic read-modify-write out of immutable values, which is why it replaces the state object instead of editing it.
- The second answer is confinement: keep the mutable object inside one [stack frame]({{ "/en/glossary/stack-frame/" | relative_url }}), or on one thread. Most "we need a lock here" conclusions are actually a mutable object that escaped a function it should never have left.
- Concurrency is not parallelism. Coroutines interleave suspending work on a single thread perfectly happily — the state hazards are identical, because a suspension point is exactly where another coroutine can observe your half-finished [mutation]({{ "/en/glossary/mutation/" | relative_url }}).

**Kotlin docs:** [Coroutines guide](https://kotlinlang.org/docs/coroutines-guide.html) · [Shared mutable state and concurrency](https://kotlinlang.org/docs/shared-mutable-state-and-concurrency.html)

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
