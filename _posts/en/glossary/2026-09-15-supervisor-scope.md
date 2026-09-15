---
layout: post
title: "supervisorScope"
date: 2026-09-15 12:00:00 +0000
categories: [en, glossary]
tags: [coroutines, cancellation, error-handling]
lang: en
permalink: /en/glossary/supervisor-scope/
---

## The Theory (The What)

**`supervisorScope { }`** is the sibling of [`coroutineScope { }`]({{ "/en/glossary/coroutine-scope-builder/" | relative_url }}): a [suspend function]({{ "/en/glossary/suspend-functions/" | relative_url }}) that creates a child scope, runs the block, and suspends until every coroutine launched inside it completes — but with [`SupervisorJob`]({{ "/en/glossary/supervisor-job/" | relative_url }}) semantics. A child that fails does **not** cancel its siblings or the scope; its exception goes to the [`CoroutineExceptionHandler`]({{ "/en/glossary/coroutine-exception-handler/" | relative_url }}) in the context (for [`launch`]({{ "/en/glossary/launch/" | relative_url }})) or stays in the [`Deferred`]({{ "/en/glossary/deferred/" | relative_url }}) (for [`async`]({{ "/en/glossary/async/" | relative_url }})).

```kotlin
// Not found in FAS — standalone example
suspend fun loadDashboardLenient(): Dashboard = supervisorScope {
    val header = async { api.header() }
    val items = async { api.items() }
    Dashboard(
        header = runCatching { header.await() }.getOrNull(),
        items = runCatching { items.await() }.getOrDefault(emptyList())
    )
}
```

## The Senior Nuance

- **Choose it when the children are independent units of work.** "Write as many as you can and report the failures" is `supervisorScope`; "all or nothing" is `coroutineScope`.
- **It still waits and still cancels downward.** Only *failure propagation between siblings* changes. Cancelling the enclosing coroutine cancels everything inside.
- **A `launch` failure inside it needs a handler.** With no [`CoroutineExceptionHandler`]({{ "/en/glossary/coroutine-exception-handler/" | relative_url }}) in the context, an uncaught exception in a `launch` child crashes the process even though the siblings survive.
- See [Structured Concurrency]({{ "/en/02-coroutines-flow/structured-concurrency/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
