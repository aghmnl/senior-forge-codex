---
layout: post
title: "callbackFlow"
date: 2026-10-02 12:00:00 +0000
categories: [en, glossary]
tags: [flow, callbacks, coroutines]
lang: en
permalink: /en/glossary/callback-flow/
---

## The Theory (The What)

**`callbackFlow { }`** builds a [Flow]({{ "/en/glossary/flow/" | relative_url }}) from a [callback]({{ "/en/glossary/callbacks/" | relative_url }})-based API, such as location updates, a sensor or a listener. Inside the block you register the callback, and every time it fires you send the value into the flow with [trySend]({{ "/en/glossary/try-send/" | relative_url }}). The block ends with `awaitClose { }`, which keeps the flow alive while it is collected and **unregisters the callback** when the collector stops. Internally it is backed by a [Channel]({{ "/en/glossary/channel/" | relative_url }}), which is why callbacks can send values even though they cannot suspend.

```kotlin
// Not found in FAS — standalone example
fun locationUpdates(client: LocationClient): Flow<Location> = callbackFlow {
    val listener = LocationListener { location -> trySend(location) }
    client.register(listener)
    awaitClose { client.unregister(listener) }   // runs when collection stops
}
```

## The Senior Nuance

- **`awaitClose` is mandatory.** If the block ends without it, `callbackFlow` fails with an `IllegalStateException`; and without the cleanup lambda the callback is never unregistered and leaks.
- **It turns a push API into a cold flow.** Each collector registers its own callback, and stopping collection unregisters it, so the listener lives exactly as long as someone is listening.
- See [callbackFlow]({{ "/en/02-coroutines-flow/callback-flow/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
