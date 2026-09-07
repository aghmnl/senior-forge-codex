---
layout: post
title: "Observable State"
date: 2026-09-04 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/observable-state/
---

## The Theory (The What)

**Observable state** is state that automatically notifies its observers when it changes. In Android development, observable state is the foundation of reactive UI: the UI subscribes to state, and when state changes, the UI updates without explicit imperative calls.

Kotlin and Android provide several observable state mechanisms:

- **Compose's [snapshot system]({{ "/en/glossary/snapshot-system/" | relative_url }})**: `mutableStateOf()` creates state that triggers recomposition when written. When used with the [`by`]({{ "/en/glossary/by-delegation/" | relative_url }}) [keyword]({{ "/en/glossary/keyword/" | relative_url }}) as a [delegated property]({{ "/en/01-kotlin-core/delegated-properties/" | relative_url }}), reads and writes look like plain variables while the snapshot system tracks every change.
- **[StateFlow]({{ "/en/glossary/stateflow/" | relative_url }})**: A [coroutine]({{ "/en/glossary/coroutines/" | relative_url }})-based observable state holder that emits the current value to new collectors and all subsequent updates. Converted to Compose state via `collectAsStateWithLifecycle()`.
- **`Delegates.observable`**: A [standard library]({{ "/en/glossary/standard-library/" | relative_url }}) [property delegate]({{ "/en/glossary/property-delegate/" | relative_url }}) that fires a callback after every property assignment.
- **LiveData** (legacy): An older [lifecycle-aware]({{ "/en/glossary/lifecycle-aware/" | relative_url }}) observable, largely superseded by [StateFlow]({{ "/en/glossary/stateflow/" | relative_url }}) and Compose state.

## The Senior Nuance

- A Senior chooses the right observable state mechanism for the layer: `mutableStateOf()` for UI-layer state inside Compose, [StateFlow]({{ "/en/glossary/stateflow/" | relative_url }}) for ViewModel-layer state that needs to survive recomposition and can be collected from multiple observers.
- Observable state in Compose uses structural equality (`equals()`) to determine whether recomposition is needed. If `equals()` returns `true`, the write is a no-op. This is why [`@Stable`]({{ "/en/glossary/stable/" | relative_url }}) classes must guarantee consistent `equals()` behavior.
- Not all state needs to be observable. Local computation variables, loop counters, and intermediate values should be plain `val`/`var`. Making everything observable adds [overhead]({{ "/en/glossary/overhead/" | relative_url }}) and obscures what actually drives the UI.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
