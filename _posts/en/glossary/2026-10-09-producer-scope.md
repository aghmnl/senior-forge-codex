---
layout: post
title: "ProducerScope"
date: 2026-10-09 12:00:00 +0000
categories: [en, glossary]
tags: [coroutines, concurrency]
lang: en
permalink: /en/glossary/producer-scope/
---

## The Theory (The What)

**`ProducerScope<T>`** is the receiver of the blocks of `produce { }`, `channelFlow { }` and `callbackFlow { }`. It is both a [`CoroutineScope`]({{ "/en/glossary/coroutine-scope/" | relative_url }}) (you can [`launch`]({{ "/en/glossary/launch/" | relative_url }}) inside it) and a `SendChannel<T>` (you can [`send`]({{ "/en/glossary/send/" | relative_url }}), [`trySend`]({{ "/en/glossary/try-send/" | relative_url }}) and [`close`]({{ "/en/glossary/close/" | relative_url }})), and it exposes the [channel]({{ "/en/glossary/channel/" | relative_url }}) itself as [`channel`]({{ "/en/glossary/channel/" | relative_url }}).

## The Senior Nuance

- **Being a scope matters.** [Coroutines]({{ "/en/glossary/coroutines/" | relative_url }}) launched inside it are children of the producer, so they are cancelled when the collection stops; that is how [`channelFlow`]({{ "/en/glossary/channel-flow/" | relative_url }}) merges several sources safely.
- **Being a [`SendChannel`]({{ "/en/glossary/send-channel/" | relative_url }}) matters too**: [`close()`]({{ "/en/glossary/close/" | relative_url }}) and `close(cause)` end the stream from inside, which is how a [callback]({{ "/en/glossary/callbacks/" | relative_url }}) reports the end or an error.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
