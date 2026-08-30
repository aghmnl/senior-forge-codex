---
layout: post
title: "StateFlow"
date: 2026-08-30 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/stateflow/
---

## The Theory (El Qué)

**StateFlow** es un primitivo de Kotlin Coroutines (`kotlinx.coroutines.flow.StateFlow`) que mantiene un único valor observable y lo emite a todos los collectors. Es un flow hot y conflated: siempre tiene un valor actual (accesible vía `.value`), los nuevos collectors reciben inmediatamente el último estado, y las emisiones consecutivas duplicadas se suprimen mediante igualdad estructural (`equals()`). Su contraparte mutable, `MutableStateFlow`, es el state holder estándar en ViewModels de Android.

```kotlin
// De FollowApp Suite — SettingsViewModel.kt
// El patrón canónico de StateFlow en arquitectura Android
private val _uiState = MutableStateFlow(SettingsUiState())
val uiState: StateFlow<SettingsUiState> = _uiState.asStateFlow()

// Los collectors reciben el último estado inmediatamente al colectar
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

## The Senior Nuance (El Matiz Senior)

- StateFlow usa `equals()` para la conflation: si emitís un valor que es estructuralmente igual al actual, los collectors no son notificados. Por eso los objetos de estado `data class` son esenciales — su `equals()` generado por el compilador hace que la conflation funcione correctamente. Una clase regular sin un `equals()` adecuado notificaría en cada emisión, aunque nada haya cambiado.
- La convención de nombres `_uiState` / `uiState` no es arbitraria — fuerza [flujo unidireccional]({{ "/es/glosario/unidirectional-data-flow/" | relative_url }}). La versión mutable con guión bajo se queda privada en el ViewModel; el `StateFlow` público de solo lectura previene que la UI haga push de cambios de estado, asegurando que todas las [transiciones de estado]({{ "/es/glosario/state-transitions/" | relative_url }}) pasen por métodos del ViewModel.
- StateFlow vs LiveData: StateFlow no depende del lifecycle, funciona en cualquier contexto Kotlin (no solo Android), soporta operadores `combine` / `map` / `flatMapLatest`, y tiene un valor inicial claramente definido. En Compose, `collectAsStateWithLifecycle()` cubre el gap del lifecycle. No hay razón técnica para elegir LiveData en código nuevo.
- Para [patrones de emisión de estado]({{ "/es/glosario/state-emission-patterns/" | relative_url }}), siempre usá `update {}` en `MutableStateFlow` — es atómico y previene sobrescrituras concurrentes, a diferencia de la asignación directa `value =`.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
