---
layout: post
title: "State Transitions"
date: 2026-08-28 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/state-transitions/
---

## The Theory (El Qué)

Una **state transition** (transición de estado) es el cambio de un estado definido a otro en respuesta a un evento o acción. En Kotlin, las transiciones de estado se modelan comúnmente con jerarquías de `sealed class` o `sealed interface`, donde cada subclase representa un estado discreto, y las expresiones `when` aseguran el manejo exhaustivo de todas las transiciones posibles.

```kotlin
// De FollowApp Suite — FilterState.kt
sealed class ScaleFilterState {
    object Off : ScaleFilterState()
    data class Include(val values: Set<String>) : ScaleFilterState()
    object Exclude : ScaleFilterState()
}

// De FollowApp Suite — PresetMapper.kt
when (state) {
    is ScaleFilterState.Off -> json.put(key, JSONObject().put("type", "OFF"))
    is ScaleFilterState.Include -> { /* serialize values */ }
    is ScaleFilterState.Exclude -> json.put(key, JSONObject().put("type", "EXCLUDE"))
}
```

## The Senior Nuance (El Matiz Senior)

- Las jerarquías sealed + `when` crean una garantía en tiempo de compilación: agregar un nuevo estado te obliga a manejarlo en todas partes. Es el equivalente Kotlin de una máquina de estados — el compilador es el verificador.
- En arquitecturas de [flujo unidireccional]({{ "/es/glosario/unidirectional-data-flow/" | relative_url }}), las transiciones de estado ocurren a través de `copy()` en objetos de estado `data class` inmutables, nunca a través de [mutación]({{ "/es/glosario/mutation/" | relative_url }}). Esto hace que cada transición sea explícita, auditable y reproducible en tests.
- Un patrón Senior común es modelar las transiciones *ilegales* como errores de compilación: si `Loading` solo puede transicionar a `Success` o `Error`, hacé que esos sean los únicos subtipos de una sealed class. Si un desarrollador intenta ir de `Error` de vuelta a `Loading`, el sistema de tipos lo rechaza — no un chequeo en runtime.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
