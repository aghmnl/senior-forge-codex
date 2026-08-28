---
layout: page
title: "Data Classes: copy, equals, toString"
lang: en
permalink: /en/01-kotlin-core/data-classes/
order: 3
---

## The Theory (The What)

A `data class` in Kotlin is a class whose primary purpose is to hold data. The compiler automatically generates `equals()`, `hashCode()`, `toString()`, `copy()`, and `componentN()` functions based on the properties declared in the primary constructor. This eliminates the boilerplate that Java developers traditionally write (or generate with IDE tools) for value-holding objects.

## The Senior Perspective (The Why)

A Senior Engineer sees `data class` not just as syntactic sugar, but as a contract and a design decision with real implications.

- **Structural Equality by Default**: `equals()` and `hashCode()` are generated from primary constructor properties only. Properties declared in the body are excluded — a subtle but critical detail when using data classes as keys in maps or elements in sets.
- **Immutable Modeling with `copy()`**: The `copy()` function enables creating modified copies without mutating the original, which is foundational for unidirectional data flow architectures (MVI, Redux). Combined with `val` properties, it makes state transitions explicit and safe.
- **Destructuring for Readability**: The generated `componentN()` functions enable destructuring declarations (`val (name, age) = user`), which improve readability in lambdas, loop assignments, and multi-return patterns.
- **Pitfall — Inheritance**: Data classes cannot be `open` (since Kotlin 1.1+), which means they cannot serve as base classes. This is intentional: the compiler-generated methods depend on the primary constructor, and inheritance would break the contract.

## Code in Action

```kotlin
// From FollowApp Suite — RecurrenceRule.kt
// A non-trivial data class with defaults, a sealed end-condition,
// and an optional pattern — all in the primary constructor
data class RecurrenceRule(
    val frequency: RecurrenceFrequency,
    val interval: Int = 1,
    val weekdays: Set<DayOfWeek> = emptySet(),
    val end: RecurrenceEnd = RecurrenceEnd.Never,
    val pattern: RecurrencePattern? = null
)

// From FollowApp Suite — CleanUpPresetsUseCase.kt
// copy() for immutable state updates: only the affected fields change
fun onLabelRenamed(preset: Preset, oldName: String, newName: String) {
    val newLabelFilters = if (oldName in preset.labelFilters) {
        preset.labelFilters - oldName + (newName to preset.labelFilters.getValue(oldName))
    } else preset.labelFilters

    presetRepository.save(
        preset.copy(
            labelFilters = newLabelFilters,
            scaleFilters = newScaleFilters,
            groupBy = newGroupBy
        )
    )
}

// From FollowApp Suite — MyTasksApplication.kt
// Destructuring a Triple (itself a data class) to extract three settings
val (language, themeMode, contrastLevel) = runBlocking {
    Triple(
        languagePreferences.getLanguage().first(),
        themePreferences.getThemeMode().first(),
        themePreferences.getContrastLevel().first()
    )
}
```

## The Interview (The Hot Seat)

**Question**: A developer adds a `timestamp` property to the body of a `data class` and notices that two objects with different timestamps are considered equal. Why?

**Senior Answer**: Properties declared in the class body — outside the primary constructor — are not included in the compiler-generated `equals()`, `hashCode()`, `toString()`, or `copy()` functions. Only primary constructor parameters participate in these generated methods. If `timestamp` needs to affect equality, it must be moved into the primary constructor. This is a deliberate design choice: Kotlin assumes that the primary constructor defines the "identity" of a data class instance.

---

[Back to Chapters]({{ "/" | relative_url }})
