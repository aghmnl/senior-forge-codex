---
layout: page
title: Smart Casts
lang: en
permalink: /en/01-kotlin-core/smart-casts/
order: 2
---

## The Theory (The What)

Smart Casting is the Kotlin compiler's ability to automatically cast a variable to a more specific type after a type check (`is`), a null check (`!= null`), or other control-flow conditions that guarantee the type. Unlike Java, where explicit casts are required after `instanceof`, Kotlin tracks the type information through the control flow graph and makes the narrowed type available without any manual cast.

## The Senior Perspective (The Why)

A Senior Engineer leverages smart casts not only for cleaner code, but understands the boundaries where they apply and where they don't.

- **Sealed Hierarchy Navigation**: Smart casts shine in `when` expressions over [sealed classes]({{ "/en/01-kotlin-core/sealed-classes-interfaces/" | relative_url }}). After matching `is UIState.Success`, the compiler knows the variable is `Success` and grants direct access to its properties — no explicit cast needed. This is the foundation of type-safe state handling in MVI.
- **Mutability Limitation**: Smart casts only work on `val` (immutable) local variables and properties. A `var` or a property with a custom getter can change between the check and the usage, so the compiler refuses to smart cast. This is a deliberate safety guarantee, not a limitation.
- **Contract Functions**: Kotlin's `contract` mechanism (used by `require`, `check`, `checkNotNull`) informs the compiler about type guarantees, enabling smart casts after validation calls. The stdlib's `requireNotNull(value)` makes `value` smart-cast to non-null in subsequent code.
- **Explicit Cast Fallback**: When smart cast is unavailable (mutable properties, cross-module boundaries), use the safe cast `as?` which returns null on failure, never throws. Reserve the unsafe `as` for situations where failure is genuinely impossible.

## Code in Action

```kotlin
// From FollowApp Suite — FilterState.kt
// The sealed hierarchy that enables the smart casts below
sealed class ScaleFilterState {
    object Off : ScaleFilterState()
    data class Include(val values: Set<String>) : ScaleFilterState()
    object Exclude : ScaleFilterState()
}

// From FollowApp Suite — PresetMapper.kt
// when + is: the compiler smart-casts `state` to Include,
// granting direct access to `state.values`
fun serializeScaleFilters(filters: Map<String, ScaleFilterState>): String {
    val json = JSONObject()
    filters.forEach { (key, state) ->
        when (state) {
            is ScaleFilterState.Off -> json.put(key, JSONObject().put("type", "OFF"))
            is ScaleFilterState.Include -> {
                val arr = JSONArray(state.values.toList())  // smart cast
                json.put(key, JSONObject().put("type", "INCLUDE").put("values", arr))
            }
            is ScaleFilterState.Exclude -> json.put(key, JSONObject().put("type", "EXCLUDE"))
        }
    }
    return json.toString()
}

// From FollowApp Suite — CleanUpPresetsUseCase.kt
// is inside if: after the check, filter.values is accessible
if (filter is ScaleFilterState.Include && oldValue in filter.values) {
    val updatedValues = filter.values - oldValue + newValue
}

// From FollowApp Suite — TasksViewModel.kt
// as? safe cast: returns null if the LabelValue is Scale (not Tag)
val taskLabels = (task.customLabels["labels"] as? LabelValue.Tag)
    ?.values?.toSet() ?: emptySet()

// From FollowApp Suite — RecurrenceCalculator.kt
// as? + null-check smart cast: until becomes Long (non-null) after the check
val until = (rule.end as? RecurrenceEnd.UntilDate)?.date
return if (until != null && candidate > until) null else candidate
```

## The Interview (The Hot Seat)

**Question**: Why does the Kotlin compiler refuse to smart cast a `var` property after an `is` check?

**Senior Answer**: Between the `is` check and the subsequent usage, another thread — or even the same thread via a callback — could reassign the `var` to a different type. The compiler cannot guarantee that the checked type still holds at the point of use, so it refuses the smart cast to prevent a `ClassCastException` at runtime. This is the same principle behind Kotlin's [null safety]({{ "/en/01-kotlin-core/null-safety-elvis-safe-calls/" | relative_url }}) design: the type system only makes promises it can enforce. The workaround is to capture the value in a local `val` first, then the smart cast applies to the immutable local.

---

[Back to Chapters]({{ "/" | relative_url }})
