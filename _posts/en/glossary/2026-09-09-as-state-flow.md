---
layout: post
title: "asStateFlow"
date: 2026-09-09 12:00:00 +0000
categories: [en, glossary]
tags: [flow, state-management, architecture]
lang: en
permalink: /en/glossary/as-state-flow/
---

## The Theory (The What)

`asStateFlow()` wraps a `MutableStateFlow` in a read-only `StateFlow` view. It exists so a state holder can expose its state without exposing the ability to write it.

```kotlin
// From FollowApp Suite — TasksViewModel.kt
private val _uiState = MutableStateFlow(TasksUiState())
val uiState: StateFlow<TasksUiState> = _uiState.asStateFlow()
```

## The Senior Nuance

- The alternative, `val uiState: StateFlow<T> = _uiState`, is weaker than it looks: the declared type forbids writing, but a caller can downcast back to `MutableStateFlow` and emit. `asStateFlow()` returns a genuinely different object that delegates reads, so the cast fails. It is a [read-only view]({{ "/en/glossary/read-only-view/" | relative_url }}) that actually holds.
- It costs one wrapper allocation per state holder, forever, and buys an architectural boundary: the [ViewModel]({{ "/en/glossary/viewmodel-store/" | relative_url }}) is the only writer, which is the "unidirectional" half of [Unidirectional Data Flow]({{ "/en/glossary/unidirectional-data-flow/" | relative_url }}). Without it, a composable can push state upward and the flow stops being one-directional.
- It does **not** make the *value* immutable. If `TasksUiState` holds a `MutableList`, the UI can still mutate the contents through the read-only flow. `asStateFlow()` protects the pipe; [immutability]({{ "/en/glossary/immutability/" | relative_url }}) of the state class protects the payload — you need both.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
