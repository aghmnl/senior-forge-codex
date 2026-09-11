---
layout: post
title: "Mapper Pattern"
date: 2026-09-04 12:00:00 +0000
categories: [en, glossary]
tags: [architecture, design-patterns, functional]
lang: en
permalink: /en/glossary/mapper-pattern/
---

## The Theory (The What)

The **Mapper pattern** is an architectural pattern where each boundary between [data layers]({{ "/en/glossary/data-layer/" | relative_url }}) has dedicated [mapper functions]({{ "/en/glossary/mapper-function/" | relative_url }}) that convert between the layer-specific models. In a typical Android Clean Architecture setup, the transformation [pipeline]({{ "/en/glossary/pipeline/" | relative_url }}) looks like:

```
NetworkResponse → Entity → DomainModel → UiState
```

Each model exists because its layer has different concerns: `Entity` mirrors the database schema, `DomainModel` represents business logic, and `UiState` is shaped for the view. The mapper functions at each boundary ensure that changes in one layer (e.g., a database column rename) don't cascade through the rest of the application.

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

## The Senior Nuance

- A Senior knows that the Mapper pattern introduces [overhead]({{ "/en/glossary/overhead/" | relative_url }}) — more classes, more files, more boilerplate. The tradeoff is worth it when layers evolve independently (different teams, different release cycles) or when the mapping itself encodes logic (deserialization, default values, format conversion). For simple CRUD apps with 1:1 models, a Senior questions whether the pattern earns its cost.
- Mapper functions should be **bidirectional when needed** (`toDomain()` / `toEntity()`) but never forced. Some boundaries are one-way: `DomainModel → UiState` rarely needs a reverse mapper because the UI doesn't write back in the same shape.
- In Kotlin, [extension functions]({{ "/en/glossary/extension-functions/" | relative_url }}) are the idiomatic way to write mappers — they keep the conversion discoverable via autocomplete and readable at the call site: `entities.map { it.toDomain() }`.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
