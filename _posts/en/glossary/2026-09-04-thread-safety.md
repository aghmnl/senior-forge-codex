---
layout: post
title: "Thread Safety"
date: 2026-09-04 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/thread-safety/
---

## The Theory (The What)

**Thread safety** means that a piece of code behaves correctly when accessed from multiple threads concurrently, without race conditions, data corruption, or crashes. In Kotlin and Android, thread safety is achieved through several mechanisms:

- **[Immutability]({{ "/en/glossary/immutability/" | relative_url }})** — objects that cannot change need no synchronization. `val`, immutable [data classes]({{ "/en/01-kotlin-core/data-classes/" | relative_url }}), and immutable [collections]({{ "/en/glossary/collections/" | relative_url }}) are inherently thread-safe.
- **Confinement** — restricting mutable state to a single thread (e.g., the main thread for UI state, a single-threaded `Dispatchers.IO` for a database connection).
- **Synchronization** — `synchronized` blocks, `Mutex`, `@Volatile`, and atomic classes (`AtomicReference`, `AtomicInteger`) protect shared mutable state.
- **Structured concurrency** — Kotlin coroutines with `CoroutineScope` and `Dispatchers` ensure that work runs on the right thread and is cancelled properly.

## The Senior Nuance

- A Senior defaults to [immutability]({{ "/en/glossary/immutability/" | relative_url }}) as the primary thread-safety strategy. A `StateFlow` that emits immutable [data class]({{ "/en/01-kotlin-core/data-classes/" | relative_url }}) snapshots requires no synchronization — the only mutation point is the `MutableStateFlow.value` setter, which is already atomic.
- In Android, most thread-safety bugs happen at layer boundaries: a repository returning a `MutableList` from a background thread that the UI reads on the main thread. Defensive copies (`toList()`, `toMap()`) or truly immutable types eliminate this.
- `lazy(LazyThreadSafetyMode.SYNCHRONIZED)` (the default) uses a `synchronized` block for thread-safe initialization. `LazyThreadSafetyMode.NONE` skips synchronization entirely — safe only when the property is guaranteed to be accessed from one thread (e.g., a UI-only property). `PUBLICATION` allows concurrent initialization but guarantees only one result is visible. A Senior picks the mode that matches the access pattern.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
