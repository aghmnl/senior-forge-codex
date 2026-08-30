---
layout: post
title: "StateFlow"
date: 2026-08-30 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/stateflow/
---

## The Theory (The What)

**StateFlow** is a Kotlin Coroutines primitive (`kotlinx.coroutines.flow.StateFlow`) that holds a single, observable value and emits it to all collectors. It is a hot, conflated flow: it always has a current value (accessible via `.value`), new collectors immediately receive the latest state, and duplicate consecutive emissions are suppressed via structural equality (`equals()`). Its mutable counterpart, `MutableStateFlow`, is the standard state holder in Android ViewModels.

```kotlin
// From FollowApp Suite — SettingsViewModel.kt
// The canonical StateFlow pattern in Android architecture
private val _uiState = MutableStateFlow(SettingsUiState())
val uiState: StateFlow<SettingsUiState> = _uiState.asStateFlow()

// Collectors receive the latest state immediately upon collection
viewModelScope.launch {
    getRecurrenceSettingsUseCase()
        .collect { settings ->
            _uiState.update {
                it.copy(
                    timeZoneId = settings.timeZoneId,
                    holidays = settings.holidays.sorted()
                )
            }
        }
}
```

## The Senior Nuance

- StateFlow uses `equals()` for conflation: if you emit a value that is structurally equal to the current one, collectors are not notified. This is why `data class` state objects are essential — their compiler-generated `equals()` makes conflation work correctly. A regular class without proper `equals()` would notify on every emission, even if nothing changed.
- The `_uiState` / `uiState` naming convention is not arbitrary — it enforces [unidirectional data flow]({{ "/en/glossary/unidirectional-data-flow/" | relative_url }}). The underscore-prefixed mutable version stays private to the ViewModel; the public read-only `StateFlow` prevents the UI from pushing state changes, ensuring all [state transitions]({{ "/en/glossary/state-transitions/" | relative_url }}) go through ViewModel methods.
- StateFlow vs LiveData: StateFlow is lifecycle-unaware, works in any Kotlin context (not just Android), supports `combine` / `map` / `flatMapLatest` operators, and has a clearly defined initial value. In Compose, `collectAsStateWithLifecycle()` bridges the lifecycle gap. There is no technical reason to choose LiveData in new code.
- For [state emission patterns]({{ "/en/glossary/state-emission-patterns/" | relative_url }}), always use `update {}` on `MutableStateFlow` — it is atomic and prevents concurrent overwrites, unlike direct `value =` assignment.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
