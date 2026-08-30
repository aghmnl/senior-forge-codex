---
layout: page
title: "Sealed Classes vs Sealed Interfaces"
lang: en
permalink: /en/01-kotlin-core/sealed-classes-interfaces/
order: 5
---

## The Theory (The What)

Both `sealed class` and `sealed interface` restrict which types can extend them — all direct subtypes must be declared in the same package and module. This gives the compiler a closed set, enabling exhaustive [`when` expressions]({{ "/en/glossary/when-expression/" | relative_url }}) without a default `else` branch. The difference lies in what they share:

- **`sealed class`** — choose it when subtypes share state or behavior. You can declare properties in the [constructor]({{ "/en/glossary/constructor/" | relative_url }}), define common methods, and use an `init` block. Subtypes inherit that shared structure. The tradeoff: a class can only extend **one** sealed class (single [inheritance]({{ "/en/glossary/inheritance/" | relative_url }})).
- **`sealed interface`** (Kotlin 1.5+) — choose it when you only need to restrict the type hierarchy but each implementation is independent. There is no shared state, no [constructor]({{ "/en/glossary/constructor/" | relative_url }}), no `init` block — no [protected state]({{ "/en/glossary/protected-state/" | relative_url }}). The advantage: a class can implement **multiple** sealed interfaces simultaneously — something sealed classes cannot do.

The rule of thumb: prefer `sealed interface` by default; reach for `sealed class` only when the hierarchy genuinely needs shared state or a common base implementation.

## The Senior Perspective (The Why)

- **Compile-time Safety**: By avoiding the `else` block in [`when`]({{ "/en/glossary/when-expression/" | relative_url }}) statements, the compiler flags every unhandled case when a new subtype is added. This turns a runtime crash into a [compile-time]({{ "/en/glossary/compile-time/" | relative_url }}) error — the compiler is your state machine verifier. This is what makes sealed hierarchies the Kotlin embodiment of [algebraic data types (ADTs)]({{ "/en/glossary/algebraic-data-types/" | relative_url }}).
- **Memory Efficiency**: Using [`data object`]({{ "/en/01-kotlin-core/data-objects/" | relative_url }}) for stateless members (like `Loading` or `Idle`) avoids redundant object [allocations]({{ "/en/glossary/allocations/" | relative_url }}), while gaining built-in `equals` and `toString` support. A `data object` is a [singleton]({{ "/en/glossary/singleton/" | relative_url }}) — emitting it through [StateFlow]({{ "/en/glossary/stateflow/" | relative_url }}) thousands of times creates zero new objects.
- **Shared Behavior via sealed class**: When every subtype must carry the same properties (e.g., `taskId` and `childCount` in a cascade action), a sealed class avoids repeating those declarations in every variant. The `abstract` properties live in the base class, and each subtype provides them through its [primary constructor]({{ "/en/glossary/primary-constructor/" | relative_url }}).
- **Multiple Hierarchy Membership via sealed interface**: A sealed interface allows a single class to belong to multiple restricted hierarchies simultaneously. This is impossible with sealed classes due to the JVM's single-inheritance constraint, making sealed interfaces the better default for architecture-level modeling (UI state, navigation events, domain actions).
- **Architectural Foundation**: Sealed hierarchies are the building blocks for [MVI]({{ "/en/glossary/mvi-pattern/" | relative_url }}) and [unidirectional data flow]({{ "/en/glossary/unidirectional-data-flow/" | relative_url }}), ensuring the UI reacts to a single source of truth via [state emission patterns]({{ "/en/glossary/state-emission-patterns/" | relative_url }}).

## Code in Action

```kotlin
// From FollowApp Suite — CascadeAction in TasksUiState.kt
// sealed CLASS: subtypes share common state (taskId, childCount)
// that lives in abstract properties — no repetition needed
sealed class CascadeAction {
    abstract val taskId: String
    abstract val childCount: Int

    data class Complete(
        override val taskId: String,
        val isCompleted: Boolean,
        override val childCount: Int
    ) : CascadeAction()

    data class Archive(
        override val taskId: String,
        override val childCount: Int
    ) : CascadeAction()

    data class Delete(
        override val taskId: String,
        override val childCount: Int
    ) : CascadeAction()
}

// From FollowApp Suite — RecurrenceRule.kt
// sealed CLASS: the companion object provides shared constants,
// and each variant carries its own data shape
sealed class RecurrencePattern {
    data class DayOfMonth(val day: Int) : RecurrencePattern()
    data class MonthDay(val month: Int, val day: Int) : RecurrencePattern()
    data class NthWeekday(val ordinal: Int, val day: DayOfWeek) : RecurrencePattern()
    data class NthBusinessDay(val ordinal: Int) : RecurrencePattern()

    companion object {
        const val LAST = -1
    }
}

// From FollowApp Suite — StateChip.kt
// sealed INTERFACE: no shared state — each implementation defines
// its own colors, borders, and behavior independently.
// A class could implement ChipState AND another sealed interface
sealed interface ChipState {
    val foreground: Color @Composable get
    val border: BorderStroke? @Composable get
    val strikethrough: Boolean get() = false
    @Composable fun inputColors(): SelectableChipColors
    @Composable fun filterColors(): SelectableChipColors
}

// From FollowApp Suite — TrashUiState.kt
// sealed CLASS with pure data objects: all variants are stateless
// singletons — a sealed interface would work equally well here,
// but the existing pattern uses sealed class
sealed class TrashBulkAction {
    data object Restore : TrashBulkAction()
    data object PermanentDelete : TrashBulkAction()
    data object Archive : TrashBulkAction()
}
```

## The Interview (The Hot Seat)

**Question**: When would you choose a `sealed class` over a `sealed interface`, and vice versa?

**Senior Answer**: I choose `sealed class` when subtypes share common state or behavior — properties in the [constructor]({{ "/en/glossary/constructor/" | relative_url }}), shared methods, or an `init` block. For example, if every variant of a cascade action needs a `taskId` and `childCount`, a sealed class with `abstract val` properties avoids repeating those fields in every subtype. I choose `sealed interface` — which is my default — when the hierarchy only needs to restrict who can implement it, without sharing state. The key advantage is that a class can implement multiple sealed interfaces but can only inherit from one sealed class. In practice, most UI state hierarchies and domain action types work best as sealed interfaces because each variant is structurally independent, and the flexibility of multiple interface implementation matters for cross-cutting concerns like logging or analytics contracts.

---

[Back to Chapters]({{ "/" | relative_url }})
