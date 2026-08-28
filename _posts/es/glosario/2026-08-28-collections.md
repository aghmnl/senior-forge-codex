---
layout: post
title: "Collections"
date: 2026-08-28 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/collections/
---

## The Theory (El Qué)

Las **Collections** (colecciones) en Kotlin son contenedores que almacenan grupos de elementos. La biblioteca estándar provee tres familias principales: `List` (ordenada, indexada), [Set]({{ "/es/glosario/sets/" | relative_url }}) (elementos únicos) y [Map]({{ "/es/glosario/maps/" | relative_url }}) (pares clave-valor). Cada una tiene una interfaz de solo lectura (`List`, `Set`, `Map`) y una contraparte mutable (`MutableList`, `MutableSet`, `MutableMap`). La API de colecciones de Kotlin incluye un conjunto rico de operaciones funcionales — `filter`, `map`, `flatMap`, `groupBy`, `associate`, `fold` y muchas más.

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

- Las colecciones de solo lectura de Kotlin son interfaces, no implementaciones inmutables. Una `List` retornada de una función puede estar respaldada por una `MutableList` — los llamadores no pueden [mutarla]({{ "/es/glosario/mutation/" | relative_url }}) a través de la interfaz, pero el productor sí. Para inmutabilidad estructural verdadera, usá `kotlinx.collections.immutable`.
- Las operaciones de colecciones como `map`, `filter` y `flatMap` crean listas intermedias. Para datasets grandes, usá `asSequence()` para cambiar a evaluación lazy — las operaciones se ejecutan un elemento a la vez, evitando allocations intermedias. Pero para colecciones pequeñas (< ~1000 elementos), el overhead del mecanismo de sequences suele exceder el ahorro.
- En `equals()` y `hashCode()` de data class, las propiedades de colección declaradas en el [constructor primario]({{ "/es/glosario/primary-constructor/" | relative_url }}) participan en la igualdad. Dos data classes con propiedades `List<String>` son iguales si las listas contienen los mismos elementos en el mismo orden — pero `Set<String>` compara elementos sin importar el orden.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
