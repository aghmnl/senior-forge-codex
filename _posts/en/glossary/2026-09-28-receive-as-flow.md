---
layout: post
title: "receiveAsFlow"
date: 2026-09-28 12:00:00 +0000
categories: [en, glossary]
tags: [flow, concurrency, coroutines]
lang: en
permalink: /en/glossary/receive-as-flow/
---

## The Theory (The What)

**`receiveAsFlow()`** exposes a [Channel]({{ "/en/glossary/channel/" | relative_url }}) as a [Flow]({{ "/en/glossary/flow/" | relative_url }}). [Collecting]({{ "/en/glossary/collect/" | relative_url }}) it receives values from the channel, so the result keeps the channel's semantics: it is **hot**, values sent before anyone collects wait in the channel's buffer, and **each value goes to exactly one collector**. It is the usual way to expose a channel of one-shot events from a ViewModel without exposing `send`.

```kotlin
// Not found in FAS — standalone example
private val _events = Channel<UiEvent>(Channel.BUFFERED)
val events: Flow<UiEvent> = _events.receiveAsFlow()
```

## The Senior Nuance

- **Fan-out, not broadcast.** With two collectors, each value goes to one of them. If both screens must see every value, the primitive is a [SharedFlow]({{ "/en/glossary/sharedflow/" | relative_url }}), not a channel.
- **`receiveAsFlow` vs `consumeAsFlow`.** `receiveAsFlow` can be collected many times, one after another or concurrently, and cancelling a collector leaves the channel open. `consumeAsFlow` can be collected only once and cancels the channel when that collection ends; a second collection throws.
- **A value taken is a value gone.** Once a collector receives an event, it is out of the channel. If that collector is cancelled before handling it, for example during a configuration change, the event is lost.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
