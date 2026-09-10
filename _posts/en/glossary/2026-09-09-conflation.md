---
layout: post
title: "Conflation"
date: 2026-09-09 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/conflation/
---

## The Theory (The What)

**Conflation** is dropping intermediate values when a consumer is slower than the producer, keeping only the most recent one. [`StateFlow`]({{ "/en/glossary/stateflow/" | relative_url }}) is conflated by definition: it holds exactly one value, and a collector that is busy will simply see the latest state when it comes back, not the queue of states it missed.

```kotlin
// Three rapid updates while the UI is recomposing.
// The collector may observe only the last one — and that is correct for state.
_uiState.update { it.copy(isLoading = true) }
_uiState.update { it.copy(activeTasks = tasks) }
_uiState.update { it.copy(isLoading = false) }
```

## The Senior Nuance

- Conflation is *right* for state and *wrong* for events. "The current filter set" only needs its latest value; "show a snackbar" needs to happen once per occurrence. Modelling a one-shot event as a `StateFlow` field is how a toast gets swallowed on a slow frame — or replayed after a configuration change.
- It is why a `StateFlow` is safe to publish from a hot loop: a producer emitting a hundred times per second cannot back up the UI, because there is no buffer to fill. `SharedFlow` with a buffer does not have that property.
- `StateFlow` conflates on [`equals`]({{ "/en/glossary/equals/" | relative_url }}), not just on speed: setting `value` to something equal to the current value emits nothing at all. With an [immutable]({{ "/en/glossary/immutability/" | relative_url }}) state class that is exactly the deduplication you want; with a mutable one it silently drops real changes.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
