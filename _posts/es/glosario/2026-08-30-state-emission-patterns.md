---
layout: post
title: "State Emission Patterns"
date: 2026-08-30 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/state-emission-patterns/
---

## The Theory (El Qué)

Los **state emission patterns** (patrones de emisión de estado) describen cómo un ViewModel (o cualquier state holder) produce y entrega actualizaciones de estado a sus observadores. En Android moderno, el patrón dominante es exponer un [StateFlow]({{ "/es/glosario/stateflow/" | relative_url }}) de solo lectura respaldado por un `MutableStateFlow` privado, actualizándolo atómicamente vía `update {}` con `copy()`. Los tres mecanismos de emisión principales son:

1. **`update {}`** — lectura-modificación-escritura atómica a través de un lambda; thread-safe y libre de conflictos.
2. **`value =`** — asignación directa; simple pero propensa a condiciones de carrera bajo escrituras concurrentes.
3. **`emit()`** — función suspendida usada con `MutableSharedFlow`; permite manejo de backpressure.

```kotlin
// De FollowApp Suite — SettingsViewModel.kt
// Patrón canónico de emisión: MutableStateFlow privado + StateFlow público
private val _uiState = MutableStateFlow(SettingsUiState())
val uiState: StateFlow<SettingsUiState> = _uiState.asStateFlow()

// Update atómico vía update {} — el método de emisión preferido por Seniors
_uiState.update {
    it.copy(
        timeZoneId = settings.timeZoneId,
        holidays = settings.holidays.sorted()
    )
}
```

## The Senior Nuance (El Matiz Senior)

- Siempre preferí `update {}` sobre `value =` para [StateFlow]({{ "/es/glosario/stateflow/" | relative_url }}). La función `update` usa internamente un loop de compare-and-set, así que coroutines concurrentes no pueden sobrescribir los cambios de las otras — una garantía crítica cuando múltiples bloques `collect` escriben al mismo estado.
- [StateFlow]({{ "/es/glosario/stateflow/" | relative_url }}) es *conflated*: si el estado se actualiza más rápido de lo que los collectors pueden procesarlo, los valores intermedios se descartan. Esto es intencional — la UI solo necesita el último estado, no cada paso intermedio. Para eventos que no deben perderse (navegación, snackbar), usá `SharedFlow` o un `Channel`.
- Usar [data object]({{ "/es/01-kotlin-core/data-objects/" | relative_url }}) para miembros sin estado de una [jerarquía sellada]({{ "/es/glosario/sealed-hierarchy/" | relative_url }}) evita [allocations]({{ "/es/glosario/allocations/" | relative_url }}) innecesarias en cada emisión. Un `data object Loading` es un [singleton]({{ "/es/glosario/singleton/" | relative_url }}) — emitirlo miles de veces crea cero objetos nuevos.
- El wrapper `asStateFlow()` fuerza acceso de solo lectura a nivel de tipos: los consumidores de `uiState` no pueden hacer cast de vuelta a `MutableStateFlow` y mutarlo. Esto es [intent signaling]({{ "/es/glosario/intent-signaling/" | relative_url }}) a través del sistema de tipos.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
