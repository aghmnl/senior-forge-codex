---
layout: post
title: "Channel Capacity"
date: 2026-10-09 12:00:00 +0000
categories: [en, glossary]
tags: [concurrency, coroutines]
lang: en
permalink: /en/glossary/channel-capacity/
---

## The Theory (The What)

The **capacity** of a [Channel]({{ "/en/glossary/channel/" | relative_url }}) is how many values it can hold while nobody has taken them yet. It is chosen when the channel is created, and it decides two things: when [`send`]({{ "/en/glossary/send/" | relative_url }}) has to **wait**, and when [`trySend`]({{ "/en/glossary/try-send/" | relative_url }}) **fails**. There are four kinds:

- **`RENDEZVOUS`** (the default, `Channel<T>()`): no room at all. A value only passes when a sender and a receiver meet, so `send` waits until someone [receives]({{ "/en/glossary/receive/" | relative_url }}), and `trySend` fails unless a receiver is already waiting.
- **`BUFFERED`**: a fixed amount of room (64 by default, or the number you pass, like `Channel(capacity = 10)`). `send` waits only when it is full, and `trySend` fails only when it is full.
- **`UNLIMITED`**: room without limit. `send` never waits and `trySend` never fails (except on a [closed]({{ "/en/glossary/close/" | relative_url }}) channel).
- **`CONFLATED`**: room for exactly one value, the latest. A new value **replaces** the one that was waiting, so `send` never waits, `trySend` never fails, and intermediate values are dropped on purpose.

```kotlin
// Not found in FAS — standalone example
val handoff = Channel<Task>()                          // RENDEZVOUS
val queue = Channel<Task>(capacity = 10)               // BUFFERED, room for 10
val unbounded = Channel<Task>(Channel.UNLIMITED)       // UNLIMITED
val latest = Channel<Location>(Channel.CONFLATED)      // CONFLATED, keeps the newest
```

## The Senior Nuance

- **Choose by asking "what happens when the consumer falls behind?".** With `RENDEZVOUS` or `BUFFERED`, the producer waits ([backpressure]({{ "/en/glossary/backpressure/" | relative_url }})). With `UNLIMITED`, memory grows. With `CONFLATED`, old values are lost. One of those three has to be acceptable for the data.
- **`UNLIMITED` is not "safe", it moves the problem.** A producer that is always faster fills an unlimited buffer until the app runs out of memory.
- **`CONFLATED` is the channel version of [conflation]({{ "/en/glossary/conflation/" | relative_url }})**, the same idea a `StateFlow` applies: only the latest value matters. It fits location updates or sensor readings, never something like a payment confirmation.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
