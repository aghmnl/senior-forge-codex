---
layout: post
title: "Collections"
date: 2026-08-28 12:00:00 +0000
categories: [en, glossary]
tags: [collections, immutability]
lang: en
permalink: /en/glossary/collections/
---

## The Theory (The What)

**Collections** in Kotlin are containers that hold groups of elements. The standard library provides three main families: [`List`]({{ "/en/glossary/list/" | relative_url }}) (ordered, indexed), [Set]({{ "/en/glossary/sets/" | relative_url }}) (unique elements), and [Map]({{ "/en/glossary/maps/" | relative_url }}) (key-value pairs). Each has a read-only interface ([`List`]({{ "/en/glossary/list/" | relative_url }}), [`Set`]({{ "/en/glossary/sets/" | relative_url }}), [`Map`]({{ "/en/glossary/maps/" | relative_url }})) and a mutable counterpart ([`MutableList`]({{ "/en/glossary/mutable-list/" | relative_url }}), [`MutableSet`]({{ "/en/glossary/mutable-set/" | relative_url }}), [`MutableMap`]({{ "/en/glossary/mutable-map/" | relative_url }})). Kotlin's collection API includes a rich set of functional operations — [`filter`]({{ "/en/glossary/filter/" | relative_url }}), [`map`]({{ "/en/glossary/map-operator/" | relative_url }}), `flatMap`, [`groupBy`]({{ "/en/glossary/group-by/" | relative_url }}), `associate`, `fold`, and many more.

```kotlin
// From FollowApp Suite — LabelRepositoryImpl.kt
val optionsByLabelId = allOptions.groupBy { it.labelId }
labels.associate { labelEntity ->
    val label = labelEntity.toDomain()
    val options = (optionsByLabelId[labelEntity.id] ?: emptyList())
        .map { it.toDomain() }
    label to options
}
```

## The Senior Nuance

- Kotlin's read-only collections are [read-only views]({{ "/en/glossary/read-only-view/" | relative_url }}), not immutable implementations. A [`List`]({{ "/en/glossary/list/" | relative_url }}) returned from a function may be backed by a [`MutableList`]({{ "/en/glossary/mutable-list/" | relative_url }}) — callers cannot [mutate]({{ "/en/glossary/mutation/" | relative_url }}) it through the interface, but the producer can. For true structural [immutability]({{ "/en/glossary/immutability/" | relative_url }}), use a [persistent collection]({{ "/en/glossary/persistent-collections/" | relative_url }}) from `kotlinx.collections.immutable`.
- Collection operations like [`map`]({{ "/en/glossary/map-operator/" | relative_url }}), [`filter`]({{ "/en/glossary/filter/" | relative_url }}), and `flatMap` create intermediate lists. For large datasets, use [`asSequence()`]({{ "/en/glossary/as-sequence/" | relative_url }}) to switch to [Sequences]({{ "/en/glossary/sequences/" | relative_url }}) and lazy evaluation — operations execute one element at a time, avoiding intermediate allocations. But for small collections (< ~1000 elements), the overhead of sequence machinery often exceeds the savings.
- In data class [`equals()`]({{ "/en/glossary/equals/" | relative_url }}) and `hashCode()`, collection properties declared in the [primary constructor]({{ "/en/glossary/primary-constructor/" | relative_url }}) participate in equality. Two data classes with [`List<String>`]({{ "/en/glossary/list/" | relative_url }}) properties are equal if the lists contain the same elements in the same order — but [`Set<String>`]({{ "/en/glossary/sets/" | relative_url }}) compares elements regardless of order.

**Kotlin docs:** [`kotlin.collections`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/) · [Collections overview](https://kotlinlang.org/docs/collections-overview.html)

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
