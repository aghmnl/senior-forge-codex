---
layout: post
title: "Synchronized Block"
date: 2026-09-02 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/synchronized-block/
---

## The Theory (The What)

A **synchronized block** is a concurrency primitive that ensures only one thread can execute a protected section of code at a time. In Kotlin, it is expressed as `synchronized(lock) { ... }`, where `lock` is any object used as the mutex. While one thread holds the lock, any other thread that reaches the same `synchronized` block waits until the lock is released. This guarantees mutual exclusion — preventing data races when multiple threads read and write shared mutable state.

```kotlin
// Standalone example — no synchronized usage found in FAS
class ThreadSafeCounter {
    private var count = 0
    private val lock = Any()

    fun increment() = synchronized(lock) {
        count++
    }

    fun get() = synchronized(lock) { count }
}
```

## The Senior Nuance

- **`lazy` uses `synchronized` by default**: `lazy(LazyThreadSafetyMode.SYNCHRONIZED)` — the default mode — wraps the initialization [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) in a `synchronized` block. This ensures that if two threads access the property simultaneously, only one executes the initialization; the other waits and receives the cached value. Using `LazyThreadSafetyMode.NONE` skips this — appropriate only when access is guaranteed to be single-threaded.
- **[Coroutines]({{ "/en/glossary/coroutines/" | relative_url }}) prefer `Mutex`**: In coroutine code, `synchronized` is discouraged because it blocks the thread (not just the coroutine). `kotlinx.coroutines.sync.Mutex` provides the same mutual exclusion but suspends instead of blocking, keeping the thread available for other coroutines.
- **Performance cost**: `synchronized` incurs monitor acquisition overhead on the [JVM]({{ "/en/glossary/jvm/" | relative_url }}). In [hot loops]({{ "/en/glossary/hot-loops/" | relative_url }}) or high-contention scenarios, this can degrade throughput. Alternatives like `AtomicInteger`, `ConcurrentHashMap`, or lock-free algorithms avoid this overhead for specific patterns.
- **Deadlock risk**: Acquiring multiple locks in inconsistent order across different code paths is the classic deadlock scenario. Senior developers minimize synchronized scope (lock only what's necessary) and always acquire locks in the same order.
- **`@Volatile` vs `synchronized`**: `@Volatile` ensures visibility (all threads see the latest write) but does not ensure atomicity of compound operations (read-modify-write). `synchronized` provides both. For a simple flag, `@Volatile` suffices; for increment or check-then-act, `synchronized` or atomics are needed.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
