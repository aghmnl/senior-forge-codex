---
layout: post
title: "MVI Pattern"
date: 2026-08-30 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/mvi-pattern/
---

## The Theory (The What)

**MVI (Model-View-Intent)** is an architectural pattern where UI state flows in a single direction: the **View** emits user **Intents** (actions), a processor (often the ViewModel) reduces those intents against the current **Model** (state) to produce a new model, and the view observes and renders the new state. MVI is the Android-specific realization of [unidirectional data flow]({{ "/en/glossary/unidirectional-data-flow/" | relative_url }}).

```kotlin
// From FollowApp Suite — SettingsViewModel.kt
// MVI in practice: Model (SettingsUiState), View (Composable),
// Intent (ViewModel methods like onThemeChanged, onLanguageChanged)

// MODEL — immutable state, updated only via copy()
data class SettingsUiState(
    val timeZoneId: String = "",
    val holidays: List<LocalDate> = emptyList(),
    val isPremium: Boolean = false,
    val themeMode: ThemeMode = ThemeMode.SYSTEM,
    val currentLanguage: String = "system"
)

// INTENT processing — ViewModel reduces user actions into state updates
private val _uiState = MutableStateFlow(SettingsUiState())
val uiState: StateFlow<SettingsUiState> = _uiState.asStateFlow()

// Each method is an Intent handler that produces a new Model
fun onThemeChanged(mode: ThemeMode) {
    viewModelScope.launch {
        setThemeModeUseCase(mode)
        _uiState.update { it.copy(themeMode = mode) }
    }
}
```

## The Senior Nuance

- MVI does not require a framework. A `ViewModel` with a `MutableStateFlow`, a `data class` state, and `copy()` is already a complete MVI implementation. FAS uses this lightweight approach throughout — no Orbit, no MVIKotlin, no Circuit.
- [Sealed hierarchies]({{ "/en/glossary/sealed-hierarchy/" | relative_url }}) are MVI's natural partner: the Model is a `data class`, Intents can be modeled as a `sealed interface` (one subtype per user action), and side effects can be a `sealed class` with [state transitions]({{ "/en/glossary/state-transitions/" | relative_url }}). The compiler enforces exhaustive handling of every intent and state.
- The "Intent" in MVI is not Android's `android.content.Intent`. It is a domain concept: a sealed type representing what the user wants to do. Confusing the two is a common interview trap.
- MVI's weakness is verbosity for simple screens. If a screen has five independent pieces of state updated from five different sources, each `update { it.copy(...) }` is an intent handler even if no sealed class exists. The pattern is there — just implicit.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
