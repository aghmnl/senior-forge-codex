---
layout: post
title: "produceIn"
date: 2026-10-09 12:00:00 +0000
categories: [en, glossary]
tags: [flow, coroutines]
lang: en
permalink: /en/glossary/produce-in/
---

## The Theory (The What)

**`produceIn(scope)`** is the opposite of [`receiveAsFlow`]({{ "/en/glossary/receive-as-flow/" | relative_url }}): it turns a [`Flow`]({{ "/en/glossary/flow/" | relative_url }}) into a [`ReceiveChannel`]({{ "/en/glossary/receive-channel/" | relative_url }}). It launches a [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) in `scope` that collects the [flow]({{ "/en/glossary/flow/" | relative_url }}) and sends each value into a new [channel]({{ "/en/glossary/channel/" | relative_url }}), which it returns. The [channel]({{ "/en/glossary/channel/" | relative_url }}) closes when the [flow]({{ "/en/glossary/flow/" | relative_url }}) completes, and cancelling the [channel]({{ "/en/glossary/channel/" | relative_url }}) cancels the collection.

```kotlin
// Not found in FAS — standalone example
val updates: ReceiveChannel<Location> = locationFlow.produceIn(scope)
val first = updates.receive()       // pull values one at a time
```

## The Senior Nuance

- **It turns push into pull.** A [`Flow`]({{ "/en/glossary/flow/" | relative_url }}) pushes values to its [collector]({{ "/en/glossary/collector/" | relative_url }}); a [channel]({{ "/en/glossary/channel/" | relative_url }}) lets the [consumer]({{ "/en/glossary/producer-consumer/" | relative_url }}) [`receive`]({{ "/en/glossary/receive/" | relative_url }}) exactly when it is ready, which is useful in `select` expressions or when merging several sources by hand.
- **It starts a [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}), so it needs a scope and has a lifetime.** If nobody receives and nobody cancels the [channel]({{ "/en/glossary/channel/" | relative_url }}), that collection keeps running until the scope ends.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
