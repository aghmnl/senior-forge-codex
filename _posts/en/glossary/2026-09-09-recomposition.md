---
layout: post
title: "Recomposition"
date: 2026-09-09 12:00:00 +0000
categories: [en, glossary]
tags: [compose, state-management, immutability]
lang: en
permalink: /en/glossary/recomposition/
---

## The Theory (The What)

**Recomposition** is [Compose]({{ "/en/glossary/jetpack-compose/" | relative_url }})'s re-execution of a composable function when a state it read has changed. Compose records which composables read which state; when that state is written, only those readers are invalidated and run again.

```kotlin
// Reading uiState.selectedTaskIds subscribes this composable to it.
// A new state object with a different set re-runs this function; a state
// object that compares equal is skipped entirely.
val uiState by viewModel.uiState.collectAsStateWithLifecycle()
```

## The Senior Nuance

- The skipping decision is [`equals`]({{ "/en/glossary/equals/" | relative_url }}), not identity, but only for parameters whose types Compose considers [`@Stable`]({{ "/en/glossary/stable/" | relative_url }}). A `data class` of stable types qualifies; the same class holding a `MutableList` does not, and Compose conservatively recomposes it on every parent recomposition.
- Recomposition can run **more than once per frame and in any order**, and can be cancelled halfway. A composable body must therefore be a pure function of its inputs: side effects belong in `LaunchedEffect`/`DisposableEffect`, and per-frame allocations in the body are how a list starts dropping frames.
- The failure mode of a mutable state object is silent: the [`StateFlow`]({{ "/en/glossary/stateflow/" | relative_url }}) emits the *same instance* it emitted before, [`equals`]({{ "/en/glossary/equals/" | relative_url }}) says "unchanged", and the screen simply does not update. [Immutability]({{ "/en/glossary/immutability/" | relative_url }}) is what makes "the state changed" and "the object is different" the same statement.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
