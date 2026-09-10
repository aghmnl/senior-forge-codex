---
layout: post
title: "Race Condition"
date: 2026-09-09 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/race-condition/
---

## The Theory (The What)

A **race condition** is a defect where the correctness of the program depends on the relative timing of two concurrent operations. The most common shape is the *check-then-act* or *read-modify-write* sequence: a thread reads shared state, computes something from it, and writes back — while another thread has already changed that state in between.

```kotlin
// Two coroutines toggling different filters at the same time
// Thread A: reads state (filters = {}), computes {dueToday}
// Thread B: reads state (filters = {}), computes {starred}
// A writes {dueToday}. B writes {starred}. A's filter is silently gone.
_uiState.value = _uiState.value.copy(filters = _uiState.value.filters + newFilter)
```

## The Senior Nuance

- Races in UI state rarely crash — they **lose updates**, which is worse. The screen renders a plausible-looking state that simply omits one of the user's actions, so the bug is reported as "sometimes my filter doesn't stick" and is unreproducible on a fast device.
- On Android the false comfort is "everything runs on the main thread". It does not: `viewModelScope.launch(Dispatchers.IO)`, `flowOn`, a `collect` on a background dispatcher, and a repository callback all write state off-Main. And even on `Main.immediate`, a `suspend` call inside a read-modify-write introduces a suspension point where another coroutine can interleave.
- The fix is not a lock; it is making the whole read-modify-write [atomic]({{ "/en/glossary/atomicity/" | relative_url }}) with [`update`]({{ "/en/glossary/update/" | relative_url }}), over [immutable]({{ "/en/glossary/immutability/" | relative_url }}) state. Detection matters too: races are invisible to normal tests, so exercise concurrent updates explicitly rather than trusting a single-threaded test dispatcher.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
