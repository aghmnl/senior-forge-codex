---
layout: post
title: "awaitClose"
date: 2026-10-02 12:00:00 +0000
categories: [en, glossary]
tags: [flow, callbacks, cancellation]
lang: en
permalink: /en/glossary/await-close/
---

## The Theory (The What)

**`awaitClose { }`** is the last call inside a [callbackFlow]({{ "/en/glossary/callback-flow/" | relative_url }}) block. It **suspends** for as long as the flow is being collected, which keeps the registered callback alive, and when the collector stops (or the flow is [cancelled]({{ "/en/glossary/cancel/" | relative_url }})) it runs its lambda, where the callback is **unregistered**. It is what ties the life of a listener to the life of its collection.

```kotlin
// Not found in FAS — standalone example
fun clicks(view: View): Flow<Unit> = callbackFlow {
    view.setOnClickListener { trySend(Unit) }
    awaitClose { view.setOnClickListener(null) }   // cleanup when collection stops
}
```

## The Senior Nuance

- **It is mandatory.** If a `callbackFlow` block ends without `awaitClose`, the flow fails with an `IllegalStateException`. The rule exists because forgetting the cleanup is the classic listener leak.
- **The lambda is the cleanup, and it always runs.** Whether the collector finishes normally, is cancelled, or fails, the unregister code in `awaitClose` runs.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
