---
layout: post
title: "Sealed Hierarchy"
date: 2026-08-28 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/sealed-hierarchy/
---

## The Theory (The What)

A **sealed hierarchy** (sealed class or sealed interface) restricts which classes can extend it — all direct subclasses must be defined in the same package and module. This gives the compiler a closed set of subtypes, enabling exhaustive `when` expressions without a default branch. Sealed hierarchies are Kotlin's primary tool for modeling [algebraic data types (ADTs)]({{ "/en/glossary/algebraic-data-types/" | relative_url }}): a finite set of variants where each variant may carry different data.

```kotlin
// From FollowApp Suite — LabelValue.kt
sealed class LabelValue {
    data class Tag(val values: List<String>) : LabelValue()
    data class Scale(val value: String) : LabelValue()
}
```

## The Senior Nuance

- The exhaustive `when` is the key benefit: if you add a new subtype to a sealed hierarchy, the compiler flags every `when` that does not handle it. This turns a runtime crash (forgetting a case) into a compile-time error — the compiler is your state machine verifier.
- The modern convention for sealed hierarchy members: use `data object` for stateless leaves ([singletons]({{ "/en/glossary/singleton/" | relative_url }}) that carry no data) and `data class` for stateful leaves (variants with properties in the [primary constructor]({{ "/en/glossary/primary-constructor/" | relative_url }})). This ensures clean `toString()`, consistent `equals()`, and zero unnecessary [allocations]({{ "/en/glossary/allocations/" | relative_url }}).
- `sealed interface` (Kotlin 1.5+) is preferred over `sealed class` when the hierarchy does not need shared state or an `init` block. A sealed interface allows a subclass to implement multiple sealed interfaces — something sealed classes cannot do due to single [inheritance]({{ "/en/glossary/inheritance/" | relative_url }}).
- [State transitions]({{ "/en/glossary/state-transitions/" | relative_url }}) in [unidirectional data flow]({{ "/en/glossary/unidirectional-data-flow/" | relative_url }}) architectures are naturally modeled as sealed hierarchies: `Loading`, `Success(data)`, `Error(exception)`.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
