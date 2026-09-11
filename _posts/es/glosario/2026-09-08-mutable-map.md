---
layout: post
title: "MutableMap"
date: 2026-09-08 12:00:00 +0000
categories: [es, glosario]
tags: [collections, generics]
lang: es
permalink: /es/glosario/mutable-map/
---

## The Theory (El Qué)

**`MutableMap<K, V>`** extiende [`Map`]({{ "/es/glosario/maps/" | relative_url }}) con [`put`]({{ "/es/glosario/put/" | relative_url }}) (también escrito `map[key] = value`), [`remove`]({{ "/es/glosario/remove/" | relative_url }}), [`clear`]({{ "/es/glosario/clear/" | relative_url }}) y los helpers `getOrPut` y `merge`. `mutableMapOf()` está respaldado por un `LinkedHashMap`.

```kotlin
// De FollowApp Suite — GetLabelReferenceCounts.kt
val refCounts = mutableMapOf<String, Int>()
tasks.forEach { task ->
    // ...
    refCounts[label] = (refCounts[label] ?: 0) + 1
}
return refCounts     // publicado como Map<String, Int>
```

## The Senior Nuance (El Matiz Senior)

- Contar y agrupar son los dos trabajos donde un `MutableMap` le gana a una cadena de [Collection Operators]({{ "/es/glosario/collection-operators/" | relative_url }}): la actualización in-place es una búsqueda hash por elemento, mientras que [`groupBy`]({{ "/es/glosario/group-by/" | relative_url }}) más `mapValues` construye primero un mapa intermedio de listas.
- `refCounts[k] = (refCounts[k] ?: 0) + 1` lee y escribe; `getOrPut(k) { 0 }` es la misma idea con una búsqueda en vez de dos. Ninguna es atómica — un `MutableMap` bajo [Concurrencia]({{ "/es/glosario/concurrency/" | relative_url }}) necesita confinamiento a un solo [Stack Frame]({{ "/es/glosario/stack-frame/" | relative_url }}), no un `ConcurrentHashMap` atornillado después.
- `Map<K, out V>` es [covariante]({{ "/es/glosario/covariance/" | relative_url }}) solo en su *valor*; `MutableMap<K, V>` es completamente [invariante]({{ "/es/glosario/invariance/" | relative_url }}). Las claves nunca son covariantes, en ninguna de las dos versiones, porque se hashean y se comparan.

**Documentación oficial:** [`kotlin.collections.MutableMap`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/-mutable-map/) · [Map-specific operations](https://kotlinlang.org/docs/map-operations.html)

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
