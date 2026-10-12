---
layout: post
title: "flow { }"
date: 2026-10-09 12:00:00 +0000
categories: [en, glossary]
tags: [flow, coroutines]
lang: en
permalink: /en/glossary/flow-builder/
---

## The Theory (The What)

**`flow { }`** is the basic builder of a [cold]({{ "/en/glossary/cold-stream/" | relative_url }}) [`Flow`]({{ "/en/glossary/flow/" | relative_url }}). Its block runs every time someone collects, and it produces values by calling `emit(value)`, a [suspend function]({{ "/en/glossary/suspend-functions/" | relative_url }}) that hands each value to the [collector]({{ "/en/glossary/collector/" | relative_url }}) and waits until it has been processed.

```kotlin
// Not found in FAS — standalone example
fun countdown(from: Int): Flow<Int> = flow {
    for (i in from downTo 0) {
        emit(i)
        delay(1_000)
    }
}
```

## The Senior Nuance

- **Sequential and single-[coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) by contract.** Every [`emit`]({{ "/en/glossary/emit/" | relative_url }}) must happen in the [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) that collects: emitting from [`launch`]({{ "/en/glossary/launch/" | relative_url }}), [`withContext`]({{ "/en/glossary/with-context/" | relative_url }}) or a [callback]({{ "/en/glossary/callbacks/" | relative_url }}) on another [thread]({{ "/en/glossary/thread/" | relative_url }}) fails at [runtime]({{ "/en/glossary/runtime/" | relative_url }}) ("[Flow]({{ "/en/glossary/flow/" | relative_url }}) invariant is violated"). To change the [thread]({{ "/en/glossary/thread/" | relative_url }}), use [`flowOn`]({{ "/en/glossary/flow-on/" | relative_url }}); to [emit]({{ "/en/glossary/emit/" | relative_url }}) from several [coroutines]({{ "/en/glossary/coroutines/" | relative_url }}) or a [callback]({{ "/en/glossary/callbacks/" | relative_url }}), use [`channelFlow`]({{ "/en/glossary/channel-flow/" | relative_url }}) or [`callbackFlow`]({{ "/en/glossary/callback-flow/" | relative_url }}).
- **It is the cheapest builder**: no [channel]({{ "/en/glossary/channel/" | relative_url }}), no buffer, values go straight from producer to [collector]({{ "/en/glossary/collector/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
