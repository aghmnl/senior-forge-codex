---
layout: post
title: "trySendBlocking"
date: 2026-10-02 12:00:00 +0000
categories: [en, glossary]
tags: [concurrency, threading, coroutines]
lang: en
permalink: /en/glossary/try-send-blocking/
---

## The Theory (The What)

**`trySendBlocking(value)`** sends a value into a [Channel]({{ "/en/glossary/channel/" | relative_url }}) from code that is **not a coroutine**, waiting for room by **blocking the current [thread]({{ "/en/glossary/thread/" | relative_url }})**. It is the bridge for a background thread that produces values (a socket reader, a legacy library) and must respect [backpressure]({{ "/en/glossary/backpressure/" | relative_url }}) instead of dropping values. Like [trySend]({{ "/en/glossary/try-send/" | relative_url }}), it returns a [ChannelResult]({{ "/en/glossary/channel-result/" | relative_url }}) instead of throwing.

```kotlin
// Not found in FAS — standalone example
// A legacy library delivers frames on its own background thread
legacyDecoder.setFrameCallback { frame ->
    frames.trySendBlocking(frame)   // blocks THIS thread until there is room
}
```

## The Senior Nuance

- **Never on the main thread.** Blocking the [main thread]({{ "/en/glossary/main-thread/" | relative_url }}) freezes the UI, and after a few seconds the system shows an [ANR]({{ "/en/glossary/anr/" | relative_url }}).
- **Inside a coroutine, use [send]({{ "/en/glossary/send/" | relative_url }}) instead.** `send` waits by suspending, which frees the thread; `trySendBlocking` waits by blocking it.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
