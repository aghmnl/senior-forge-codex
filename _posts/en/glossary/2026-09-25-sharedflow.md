---
layout: post
title: "SharedFlow"
date: 2026-09-25 12:00:00 +0000
categories: [en, glossary]
tags: [flow, coroutines, concurrency]
lang: en
permalink: /en/glossary/sharedflow/
---

## The Theory (The What)

**`SharedFlow<T>`** is the general [hot stream]({{ "/en/glossary/hot-stream/" | relative_url }}) of kotlinx.coroutines: a single source that **broadcasts every emission to all current [collectors]({{ "/en/glossary/collector/" | relative_url }})**. `MutableSharedFlow(replay, extraBufferCapacity, onBufferOverflow)` configures how many past values a new subscriber receives (`replay`), how much room there is before [emit]({{ "/en/glossary/emit/" | relative_url }}) suspends, and what happens when the buffer is full. It has no initial value, no current value and no equality filtering, and its `collect` never completes. [StateFlow]({{ "/en/glossary/stateflow/" | relative_url }}) is a `SharedFlow` with a fixed configuration: replay of 1, drop-oldest overflow, an initial value and [distinctUntilChanged]({{ "/en/glossary/distinct-until-changed/" | relative_url }}).

```kotlin
// Not found in FAS — standalone example
private val _events = MutableSharedFlow<UiEvent>()          // replay = 0
val events: SharedFlow<UiEvent> = _events.asSharedFlow()

fun onSaveClicked() {
    viewModelScope.launch {
        _events.emit(UiEvent.ShowSaved)   // suspends until every subscriber takes it
    }
}
```

## The Senior Nuance

- **With `replay = 0` and no subscribers, emissions are lost.** That is the point for real fire-and-forget signals and the trap for anything the UI must not miss (an event emitted while the screen is rotating simply disappears).
- **Broadcast, not queue.** Every collector gets every value. When a value must be handled exactly once by exactly one consumer, the primitive is a [Channel]({{ "/en/glossary/channel/" | relative_url }}).
- **`tryEmit` without buffer fails.** With the default configuration `tryEmit` returns `false` whenever a subscriber is present, because there is no room to put the value without suspending. It needs `extraBufferCapacity` or a non-suspending overflow policy.
- It is also what [stateIn]({{ "/en/glossary/state-in/" | relative_url }})'s sibling `shareIn` produces: one upstream collection shared by many subscribers.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
