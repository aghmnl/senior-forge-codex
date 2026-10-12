---
layout: post
title: "SendChannel"
date: 2026-10-09 12:00:00 +0000
categories: [en, glossary]
tags: [concurrency, coroutines]
lang: en
permalink: /en/glossary/send-channel/
---

## The Theory (The What)

**`SendChannel<T>`** is the **sending side** of a [Channel]({{ "/en/glossary/channel/" | relative_url }}): the interface with [`send`]({{ "/en/glossary/send/" | relative_url }}), [`trySend`]({{ "/en/glossary/try-send/" | relative_url }}) and [`close`]({{ "/en/glossary/close/" | relative_url }}). A [`Channel`]({{ "/en/glossary/channel/" | relative_url }}) implements both `SendChannel` and [`ReceiveChannel`]({{ "/en/glossary/receive-channel/" | relative_url }}); handing out only the `SendChannel` type lets other code [produce]({{ "/en/glossary/produce/" | relative_url }}) values without being able to consume them.

## The Senior Nuance

- **[`close()`]({{ "/en/glossary/close/" | relative_url }}) belongs to the sender.** It means "no more values": receivers drain what is buffered and then finish. The receiving side stops early with [`cancel()`]({{ "/en/glossary/cancel/" | relative_url }}) instead.
- **[`ProducerScope`]({{ "/en/glossary/producer-scope/" | relative_url }}) is a `SendChannel`**, which is why [`trySend`]({{ "/en/glossary/try-send/" | relative_url }}) and [`close`]({{ "/en/glossary/close/" | relative_url }}) are available directly inside [`callbackFlow`]({{ "/en/glossary/callback-flow/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
