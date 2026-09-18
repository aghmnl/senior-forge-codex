---
layout: post
title: "is Operator"
date: 2026-09-18 12:00:00 +0000
categories: [en, glossary]
tags: [type-system, syntax, sealed-types]
lang: en
permalink: /en/glossary/is-operator/
---

## The Theory (The What)

**`is`** is Kotlin's type-check operator: `x is Foo` returns `true` when `x` is an instance of `Foo` (or a subtype), and `!is` negates it. It replaces Java's `instanceof`, with one decisive difference: after a positive check, the compiler applies a [Smart Casts]({{ "/en/01-kotlin-core/smart-casts/" | relative_url }}) smart cast, so `x` can be used as a `Foo` inside the branch with no explicit [cast]({{ "/en/glossary/cast/" | relative_url }}). In a [`when` expression]({{ "/en/glossary/when-expression/" | relative_url }}) over a [sealed hierarchy]({{ "/en/glossary/sealed-hierarchy/" | relative_url }}), `is` branches double as [exhaustiveness]({{ "/en/glossary/exhaustiveness/" | relative_url }}) checks.

```kotlin
// From FollowApp Suite — CleanUpPresetsUseCase.kt
// After the check, `filter` is a ScaleFilterState.Include: `filter.values` needs no cast
if (filter is ScaleFilterState.Include && oldValue in filter.values) {
    val updatedValues = filter.values - oldValue + newValue
}
```

## The Senior Nuance

- **The check is only half the feature.** `is` without the smart cast that follows it is just `instanceof`; the value is in what the compiler lets you do next. That only works when the checked value is stable — a local or a [`val`]({{ "/en/glossary/val/" | relative_url }}) without a custom [getter]({{ "/en/glossary/getter/" | relative_url }}). On a [`var`]({{ "/en/glossary/var/" | relative_url }}) property the check compiles but the smart cast does not.
- **`is` in `when` is exhaustive over sealed types.** Adding a subtype breaks every `when` that does not cover it, which is why `is` branches are the backbone of type-safe UI state handling.
- **Prefer `is` over `as?` when you already branch.** `if (x is Foo)` gives you a non-null `Foo` in the branch; `(x as? Foo)?.bar` gives you a nullable. Use `is` for control flow, [`as?`]({{ "/en/glossary/as-safe-cast/" | relative_url }}) for expressions.
- See [Smart Casts]({{ "/en/01-kotlin-core/smart-casts/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
