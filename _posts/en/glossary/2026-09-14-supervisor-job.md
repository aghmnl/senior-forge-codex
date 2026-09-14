---
layout: post
title: "SupervisorJob"
date: 2026-09-14 12:00:00 +0000
categories: [en, glossary]
tags: [coroutines, cancellation, error-handling]
lang: en
permalink: /en/glossary/supervisor-job/
---

## The Theory (The What)

A **`SupervisorJob`** is a [`Job`]({{ "/en/glossary/job/" | relative_url }}) whose children fail independently: one child's exception does not cancel the parent, and therefore does not cancel its siblings. Everything else about the tree is unchanged — cancelling the supervisor still cancels every child. It is the right root for a [scope]({{ "/en/glossary/coroutine-scope/" | relative_url }}) that owns several unrelated long-running coroutines.

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

`viewModelScope` and `lifecycleScope` are built on a `SupervisorJob` for the same reason: one failed `launch` must not tear down every other coroutine on the screen.

## The Senior Nuance

- **It changes where uncaught exceptions go.** With a plain `Job`, a child's exception propagates up to the parent, which can handle it. With a `SupervisorJob` there is no upward propagation, so the exception goes to the [`CoroutineExceptionHandler`]({{ "/en/glossary/coroutine-exception-handler/" | relative_url }}) in the context — and if there is none, to the thread's uncaught handler, which crashes the app. A `SupervisorJob` without a handler is a crash waiting for a `collect` to throw.
- **It only supervises *direct* children.** Inside a child, the normal rules apply: a grandchild's failure still cancels its parent (the child). Supervision does not nest automatically.
- **`supervisorScope { }` is the structured, suspend-function form.** Use it for a bounded fan-out where failures should be independent; use `SupervisorJob()` in a `CoroutineScope(...)` for long-lived scopes.
- **Do not put it in `launch(SupervisorJob())`.** That detaches the coroutine from the scope's tree entirely — the scope can no longer cancel it. The supervisor belongs in the scope's context, not at the call site.
- See [Context & Dispatchers]({{ "/en/02-coroutines-flow/context-dispatchers/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
