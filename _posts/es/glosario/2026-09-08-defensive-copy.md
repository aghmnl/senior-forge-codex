---
layout: post
title: "Defensive Copy"
date: 2026-09-08 12:00:00 +0000
categories: [es, glosario]
tags: [immutability, collections, concurrency]
lang: es
permalink: /es/glosario/defensive-copy/
---

## The Theory (El Qué)

Una **Defensive Copy** (copia defensiva) duplica un objeto mutable en un límite, de modo que ninguno de los dos lados pueda observar las [mutaciones]({{ "/es/glosario/mutation/" | relative_url }}) del otro. En Kotlin el idiom es `toList()`, `toSet()`, `toMap()` a la *salida* de un componente, y `toMutableList()` a la *entrada* cuando la intención es modificar.

```kotlin
// De FollowApp Suite — TasksScreen.kt
val source = localGroups[originIdx].tasks.toMutableList()
val target = localGroups[targetIdx].tasks.toMutableList()
```

## The Senior Nuance (El Matiz Senior)

- La copia es lo que asciende una [Read-Only View]({{ "/es/glosario/read-only-view/" | relative_url }}) a un valor real. `_items.toList()` cuesta una copia de array y elimina toda una clase de bugs de `ConcurrentModificationException` y de renderizado obsoleto.
- La copia es **shallow** (superficial): la [Collection]({{ "/es/glosario/collections/" | relative_url }}) nueva contiene las mismas referencias a elementos. Copiar un `List<TaskEntity>` protege la estructura de la lista, no las entidades — por eso los elementos deberían ser [Data Classes]({{ "/es/01-kotlin-core/data-classes/" | relative_url }}) [inmutables]({{ "/es/glosario/immutability/" | relative_url }}).
- Copiar en cada límite no es gratis: en un camino caliente es presión real de [Allocations]({{ "/es/glosario/allocations/" | relative_url }}). La alternativa no es saltear la copia — es no crear nunca un objeto mutable que escape, o usar una [Persistent Collection]({{ "/es/glosario/persistent-collections/" | relative_url }}) que comparte estructura en vez de copiar.

**Documentación oficial:** [`kotlin.collections.toList`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/to-list.html)

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
