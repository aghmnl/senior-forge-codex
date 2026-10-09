---
layout: post
title: "consumeAsFlow"
date: 2026-10-09 12:00:00 +0000
categories: [en, glossary]
tags: [flow, coroutines, cancellation]
lang: en
permalink: /en/glossary/consume-as-flow/
---

## The Theory (The What)

**`consumeAsFlow()`** exposes a [Channel]({{ "/en/glossary/channel/" | relative_url }}) as a [`Flow`]({{ "/en/glossary/flow/" | relative_url }}), like [`receiveAsFlow`]({{ "/en/glossary/receive-as-flow/" | relative_url }}), but **takes ownership** of it: the [flow]({{ "/en/glossary/flow/" | relative_url }}) can be collected **only once** (a second [`collect`]({{ "/en/glossary/collect/" | relative_url }}) throws an [`IllegalStateException`]({{ "/en/glossary/illegal-state-exception/" | relative_url }})), and when that collection ends, normally, with an error or by cancellation, it **cancels the [channel]({{ "/en/glossary/channel/" | relative_url }})**.

```kotlin
// Not found in FAS — standalone example
val progress = Channel<Int>(Channel.CONFLATED)
progress.consumeAsFlow()          // one collection; the channel dies with it
    .map { "$it%" }
    .collect { label.text = it }
```

## The Senior Nuance

- **Ownership is the whole difference.** [`receiveAsFlow`]({{ "/en/glossary/receive-as-flow/" | relative_url }}) lends the [channel]({{ "/en/glossary/channel/" | relative_url }}) and leaves it open; `consumeAsFlow` gives it to the [collector]({{ "/en/glossary/collector/" | relative_url }}) and closes it when that [collector]({{ "/en/glossary/collector/" | relative_url }}) is done.
- **Wrong choice for a [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}) [event]({{ "/en/glossary/one-shot-event/" | relative_url }}) [channel]({{ "/en/glossary/channel/" | relative_url }}).** Collection there is cancelled every time the screen goes to the background; with `consumeAsFlow`, that first cancellation kills the [channel]({{ "/en/glossary/channel/" | relative_url }}) and the next collection throws.
- **Right choice when the [channel]({{ "/en/glossary/channel/" | relative_url }}) exists for one collection**, and releasing it with that collection is exactly what you want.
- See [receiveAsFlow()]({{ "/en/02-coroutines-flow/receive-as-flow/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
