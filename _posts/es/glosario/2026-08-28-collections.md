---
layout: post
title: "Collections"
date: 2026-08-28 12:00:00 +0000
categories: [es, glosario]
tags: [collections, immutability]
lang: es
permalink: /es/glosario/collections/
---

## The Theory (El Qué)

Las **Collections** (colecciones) en Kotlin son contenedores que almacenan grupos de elementos. La biblioteca estándar provee tres familias principales: [`List`]({{ "/es/glosario/list/" | relative_url }}) (ordenada, indexada), [Set]({{ "/es/glosario/sets/" | relative_url }}) (elementos únicos) y [Map]({{ "/es/glosario/maps/" | relative_url }}) (pares clave-valor). Cada una tiene una interfaz de solo lectura ([`List`]({{ "/es/glosario/list/" | relative_url }}), [`Set`]({{ "/es/glosario/sets/" | relative_url }}), [`Map`]({{ "/es/glosario/maps/" | relative_url }})) y una contraparte mutable ([`MutableList`]({{ "/es/glosario/mutable-list/" | relative_url }}), [`MutableSet`]({{ "/es/glosario/mutable-set/" | relative_url }}), [`MutableMap`]({{ "/es/glosario/mutable-map/" | relative_url }})). La API de colecciones de Kotlin incluye un conjunto rico de operaciones funcionales — [`filter`]({{ "/es/glosario/filter/" | relative_url }}), [`map`]({{ "/es/glosario/map-operator/" | relative_url }}), `flatMap`, [`groupBy`]({{ "/es/glosario/group-by/" | relative_url }}), `associate`, `fold` y muchas más.

```kotlin
// De FollowApp Suite — LabelRepositoryImpl.kt
val optionsByLabelId = allOptions.groupBy { it.labelId }
labels.associate { labelEntity ->
    val label = labelEntity.toDomain()
    val options = (optionsByLabelId[labelEntity.id] ?: emptyList())
        .map { it.toDomain() }
    label to options
}
```

## The Senior Nuance (El Matiz Senior)

- Las colecciones de solo lectura de Kotlin son [Read-Only Views]({{ "/es/glosario/read-only-view/" | relative_url }}), no implementaciones inmutables. Una [`List`]({{ "/es/glosario/list/" | relative_url }}) retornada de una función puede estar respaldada por una [`MutableList`]({{ "/es/glosario/mutable-list/" | relative_url }}) — los llamadores no pueden [mutarla]({{ "/es/glosario/mutation/" | relative_url }}) a través de la interfaz, pero el productor sí. Para [inmutabilidad]({{ "/es/glosario/immutability/" | relative_url }}) estructural verdadera, usá una [Persistent Collection]({{ "/es/glosario/persistent-collections/" | relative_url }}) de `kotlinx.collections.immutable`.
- Las operaciones de colecciones como [`map`]({{ "/es/glosario/map-operator/" | relative_url }}), [`filter`]({{ "/es/glosario/filter/" | relative_url }}) y `flatMap` crean listas intermedias. Para datasets grandes, usá [`asSequence()`]({{ "/es/glosario/as-sequence/" | relative_url }}) para pasar a [Sequences]({{ "/es/glosario/sequences/" | relative_url }}) y evaluación lazy — las operaciones se ejecutan un elemento a la vez, evitando allocations intermedias. Pero para colecciones pequeñas (< ~1000 elementos), el overhead del mecanismo de sequences suele exceder el ahorro.
- En [`equals()`]({{ "/es/glosario/equals/" | relative_url }}) y `hashCode()` de data class, las propiedades de colección declaradas en el [constructor primario]({{ "/es/glosario/primary-constructor/" | relative_url }}) participan en la igualdad. Dos data classes con propiedades [`List<String>`]({{ "/es/glosario/list/" | relative_url }}) son iguales si las listas contienen los mismos elementos en el mismo orden — pero [`Set<String>`]({{ "/es/glosario/sets/" | relative_url }}) compara elementos sin importar el orden.

**Documentación oficial:** [`kotlin.collections`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/) · [Collections overview](https://kotlinlang.org/docs/collections-overview.html)

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
