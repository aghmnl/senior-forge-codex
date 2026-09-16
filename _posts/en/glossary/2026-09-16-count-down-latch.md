---
layout: post
title: "CountDownLatch"
date: 2026-09-16 12:00:00 +0000
categories: [en, glossary]
tags: [threading, concurrency, testing]
lang: en
permalink: /en/glossary/count-down-latch/
---

## The Theory (The What)

**`java.util.concurrent.CountDownLatch`** is a JVM synchroniser: a counter initialised to N, decremented with `countDown()`, and a blocking `await()` that parks the calling [thread]({{ "/en/glossary/thread/" | relative_url }}) until the counter reaches zero. It is the classic tool for "wait until N things have happened" across threads — and the classic tool in pre-coroutine Android tests for waiting on a [callback]({{ "/en/glossary/callbacks/" | relative_url }}).

```kotlin
// Not found in FAS — standalone example
val latch = CountDownLatch(1)
legacyApi.load { result -> captured = result; latch.countDown() }
latch.await(5, TimeUnit.SECONDS)      // blocks the test thread
```

## The Senior Nuance

- **Its `await()` blocks a thread; coroutine `await()` suspends.** Calling `CountDownLatch.await()` from a coroutine parks a dispatcher thread — on [Main]({{ "/en/glossary/dispatchers-main/" | relative_url }}) it is an ANR, on [Default]({{ "/en/glossary/dispatchers-default/" | relative_url }}) it starves a core.
- **The coroutine-native replacement is [`CompletableDeferred`]({{ "/en/glossary/completable-deferred/" | relative_url }}).** `CountDownLatch(1)` with a result you read afterwards is exactly `CompletableDeferred<T>`: `complete(value)` instead of `countDown()`, a suspending `await()` that returns the value.
- **Under [`runTest`]({{ "/en/glossary/run-test/" | relative_url }}) it is a deadlock.** Virtual time never advances while a real thread is blocked on a latch.
- See [Launch vs Async/Await]({{ "/en/02-coroutines-flow/launch-vs-async-await/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
