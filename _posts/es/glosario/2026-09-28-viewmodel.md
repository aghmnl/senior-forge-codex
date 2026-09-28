---
layout: post
title: "ViewModel"
date: 2026-09-28 12:00:00 +0000
categories: [es, glosario]
tags: [architecture, lifecycle, state-management]
lang: es
permalink: /es/glosario/viewmodel/
---

## The Theory (El Qué)

Un **`ViewModel`** es la clase de Jetpack que mantiene el estado y la lógica de una pantalla y **sobrevive a los cambios de configuración**, como una rotación. La `Activity` o el `Fragment` se destruyen y se recrean; el `ViewModel` se guarda en un [ViewModelStore]({{ "/es/glosario/viewmodel-store/" | relative_url }}) y se le entrega a la nueva instancia. Es el [state holder]({{ "/es/glosario/state-holder/" | relative_url }}) habitual de una pantalla: expone el estado de UI (normalmente un [StateFlow]({{ "/es/glosario/stateflow/" | relative_url }})), recibe los eventos de la UI, y ejecuta trabajo en [viewModelScope]({{ "/es/glosario/viewmodel-scope/" | relative_url }}), que se cancela en [onCleared()]({{ "/es/glosario/on-cleared/" | relative_url }}) cuando la pantalla desaparece definitivamente.

```kotlin
// De FollowApp Suite — SettingsViewModel.kt
@HiltViewModel
class SettingsViewModel @Inject constructor(
    getPremiumStatusUseCase: GetPremiumStatusUseCase,
    // ... use cases inyectados por Hilt
) : ViewModel() {
    private val _uiState = MutableStateFlow(SettingsUiState())
    val uiState: StateFlow<SettingsUiState> = _uiState.asStateFlow()
}

// De FollowApp Suite — SettingsScreen.kt
// Después de una rotación vuelve la misma instancia
val viewModel: SettingsViewModel = hiltViewModel()
```

## The Senior Nuance (El Matiz Senior)

- **Sobrevive a la rotación, no a la muerte del proceso.** Si el sistema mata la app en background, el `ViewModel` también desaparece. El estado que tiene que sobrevivir a eso pasa por `SavedStateHandle` o por almacenamiento persistente.
- **Nunca debe guardar una referencia a la UI.** Mantener una `Activity`, una `View` o un `Context` atado a ellas produce una [memory leak]({{ "/es/glosario/memory-leaks/" | relative_url }}), porque el `ViewModel` vive más que ellas. Expone estado y la UI lo observa, nunca al revés.
- **No sabe nada de visibilidad.** `viewModelScope` sigue corriendo mientras la pantalla está en background. Por eso los flows colectados de forma eager en `init` siguen trabajando, y por eso se prefiere exponer el estado con [stateIn]({{ "/es/glosario/state-in/" | relative_url }}) y [WhileSubscribed]({{ "/es/glosario/while-subscribed/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
