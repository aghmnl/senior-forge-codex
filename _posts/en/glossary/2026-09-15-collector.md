---
layout: post
title: "Collector"
date: 2026-09-15 12:00:00 +0000
categories: [en, glossary]
tags: [flow, coroutines]
lang: en
permalink: /en/glossary/collector/
---

## The Theory (The What)

A **collector** is the coroutine that calls [`collect`]({{ "/en/glossary/collect/" | relative_url }}) on a [`Flow`]({{ "/en/glossary/flow/" | relative_url }}) — the consumer end of the stream. A cold `Flow` does nothing until a collector arrives; each collector triggers its own execution of the producer block. The collector is an ordinary coroutine node: it lives in the scope that launched it, suspends between emissions, and stops when its [`Job`]({{ "/en/glossary/job/" | relative_url }}) is cancelled or the flow completes.

```kotlin
// From FollowApp Suite — TasksViewModel.kt
subtasksJob = viewModelScope.launch {
    getSubtasksUseCase(task.id)
        .catch { error -> Log.e(TAG, "Error loading subtasks", error) }
        .collect { subtasks ->
            _uiState.update { it.copy(form = it.form.copy(subtasks = subtasks)) }
        }
}
```

## The Senior Nuance

- **A collector is a long-lived child.** For an infinite source (Room, [`StateFlow`]({{ "/en/glossary/stateflow/" | relative_url }})), `collect` never returns; the collector's coroutine ends only by cancellation. Its scope decides its lifetime.
- **One collector per source is often a rule.** Keeping a `Job?` and cancelling the previous collector before starting the next prevents two collectors writing competing values into the same state.
- **`.catch` is upstream-only.** It sees exceptions from the producer, not from the collector's lambda — and never a [`CancellationException`]({{ "/en/glossary/cancellation-exception/" | relative_url }}).
- See [Structured Concurrency]({{ "/en/02-coroutines-flow/structured-concurrency/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
