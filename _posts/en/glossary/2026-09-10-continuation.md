---
layout: post
title: "Continuation"
date: 2026-09-10 12:00:00 +0000
categories: [en, glossary]
tags: [coroutines, compiler, memory]
lang: en
permalink: /en/glossary/continuation/
---

## The Theory (The What)

A **Continuation** is the object a [suspend function]({{ "/en/glossary/suspend-functions/" | relative_url }}) receives as its hidden last parameter after the compiler applies [Continuation-Passing Style]({{ "/en/glossary/continuation-passing-style/" | relative_url }}). It represents "the rest of the computation": it holds the caller's saved locals, the current [state machine]({{ "/en/glossary/state-machine/" | relative_url }}) label, and the [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}) to resume on. Calling `resume(value)` or `resumeWithException(e)` re-enters the suspended function at the [suspension point]({{ "/en/glossary/suspension-point/" | relative_url }}) where it left off.

```kotlin
// Not found in FAS — standalone example
// What you write:
suspend fun load(id: String): Task

// What the compiler emits (JVM signature):
fun load(id: String, cont: Continuation<Task>): Any?
```

Every `suspend` call in FAS — a [DAO]({{ "/en/glossary/dao/" | relative_url }}) query, a use case, `withContext` — passes its continuation down the chain, which is how the [Runtime]({{ "/en/glossary/runtime/" | relative_url }}) knows how to get back to the caller when the work completes.

## The Senior Nuance

- **It lives on the [heap]({{ "/en/glossary/heap/" | relative_url }}), not the [stack]({{ "/en/glossary/stack-frame/" | relative_url }}).** Locals that must survive a suspension are stored as fields of the continuation. That is why a suspended [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) costs a few hundred bytes, not a thread's stack.
- **It is a [callback]({{ "/en/glossary/callbacks/" | relative_url }}) you never write.** `suspendCancellableCoroutine` is the one place where user code touches a continuation directly — see [suspendCancellableCoroutine]({{ "/en/glossary/suspend-cancellable-coroutine/" | relative_url }}).
- **Resume exactly once.** Resuming twice throws `IllegalStateException`; never resuming leaks the coroutine forever. Both bugs come from hand-written bridges, never from generated code.
- Full mechanics in [Suspend Functions]({{ "/en/02-coroutines-flow/suspend-functions/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
