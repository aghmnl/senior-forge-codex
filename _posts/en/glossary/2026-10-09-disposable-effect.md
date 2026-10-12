---
layout: post
title: "DisposableEffect"
date: 2026-10-09 12:00:00 +0000
categories: [en, glossary]
tags: [compose, lifecycle]
lang: en
permalink: /en/glossary/disposable-effect/
---

## The Theory (The What)

**`DisposableEffect(key) { ... onDispose { } }`** runs a setup block when the composable enters the [composition]({{ "/en/glossary/composition/" | relative_url }}) (or when its key changes) and requires an `onDispose` block that runs when it leaves (or before the setup runs again for a new key). It is the place to register and unregister [listeners]({{ "/en/glossary/listener/" | relative_url }}) or observers tied to a composable.

```kotlin
// Not found in FAS — standalone example
DisposableEffect(lifecycleOwner) {
    val observer = LifecycleEventObserver { _, event -> onEvent(event) }
    lifecycleOwner.lifecycle.addObserver(observer)
    onDispose { lifecycleOwner.lifecycle.removeObserver(observer) }
}
```

## The Senior Nuance

- **`onDispose` is mandatory on purpose**: every registration has its cleanup next to it, the same idea as [`awaitClose`]({{ "/en/glossary/await-close/" | relative_url }}) in [`callbackFlow`]({{ "/en/glossary/callback-flow/" | relative_url }}).
- **The key decides when it restarts.** With the wrong key, the effect keeps using an old object, or registers and unregisters on every [recomposition]({{ "/en/glossary/recomposition/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
