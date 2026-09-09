---
layout: post
title: "map (Operator)"
date: 2026-09-08 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/map-operator/
---

## The Theory (The What)

**`map { }`** applies a transform to every element and returns a new [`List`]({{ "/en/glossary/list/" | relative_url }}) of the results. It is the canonical [collection operator]({{ "/en/glossary/collection-operators/" | relative_url }}) and the core of every [mapper function]({{ "/en/glossary/mapper-function/" | relative_url }}) — not to be confused with [`Map`]({{ "/en/glossary/maps/" | relative_url }}), the key-value structure.

```kotlin
// From FollowApp Suite — TasksScreen.kt
onDragEnd = { onReorderComplete(localTasks.map { it.id }) }

// From FollowApp Suite — LabelRepositoryImpl.kt
val options = (optionsByLabelId[labelEntity.id] ?: emptyList()).map { it.toDomain() }
```

## The Senior Nuance

- `map` is eager and always allocates a full result list. A four-step chain over ten thousand items allocates forty thousand entries and hands the [Garbage Collector]({{ "/en/glossary/garbage-collector/" | relative_url }}) work; [`asSequence`]({{ "/en/glossary/as-sequence/" | relative_url }}) removes the intermediates when the chain is long enough to matter.
- Variants exist for exactly the cases where the naive chain wastes a pass: `mapNotNull` fuses map + filter, `mapTo(target)` collects straight into a [`MutableSet`]({{ "/en/glossary/mutable-set/" | relative_url }}) or list, `flatMap` flattens, `mapValues` transforms a [`Map`]({{ "/en/glossary/maps/" | relative_url }})'s values while keeping keys.
- It is also the boundary tool between layers: mapping entities to domain models is what stops the [data layer]({{ "/en/glossary/data-layer/" | relative_url }}) leaking into the UI, and the [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) is [inlined]({{ "/en/glossary/inline-functions/" | relative_url }}) so the abstraction costs nothing.

**Kotlin docs:** [`kotlin.collections.map`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/map.html)

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
