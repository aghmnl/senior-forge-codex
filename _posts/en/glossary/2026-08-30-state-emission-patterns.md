---
layout: post
title: "State Emission Patterns"
date: 2026-08-30 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/state-emission-patterns/
---

## The Theory (The What)

**State emission patterns** describe how a ViewModel (or any state holder) produces and delivers state updates to its observers. In modern Android, the dominant pattern is exposing a read-only [StateFlow]({{ "/en/glossary/stateflow/" | relative_url }}) backed by a private `MutableStateFlow`, updating it atomically via `update {}` with `copy()`. The three main emission mechanisms are:

1. **`update {}`** — atomic read-modify-write through a lambda; thread-safe and conflict-free.
2. **`value =`** — direct assignment; simple but racy under concurrent writes.
3. **`emit()`** — suspend function used with `MutableSharedFlow`; allows backpressure handling.

```kotlin
// From FollowApp Suite — SettingsViewModel.kt
// Canonical emission pattern: private MutableStateFlow + public StateFlow
private val _uiState = MutableStateFlow(SettingsUiState())
val uiState: StateFlow<SettingsUiState> = _uiState.asStateFlow()

// Atomic update via update {} — the Senior-preferred emission method
_uiState.update {
    it.copy(
        timeZoneId = settings.timeZoneId,
        holidays = settings.holidays.sorted()
    )
}
```

## The Senior Nuance

- Always prefer `update {}` over `value =` for [StateFlow]({{ "/en/glossary/stateflow/" | relative_url }}). The `update` function uses a compare-and-set loop internally, so concurrent coroutines cannot overwrite each other's changes — a critical guarantee when multiple `collect` blocks write to the same state.
- [StateFlow]({{ "/en/glossary/stateflow/" | relative_url }}) is *conflated*: if the state is updated faster than collectors can process it, intermediate values are dropped. This is intentional — the UI only needs the latest state, not every intermediate step. For events that must not be lost (navigation, snackbar), use `SharedFlow` or a `Channel`.
- Using [data object]({{ "/en/01-kotlin-core/data-objects/" | relative_url }}) for stateless members of a [sealed hierarchy]({{ "/en/glossary/sealed-hierarchy/" | relative_url }}) avoids unnecessary [allocations]({{ "/en/glossary/allocations/" | relative_url }}) on every emission. A `data object Loading` is a [singleton]({{ "/en/glossary/singleton/" | relative_url }}) — emitting it thousands of times creates zero new objects.
- The `asStateFlow()` wrapper enforces read-only access at the type level: callers of `uiState` cannot cast it back to `MutableStateFlow` and mutate it. This is [intent signaling]({{ "/en/glossary/intent-signaling/" | relative_url }}) through the type system.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
