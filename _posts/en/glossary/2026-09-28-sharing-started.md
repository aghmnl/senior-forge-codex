---
layout: post
title: "SharingStarted"
date: 2026-09-28 12:00:00 +0000
categories: [en, glossary]
tags: [flow, lifecycle, performance]
lang: en
permalink: /en/glossary/sharing-started/
---

## The Theory (The What)

**`SharingStarted`** is the parameter of [stateIn]({{ "/en/glossary/state-in/" | relative_url }}) and [shareIn]({{ "/en/glossary/share-in/" | relative_url }}) that decides **when the shared [upstream]({{ "/en/glossary/upstream/" | relative_url }}) collection runs**. It has three built-in strategies:

- **`SharingStarted.Eagerly`**: starts immediately and never stops until the scope is cancelled.
- **`SharingStarted.Lazily`**: starts with the first subscriber and never stops after that.
- **[SharingStarted.WhileSubscribed]({{ "/en/glossary/while-subscribed/" | relative_url }})**: runs only while at least one [collector]({{ "/en/glossary/collector/" | relative_url }}) is subscribed, and stops after a timeout when the last one leaves.

```kotlin
// Not found in FAS — standalone example
val uiState = repository.observe()
    .map { it.toUiState() }
    .stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5_000),   // the usual choice for UI state
        initialValue = UiState.Loading
    )
```

## The Senior Nuance

- **`WhileSubscribed(5_000)` is the default for UI state.** It survives a rotation (the subscriber is gone for about a second) and still stops the work when the user leaves the app.
- **`Eagerly` and `Lazily` mean "for the whole life of the scope".** In an application-level scope, that is the whole life of the process. They fit data the app needs warm at all times, not a single screen.
- It is an interface, so a custom strategy is possible, but the three built-in ones cover practically every case.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
