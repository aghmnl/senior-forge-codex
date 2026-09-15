---
layout: post
title: "ensureActive"
date: 2026-09-15 12:00:00 +0000
categories: [en, glossary]
tags: [cancellation, coroutines]
lang: en
permalink: /en/glossary/ensure-active/
---

## The Theory (The What)

**`ensureActive()`** is the explicit cancellation check: it throws [`CancellationException`]({{ "/en/glossary/cancellation-exception/" | relative_url }}) if the current [`Job`]({{ "/en/glossary/job/" | relative_url }}) has been cancelled, and does nothing otherwise. Every `kotlinx.coroutines` [suspend function]({{ "/en/glossary/suspend-functions/" | relative_url }}) calls it (or an equivalent) on your behalf, which is why cancellation is only observed at [suspension points]({{ "/en/glossary/suspension-point/" | relative_url }}). Code that runs a long loop *without* suspending has no such point, and must call `ensureActive()` itself to stay [cooperative]({{ "/en/glossary/cooperative-cancellation/" | relative_url }}).

```kotlin
// Not found in FAS — standalone example
withContext(Dispatchers.Default) {
    for (chunk in bigList.chunked(500)) {
        ensureActive()          // otherwise cancellation waits for the whole loop
        index.addAll(chunk.map(::tokenize))
    }
}
```

## The Senior Nuance

- **Prefer it over `if (!isActive) return`.** Returning early completes the coroutine *normally*, hiding the cancellation from the parent. Throwing keeps the tree's semantics intact.
- **`yield()` does the same and also gives up the thread.** Use `yield()` when fairness matters, `ensureActive()` when you only need the check.
- **It is available on `Job`, `CoroutineScope` and `CoroutineContext`.** Inside a coroutine builder lambda the receiver is a scope, so a bare `ensureActive()` works.
- See [Structured Concurrency]({{ "/en/02-coroutines-flow/structured-concurrency/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
