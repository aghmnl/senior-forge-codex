---
layout: post
title: "Async Operations"
date: 2026-09-02 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/async-operations/
---

## The Theory (The What)

An **async operation** (asynchronous operation) is any unit of work that does not complete immediately and lets the program continue executing other work while waiting for the result. In Android, common async operations include network requests, database queries, file I/O, and inter-process communication. Kotlin provides [coroutines]({{ "/en/glossary/coroutines/" | relative_url }}) as its primary mechanism for async operations, replacing older patterns like raw threads, `AsyncTask`, and [callback]({{ "/en/glossary/callbacks/" | relative_url }})-based listeners.

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

    override fun isPremium(): Flow<Boolean> = premiumPreferences.isAdsRemoved()
}
```

The `scope.launch` starts an async operation that collects billing ownership verdicts on `Dispatchers.IO` without blocking the main thread.

## The Senior Nuance

- **Coroutines vs threads**: A coroutine is a lightweight async mechanism — thousands can run on a small thread pool. A thread is an OS-level resource. Senior developers use coroutines for application-level concurrency and only touch threads directly for CPU-bound parallelism or when interoping with Java threading APIs.
- **`launch` vs `async`**: `launch` fires an async operation that returns `Job` (fire-and-forget). `async` returns a `Deferred<T>` whose result you `await()`. Choose `launch` for side-effects (writing to DB, sending analytics), `async` when you need the return value and want to run multiple operations concurrently.
- **Structured concurrency** ensures async operations are scoped to a lifecycle. `viewModelScope` ties work to ViewModel lifecycle; `lifecycleScope` ties work to Activity/Fragment lifecycle. The FAS example creates a custom `CoroutineScope` with `SupervisorJob()` because the repository outlives any single screen — a deliberate architecture decision.
- **[Suspend functions]({{ "/en/glossary/suspend-functions/" | relative_url }})** are the sequential face of async operations: they look synchronous but suspend at I/O boundaries. This is why [callback]({{ "/en/glossary/callbacks/" | relative_url }})-heavy code converts naturally to sequential [suspend function]({{ "/en/glossary/suspend-functions/" | relative_url }}) chains.
- **Error handling**: In callback-based async code, errors scatter across `onFailure` handlers. With [coroutines]({{ "/en/glossary/coroutines/" | relative_url }}), standard `try/catch` works because [suspend functions]({{ "/en/glossary/suspend-functions/" | relative_url }}) throw exceptions normally — the structured concurrency framework propagates them up the [scope]({{ "/en/glossary/scope/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
