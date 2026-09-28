---
layout: post
title: "MutableSharedFlow"
date: 2026-09-28 12:00:00 +0000
categories: [en, glossary]
tags: [flow, concurrency, coroutines]
lang: en
permalink: /en/glossary/mutable-shared-flow/
---

## The Theory (The What)

**`MutableSharedFlow<T>`** is the writable version of [SharedFlow]({{ "/en/glossary/sharedflow/" | relative_url }}). The constructor function `MutableSharedFlow(replay, extraBufferCapacity, onBufferOverflow)` fixes its whole behavior: how many past values a new subscriber receives, how much room there is before [emit]({{ "/en/glossary/emit/" | relative_url }}) suspends, and what happens when the buffer is full. It adds [emit]({{ "/en/glossary/emit/" | relative_url }}) and [tryEmit]({{ "/en/glossary/try-emit/" | relative_url }}) to put values in, `subscriptionCount` (a [StateFlow]({{ "/en/glossary/stateflow/" | relative_url }}) with the number of active [collectors]({{ "/en/glossary/collector/" | relative_url }})) and [resetReplayCache()]({{ "/en/glossary/reset-replay-cache/" | relative_url }}). It stays private and is exposed read-only with [asSharedFlow()]({{ "/en/glossary/as-shared-flow/" | relative_url }}).

```kotlin
// Not found in FAS — standalone example
private val _refreshRequests = MutableSharedFlow<Unit>(
    extraBufferCapacity = 1,
    onBufferOverflow = BufferOverflow.DROP_OLDEST
)
val refreshRequests: SharedFlow<Unit> = _refreshRequests.asSharedFlow()

// subscriptionCount: do the expensive work only while someone listens
_refreshRequests.subscriptionCount
    .map { it > 0 }
    .distinctUntilChanged()
    .onEach { active -> if (active) startPolling() else stopPolling() }
    .launchIn(scope)
```

## The Senior Nuance

- **The defaults are a rendezvous.** `MutableSharedFlow<T>()` has no replay and no buffer: `emit` waits for every subscriber and [`tryEmit`]({{ "/en/glossary/try-emit/" | relative_url }}) fails whenever there is one. Most surprises with shared flows come from not choosing these parameters on purpose.
- **Drop policies need a buffer.** `DROP_OLDEST` and `DROP_LATEST` are only accepted when `replay` or `extraBufferCapacity` is above zero; with no buffer there is nothing to drop from.
- **`MutableStateFlow` is one too.** A [MutableStateFlow]({{ "/en/glossary/mutable-state-flow/" | relative_url }}) is a `MutableSharedFlow` with a fixed configuration, which is why it also has `subscriptionCount`, and why its [`resetReplayCache()`]({{ "/en/glossary/reset-replay-cache/" | relative_url }}) throws: a state flow must always have a value.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
