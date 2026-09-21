---
layout: post
title: "Context Preservation"
date: 2026-09-21 12:00:00 +0000
categories: [en, glossary]
tags: [flow, coroutines, concurrency]
lang: en
permalink: /en/glossary/context-preservation/
---

## The Theory (The What)

**Context preservation** is the [`Flow`]({{ "/en/glossary/flow/" | relative_url }}) invariant that a flow must [emit]({{ "/en/glossary/emit/" | relative_url }}) from the same [coroutine context]({{ "/en/glossary/coroutine-context/" | relative_url }}) in which it is collected. Emitting from another context — `flow { withContext(IO) { emit(x) } }` — throws `IllegalStateException: Flow invariant is violated`. The rule exists so that a flow's emissions stay sequential and its exceptions stay traceable; `flowOn` is the sanctioned way around it, because it changes the context of the whole [upstream]({{ "/en/glossary/upstream/" | relative_url }}) rather than of a single emission.

```kotlin
// Not found in FAS — standalone example
// Throws at runtime: "Flow invariant is violated"
fun broken(): Flow<String> = flow {
    withContext(Dispatchers.IO) { emit(readFile()) }
}

// Correct: the whole upstream moves, emissions stay in one context
fun correct(): Flow<String> = flow {
    emit(readFile())
}.flowOn(Dispatchers.IO)
```

## The Senior Nuance

- **The check is at runtime, not compile time.** `withContext` inside a `flow { }` builder compiles cleanly and fails on the first emission — often only on a device, in a path your tests do not cover.
- **`channelFlow` is the escape hatch.** When you genuinely need to emit from several coroutines (merging callbacks, parallel producers), `channelFlow { send(...) }` is concurrency-safe by design; a plain `flow { }` is not.
- **The invariant is why `flowOn` needs a channel.** Crossing a dispatcher boundary requires handing values to another coroutine, which is also what gives `flowOn` its [buffering]({{ "/en/glossary/buffer/" | relative_url }}) behaviour.
- See [withContext vs flowOn]({{ "/en/02-coroutines-flow/with-context-vs-flow-on/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
