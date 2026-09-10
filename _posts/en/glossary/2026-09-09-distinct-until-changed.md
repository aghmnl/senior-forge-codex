---
layout: post
title: "distinctUntilChanged"
date: 2026-09-09 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/distinct-until-changed/
---

## The Theory (The What)

`distinctUntilChanged()` is a `Flow` operator that suppresses an emission when it is [equal]({{ "/en/glossary/equals/" | relative_url }}) to the previous one. It turns a stream of *events* into a stream of *changes*.

```kotlin
// From FollowApp Suite — TasksViewModel.kt
_uiState
    .map { s -> PersistKey(s.sortOrder, s.groupBy, s.doneFilter, /* ... */) }
    .distinctUntilChanged()
    .drop(1)
    .debounce(200L)
    .collect { key -> /* write preferences to disk */ }
```

## The Senior Nuance

- The idiom above is the important one: `map` to a **narrow projection** of the state, then `distinctUntilChanged`. The whole `TasksUiState` changes on every keystroke; the seven properties worth persisting change rarely. Without the projection, disk writes fire on every character typed.
- It compares with `equals`, so it inherits every immutability caveat. A projection holding a mutable collection can compare equal while its contents differ — the operator will swallow a real change, and the symptom is a preference that silently fails to persist.
- [`StateFlow`]({{ "/en/glossary/stateflow/" | relative_url }}) already applies this rule to its own value: setting `value` to something equal to the current value emits nothing. So `stateFlow.distinctUntilChanged()` is redundant, while `stateFlow.map { ... }.distinctUntilChanged()` is not — `map` produces a plain `Flow` with no such conflation.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
