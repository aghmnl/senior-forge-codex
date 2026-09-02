---
layout: post
title: "Operator Overloading"
date: 2026-09-02 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/operator-overloading/
---

## The Theory (The What)

**Operator Overloading** lets you define or redefine operators (`+`, `-`, `[]`, `()`, `in`, `..`, etc.) for your own types by writing a function with the `operator` modifier and a predefined name (`plus`, `minus`, `get`, `invoke`, `contains`, `rangeTo`, etc.). This is one of the building blocks that enables Kotlin [DSLs]({{ "/en/glossary/dsl/" | relative_url }}): [Jetpack Compose]({{ "/en/glossary/jetpack-compose/" | relative_url }})'s `Modifier.then()` chaining, [Gradle Kotlin DSL]({{ "/en/glossary/gradle-kotlin-dsl/" | relative_url }})'s `dependencies {}` block, collection [destructuring]({{ "/en/glossary/destructuring/" | relative_url }}), and even the `by` keyword for delegated properties all rely on operator conventions under the hood.

The most architecturally significant operator in Android is `invoke` — it allows a class instance to be called like a function using `()`.

```kotlin
// From FollowApp Suite — GetPresetsUseCase.kt
class GetPresetsUseCase @Inject constructor(
    private val repository: PresetRepository
) {
    operator fun invoke(): Flow<List<Preset>> = repository.getAll()
}
```

```kotlin
// From FollowApp Suite — DeleteLabelUseCase.kt
class DeleteLabelUseCase @Inject constructor(
    private val labelRepository: LabelRepository
) {
    suspend operator fun invoke(labelId: String) {
        labelRepository.deleteLabel(labelId)
    }
}
```

With `operator fun invoke`, use cases are called as `getPresetsUseCase()` instead of `getPresetsUseCase.execute()` — this is the convention adopted by Google's architecture guidelines for Android.

## The Senior Nuance

- **`invoke` as the Use Case Convention**: The `operator fun invoke` pattern turns a class into a callable object. Every use case in a Clean Architecture Android project follows this convention — the ViewModel holds a reference to the use case and calls it like a function. This keeps the API surface minimal (one public method per class) while still allowing [constructor]({{ "/en/glossary/constructor/" | relative_url }})-injected dependencies.
- **`get` / `set` for indexed access**: `operator fun get(index: Int)` lets your type support bracket syntax (`myCollection[3]`). [Collections]({{ "/en/glossary/collections/" | relative_url }}) like `List` and `Map` use this. It is also used by Compose's `SnapshotStateList`.
- **`contains` for `in` checks**: `operator fun contains(element: T): Boolean` enables `element in myCollection` syntax — more readable than `.contains()` and used by [when expressions]({{ "/en/glossary/when-expression/" | relative_url }}) with ranges.
- **Abuse Warning**: Overloading operators to mean something unexpected (e.g., `+` for database insert) is a serious anti-pattern. The operator's semantics must match the reader's expectations. If it is not immediately obvious what `a + b` means for your type, use a named function instead.
- **DSL Foundation**: [Extension functions]({{ "/en/01-kotlin-core/extension-functions/" | relative_url }}) with `operator` enable natural [DSL]({{ "/en/glossary/dsl/" | relative_url }}) syntax — `rangeTo` powers `1..10`, `compareTo` powers `<`/`>` comparisons, and `provideDelegate` powers `by` delegation. Understanding the operator table is key to reading Kotlin [DSL]({{ "/en/glossary/dsl/" | relative_url }}) internals.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
