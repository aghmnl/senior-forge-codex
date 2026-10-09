---
layout: post
title: "ChannelResult"
date: 2026-10-02 12:00:00 +0000
categories: [en, glossary]
tags: [coroutines, concurrency, error-handling]
lang: en
permalink: /en/glossary/channel-result/
---

## The Theory (The What)

**`ChannelResult`** is what [trySend]({{ "/en/glossary/try-send/" | relative_url }}) returns: a small value that says how the attempt went. It has three properties: **`isSuccess`** (the value was added), **`isFailure`** (it was not, for example because the buffer was full) and **`isClosed`** (it was not, because the channel is [closed]({{ "/en/glossary/close/" | relative_url }})). A closed result is also a failure, so `isFailure` is `true` in that case too. It never throws: the outcome is in the result, and it is up to the caller to look at it.

```kotlin
// Not found in FAS — standalone example
val result = channel.trySend(event)
when {
    result.isSuccess -> Unit
    result.isClosed -> Log.w(TAG, "Channel closed, event dropped")
    result.isFailure -> Log.w(TAG, "Buffer full, event dropped")
}
```

## The Senior Nuance

- **Ignoring it is how values get lost silently.** A failed `trySend` produces no error and no log unless the code checks the result.
- **Check `isClosed` before `isFailure`.** Since a closed result is also a failure, the order matters when each case needs different handling. The helpers `onSuccess`, `onFailure` and `onClosed` follow the same rule: `onFailure` also runs for a closed channel.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
