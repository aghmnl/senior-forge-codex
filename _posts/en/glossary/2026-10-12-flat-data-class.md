---
layout: post
title: "Flat Data Class"
date: 2026-10-12 12:00:00 +0000
categories: [en, glossary]
tags: [state-management, architecture, data-classes]
lang: en
permalink: /en/glossary/flat-data-class/
---

## The Theory (The What)

A **flat data class** is a way of modeling a screen's UI state as a single `data class` that holds every property side by side: flags (`isLoading`), nullable fields (`errorMessage`) and the data itself. Each change creates a new instance with `copy()`, usually inside `MutableStateFlow.update { }`.

```kotlin
// Not found in FAS — standalone example
data class SearchUiState(
    val isLoading: Boolean = false,
    val query: String = "",
    val results: List<Item> = emptyList(),
    val errorMessage: String? = null,
)
```

## The Senior Nuance

- **Fits screens whose concerns overlap** (search, filters, selection, forms), because each one can change without touching the others.
- **It can hold impossible combinations**, so consistency is the code's job: derived properties instead of contradicting flags, and tests for the transitions.
- See [UI State Modeling: Sealed vs Flat Data Class]({{ "/en/05-architecture/ui-state-modeling/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
