---
layout: post
title: "data object"
date: 2026-09-21 12:00:00 +0000
categories: [es, glosario]
tags: [sealed-types, state-management, oop]
lang: es
permalink: /es/glosario/data-object/
---

## The Theory (El Qué)

**`data object`** (estable desde Kotlin 1.9) es un [declaración object]({{ "/es/glosario/object/" | relative_url }}) con `toString`, `equals` y `hashCode` generados por el compilador. El `toString` imprime solo el nombre de la declaración — `Loading` en vez de `Loading@3a71f4dd` — que es toda la razón por la que existe. **No** genera `copy()` ni `componentN()`: un [singleton]({{ "/es/glosario/singleton/" | relative_url }}) no tiene propiedades de constructor que copiar ni desestructurar, y esa es la línea exacta que lo separa de una [Data Classes: copy, equals, toString]({{ "/es/01-kotlin-core/data-classes/" | relative_url }}).

```kotlin
// De FollowApp Suite — RecurrenceRule.kt
sealed class RecurrenceEnd {
    data object Never : RecurrenceEnd()                   // sin payload → data object
    data class AfterOccurrences(val remaining: Int) : RecurrenceEnd()
    data class UntilDate(val date: Long) : RecurrenceEnd()
}

println(RecurrenceEnd.Never)      // "Never", no "Never@3a71f4dd"
```

## The Senior Nuance (El Matiz Senior)

- **La convención para jerarquías selladas:** `data object` para los miembros sin estado, `data class` para los que llevan datos. Esa división es lo que hace legibles los logs, los reportes de crash y los mensajes de aserción de los tests.
- **Cero [allocations]({{ "/es/glosario/allocations/" | relative_url }}) para los estados sin datos.** Un `Loading` emitido mil veces por un [`StateFlow`]({{ "/es/glosario/stateflow/" | relative_url }}) reusa una instancia; una `data class Loading()` alocaría mil objetos para el GC.
- **Tiene que seguir siendo inmutable.** Una `var` adentro de un `data object` es estado global con la vida del proceso, y además rompe el contrato de [`hashCode`]({{ "/es/glosario/hash-code/" | relative_url }}) si el objeto está en una colección hash.
- Ver [Data Objects: Singleton & Memory Savings]({{ "/es/01-kotlin-core/data-objects/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
