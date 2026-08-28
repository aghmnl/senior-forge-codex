---
layout: post
title: "Unidirectional Data Flow"
date: 2026-08-28 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/unidirectional-data-flow/
---

## The Theory (The What)

**Unidirectional Data Flow** (UDF) is an architectural pattern where data moves in a single direction through a defined pipeline: user actions produce events, events are processed to produce new state, and state is rendered to the UI. The UI never modifies state directly — it only emits actions. In Android, this is commonly implemented through the MVI (Model-View-Intent) pattern: the View emits Intents, a Reducer processes them against the current Model, and the resulting new Model is observed by the View.

```kotlin
// From FollowApp Suite — SettingsViewModel.kt
// UDF: ViewModel holds single source of truth, UI observes it
private val _uiState = MutableStateFlow(SettingsUiState())
val uiState: StateFlow<SettingsUiState> = _uiState.asStateFlow()

// State updates via copy() — never mutating in place
_uiState.update {
    it.copy(
        timeZoneId = settings.timeZoneId,
        holidays = settings.holidays.sorted()
    )
}
```

## The Senior Nuance

- UDF makes [state transitions]({{ "/en/glossary/state-transitions/" | relative_url }}) predictable: given the same current state and the same action, the result is always the same. This makes debugging, testing, and time-travel debugging straightforward.
- The `copy()` function on `data class` is what makes UDF practical in Kotlin: you produce a new state from the old one without [mutation]({{ "/en/glossary/mutation/" | relative_url }}), and `StateFlow` / `LiveData` notifies observers of the change.
- UDF does not require a framework. A `ViewModel` with a `MutableStateFlow`, `data class` state, and `copy()` is already a complete UDF implementation. Libraries like Orbit, MVIKotlin, or Circuit add structure but not capability.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
