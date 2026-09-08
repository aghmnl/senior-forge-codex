---
layout: post
title: "map (Operator)"
date: 2026-09-08 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/map-operator/
---

## The Theory (El Qué)

**`map { }`** aplica una transformación a cada elemento y devuelve un [`List`]({{ "/es/glosario/list/" | relative_url }}) nuevo con los resultados. Es el [Collection Operator]({{ "/es/glosario/collection-operators/" | relative_url }}) canónico y el núcleo de toda [Mapper Function]({{ "/es/glosario/mapper-function/" | relative_url }}) — no confundir con [`Map`]({{ "/es/glosario/maps/" | relative_url }}), la estructura clave-valor.

```kotlin
// De FollowApp Suite — TasksScreen.kt
onDragEnd = { onReorderComplete(localTasks.map { it.id }) }

// De FollowApp Suite — LabelRepositoryImpl.kt
val options = (optionsByLabelId[labelEntity.id] ?: emptyList()).map { it.toDomain() }
```

## The Senior Nuance (El Matiz Senior)

- `map` es eager y siempre asigna una lista completa de resultados. Una cadena de cuatro pasos sobre diez mil ítems asigna cuarenta mil entradas y le da trabajo al [Garbage Collector]({{ "/es/glosario/garbage-collector/" | relative_url }}); [`asSequence`]({{ "/es/glosario/as-sequence/" | relative_url }}) elimina las intermedias cuando la cadena es lo bastante larga como para importar.
- Existen variantes justo para los casos donde la cadena ingenua desperdicia una pasada: `mapNotNull` fusiona map + filter, `mapTo(target)` recolecta directo en un [`MutableSet`]({{ "/es/glosario/mutable-set/" | relative_url }}) o lista, `flatMap` aplana, `mapValues` transforma los valores de un [`Map`]({{ "/es/glosario/maps/" | relative_url }}) conservando las claves.
- Es además la herramienta de frontera entre capas: mapear entidades a modelos de dominio es lo que evita que la [Data Layer]({{ "/es/glosario/data-layer/" | relative_url }}) se filtre a la UI, y la [lambda]({{ "/es/glosario/lambdas/" | relative_url }}) se [inlinea]({{ "/es/glosario/inline-functions/" | relative_url }}), así que la abstracción no cuesta nada.

**Documentación oficial:** [`kotlin.collections.map`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/map.html)

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
