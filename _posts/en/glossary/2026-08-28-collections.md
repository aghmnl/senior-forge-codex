---
layout: post
title: "Collections"
date: 2026-08-28 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/collections/
---

## The Theory (The What)

**Collections** in Kotlin are containers that hold groups of elements. The standard library provides three main families: `List` (ordered, indexed), [Set]({{ "/en/glossary/sets/" | relative_url }}) (unique elements), and [Map]({{ "/en/glossary/maps/" | relative_url }}) (key-value pairs). Each has a read-only interface (`List`, `Set`, `Map`) and a mutable counterpart (`MutableList`, `MutableSet`, `MutableMap`). Kotlin's collection API includes a rich set of functional operations — `filter`, `map`, `flatMap`, `groupBy`, `associate`, `fold`, and many more.

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

- Kotlin's read-only collections are interfaces, not immutable implementations. A `List` returned from a function may be backed by a `MutableList` — callers cannot [mutate]({{ "/en/glossary/mutation/" | relative_url }}) it through the interface, but the producer can. For true structural immutability, use `kotlinx.collections.immutable`.
- Collection operations like `map`, `filter`, and `flatMap` create intermediate lists. For large datasets, use `asSequence()` to switch to lazy evaluation — operations execute one element at a time, avoiding intermediate allocations. But for small collections (< ~1000 elements), the overhead of sequence machinery often exceeds the savings.
- In data class `equals()` and `hashCode()`, collection properties declared in the [primary constructor]({{ "/en/glossary/primary-constructor/" | relative_url }}) participate in equality. Two data classes with `List<String>` properties are equal if the lists contain the same elements in the same order — but `Set<String>` compares elements regardless of order.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
