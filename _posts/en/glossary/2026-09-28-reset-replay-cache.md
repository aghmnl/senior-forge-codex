---
layout: post
title: "resetReplayCache"
date: 2026-09-28 12:00:00 +0000
categories: [en, glossary]
tags: [flow, state-management]
lang: en
permalink: /en/glossary/reset-replay-cache/
---

## The Theory (The What)

**`resetReplayCache()`** empties the replay cache of a [MutableSharedFlow]({{ "/en/glossary/mutable-shared-flow/" | relative_url }}). After the call, **new** subscribers only receive values emitted from then on; subscribers that were already collecting still receive the values that were buffered for them. It only matters for shared flows created with `replay` above zero.

```kotlin
// Not found in FAS — standalone example
private val _banner = MutableSharedFlow<String>(replay = 1)

fun showBanner(text: String) { _banner.tryEmit(text) }

fun onBannerHandled() {
    // Without this, every new subscriber (a rotated screen) sees it again
    _banner.resetReplayCache()
}
```

## The Senior Nuance

- **It is usually a sign that the value is really state.** Clearing a replayed value "once it has been handled" is exactly the acknowledge pattern, done with a primitive that was not designed for it. Modeling the value as UI state that the UI acknowledges is simpler and survives process death.
- **Timing is fragile.** Between the emission and the reset, any new subscriber still receives the old value. Calling it too early drops the value for a screen that has not seen it yet.
- **It throws on a [StateFlow]({{ "/en/glossary/stateflow/" | relative_url }}).** Calling it on a [MutableStateFlow]({{ "/en/glossary/mutable-state-flow/" | relative_url }}) throws `UnsupportedOperationException`, because a state flow must always have a current value.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
