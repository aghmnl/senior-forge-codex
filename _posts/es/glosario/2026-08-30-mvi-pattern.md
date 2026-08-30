---
layout: post
title: "MVI Pattern"
date: 2026-08-30 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/mvi-pattern/
---

## The Theory (El Qué)

**MVI (Model-View-Intent)** es un patrón arquitectónico donde el estado de la UI fluye en una sola dirección: la **View** emite **Intents** del usuario (acciones), un procesador (generalmente el ViewModel) reduce esos intents contra el **Model** actual (estado) para producir un nuevo modelo, y la view observa y renderiza el nuevo estado. MVI es la realización Android-específica del [flujo unidireccional]({{ "/es/glosario/unidirectional-data-flow/" | relative_url }}).

```kotlin
// De FollowApp Suite — SettingsViewModel.kt
// MVI en práctica: Model (SettingsUiState), View (Composable),
// Intent (métodos del ViewModel como onThemeChanged, onLanguageChanged)

// MODEL — estado inmutable, actualizado solo vía copy()
data class SettingsUiState(
    val timeZoneId: String = "",
    val holidays: List<LocalDate> = emptyList(),
    val isPremium: Boolean = false,
    val themeMode: ThemeMode = ThemeMode.SYSTEM,
    val currentLanguage: String = "system"
)

// Procesamiento de INTENT — el ViewModel reduce acciones del usuario en updates de estado
private val _uiState = MutableStateFlow(SettingsUiState())
val uiState: StateFlow<SettingsUiState> = _uiState.asStateFlow()

// Cada método es un handler de Intent que produce un nuevo Model
fun onThemeChanged(mode: ThemeMode) {
    viewModelScope.launch {
        setThemeModeUseCase(mode)
        _uiState.update { it.copy(themeMode = mode) }
    }
}
```

## The Senior Nuance (El Matiz Senior)

- MVI no requiere un framework. Un `ViewModel` con un `MutableStateFlow`, un estado `data class` y `copy()` ya es una implementación completa de MVI. FAS usa este enfoque liviano en todo — sin Orbit, sin MVIKotlin, sin Circuit.
- Las [jerarquías selladas]({{ "/es/glosario/sealed-hierarchy/" | relative_url }}) son el compañero natural de MVI: el Model es una `data class`, los Intents pueden modelarse como una `sealed interface` (un subtipo por acción del usuario), y los side effects pueden ser una `sealed class` con [transiciones de estado]({{ "/es/glosario/state-transitions/" | relative_url }}). El compilador fuerza el manejo exhaustivo de cada intent y estado.
- El "Intent" en MVI no es el `android.content.Intent` de Android. Es un concepto de dominio: un tipo sellado que representa lo que el usuario quiere hacer. Confundir los dos es una trampa común en entrevistas.
- La debilidad de MVI es la verbosidad para pantallas simples. Si una pantalla tiene cinco piezas independientes de estado actualizadas desde cinco fuentes diferentes, cada `update { it.copy(...) }` es un handler de intent aunque no exista ninguna sealed class. El patrón está ahí — solo que implícito.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
