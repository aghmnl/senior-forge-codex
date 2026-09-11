---
layout: post
title: "Mapper Function"
date: 2026-09-04 12:00:00 +0000
categories: [en, glossary]
tags: [architecture, functional]
lang: en
permalink: /en/glossary/mapper-function/
---

## The Theory (The What)

A **mapper function** is a function whose sole responsibility is converting a value from one type to another — typically between [data layers]({{ "/en/glossary/data-layer/" | relative_url }}) in an Android architecture. In Kotlin, mapper functions are commonly written as [extension functions]({{ "/en/glossary/extension-functions/" | relative_url }}) (e.g., `fun LabelEntity.toDomain(): Label`) so the conversion reads naturally at the call site: `entity.toDomain()`.

Mapper functions are the building blocks of a [data transformation]({{ "/en/glossary/data-transformation/" | relative_url }}) [pipeline]({{ "/en/glossary/pipeline/" | relative_url }}): each function handles one boundary crossing (`Entity → Domain`, `Domain → UiState`), and they compose together through [collection operators]({{ "/en/glossary/collection-operators/" | relative_url }}) like `map`:

```kotlin
// From FollowApp Suite — LabelRepositoryImpl.kt
val options = (optionsByLabelId[labelEntity.id] ?: emptyList()).map { it.toDomain() }
```

## The Senior Nuance

- A Senior keeps mapper functions **pure** — no side effects, no I/O, no [scope function]({{ "/en/01-kotlin-core/scope-functions/" | relative_url }}) chains that hide mutation. A pure mapper is trivially testable: given input X, assert output Y.
- Naming convention matters: `toDomain()`, `toEntity()`, `toUiModel()` communicate direction. Placing them in a dedicated `mapper` package (as in `com.followapp.core.data.mapper`) signals that the file contains only [data transformation]({{ "/en/glossary/data-transformation/" | relative_url }}) logic — no business rules.
- A common mistake is letting mapper functions grow into mini use cases that fetch data, apply business rules, and transform. A Senior enforces the boundary: mapper functions convert shapes, use cases orchestrate behavior.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
