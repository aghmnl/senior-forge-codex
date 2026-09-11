---
layout: post
title: "Sequences"
date: 2026-09-08 12:00:00 +0000
categories: [es, glosario]
tags: [collections, functional, performance]
lang: es
permalink: /es/glosario/sequences/
---

## The Theory (El Qué)

Una **`Sequence<T>`** es la contraparte de evaluación perezosa de una [Collection]({{ "/es/glosario/collections/" | relative_url }}). Los [Collection Operators]({{ "/es/glosario/collection-operators/" | relative_url }}) sobre un `List` son *eager*: cada `map` o `filter` recorre todo el input y asigna una lista nueva. Sobre una `Sequence` son operaciones *intermedias* que construyen un pipeline; nada corre hasta que una operación terminal (`toList`, `first`, `sum`, `any`) tira de los elementos, uno por vez.

```kotlin
// De FollowApp Suite — TasksViewModel.kt
val seed = (0..6).asSequence()
    .map { today.plusDays(it.toLong()) }
    .first { it.dayOfWeek in rule.weekdays }   // corta en la primera coincidencia
```

## The Senior Nuance (El Matiz Senior)

- La ganancia es doble: sin [Allocations]({{ "/es/glosario/allocations/" | relative_url }}) intermedias, y con corte temprano en las [Terminal Operations]({{ "/es/glosario/terminal-operations/" | relative_url }}) — el `first` de arriba puede mapear un solo elemento en vez de todo el rango.
- El costo es [Overhead]({{ "/es/glosario/overhead/" | relative_url }}) por elemento: cada paso es un iterador con una llamada virtual y una [lambda]({{ "/es/glosario/lambdas/" | relative_url }}) capturada. Por debajo de unos mil elementos, o para una cadena de uno o dos pasos, la versión eager suele ser más rápida. Medí en vez de asumir.
- Algunas operaciones son inherentemente eager y fuerzan todo el pipeline: `sorted`, `groupBy` y `distinct` deben materializar todo. Una sequence que termina en `sorted` casi no gana nada.
- Una `Sequence` es de una sola pasada por defecto — iterarla dos veces lanza excepción. Eso la hace el tipo equivocado para guardar en un objeto de estado de UI; convertila con `toList()` en el límite.

**Documentación oficial:** [`kotlin.sequences.Sequence`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.sequences/-sequence/) · [Sequences](https://kotlinlang.org/docs/sequences.html)

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
