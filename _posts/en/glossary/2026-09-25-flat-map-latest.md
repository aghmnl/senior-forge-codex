---
layout: post
title: "flatMapLatest"
date: 2026-09-25 12:00:00 +0000
categories: [en, glossary]
tags: [flow, cancellation, coroutines]
lang: en
permalink: /en/glossary/flat-map-latest/
---

## The Theory (The What)

**`flatMapLatest`** is a [Flow]({{ "/en/glossary/flow/" | relative_url }}) operator that maps each [upstream]({{ "/en/glossary/upstream/" | relative_url }}) value to a new inner flow and **collects only the latest one**: when a new value arrives, the inner flow of the previous value is cancelled and replaced. It is the tool for "the query depends on parameters that change": each new parameter set cancels the previous query and starts a new one. It is marked `@ExperimentalCoroutinesApi`.

```kotlin
// From FollowApp Suite — TasksViewModel.kt
// Each distinct QueryParams cancels the previous database query
// and starts a new one with the new sort and filters
@OptIn(ExperimentalCoroutinesApi::class)
private fun observeTasks() {
    viewModelScope.launch {
        _restored
            .filter { it }
            .flatMapLatest { _queryParams }
            .flatMapLatest { params ->
                if (params.query.isNotEmpty()) {
                    searchTasksUseCase(query = params.query, statuses = params.filters, sort = params.sort)
                } else {
                    getActiveTasksUseCase(params.sort)
                }
            }
            .collect { /* ... */ }
    }
}
```

## The Senior Nuance

- **Latest vs concat vs merge.** `flatMapLatest` cancels the old inner flow; `flatMapConcat` waits for it to finish before starting the next; `flatMapMerge` runs them concurrently. For a search box, only *latest* is correct: results for an old query must never arrive after the new one.
- **Cancellation is the feature.** The previous inner flow is cancelled through [cooperative cancellation]({{ "/en/glossary/cooperative-cancellation/" | relative_url }}), so the work inside must be cancellable for the saving to be real.
- **It pairs naturally with a [StateFlow]({{ "/en/glossary/stateflow/" | relative_url }}) of parameters.** Because a `StateFlow` drops equal writes, setting the same filters twice does not restart the query.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
