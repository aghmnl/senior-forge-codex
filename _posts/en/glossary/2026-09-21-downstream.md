---
layout: post
title: "Downstream"
date: 2026-09-21 12:00:00 +0000
categories: [en, glossary]
tags: [flow, coroutines]
lang: en
permalink: /en/glossary/downstream/
---

## The Theory (The What)

**Downstream** is everything that comes *after* a given point in a [`Flow`]({{ "/en/glossary/flow/" | relative_url }}) chain: the operators declared below it and, at the end, the [`collect`]({{ "/en/glossary/collect/" | relative_url }}) block. Downstream code always runs in the [context]({{ "/en/glossary/coroutine-context/" | relative_url }}) of whoever collects the flow — a `flowOn` placed above it has no effect on it. That asymmetry is the core of [withContext vs flowOn]({{ "/en/02-coroutines-flow/with-context-vs-flow-on/" | relative_url }}): `flowOn` governs upstream only.

```kotlin
// Not found in FAS — standalone example
viewModelScope.launch {                 // collector context: Main.immediate
    repository.tasks()                  // upstream: wherever flowOn says
        .map { it.toUiModel() }         // downstream: runs on Main
        .collect { _uiState.value = it } // downstream: runs on Main
}
```

## The Senior Nuance

- **The collector decides the downstream context, not the flow.** Launching the same flow from `viewModelScope` or from a background scope changes where every downstream operator runs — the flow declaration says nothing about it.
- **That is usually what you want.** Updating a `StateFlow` or touching UI state belongs on Main; keeping the mapping downstream and the I/O [upstream]({{ "/en/glossary/upstream/" | relative_url }}) of `flowOn` gives exactly that split.
- **Heavy work downstream blocks the collector.** A slow `map` after `flowOn` runs on Main and causes [jank]({{ "/en/glossary/jank/" | relative_url }}); move it above the `flowOn`.
- See [withContext vs flowOn]({{ "/en/02-coroutines-flow/with-context-vs-flow-on/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
