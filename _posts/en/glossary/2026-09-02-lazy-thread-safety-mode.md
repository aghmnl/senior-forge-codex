---
layout: post
title: "LazyThreadSafetyMode"
date: 2026-09-02 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/lazy-thread-safety-mode/
---

## The Theory (The What)

**`LazyThreadSafetyMode`** is an enum that controls how a `lazy` property handles concurrent first-access from multiple threads. It has three values:

- **`SYNCHRONIZED`** (default): The initialization [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) runs inside a [synchronized block]({{ "/en/glossary/synchronized-block/" | relative_url }}). Only one thread executes the lambda; all others wait and receive the cached result. Safe but carries synchronization overhead.
- **`PUBLICATION`**: Multiple threads can execute the initialization lambda simultaneously. The first thread to finish stores its result; all others discard theirs. Safe when the lambda has no side effects and you want to avoid blocking — at the cost of redundant computation.
- **`NONE`**: No synchronization at all. The lambda runs on whatever thread accesses it first, with no protection against concurrent access. **Fastest**, but only safe when you guarantee single-threaded access (e.g., the UI thread in [Jetpack Compose]({{ "/en/glossary/jetpack-compose/" | relative_url }})).

```kotlin
// Standalone example — no LazyThreadSafetyMode usage found in FAS
// UI-only property — safe to skip synchronization
val headerConfig: HeaderConfig by lazy(LazyThreadSafetyMode.NONE) {
    repository.loadExpensiveHeaderConfig()
}

// Multi-threaded safe init — redundant computation is OK
val sharedConfig: Config by lazy(LazyThreadSafetyMode.PUBLICATION) {
    parseConfigFromDisk()
}
```

## The Senior Nuance

- **Default is almost always correct**: `SYNCHRONIZED` is the safe default and should be used unless profiling shows the synchronization is a bottleneck. Premature optimization with `NONE` on a multi-threaded path leads to subtle, hard-to-reproduce bugs.
- **`NONE` in Compose**: Properties accessed only from the main thread (Composable functions, ViewModel state) are safe candidates for `NONE`. Since Compose guarantees single-threaded recomposition on the main thread, the synchronization overhead is pure waste.
- **`PUBLICATION` use case**: Ideal for immutable configuration or expensive computations where the result is always the same regardless of which thread computes it. The lambda may run more than once during the race, but the stored value is consistent.
- **Visibility with `NONE`**: Even with `NONE`, the `Lazy` delegate stores the result in a `@Volatile` field, so once initialized, all threads see the value. The risk is only during the initialization race itself — two threads could both execute the lambda and one's result is silently discarded.
- **Testing**: If tests run on multiple threads (e.g., `runTest` with `UnconfinedTestDispatcher`), a `lazy(NONE)` property can exhibit flaky behavior. Use `SYNCHRONIZED` in test contexts or ensure single-threaded access.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
