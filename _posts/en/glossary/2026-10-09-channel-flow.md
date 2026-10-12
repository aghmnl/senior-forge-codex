---
layout: post
title: "channelFlow"
date: 2026-10-09 12:00:00 +0000
categories: [en, glossary]
tags: [flow, coroutines, concurrency]
lang: en
permalink: /en/glossary/channel-flow/
---

## The Theory (The What)

**`channelFlow { }`** builds a [cold]({{ "/en/glossary/cold-stream/" | relative_url }}) [`Flow`]({{ "/en/glossary/flow/" | relative_url }}) whose block runs in a [`ProducerScope`]({{ "/en/glossary/producer-scope/" | relative_url }}): values are sent into an internal [channel]({{ "/en/glossary/channel/" | relative_url }}) with [`send`]({{ "/en/glossary/send/" | relative_url }}) or [`trySend`]({{ "/en/glossary/try-send/" | relative_url }}), so they can come from **several [coroutines]({{ "/en/glossary/coroutines/" | relative_url }}) at once** or from another [thread]({{ "/en/glossary/thread/" | relative_url }}), which plain [`flow { }`]({{ "/en/glossary/flow-builder/" | relative_url }}) forbids.

```kotlin
// Not found in FAS — standalone example
fun search(query: String): Flow<Result> = channelFlow {
    launch { send(localSource.find(query)) }    // both run concurrently
    launch { send(remoteSource.find(query)) }
}
```

## The Senior Nuance

- **[`callbackFlow`]({{ "/en/glossary/callback-flow/" | relative_url }}) is `channelFlow` that requires [`awaitClose`]({{ "/en/glossary/await-close/" | relative_url }}).** Use `channelFlow` when the block itself does the work and finishes; use [`callbackFlow`]({{ "/en/glossary/callback-flow/" | relative_url }}) when the values come from a registered [callback]({{ "/en/glossary/callbacks/" | relative_url }}) that must be unregistered.
- **It costs a [channel]({{ "/en/glossary/channel/" | relative_url }}).** For a single sequential producer, [`flow { }`]({{ "/en/glossary/flow-builder/" | relative_url }}) is simpler and cheaper.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
