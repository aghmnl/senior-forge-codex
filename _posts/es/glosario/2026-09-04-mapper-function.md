---
layout: post
title: "Mapper Function"
date: 2026-09-04 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/mapper-function/
---

## The Theory (El Qué)

Una **mapper function** (función mapper) es una función cuya única responsabilidad es convertir un valor de un tipo a otro — típicamente entre [capas de datos]({{ "/es/glosario/data-layer/" | relative_url }}) en una arquitectura Android. En Kotlin, las mapper functions se escriben comúnmente como [extension functions]({{ "/es/glosario/extension-functions/" | relative_url }}) (ej., `fun LabelEntity.toDomain(): Label`) para que la conversión se lea naturalmente en el call site: `entity.toDomain()`.

Las mapper functions son los bloques constructivos de un [pipeline]({{ "/es/glosario/pipeline/" | relative_url }}) de [data transformation]({{ "/es/glosario/data-transformation/" | relative_url }}): cada función maneja un cruce de frontera (`Entity → Domain`, `Domain → UiState`), y se componen juntas a través de [operadores de colecciones]({{ "/es/glosario/collection-operators/" | relative_url }}) como `map`:

```kotlin
// From FollowApp Suite — LabelRepositoryImpl.kt
val options = (optionsByLabelId[labelEntity.id] ?: emptyList()).map { it.toDomain() }
```

## The Senior Nuance (El Matiz Senior)

- Un Senior mantiene las mapper functions **puras** — sin side effects, sin I/O, sin cadenas de [scope functions]({{ "/es/01-kotlin-core/scope-functions/" | relative_url }}) que oculten mutación. Un mapper puro es trivialmente testeable: dado input X, assert output Y.
- La convención de nombres importa: `toDomain()`, `toEntity()`, `toUiModel()` comunican dirección. Ubicarlas en un package dedicado `mapper` (como en `com.followapp.core.data.mapper`) señala que el archivo contiene solo lógica de [data transformation]({{ "/es/glosario/data-transformation/" | relative_url }}) — sin reglas de negocio.
- Un error común es dejar que las mapper functions crezcan hasta convertirse en mini use cases que obtienen datos, aplican reglas de negocio y transforman. Un Senior refuerza la frontera: las mapper functions convierten formas, los use cases orquestan comportamiento.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
