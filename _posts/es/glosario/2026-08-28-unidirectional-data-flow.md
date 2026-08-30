---
layout: post
title: "Unidirectional Data Flow"
date: 2026-08-28 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/unidirectional-data-flow/
---

## The Theory (El Qué)

**Unidirectional Data Flow** (flujo unidireccional de datos, UDF) es un patrón arquitectónico donde los datos se mueven en una sola dirección a través de un pipeline definido: las acciones del usuario producen eventos, los eventos se procesan para producir nuevo estado, y el estado se renderiza en la UI. La UI nunca modifica el estado directamente — solo emite acciones. En Android, esto se implementa comúnmente a través del patrón MVI (Model-View-Intent): la View emite Intents, un Reducer los procesa contra el Model actual, y el nuevo Model resultante es observado por la View.

```kotlin
// De FollowApp Suite — SettingsViewModel.kt
// UDF: el ViewModel contiene la fuente única de verdad, la UI lo observa
private val _uiState = MutableStateFlow(SettingsUiState())
val uiState: StateFlow<SettingsUiState> = _uiState.asStateFlow()

// Updates de estado vía copy() — nunca mutando in-place
_uiState.update {
    it.copy(
        timeZoneId = settings.timeZoneId,
        holidays = settings.holidays.sorted()
    )
}
```

## The Senior Nuance (El Matiz Senior)

- UDF hace las [transiciones de estado]({{ "/es/glosario/state-transitions/" | relative_url }}) predecibles: dado el mismo estado actual y la misma acción, el resultado es siempre el mismo. Esto hace que el debugging, testing y time-travel debugging sean directos.
- La función `copy()` en `data class` es lo que hace UDF práctico en Kotlin: producís un nuevo estado desde el anterior sin [mutación]({{ "/es/glosario/mutation/" | relative_url }}), y [StateFlow]({{ "/es/glosario/stateflow/" | relative_url }}) / `LiveData` notifica a los observadores del cambio.
- UDF no requiere un framework. Un `ViewModel` con un `MutableStateFlow`, estado `data class` y `copy()` ya es una implementación completa de UDF. Librerías como Orbit, MVIKotlin o Circuit agregan estructura pero no capacidad. Ver [patrones de emisión de estado]({{ "/es/glosario/state-emission-patterns/" | relative_url }}) para la mecánica de updates atómicos.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
