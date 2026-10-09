---
layout: post
title: "Producer-Consumer"
date: 2026-10-02 12:00:00 +0000
categories: [en, glossary]
tags: [concurrency, design-patterns, coroutines]
lang: en
permalink: /en/glossary/producer-consumer/
---

## The Theory (The What)

**Producer-consumer** is the pattern where one part of the code, the **producer**, generates values, and another part, the **consumer**, processes them, connected by a queue in between. Each side works at its own pace: the queue absorbs the difference. In coroutines that queue is usually a [Channel]({{ "/en/glossary/channel/" | relative_url }}): the producer calls [send]({{ "/en/glossary/send/" | relative_url }}) and the consumer [receives]({{ "/en/glossary/receive/" | relative_url }}). When the producer is faster and the queue fills up, [backpressure]({{ "/en/glossary/backpressure/" | relative_url }}) makes it wait.

```kotlin
// Not found in FAS — standalone example
val pages = Channel<List<Task>>(capacity = 2)

launch {                                   // producer
    for (n in 0 until pageCount) pages.send(api.fetchPage(n))
    pages.close()
}
launch {                                   // consumer
    for (page in pages) dao.insertAll(page)
}
```

## The Senior Nuance

- **The queue decouples speeds, it does not erase the difference.** If the producer is always faster, a bounded queue makes it wait, and an unbounded one grows until memory runs out.
- **Several consumers on one queue split the work:** that is [fan-out]({{ "/en/glossary/fan-out/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
