---
layout: post
title: "Dispatchers.Default"
date: 2026-09-14 12:00:00 +0000
categories: [en, glossary]
tags: [coroutines, threading, performance]
lang: en
permalink: /en/glossary/dispatchers-default/
---

## The Theory (The What)

**`Dispatchers.Default`** is the [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}) for CPU-bound work: sorting, parsing, diffing, date arithmetic, image decoding. Its [thread pool]({{ "/en/glossary/thread-pool/" | relative_url }}) is sized to the number of cores (minimum 2), because more threads than cores cannot make computation faster. It is also the default for `launch`/`async` on a scope that specifies no dispatcher.

```kotlin
// From FollowApp Suite — TasksViewModel.kt
// Date math off the main thread: pattern scans over months/years
// must never stall input dispatching (popup ANR)
val suggested = withContext(Dispatchers.Default) {
    RecurrenceCalculator.suggestPatternDueDate(/* ... */)
}
```

## The Senior Nuance

- **Blocking on `Default` is the expensive mistake.** With only as many threads as cores, one thread parked in I/O removes a whole core from every other coroutine. Blocking work belongs on [`IO`]({{ "/en/glossary/dispatchers-io/" | relative_url }}).
- **"Slow" is not the criterion.** Date math is slow *and* CPU-bound → `Default`. A network call is slow *and* blocking → `IO`. Choose by what the thread does while it waits.
- **It shares threads with `IO`.** Hopping `Default → IO → Default` often reuses the same worker; the [Runtime]({{ "/en/glossary/runtime/" | relative_url }}) elides the switch when the parallelism limits allow.
- **Long CPU loops must cooperate.** Add `ensureActive()` or `yield()` so [cancellation]({{ "/en/glossary/cooperative-cancellation/" | relative_url }}) can reach them.
- See [Context & Dispatchers]({{ "/en/02-coroutines-flow/context-dispatchers/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
