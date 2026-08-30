---
layout: post
title: "Algebraic Data Types (ADTs)"
date: 2026-08-30 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/algebraic-data-types/
---

## The Theory (El Qué)

Los **Algebraic Data Types (ADTs)** (tipos de datos algebraicos) son tipos compuestos formados al combinar otros tipos a través de dos operaciones fundamentales: **sum types** (un valor es una de varias variantes) y **product types** (un valor contiene varios campos). En Kotlin, los sum types se modelan con `sealed class` / `sealed interface` ([jerarquías selladas]({{ "/es/glosario/sealed-hierarchy/" | relative_url }})), y los product types se modelan con `data class` (donde cada parámetro del constructor es un "factor" del producto). Juntos permiten definir un modelo de dominio cerrado y exhaustivo que el compilador puede verificar.

```kotlin
// De FollowApp Suite — RecurrenceRule.kt
// Sum type: RecurrenceEnd es exactamente una de estas tres variantes
sealed class RecurrenceEnd {
    data object Never : RecurrenceEnd()                          // variante unitaria (sin datos)
    data class AfterOccurrences(val remaining: Int) : RecurrenceEnd()  // product: 1 campo
    data class UntilDate(val date: Long) : RecurrenceEnd()             // product: 1 campo
}

// De FollowApp Suite — ArchiveUiState.kt
// Sum type: cada acción es un data object (variante sin estado)
sealed class ArchiveBulkAction {
    data object Unarchive : ArchiveBulkAction()
    data object Delete : ArchiveBulkAction()
}
```

## The Senior Nuance (El Matiz Senior)

- El poder de los ADTs es la exhaustividad: una expresión `when` sobre una jerarquía sellada requiere manejar cada variante. Agregar una nueva variante es un breaking change en tiempo de compilación — el compilador marca cada rama no manejada. Por eso los ADTs son la base de [transiciones de estado]({{ "/es/glosario/state-transitions/" | relative_url }}) seguras.
- Las variantes `data object` son el equivalente ADT de los unit types (variantes que no llevan datos). Son [singletons]({{ "/es/glosario/singleton/" | relative_url }}) y crean cero [allocations]({{ "/es/glosario/allocations/" | relative_url }}) al emitirse, lo cual importa en [patrones de emisión de estado]({{ "/es/glosario/state-emission-patterns/" | relative_url }}) de alta frecuencia.
- Los ADTs de Kotlin no son tan potentes como los de Haskell o el `enum` de Rust — carecen de desestructuración automática de patrones y definiciones de tipos recursivos. Pero combinados con smart casts en `when`, proveen la misma seguridad práctica para modelado de estado en Android.
- Al diseñar un ADT, preguntate: "¿Puedo enumerar cada estado legal?" Si sí, usá una jerarquía sellada. Si el conjunto de estados es abierto (plugins, tipos definidos por el usuario), usá una interfaz o [clase abstracta]({{ "/es/glosario/abstract-class/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
