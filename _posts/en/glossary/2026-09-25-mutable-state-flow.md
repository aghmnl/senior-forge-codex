---
layout: post
title: "MutableStateFlow"
date: 2026-09-25 12:00:00 +0000
categories: [en, glossary]
tags: [flow, state-management, concurrency]
lang: en
permalink: /en/glossary/mutable-state-flow/
---

## The Theory (The What)

**`MutableStateFlow<T>`** is the writable version of [StateFlow]({{ "/en/glossary/stateflow/" | relative_url }}). It is created with `MutableStateFlow(initialValue)` and adds three ways to change the state: assigning `value`, the atomic [compareAndSet(expect, update)]({{ "/en/glossary/compare-and-set/" | relative_url }}), and the [update {}]({{ "/en/glossary/update/" | relative_url }}) extension built on top of it. All of them are [thread-safe]({{ "/en/glossary/thread-safety/" | relative_url }}), and every write that is not [equal]({{ "/en/glossary/equals/" | relative_url }}) to the current value is delivered to the [collectors]({{ "/en/glossary/collector/" | relative_url }}). It stays private inside a [state holder]({{ "/en/glossary/state-holder/" | relative_url }}) and is exposed read-only with [asStateFlow()]({{ "/en/glossary/as-state-flow/" | relative_url }}).

```kotlin
// From FollowApp Suite — BillingConnector.kt
// Mutable and private inside; read-only outside.
// null = "Play has not answered yet", distinct from a real false
private val _isOwned = MutableStateFlow<Boolean?>(null)
val isOwned: StateFlow<Boolean?> = _isOwned.asStateFlow()
```

## The Senior Nuance

- **`value = value.copy(...)` is not atomic.** It reads and then writes; two coroutines doing it at once can lose one change. `update {}` retries with `compareAndSet` until the write lands on the value it was computed from.
- **Exposing the mutable type leaks write access.** A public `MutableStateFlow` lets the UI change state directly and breaks [unidirectional data flow]({{ "/en/glossary/unidirectional-data-flow/" | relative_url }}). Upcasting to `StateFlow` is not enough either, because a caller can cast it back; `asStateFlow()` returns a real read-only wrapper.
- **It is also a handy test double.** A `MutableStateFlow` returned from a fake repository lets a test push new values on demand and check how the ViewModel reacts.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
