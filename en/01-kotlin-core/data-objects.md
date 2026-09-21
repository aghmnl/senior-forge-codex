---
layout: page
title: "Data Objects: Singleton & Memory Efficiency"
lang: en
permalink: /en/01-kotlin-core/data-objects/
order: 4
---

## The Theory (The What)

A [`data object`]({{ "/en/glossary/data-object/" | relative_url }}) (introduced in Kotlin 1.9) combines the [singleton]({{ "/en/glossary/singleton/" | relative_url }}) guarantee of [`object`]({{ "/en/glossary/object/" | relative_url }}) with the compiler-generated [`toString()`]({{ "/en/glossary/to-string/" | relative_url }}), [`equals()`]({{ "/en/glossary/equals/" | relative_url }}), and [`hashCode()`]({{ "/en/glossary/hash-code/" | relative_url }}) methods of a [`data class`]({{ "/en/01-kotlin-core/data-classes/" | relative_url }}). Unlike a plain [`object`]({{ "/en/glossary/object/" | relative_url }}), which produces a default [`toString()`]({{ "/en/glossary/to-string/" | relative_url }}) like `Loading@3a71f4dd`, a [`data object`]({{ "/en/glossary/data-object/" | relative_url }}) generates a clean, readable [`toString()`]({{ "/en/glossary/to-string/" | relative_url }}) using the class name — e.g., `Loading`. No [`copy()`]({{ "/en/glossary/copy/" | relative_url }}) or [`componentN()`]({{ "/en/glossary/component-n/" | relative_url }}) functions are generated, as [singletons]({{ "/en/glossary/singleton/" | relative_url }}) have no constructor properties to copy or [destructure]({{ "/en/glossary/destructuring/" | relative_url }}).

## The Senior Perspective (The Why)

For a Senior Engineer, [`data object`]({{ "/en/glossary/data-object/" | relative_url }}) solves a specific pain point in [sealed hierarchies]({{ "/en/glossary/sealed-hierarchy/" | relative_url }}) and state modeling.

- **Clean Logging and Debugging**: In [sealed hierarchy]({{ "/en/glossary/sealed-hierarchy/" | relative_url }}) classes, stateless members like `Loading` or [`Idle`]({{ "/en/glossary/idle-state/" | relative_url }}) declared as plain [`object`]({{ "/en/glossary/object/" | relative_url }}) produce unhelpful toString output (`Loading@3a71f4dd`). A [`data object`]({{ "/en/glossary/data-object/" | relative_url }}) guarantees a human-readable representation without manual overrides.
- **[Singleton]({{ "/en/glossary/singleton/" | relative_url }}) Guarantee**: Unlike [`data class`]({{ "/en/01-kotlin-core/data-classes/" | relative_url }}), a [`data object`]({{ "/en/glossary/data-object/" | relative_url }}) is a true [singleton]({{ "/en/glossary/singleton/" | relative_url }}) — there is exactly one instance. This means no unnecessary [allocations]({{ "/en/glossary/allocations/" | relative_url }}) for states that carry no data, which matters in high-frequency [state emission patterns]({{ "/en/glossary/state-emission-patterns/" | relative_url }}) (e.g., [StateFlow]({{ "/en/glossary/stateflow/" | relative_url }}) updates).
- **Consistent Equality**: [`equals()`]({{ "/en/glossary/equals/" | relative_url }}) always returns `true` when comparing a [`data object`]({{ "/en/glossary/data-object/" | relative_url }}) to itself (referential and structural equality are identical for [singletons]({{ "/en/glossary/singleton/" | relative_url }})). This prevents subtle bugs when mixing [`==`]({{ "/en/glossary/structural-equality/" | relative_url }}) and [`===`]({{ "/en/glossary/referential-equality/" | relative_url }}) checks in [`when`]({{ "/en/glossary/when-expression/" | relative_url }}) expressions or [collection]({{ "/en/glossary/collections/" | relative_url }}) operations.
- **[Sealed Hierarchy]({{ "/en/glossary/sealed-hierarchy/" | relative_url }}) Best Practice**: The modern convention is to use [`data object`]({{ "/en/glossary/data-object/" | relative_url }}) for stateless members and [`data class`]({{ "/en/01-kotlin-core/data-classes/" | relative_url }}) for stateful members of a [sealed hierarchy]({{ "/en/glossary/sealed-hierarchy/" | relative_url }}).

## Code in Action

```kotlin
// From FollowApp Suite — RecurrenceRule.kt
// Mixed sealed hierarchy: data object for stateless leaves,
// data class for leaves that carry data
sealed class RecurrenceEnd {
    data object Never : RecurrenceEnd()
    data class AfterOccurrences(val remaining: Int) : RecurrenceEnd()
    data class UntilDate(val date: Long) : RecurrenceEnd()
}

// From FollowApp Suite — ArchiveUiState.kt
// data object (Kotlin 1.9+): clean toString, consistent equals
sealed class ArchiveBulkAction {
    data object Unarchive : ArchiveBulkAction()
    data object Delete : ArchiveBulkAction()
}

// From FollowApp Suite — BulkSelection.kt
// Contrast: plain object (pre-1.9) — same pattern, but toString
// produces "Archive@3a71f4dd" instead of "Archive"
sealed class BulkAction {
    data class Complete(val isCompleted: Boolean) : BulkAction()
    object Archive : BulkAction()   // pre-1.9: no clean toString
    object Delete : BulkAction()
}

// From FollowApp Suite — FilterState.kt
// Sealed ADT with object singletons for stateless variants
sealed class ScaleFilterState {
    object Off : ScaleFilterState()
    data class Include(val values: Set<String>) : ScaleFilterState()
    object Exclude : ScaleFilterState()
}

fun main() {
    // data object: readable logging
    println(RecurrenceEnd.Never)           // "Never"
    println(ArchiveBulkAction.Unarchive)   // "Unarchive"

    // plain object: unhelpful logging
    println(BulkAction.Archive)            // "Archive@3a71f4dd"
    println(ScaleFilterState.Off)          // "Off@7c53a9eb"
}
```

## The Interview (The Hot Seat)

**Question**: Why should you prefer [`data object`]({{ "/en/glossary/data-object/" | relative_url }}) over plain [`object`]({{ "/en/glossary/object/" | relative_url }}) for stateless members of a sealed hierarchy?

**Senior Answer**: A plain [`object`]({{ "/en/glossary/object/" | relative_url }}) generates a default [`toString()`]({{ "/en/glossary/to-string/" | relative_url }}) that includes the memory address (e.g., `Loading@3a71f4dd`), which is unhelpful for logging and debugging. A [`data object`]({{ "/en/glossary/data-object/" | relative_url }}) generates a clean [`toString()`]({{ "/en/glossary/to-string/" | relative_url }}) using just the class name, plus consistent [`equals()`]({{ "/en/glossary/equals/" | relative_url }}) and [`hashCode()`]({{ "/en/glossary/hash-code/" | relative_url }}) implementations. Since stateless members of a [sealed hierarchy]({{ "/en/glossary/sealed-hierarchy/" | relative_url }}) are frequently logged, compared, and emitted through [StateFlow]({{ "/en/glossary/stateflow/" | relative_url }}), the [`data object`]({{ "/en/glossary/data-object/" | relative_url }}) provides correct, readable behavior out of the box without manual overrides.

---

[Back to Chapters]({{ "/" | relative_url }})
