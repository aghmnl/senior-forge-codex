---
layout: post
title: "WhileSubscribed"
date: 2026-09-25 12:00:00 +0000
categories: [en, glossary]
tags: [flow, lifecycle, performance]
lang: en
permalink: /en/glossary/while-subscribed/
---

## The Theory (The What)

**`SharingStarted.WhileSubscribed(stopTimeoutMillis, replayExpirationMillis)`** is the sharing strategy for [stateIn]({{ "/en/glossary/state-in/" | relative_url }}) and `shareIn` that keeps the [upstream]({{ "/en/glossary/upstream/" | relative_url }}) collection running **only while there is at least one subscriber**. When the last [collector]({{ "/en/glossary/collector/" | relative_url }}) leaves, it waits `stopTimeoutMillis` and then cancels the upstream; when a new subscriber arrives, it starts it again. `replayExpirationMillis` controls how long the cached value survives after the upstream stops (by default, forever).

```kotlin
// Not found in FAS — standalone example
.stateIn(
    scope = viewModelScope,
    // Survives a rotation (~1 s without subscribers),
    // stops the query after 5 s in the background
    started = SharingStarted.WhileSubscribed(5_000),
    initialValue = UiState.Loading
)
```

## The Senior Nuance

- **Why 5 seconds.** A configuration change removes the subscriber for a moment and adds it back. With a timeout of `0` the upstream would restart on every rotation; with `5_000` it survives the rotation but still stops when the user really leaves the app.
- **It only works if the collector actually leaves.** `collectAsState()` keeps collecting in the background, so `WhileSubscribed` never sees zero subscribers. It needs a [lifecycle-aware]({{ "/en/glossary/lifecycle-aware/" | relative_url }}) collector: [collectAsStateWithLifecycle]({{ "/en/glossary/collect-as-state-with-lifecycle/" | relative_url }}) or [repeatOnLifecycle]({{ "/en/glossary/repeat-on-lifecycle/" | relative_url }}).
- **Restarting means re-running.** When the upstream restarts it is a cold [Flow]({{ "/en/glossary/flow/" | relative_url }}) collected again from scratch: the query runs again and the UI briefly sees the cached value first.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
