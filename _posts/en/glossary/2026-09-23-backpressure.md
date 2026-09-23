---
layout: post
title: "Backpressure"
date: 2026-09-23 12:00:00 +0000
categories: [en, glossary]
tags: [flow, coroutines, performance]
lang: en
permalink: /en/glossary/backpressure/
---

## The Theory (The What)

**Backpressure** is what happens when a producer emits faster than its consumer can process. A [`Flow`]({{ "/en/glossary/flow/" | relative_url }}) handles it by construction: [`emit`]({{ "/en/glossary/emit/" | relative_url }}) is a suspending function that does not return until the collector has finished with that value, so a slow consumer simply slows the producer down — no queue grows, no value is dropped, and nothing is lost. Opting out is explicit: [`buffer`]({{ "/en/glossary/buffer/" | relative_url }}) decouples them with a channel, `conflate()` keeps only the latest, and [`flowOn`]({{ "/en/glossary/flow-on/" | relative_url }}) buffers as a side effect.

```kotlin
// Not found in FAS — standalone example
// Sequential: total time ≈ producer + consumer
pages().collect { render(it) }

// Decoupled: producer runs ahead, memory grows
pages().buffer().collect { render(it) }

// Latest-only: no growth, intermediate values dropped
pages().conflate().collect { render(it) }
```

## The Senior Nuance

- **The default is the safe one.** Suspension-based backpressure cannot overflow memory, unlike a callback API that keeps pushing. That is one of the strongest arguments for flows over listeners.
- **For UI state, `conflate()` is usually right.** Rendering every intermediate value of a fast stream is wasted work: the screen only shows the last one.
- **Unbounded buffers are a leak in disguise.** `buffer(Channel.UNLIMITED)` in front of a slow collector grows until the process dies; pick a capacity or conflate.
- See [Flow (Cold Streams)]({{ "/en/02-coroutines-flow/flow-cold-streams/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
