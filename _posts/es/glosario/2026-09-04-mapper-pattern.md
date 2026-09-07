---
layout: post
title: "Mapper Pattern"
date: 2026-09-04 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/mapper-pattern/
---

## The Theory (El Qué)

El **Mapper pattern** (patrón Mapper) es un patrón arquitectónico donde cada frontera entre [capas de datos]({{ "/es/glosario/data-layer/" | relative_url }}) tiene [mapper functions]({{ "/es/glosario/mapper-function/" | relative_url }}) dedicadas que convierten entre los modelos específicos de cada capa. En un setup típico de Clean Architecture en Android, el [pipeline]({{ "/es/glosario/pipeline/" | relative_url }}) de transformación se ve así:

```
NetworkResponse → Entity → DomainModel → UiState
```

Cada modelo existe porque su capa tiene preocupaciones diferentes: `Entity` refleja el esquema de base de datos, `DomainModel` representa la lógica de negocio, y `UiState` está modelado para la vista. Las mapper functions en cada frontera aseguran que los cambios en una capa (ej., renombrar una columna de base de datos) no se propaguen por el resto de la aplicación.

```kotlin
// From FollowApp Suite — PresetMapper.kt
fun PresetEntity.toDomain(): Preset {
    return Preset(
        id = id,
        name = name,
        labelFilters = deserializeLabelFilters(labelFilters),
        scaleFilters = deserializeScaleFilters(scaleFilters),
        sortOrder = runCatching { ListSort.valueOf(sortOrder) }.getOrDefault(ListSort.TITLE_ASC),
        // ...
    )
}

fun Preset.toEntity(): PresetEntity {
    return PresetEntity(
        id = id,
        name = name,
        labelFilters = serializeLabelFilters(labelFilters),
        scaleFilters = serializeScaleFilters(scaleFilters),
        // ...
    )
}
```

## The Senior Nuance (El Matiz Senior)

- Un Senior sabe que el Mapper pattern introduce [overhead]({{ "/es/glosario/overhead/" | relative_url }}) — más clases, más archivos, más boilerplate. El tradeoff vale la pena cuando las capas evolucionan independientemente (distintos equipos, distintos ciclos de release) o cuando el mapping en sí codifica lógica (deserialización, valores por defecto, conversión de formato). Para apps CRUD simples con modelos 1:1, un Senior cuestiona si el patrón justifica su costo.
- Las mapper functions deben ser **bidireccionales cuando es necesario** (`toDomain()` / `toEntity()`) pero nunca forzadas. Algunas fronteras son unidireccionales: `DomainModel → UiState` raramente necesita un mapper inverso porque la UI no escribe de vuelta con la misma forma.
- En Kotlin, las [extension functions]({{ "/es/glosario/extension-functions/" | relative_url }}) son la forma idiomática de escribir mappers — mantienen la conversión descubrible vía autocomplete y legible en el call site: `entities.map { it.toDomain() }`.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
