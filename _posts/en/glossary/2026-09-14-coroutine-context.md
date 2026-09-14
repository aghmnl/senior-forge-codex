---
layout: post
title: "CoroutineContext"
date: 2026-09-14 12:00:00 +0000
categories: [en, glossary]
tags: [coroutines, threading, cancellation]
lang: en
permalink: /en/glossary/coroutine-context/
---

## The Theory (The What)

A **`CoroutineContext`** is the immutable, indexed set of elements every [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) carries: its [`Job`]({{ "/en/glossary/job/" | relative_url }}), its [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}), an optional [`CoroutineExceptionHandler`]({{ "/en/glossary/coroutine-exception-handler/" | relative_url }}) and a `CoroutineName`. Each element type occupies one slot, so contexts compose with `+` and a later element of the same type replaces the earlier one. A child coroutine inherits its parent's context; whatever is passed to `launch`, `async` or [`withContext`]({{ "/en/glossary/with-context/" | relative_url }}) is merged on top.

```kotlin
// From FollowApp Suite — TasksViewModel.kt
// Dispatchers.IO because viewModelScope defaults to Main.immediate,
// and Main is saturated by Compose's first composition on cold start.
viewModelScope.launch(Dispatchers.IO) {
    val snapshot = runCatching { tasksViewPreferences.read() }.getOrNull()
    // ...
}
```

`launch(Dispatchers.IO)` keeps `viewModelScope`'s `SupervisorJob` and `Main.immediate` is replaced by `IO` — only the dispatcher slot changed.

## The Senior Nuance

- **Inheritance is the whole point.** Cancellation works because a child's `Job` is created as a child of the parent's `Job` from the inherited context. Passing a *new* `Job()` to `launch` breaks that link — the coroutine is no longer cancelled with its scope, which is almost always a bug.
- **`coroutineContext` is readable from any suspend function.** `coroutineContext[Job]`, `coroutineContext[CoroutineDispatcher]` and `ensureActive()` all read it; that is how [cooperative cancellation]({{ "/en/glossary/cooperative-cancellation/" | relative_url }}) checks the current job without a parameter.
- **Not the same as `CoroutineScope`.** A [scope]({{ "/en/glossary/coroutine-scope/" | relative_url }}) is just an object holding a context and giving `launch` a receiver; the context is the data. `CoroutineScope(ctx).coroutineContext === ctx`.
- **Not the same as Android's `Context` either** — a classic interview mix-up. See [Context]({{ "/en/glossary/context-programming/" | relative_url }}) for the three meanings of the word.
- Full treatment in [Context & Dispatchers]({{ "/en/02-coroutines-flow/context-dispatchers/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
