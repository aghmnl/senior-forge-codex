---
layout: post
title: "ArrayList"
date: 2026-09-08 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/arraylist/
---

## The Theory (El Qué)

**`ArrayList<E>`** es la implementación concreta respaldada por un array que está detrás de casi todo [`MutableList`]({{ "/es/glosario/mutable-list/" | relative_url }}) en Kotlin — `mutableListOf()`, [`toMutableList`]({{ "/es/glosario/to-mutable-list/" | relative_url }}) y [`buildList`]({{ "/es/glosario/build-list/" | relative_url }}) devuelven uno. El acceso indexado es `O(1)`; [`add`]({{ "/es/glosario/add/" | relative_url }}) es `O(1)` amortizado, creciendo por copia a un array más grande cuando se llena.

```kotlin
// De FollowApp Suite — LegacyTaskReader.kt
val tasks = ArrayList<LegacyTask>(cursor.count)   // predimensionado: sin copias de crecimiento
while (cursor.moveToNext()) {
    tasks.add(LegacyTask(/* ... */))
}
```

## The Senior Nuance (El Matiz Senior)

- Nombrar `ArrayList` explícitamente se justifica exactamente cuando conocés el tamaño de antemano, como arriba: predimensionar el array de respaldo convierte una secuencia de [Allocations]({{ "/es/glosario/allocations/" | relative_url }}) de crecer-y-copiar en una sola. En cualquier otro lado, `mutableListOf()` dice lo mismo sobre la intención y menos sobre la implementación.
- `removeAt(0)` y `add(0, e)` desplazan todos los elementos restantes — `O(n)`. Una lista usada como cola debería ser un `ArrayDeque`, no un `ArrayList`.
- Es la razón por la que una [Read-Only View]({{ "/es/glosario/read-only-view/" | relative_url }}) no es [Inmutabilidad]({{ "/es/glosario/immutability/" | relative_url }}): un [`List`]({{ "/es/glosario/list/" | relative_url }}) devuelto por una función es, en [Runtime]({{ "/es/glosario/runtime/" | relative_url }}), normalmente un `ArrayList` común que la interoperabilidad con Java puede escribir sin problema.

**Documentación oficial:** [`kotlin.collections.ArrayList`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/-array-list/)

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
