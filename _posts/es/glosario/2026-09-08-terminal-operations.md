---
layout: post
title: "Terminal Operations"
date: 2026-09-08 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/terminal-operations/
---

## The Theory (El Qué)

Una **Terminal Operation** (operación terminal) es la que consume una cadena y produce un valor en vez de otra cadena: `first`, `firstOrNull`, `any`, `all`, `none`, `count`, `sum`, `fold`, [`toList`]({{ "/es/glosario/to-list/" | relative_url }}), [`toSet`]({{ "/es/glosario/to-set/" | relative_url }}). Sobre una [Sequence]({{ "/es/glosario/sequences/" | relative_url }}) nada corre hasta que se llama una; sobre una [Collection]({{ "/es/glosario/collections/" | relative_url }}) común cada paso ya corrió de forma eager, y la terminal es simplemente el último.

```kotlin
// De FollowApp Suite — TasksViewModel.kt
// Corta temprano: se detiene en el primer día que coincide
val seed = (0..6).asSequence()
    .map { today.plusDays(it.toLong()) }
    .first { it.dayOfWeek in rule.weekdays }

// De FollowApp Suite — TasksViewModel.kt
val hasSubtask = tasks.any { it.parentTaskId != null }
val duplicate = state.activeTasks.any { it.title.equals(title, ignoreCase = true) }
```

## The Senior Nuance (El Matiz Senior)

- `any`, `all`, `none`, `first` y `find` **cortan temprano**: se detienen en el elemento que decide. `tasks.any { it.parentTaskId != null }` es `O(1)` en una lista cuya primera task tiene padre — mientras que `tasks.filter { ... }.isNotEmpty()` siempre recorre todo y asigna una lista para tirarla.
- `first { }` lanza `NoSuchElementException` cuando nada coincide; `firstOrNull { }` devuelve `null`. Elegir entre las dos es una decisión de [Intent-Signaling]({{ "/es/glosario/intent-signaling/" | relative_url }}) — lanzá cuando la ausencia es un bug, devolvé `null` cuando es un estado esperado.
- Las terminales son además donde se agota una [Sequence]({{ "/es/glosario/sequences/" | relative_url }}): es de una sola pasada, así que una segunda terminal sobre la misma sequence lanza excepción. Y [`sorted`]({{ "/es/glosario/sorted/" | relative_url }})/[`groupBy`]({{ "/es/glosario/group-by/" | relative_url }}) quedan en el medio — intermedias en la API, pero forzadas a bufferear todo, lo que cancela la lazyness.
- Ubicar bien la terminal es la mayor parte de la optimización: `map { }.first { }` sobre una lista mapea todos los elementos, mientras que la misma cadena sobre [`asSequence`]({{ "/es/glosario/as-sequence/" | relative_url }}) mapea solo hasta la coincidencia.

**Documentación oficial:** [`first`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/first.html) · [`any`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/any.html) · [Collection operations overview](https://kotlinlang.org/docs/collection-operations.html)

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
