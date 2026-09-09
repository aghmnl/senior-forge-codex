---
layout: post
title: "Read-Only View"
date: 2026-09-08 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/read-only-view/
---

## The Theory (El Qué)

Una **Read-Only View** (vista de solo lectura) es una referencia cuyo *tipo* omite las operaciones de mutación, sobre un objeto que puede seguir siendo mutable. Las [Collections]({{ "/es/glosario/collections/" | relative_url }}) de Kotlin están construidas así: `List<out E>` no declara `add` ni `remove`, y `MutableList<E>` la extiende con ellos. Hacer upcast de un `MutableList` a `List` produce una Read-Only View — no un objeto nuevo e [inmutable]({{ "/es/glosario/immutability/" | relative_url }}).

```kotlin
// De FollowApp Suite — GetLabelReferenceCounts.kt
operator fun invoke(tasks: List<Task>, scaleName: String): Map<String, Int> {
    val refCounts = mutableMapOf<String, Int>()
    // ...se puebla in-place...
    return refCounts     // devuelto como Read-Only View de un LinkedHashMap
}
```

## The Senior Nuance (El Matiz Senior)

- La vista es segura solo mientras el objeto subyacente sea inalcanzable para alguien que pueda [mutarlo]({{ "/es/glosario/mutation/" | relative_url }}). Devolver un acumulador local (como arriba) es seguro: la referencia mutable muere con el [Stack Frame]({{ "/es/glosario/stack-frame/" | relative_url }}). Exponer un `MutableList` privado de larga vida a través de una propiedad de solo lectura no lo es — los callers obtienen una ventana viva que puede cambiar bajo sus pies.
- Una Read-Only View es exactamente lo que hace segura a la [covarianza]({{ "/es/glosario/covariance/" | relative_url }}). `List<out E>` puede ser [covariante]({{ "/es/glosario/covariance/" | relative_url }}) porque no hay posición de escritura para `E`; `MutableList<E>` debe quedar [invariante]({{ "/es/glosario/invariance/" | relative_url }}).
- Para convertir una vista en un valor, tomá una [Defensive Copy]({{ "/es/glosario/defensive-copy/" | relative_url }}) con `toList()`, o usá una [Persistent Collection]({{ "/es/glosario/persistent-collections/" | relative_url }}). La interoperabilidad con Java saltea la vista por completo: un `List<String>` entregado a código Java es simplemente un `java.util.List` y se puede escribir.

**Documentación oficial:** [Collection types: read-only vs mutable](https://kotlinlang.org/docs/collections-overview.html#collection-types)

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
