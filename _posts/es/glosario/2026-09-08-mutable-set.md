---
layout: post
title: "MutableSet"
date: 2026-09-08 12:00:00 +0000
categories: [es, glosario]
tags: [collections, immutability]
lang: es
permalink: /es/glosario/mutable-set/
---

## The Theory (El Qué)

**`MutableSet<E>`** extiende [`Set`]({{ "/es/glosario/sets/" | relative_url }}) con [`add`]({{ "/es/glosario/add/" | relative_url }}), [`remove`]({{ "/es/glosario/remove/" | relative_url }}) y [`clear`]({{ "/es/glosario/clear/" | relative_url }}). `mutableSetOf()` está respaldado por un `LinkedHashSet`, así que el orden de iteración es el de inserción; `hashSetOf()` no garantiza orden alguno.

```kotlin
// De FollowApp Suite — TasksViewModel.kt
val parentIds = if (hasSubtasksFilter != null) {
    tasks.mapNotNullTo(mutableSetOf()) { it.parentTaskId }
} else emptySet()
```

## The Senior Nuance (El Matiz Senior)

- `mapNotNullTo(mutableSetOf())` es la forma fusionada idiomática: mapea y recolecta en la [Collection]({{ "/es/glosario/collections/" | relative_url }}) destino en una sola pasada, sin lista intermedia — y el resultado se tipa de vuelta a `Set` inmediatamente.
- [`add`]({{ "/es/glosario/add/" | relative_url }}) devuelve `false` cuando el elemento ya está, lo que convierte a un `MutableSet` en un acumulador deduplicador limpio: `if (seen.add(id)) { /* primera vez */ }` reemplaza el par `contains` + `add` por una sola búsqueda hash.
- Mutar un elemento después de insertarlo corrompe el set: su `hashCode` cambia, el elemento queda en el bucket equivocado y [`contains`]({{ "/es/glosario/contains/" | relative_url }}) devuelve `false` para un objeto que está físicamente adentro. Los elementos de un set deben ser [inmutables]({{ "/es/glosario/immutability/" | relative_url }}).

**Documentación oficial:** [`kotlin.collections.MutableSet`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/-mutable-set/)

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
