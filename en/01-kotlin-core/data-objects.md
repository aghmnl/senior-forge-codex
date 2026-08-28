---
layout: page
title: "Data Objects: Singleton & Memory Efficiency"
lang: en
permalink: /en/01-kotlin-core/data-objects/
order: 4
---

## The Theory (The What)

A `data object` (introduced in Kotlin 1.9) combines the singleton guarantee of `object` with the compiler-generated `toString()`, `equals()`, and `hashCode()` methods of a `data class`. Unlike a plain `object`, which produces a default `toString()` like `Loading@3a71f4dd`, a `data object` generates a clean, readable `toString()` using the class name — e.g., `Loading`. No `copy()` or `componentN()` functions are generated, as singletons have no constructor properties to copy or destructure.

## The Senior Perspective (The Why)

For a Senior Engineer, `data object` solves a specific pain point in sealed hierarchies and state modeling.

- **Clean Logging and Debugging**: In sealed class hierarchies, stateless members like `Loading` or `Idle` declared as plain `object` produce unhelpful toString output (`Loading@3a71f4dd`). A `data object` guarantees a human-readable representation without manual overrides.
- **Singleton Guarantee**: Unlike `data class`, a `data object` is a true singleton — there is exactly one instance. This means no unnecessary allocations for states that carry no data, which matters in high-frequency state emission patterns (e.g., StateFlow updates).
- **Consistent Equality**: `equals()` always returns `true` when comparing a `data object` to itself (referential and structural equality are identical for singletons). This prevents subtle bugs when mixing `==` and `===` checks in `when` expressions or collection operations.
- **Sealed Hierarchy Best Practice**: The modern convention is to use `data object` for stateless members and `data class` for stateful members of a sealed hierarchy.

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

**Question**: Why should you prefer `data object` over plain `object` for stateless members of a sealed hierarchy?

**Senior Answer**: A plain `object` generates a default `toString()` that includes the memory address (e.g., `Loading@3a71f4dd`), which is unhelpful for logging and debugging. A `data object` generates a clean `toString()` using just the class name, plus consistent `equals()` and `hashCode()` implementations. Since stateless members of a sealed hierarchy are frequently logged, compared, and emitted through Flows, the `data object` provides correct, readable behavior out of the box without manual overrides.

---

[Back to Chapters]({{ "/" | relative_url }})
