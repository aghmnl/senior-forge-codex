---
layout: post
title: "Type Safety"
date: 2026-09-02 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/type-safety/
---

## The Theory (The What)

**Type safety** is the degree to which a language prevents operations on values of incompatible types. In Kotlin, the type system enforces safety at [compile time]({{ "/en/glossary/compile-time/" | relative_url }}): you cannot pass a `String` where an `Int` is expected, assign `null` to a non-nullable reference, or call a method that doesn't exist on the declared type — the compiler rejects the code before it runs. This eliminates entire categories of [runtime]({{ "/en/glossary/runtime/" | relative_url }}) errors (like [NullPointerException]({{ "/en/glossary/null-pointer-exception/" | relative_url }}) and [ClassCastException]({{ "/en/glossary/class-cast-exception/" | relative_url }})) that plague weakly-typed or dynamically-typed languages.

```kotlin
// From FollowApp Suite — LabelRepository.kt
interface LabelRepository {
    suspend fun getOrCreateLabel(name: String, type: LabelType): Label
    suspend fun upsertLabelOption(
        labelId: String,
        label: String,
        sortOrder: Int = 0
    ): LabelOption
    suspend fun deleteLabelOption(labelOptionId: String)
}
```

Every parameter, return type, and nullability constraint is enforced by the compiler — callers cannot accidentally pass a `LabelOption` id where a `Label` id is expected if the design uses distinct types.

## The Senior Nuance

- **Kotlin's null safety** is type safety's most visible feature: `String` vs `String?` are distinct types. The [safe call]({{ "/en/glossary/safe-call/" | relative_url }}) operator (`?.`), Elvis (`?:`), and smart [cast]({{ "/en/glossary/cast/" | relative_url }}) remove the need for defensive null checks scattered throughout the code.
- **[Generics]({{ "/en/glossary/generic-type-parameters/" | relative_url }})** extend type safety to containers and abstractions. `Flow<Label>` guarantees the emitted values are `Label` instances — no casting at the collection site. [Reified]({{ "/en/glossary/reified/" | relative_url }}) type parameters preserve this guarantee even at [runtime]({{ "/en/glossary/runtime/" | relative_url }}), bypassing [type erasure]({{ "/en/glossary/type-erasure/" | relative_url }}).
- **[Sealed hierarchies]({{ "/en/glossary/sealed-hierarchy/" | relative_url }})** provide [exhaustiveness]({{ "/en/glossary/exhaustiveness/" | relative_url }}) checking: a `when` expression over a sealed class forces the developer to handle every subtype, making it impossible to forget a case — a type-safe alternative to string/int constants.
- **[Callbacks]({{ "/en/glossary/callbacks/" | relative_url }})** in Kotlin are type-safe because they are expressed as function types (`(String) -> Unit`) rather than raw `Object` references. The compiler verifies that the [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) you pass matches the expected signature.
- Senior engineers leverage type safety to **make illegal states unrepresentable**: value classes, sealed types, and non-nullable parameters encode business rules in the type system so the compiler enforces them, reducing reliance on runtime validation.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
