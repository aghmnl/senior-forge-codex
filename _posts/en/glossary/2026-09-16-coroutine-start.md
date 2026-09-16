---
layout: post
title: "CoroutineStart"
date: 2026-09-16 12:00:00 +0000
categories: [en, glossary]
tags: [coroutines, syntax]
lang: en
permalink: /en/glossary/coroutine-start/
---

## The Theory (The What)

**`CoroutineStart`** is the enum passed as the `start` parameter of [`launch`]({{ "/en/glossary/launch/" | relative_url }}) and [`async`]({{ "/en/glossary/async/" | relative_url }}) that decides *when* the new coroutine's block begins executing:

- **`DEFAULT`** — scheduled immediately on the [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}); runs at its first opportunity.
- **`LAZY`** — created but not started. It runs only when someone calls [`start()`]({{ "/en/glossary/start/" | relative_url }}), [`join()`]({{ "/en/glossary/join/" | relative_url }}) or [`await()`]({{ "/en/glossary/await/" | relative_url }}) on it. A lazy [`Deferred`]({{ "/en/glossary/deferred/" | relative_url }}) is a memoised, cancellable, on-demand computation.
- **`ATOMIC`** — like `DEFAULT`, but cannot be cancelled before its first [suspension point]({{ "/en/glossary/suspension-point/" | relative_url }}). Rarely needed.
- **`UNDISPATCHED`** — starts executing *in the caller's thread* up to the first suspension, then continues on the dispatcher. Framework-level.

```kotlin
// Not found in FAS — standalone example
val config = async(start = CoroutineStart.LAZY) { loadConfig() }   // nothing runs yet
// ... later, only if actually needed:
val c = config.await()                                              // starts it now
```

## The Senior Nuance

- **`LAZY` is the one worth knowing.** It expresses "compute this at most once, only if asked" without a manual `by lazy` plus scope juggling.
- **A lazy child that is never started blocks its parent.** [`coroutineScope`]({{ "/en/glossary/coroutine-scope-builder/" | relative_url }}) waits for all children, including a `LAZY` one nobody awaited — the parent never completes. Either await it, `start()` it, or `cancel()` it.
- **The rest is for library code.** `ATOMIC` and `UNDISPATCHED` are marked delicate for a reason; in application code the answer is almost always `DEFAULT`.
- See [Launch vs Async/Await]({{ "/en/02-coroutines-flow/launch-vs-async-await/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
