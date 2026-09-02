---
layout: post
title: "Exhaustiveness"
date: 2026-09-02 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/exhaustiveness/
---

## The Theory (The What)

**Exhaustiveness** is the compiler's guarantee that a `when` expression covers every possible case of a type hierarchy. When the subject of a `when` is a [sealed class]({{ "/en/01-kotlin-core/sealed-classes-interfaces/" | relative_url }}) or [sealed interface]({{ "/en/01-kotlin-core/sealed-classes-interfaces/" | relative_url }}), the compiler knows the complete set of subtypes and enforces that each one is handled — no `else` branch needed. If a new subtype is added later, every exhaustive `when` that misses it becomes a [compile time]({{ "/en/glossary/compile-time/" | relative_url }}) error, forcing the developer to handle the new case explicitly.

```kotlin
// From FollowApp Suite — TaskConfirmationDialogs.kt
val (titleRes, messageRes) = when (action) {
    is BulkAction.Complete -> R.string.bulk_complete_title to R.string.bulk_complete_message
    is BulkAction.Archive  -> R.string.bulk_archive_title to R.string.bulk_archive_message
    is BulkAction.Delete   -> R.string.bulk_delete_title to R.string.bulk_delete_message
}
```

No `else` branch — the compiler verifies that `Complete`, `Archive`, and `Delete` cover every `BulkAction` subtype. Adding a fourth subtype would immediately break this `when`, surfacing the omission at build time rather than as a [Runtime]({{ "/en/glossary/runtime/" | relative_url }}) crash.

## The Senior Nuance

- Exhaustiveness is the main reason [sealed classes]({{ "/en/01-kotlin-core/sealed-classes-interfaces/" | relative_url }}) exist. The [final]({{ "/en/glossary/final/" | relative_url }})-by-default design of Kotlin restricts inheritance; sealed hierarchies extend that restriction to a known set of subtypes, enabling the compiler to reason about completeness.
- **Never add a default `else` branch** to a `when` on a sealed type. An `else` silences the compiler: new subtypes get silently routed to the default path instead of triggering a compilation error. This is the single most common mistake — it turns a [compile time]({{ "/en/glossary/compile-time/" | relative_url }}) safety net into a [Runtime]({{ "/en/glossary/runtime/" | relative_url }}) bug.
- In FAS, the same pattern repeats for `CascadeAction`:

```kotlin
// From FollowApp Suite — TaskConfirmationDialogs.kt
val (titleRes, messageRes) = when (action) {
    is CascadeAction.Complete ->
        if (action.isCompleted) R.string.cascade_complete_title to R.string.cascade_complete_message
        else R.string.cascade_uncomplete_title to R.string.cascade_uncomplete_message
    is CascadeAction.Archive -> R.string.cascade_archive_title to R.string.cascade_archive_message
    is CascadeAction.Delete  -> R.string.cascade_delete_title to R.string.cascade_delete_message
}
```

- Exhaustiveness also applies to [enum classes]({{ "/en/glossary/enum/" | relative_url }}) and, since Kotlin 1.7, to sealed interfaces — enabling [polymorphism]({{ "/en/glossary/polymorphism/" | relative_url }}) patterns where the type hierarchy spans multiple inheritance trees but the compiler still guarantees completeness.
- In MVI/UDF architectures (common in Android), sealed classes model screen states (`Loading`, `Content`, `Error`) and the `when` in the UI layer is exhaustive — guaranteeing every state has a corresponding rendering. This is a key pattern in [Jetpack Compose]({{ "/en/glossary/jetpack-compose/" | relative_url }}) UI code.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
