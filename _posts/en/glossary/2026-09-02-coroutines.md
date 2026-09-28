---
layout: post
title: "Coroutines"
date: 2026-09-02 12:00:00 +0000
categories: [en, glossary]
tags: [coroutines, concurrency, lifecycle]
lang: en
permalink: /en/glossary/coroutines/
---

## The Theory (The What)

**Coroutines** are Kotlin's lightweight concurrency primitives for writing [async operations]({{ "/en/glossary/async-operations/" | relative_url }}) in a sequential, readable style. A coroutine is not a thread — it's a suspendable computation that can pause at any [suspend function]({{ "/en/glossary/suspend-functions/" | relative_url }}) call and resume later, potentially on a different thread, without blocking the thread it was running on. Thousands of coroutines can run on a small thread pool because they only occupy a thread while actually executing code.

Coroutines come in two parts. **Kotlin itself** provides the [`suspend`]({{ "/en/glossary/suspend-functions/" | relative_url }}) keyword and the basic types behind it, in its `kotlin.coroutines` package, with no extra dependency. Everything used day to day — [`CoroutineScope`]({{ "/en/glossary/coroutine-scope/" | relative_url }}), [`launch`]({{ "/en/glossary/launch/" | relative_url }}), [`Job`]({{ "/en/glossary/job/" | relative_url }}), [`SupervisorJob`]({{ "/en/glossary/supervisor-job/" | relative_url }}), [`Dispatchers`]({{ "/en/glossary/dispatcher/" | relative_url }}), [`Flow`]({{ "/en/glossary/flow/" | relative_url }}) — comes from the [kotlinx.coroutines]({{ "/en/glossary/kotlinx-coroutines/" | relative_url }}) library, a separate dependency.

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

[`scope.launch`]({{ "/en/glossary/launch/" | relative_url }}) creates a coroutine on [`Dispatchers.IO`]({{ "/en/glossary/dispatchers-io/" | relative_url }}) that collects billing verdicts indefinitely — without blocking any thread.

## The Senior Nuance

- **[Structured concurrency]({{ "/en/02-coroutines-flow/structured-concurrency/" | relative_url }})**: Coroutines don't exist in isolation — they run inside a [`CoroutineScope`]({{ "/en/glossary/coroutine-scope/" | relative_url }}) that defines their lifetime. When the scope is cancelled, all its coroutines are cancelled. [`viewModelScope`]({{ "/en/glossary/viewmodel-scope/" | relative_url }}) and [`lifecycleScope`]({{ "/en/glossary/lifecycle-scope/" | relative_url }}) are [lifecycle-aware]({{ "/en/glossary/lifecycle-aware/" | relative_url }}) scopes that prevent leaked work. The FAS example creates a custom scope with [`SupervisorJob()`]({{ "/en/glossary/supervisor-job/" | relative_url }}) because the repository outlives any screen.
- **[`SupervisorJob`]({{ "/en/glossary/supervisor-job/" | relative_url }}) vs [`Job`]({{ "/en/glossary/job/" | relative_url }})**: A regular [`Job`]({{ "/en/glossary/job/" | relative_url }}) cancels all siblings when one child fails. [`SupervisorJob`]({{ "/en/glossary/supervisor-job/" | relative_url }}) lets siblings survive — essential for independent operations (collecting billing + collecting analytics) that shouldn't cancel each other.
- **[Dispatchers]({{ "/en/glossary/dispatcher/" | relative_url }})**: [`Dispatchers.Main`]({{ "/en/glossary/dispatchers-main/" | relative_url }}) for UI work, [`Dispatchers.IO`]({{ "/en/glossary/dispatchers-io/" | relative_url }}) for blocking I/O (network, disk), [`Dispatchers.Default`]({{ "/en/glossary/dispatchers-default/" | relative_url }}) for CPU-intensive work. Senior developers use [`withContext`]({{ "/en/glossary/with-context/" | relative_url }}) to switch dispatchers within a [suspend function]({{ "/en/glossary/suspend-functions/" | relative_url }}) rather than creating new coroutines.
- **Coroutines replaced [callbacks]({{ "/en/glossary/callbacks/" | relative_url }})** for [async operations]({{ "/en/glossary/async-operations/" | relative_url }}) in modern Android. The key insight: [callbacks]({{ "/en/glossary/callbacks/" | relative_url }}) invert control flow ("call me back when done"), while coroutines preserve sequential flow ("suspend here, then continue"). [`suspendCancellableCoroutine`]({{ "/en/glossary/suspend-cancellable-coroutine/" | relative_url }}) bridges callback-based APIs to the coroutine world.
- **[Flow]({{ "/en/glossary/flow/" | relative_url }})** is the coroutine-based replacement for reactive streams. [`StateFlow`]({{ "/en/glossary/stateflow/" | relative_url }}) holds current state; [`SharedFlow`]({{ "/en/glossary/sharedflow/" | relative_url }}) broadcasts every emission to every collector. Both integrate naturally with [lifecycle-aware]({{ "/en/glossary/lifecycle-aware/" | relative_url }}) collection via [`repeatOnLifecycle`]({{ "/en/glossary/repeat-on-lifecycle/" | relative_url }}).
- **Testing**: [`runTest`]({{ "/en/glossary/run-test/" | relative_url }}) from [`kotlinx-coroutines-test`]({{ "/en/glossary/kotlinx-coroutines/" | relative_url }}) provides a [`TestScope`]({{ "/en/glossary/test-scope/" | relative_url }}) with a virtual time scheduler. This lets you test delay-based logic instantly and verify that structured concurrency behaves correctly.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
