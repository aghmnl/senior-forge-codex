---
layout: post
title: "asSequence"
date: 2026-09-08 12:00:00 +0000
categories: [es, glosario]
tags: [collections, functional, performance]
lang: es
permalink: /es/glosario/as-sequence/
---

## The Theory (El Qué)

**`asSequence()`** envuelve una [Collection]({{ "/es/glosario/collections/" | relative_url }}) (o un `Iterator`) en una [Sequence]({{ "/es/glosario/sequences/" | relative_url }}), cambiando los [Collection Operators]({{ "/es/glosario/collection-operators/" | relative_url }}) que siguen de eager a lazy: nada se computa hasta que una operación terminal tira de los elementos a través de la cadena, uno por vez.

```kotlin
// De FollowApp Suite — TasksViewModel.kt
// Buscar la próxima fecha que cumple la regla de recurrencia: corta en el primer acierto
val seed = (0..6).asSequence()
    .map { today.plusDays(it.toLong()) }
    .first { it.dayOfWeek in rule.weekdays }

// De FollowApp Suite — TaskMapper.kt
obj.keys().asSequence().associate { key -> /* ... */ }
```

## The Senior Nuance (El Matiz Senior)

- Las dos razones para usarlo son el corte temprano y adaptar una fuente que no es una colección. El primer snippet mapea solo hasta que el predicado coincide; el segundo es el puente idiomático desde un `Iterator` de Java (`JSONObject.keys()`) hacia los operadores de Kotlin sin materializar una lista primero.
- No es una optimización por defecto. Por debajo de unos mil elementos el [Overhead]({{ "/es/glosario/overhead/" | relative_url }}) por elemento de la cadena de iteradores supera las [Allocations]({{ "/es/glosario/allocations/" | relative_url }}) que ahorra, y una cadena que termina en [`sorted`]({{ "/es/glosario/sorted/" | relative_url }}) o [`groupBy`]({{ "/es/glosario/group-by/" | relative_url }}) materializa todo de todas formas.
- El resultado es de una sola pasada: iterar la misma sequence dos veces lanza excepción. Llamá [`toList`]({{ "/es/glosario/to-list/" | relative_url }}) en el límite antes de guardarla en cualquier lado.

**Documentación oficial:** [`kotlin.collections.asSequence`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/as-sequence.html) · [Sequences](https://kotlinlang.org/docs/sequences.html)

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
