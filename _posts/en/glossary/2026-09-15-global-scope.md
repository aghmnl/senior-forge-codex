---
layout: post
title: "GlobalScope"
date: 2026-09-15 12:00:00 +0000
categories: [en, glossary]
tags: [coroutines, lifecycle, memory]
lang: en
permalink: /en/glossary/global-scope/
---

## The Theory (The What)

**`GlobalScope`** is a [`CoroutineScope`]({{ "/en/glossary/coroutine-scope/" | relative_url }}) with no [`Job`]({{ "/en/glossary/job/" | relative_url }}) in its context: coroutines launched on it have no parent, are never waited for, and can only be cancelled one by one through the `Job` that [`launch`]({{ "/en/glossary/launch/" | relative_url }}) returns. It is the explicit opt-out from structured concurrency, and `kotlinx.coroutines` marks it `@DelicateCoroutinesApi` for that reason.

```kotlin
// Not found in FAS — standalone example
GlobalScope.launch {          // no parent: outlives the screen, the ViewModel, the test
    repository.sync()
}
```

## The Senior Nuance

- **It is a process-lifetime scope with no owner.** A `@Singleton` needs a scope too, but `CoroutineScope(SupervisorJob() + Dispatchers.IO)` in a field at least *has* a `cancel()` someone can call and a place to add a [`CoroutineExceptionHandler`]({{ "/en/glossary/coroutine-exception-handler/" | relative_url }}).
- **Its coroutines are invisible to tests.** [`runTest`]({{ "/en/glossary/run-test/" | relative_url }}) cannot wait for them, so assertions race against real work.
- **It captures references for as long as it runs.** A `GlobalScope.launch` holding an Activity or View is a [memory leak]({{ "/en/glossary/memory-leaks/" | relative_url }}) until the coroutine finishes.
- See [Structured Concurrency]({{ "/en/02-coroutines-flow/structured-concurrency/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
