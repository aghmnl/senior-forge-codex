---
layout: post
title: "suspendCancellableCoroutine"
date: 2026-09-10 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/suspend-cancellable-coroutine/
---

## The Theory (The What)

**`suspendCancellableCoroutine { cont -> }`** is the primitive that turns a [callback]({{ "/en/glossary/callbacks/" | relative_url }})-based API into a [suspend function]({{ "/en/glossary/suspend-functions/" | relative_url }}). It suspends the [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}), hands you its [Continuation]({{ "/en/glossary/continuation/" | relative_url }}), and resumes when you call `cont.resume(value)` or `cont.resumeWithException(e)`. The *cancellable* variant additionally lets you register `invokeOnCancellation { }` to tear down the callback if the caller is cancelled.

```kotlin
// Not found in FAS — standalone example
suspend fun LocationClient.awaitLastLocation(): Location? =
    suspendCancellableCoroutine { cont ->
        val listener = object : LocationListener {
            override fun onSuccess(loc: Location?) = cont.resume(loc)
            override fun onFailure(e: Exception) = cont.resumeWithException(e)
        }
        requestLastLocation(listener)
        cont.invokeOnCancellation { removeListener(listener) }
    }
```

This is how Jetpack turned `CredentialManager`, `Task<T>` (`await()`), `ListenableFuture` and the like into suspend APIs — once, at the edge.

## The Senior Nuance

- **Three obligations.** Resume exactly once; propagate failures with `resumeWithException`; unregister on cancellation. Missing the third leaks the listener; missing the first hangs the caller forever.
- **Prefer it over `suspendCoroutine`.** The non-cancellable variant ignores [cooperative cancellation]({{ "/en/glossary/cooperative-cancellation/" | relative_url }}): a cancelled caller stays suspended until the callback fires, if it ever does.
- **`callbackFlow` is the multi-shot equivalent.** One callback → `suspendCancellableCoroutine`; a stream of callbacks → `callbackFlow` with `awaitClose`.
- **You rarely need it in app code.** Room, Retrofit, DataStore, Credential Manager and Play Services already ship suspend APIs. Reach for it only when wrapping a legacy SDK.
- See [Suspend Functions]({{ "/en/02-coroutines-flow/suspend-functions/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
