---
layout: post
title: "ViewModel"
date: 2026-09-28 12:00:00 +0000
categories: [en, glossary]
tags: [architecture, lifecycle, state-management]
lang: en
permalink: /en/glossary/viewmodel/
---

## The Theory (The What)

A **`ViewModel`** is the Jetpack class that holds a screen's state and logic and **survives configuration changes** such as a rotation. The `Activity` or `Fragment` is destroyed and recreated; the `ViewModel` is kept in a [ViewModelStore]({{ "/en/glossary/viewmodel-store/" | relative_url }}) and handed back to the new instance. It is the usual [state holder]({{ "/en/glossary/state-holder/" | relative_url }}) of a screen: it exposes the UI state (typically a [StateFlow]({{ "/en/glossary/stateflow/" | relative_url }})), receives the UI's events, and runs work in [viewModelScope]({{ "/en/glossary/viewmodel-scope/" | relative_url }}), which is cancelled in [onCleared()]({{ "/en/glossary/on-cleared/" | relative_url }}) when the screen is gone for good.

```kotlin
// From FollowApp Suite — SettingsViewModel.kt
@HiltViewModel
class SettingsViewModel @Inject constructor(
    getPremiumStatusUseCase: GetPremiumStatusUseCase,
    // ... use cases injected by Hilt
) : ViewModel() {
    private val _uiState = MutableStateFlow(SettingsUiState())
    val uiState: StateFlow<SettingsUiState> = _uiState.asStateFlow()
}

// From FollowApp Suite — SettingsScreen.kt
// The same instance comes back after a rotation
val viewModel: SettingsViewModel = hiltViewModel()
```

## The Senior Nuance

- **It survives rotation, not process death.** If the system kills the app in the background, the `ViewModel` is gone too. State that must survive that goes through `SavedStateHandle` or persistent storage.
- **It must never hold a reference to the UI.** Keeping an `Activity`, a `View` or a `Context` tied to one causes a [memory leak]({{ "/en/glossary/memory-leaks/" | relative_url }}), because the `ViewModel` outlives them. It exposes state and the UI observes it, never the other way around.
- **It knows nothing about visibility.** `viewModelScope` keeps running while the screen is in the background. That is why flows collected eagerly in `init` keep working, and why exposing state with [stateIn]({{ "/en/glossary/state-in/" | relative_url }}) and [WhileSubscribed]({{ "/en/glossary/while-subscribed/" | relative_url }}) is preferred.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
