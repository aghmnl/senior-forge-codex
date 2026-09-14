---
layout: post
title: "CoroutineScope"
date: 2026-09-14 12:00:00 +0000
categories: [en, glossary]
tags: [coroutines, lifecycle, cancellation]
lang: en
permalink: /en/glossary/coroutine-scope/
---

## The Theory (The What)

A **`CoroutineScope`** is an object that holds a [`CoroutineContext`]({{ "/en/glossary/coroutine-context/" | relative_url }}) and acts as the receiver for `launch` and `async`. Its [`Job`]({{ "/en/glossary/job/" | relative_url }}) is the root of every coroutine started in it, so cancelling the scope cancels all of them — that is the mechanism behind [`viewModelScope`]({{ "/en/glossary/viewmodel-scope/" | relative_url }}), `lifecycleScope` and `rememberCoroutineScope()`. A custom scope is created with `CoroutineScope(context)` and lives until something calls `cancel()`.

```kotlin
// From FollowApp Suite — PremiumRepositoryImpl.kt
private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)

init {
    scope.launch {
        billingConnector.isOwned.filterNotNull().collect { owned ->
            premiumPreferences.setAdsRemoved(owned)
        }
    }
}
```

A `@Singleton` repository outlives every screen, so it owns a scope of its own — with a [`SupervisorJob`]({{ "/en/glossary/supervisor-job/" | relative_url }}) so independent collectors do not cancel each other, and `Dispatchers.IO` because the billing client blocks.

## The Senior Nuance

- **Every scope needs an owner who cancels it.** The framework scopes are cancelled by their lifecycle owner. A `CoroutineScope(...)` in a field is cancelled by nobody unless you write it; it is justified only for objects that genuinely live as long as the process, and should say so in a comment. `GlobalScope` is a scope with no owner at all — avoid it.
- **Do not pass scopes down.** A use case or repository that receives `viewModelScope` is coupled to the UI lifecycle. Expose [suspend functions]({{ "/en/glossary/suspend-functions/" | relative_url }}) and let the caller own the scope.
- **Not the same as the `coroutineScope { }` builder.** The [builder]({{ "/en/glossary/coroutine-scope-builder/" | relative_url }}) is a suspend function that creates a *temporary* child scope and waits for it; `CoroutineScope(...)` creates a long-lived one you must manage.
- **A scope with a `SupervisorJob` and no [`CoroutineExceptionHandler`]({{ "/en/glossary/coroutine-exception-handler/" | relative_url }})** turns any uncaught exception in a child into a process crash. Add the handler when the scope runs fire-and-forget work.
- See [Context & Dispatchers]({{ "/en/02-coroutines-flow/context-dispatchers/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
