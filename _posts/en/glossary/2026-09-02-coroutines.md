---
layout: post
title: "Coroutines"
date: 2026-09-02 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/coroutines/
---

## The Theory (The What)

**Coroutines** are Kotlin's lightweight concurrency primitives for writing [async operations]({{ "/en/glossary/async-operations/" | relative_url }}) in a sequential, readable style. A coroutine is not a thread — it's a suspendable computation that can pause at any [suspend function]({{ "/en/glossary/suspend-functions/" | relative_url }}) call and resume later, potentially on a different thread, without blocking the thread it was running on. Thousands of coroutines can run on a small thread pool because they only occupy a thread while actually executing code.

```kotlin
// From FollowApp Suite — PremiumRepositoryImpl.kt
@Singleton
class PremiumRepositoryImpl @Inject constructor(
    private val premiumPreferences: PremiumPreferences,
    private val billingConnector: BillingConnector
) : PremiumRepository {

    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)

    init {
        billingConnector.connect()
        scope.launch {
            billingConnector.isOwned
                .filterNotNull()
                .collect { owned ->
                    premiumPreferences.setAdsRemoved(owned)
                }
        }
    }
}
```

`scope.launch` creates a coroutine on `Dispatchers.IO` that collects billing verdicts indefinitely — without blocking any thread.

## The Senior Nuance

- **Structured concurrency**: Coroutines don't exist in isolation — they run inside a `CoroutineScope` that defines their lifetime. When the scope is cancelled, all its coroutines are cancelled. `viewModelScope` and `lifecycleScope` are [lifecycle-aware]({{ "/en/glossary/lifecycle-aware/" | relative_url }}) scopes that prevent leaked work. The FAS example creates a custom scope with `SupervisorJob()` because the repository outlives any screen.
- **`SupervisorJob` vs `Job`**: A regular `Job` cancels all siblings when one child fails. `SupervisorJob` lets siblings survive — essential for independent operations (collecting billing + collecting analytics) that shouldn't cancel each other.
- **Dispatchers**: `Dispatchers.Main` for UI work, `Dispatchers.IO` for blocking I/O (network, disk), `Dispatchers.Default` for CPU-intensive work. Senior developers use `withContext` to switch dispatchers within a [suspend function]({{ "/en/glossary/suspend-functions/" | relative_url }}) rather than creating new coroutines.
- **Coroutines replaced [callbacks]({{ "/en/glossary/callbacks/" | relative_url }})** for [async operations]({{ "/en/glossary/async-operations/" | relative_url }}) in modern Android. The key insight: [callbacks]({{ "/en/glossary/callbacks/" | relative_url }}) invert control flow ("call me back when done"), while coroutines preserve sequential flow ("suspend here, then continue"). `suspendCancellableCoroutine` bridges callback-based APIs to the coroutine world.
- **Flow** is the coroutine-based replacement for reactive streams. `StateFlow` holds current state; `SharedFlow` broadcasts events. Both integrate naturally with [lifecycle-aware]({{ "/en/glossary/lifecycle-aware/" | relative_url }}) collection via `repeatOnLifecycle`.
- **Testing**: `runTest` from `kotlinx-coroutines-test` provides a `TestScope` with a virtual time scheduler. This lets you test delay-based logic instantly and verify that structured concurrency behaves correctly.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
