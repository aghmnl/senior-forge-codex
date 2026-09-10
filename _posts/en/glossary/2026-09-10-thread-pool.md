---
layout: post
title: "Thread Pool"
date: 2026-09-10 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/thread-pool/
---

## The Theory (The What)

A **thread pool** is a fixed or bounded set of pre-created [threads]({{ "/en/glossary/thread/" | relative_url }}) that take tasks from a shared queue, so that work can be scheduled without paying thread creation on every call. `Dispatchers.Default` is a pool sized to the CPU core count (min 2); `Dispatchers.IO` shares the same underlying threads but allows up to 64 (or core count, whichever is larger) to be parked in [blocking calls]({{ "/en/glossary/blocking-call/" | relative_url }}) simultaneously. Room's query executor and OkHttp's connection dispatcher are pools too.

When a [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) resumes after a [suspension point]({{ "/en/glossary/suspension-point/" | relative_url }}), its [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}) enqueues the [Continuation]({{ "/en/glossary/continuation/" | relative_url }}) on the pool; whichever thread is free next runs it.

## The Senior Nuance

- **Pools are why "which thread am I on?" is the wrong question.** You are on *a* thread of the `IO` pool. It may differ from the one you were on before the last suspension.
- **`IO` is sized for parking, `Default` for computing.** Blocking on `Default` starves CPU work because there are only as many threads as cores. CPU-heavy loops on `IO` are wasteful but not harmful. Pick by the nature of the work.
- **`limitedParallelism(n)` carves a sub-pool.** `Dispatchers.IO.limitedParallelism(1)` gives you a single-threaded confinement for a legacy non-thread-safe SDK without creating a new thread.
- **Pools do not make code thread-safe.** Two coroutines on `Default` can run at the same instant; shared mutable state needs [thread safety]({{ "/en/glossary/thread-safety/" | relative_url }}) by construction.
- See [Suspend Functions]({{ "/en/02-coroutines-flow/suspend-functions/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
