---
layout: post
title: "ReceiveChannel"
date: 2026-10-09 12:00:00 +0000
categories: [en, glossary]
tags: [concurrency, coroutines]
lang: en
permalink: /en/glossary/receive-channel/
---

## The Theory (The What)

**`ReceiveChannel<T>`** is the **receiving side** of a [Channel]({{ "/en/glossary/channel/" | relative_url }}): the interface with [`receive`]({{ "/en/glossary/receive/" | relative_url }}), `tryReceive`, iteration (`for (x in channel)`) and [`cancel`]({{ "/en/glossary/cancel/" | relative_url }}). A [`Channel`]({{ "/en/glossary/channel/" | relative_url }}) implements both `SendChannel` and `ReceiveChannel`; exposing only the `ReceiveChannel` type lets a class hand out a [channel]({{ "/en/glossary/channel/" | relative_url }}) that others can read but not write to. `produce { }` returns one.

```kotlin
// Not found in FAS — standalone example
fun CoroutineScope.ticks(): ReceiveChannel<Int> = produce {
    var n = 0
    while (true) { send(n++); delay(1_000) }
}
```

## The Senior Nuance

- **It is the read-only view of a [channel]({{ "/en/glossary/channel/" | relative_url }})**, the same idea as exposing [`StateFlow`]({{ "/en/glossary/stateflow/" | relative_url }}) instead of [`MutableStateFlow`]({{ "/en/glossary/mutable-state-flow/" | relative_url }}).
- **[`cancel()`]({{ "/en/glossary/cancel/" | relative_url }}) belongs to the [receiver]({{ "/en/glossary/receive/" | relative_url }}).** The [consumer]({{ "/en/glossary/producer-consumer/" | relative_url }}) signals "I am done reading" with [`cancel()`]({{ "/en/glossary/cancel/" | relative_url }}); the [producer]({{ "/en/glossary/producer-consumer/" | relative_url }}) closes with [`close()`]({{ "/en/glossary/close/" | relative_url }}) on the `SendChannel` side.
- **Most UI code never sees it**: `receiveAsFlow()` turns it into a [`Flow`]({{ "/en/glossary/flow/" | relative_url }}), so the [consumer]({{ "/en/glossary/producer-consumer/" | relative_url }}) works with operators and lifecycle-aware collection instead.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
