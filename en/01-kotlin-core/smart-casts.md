---
layout: page
title: Smart Casts
lang: en
permalink: /en/01-kotlin-core/smart-casts/
order: 2
---

## The Theory (The What)

Smart Casting is the Kotlin compiler's ability to automatically cast a variable to a more specific type after a type check ([`is`]({{ "/en/glossary/is-operator/" | relative_url }})), a null check (`!= null`), or other control-flow conditions that guarantee the type. Unlike Java, where explicit [casts]({{ "/en/glossary/cast/" | relative_url }}) are required after `instanceof`, Kotlin tracks the type information through the control flow graph and makes the narrowed type available without any manual [cast]({{ "/en/glossary/cast/" | relative_url }}).

## The Senior Perspective (The Why)

A Senior Engineer leverages smart casts not only for cleaner code, but understands the boundaries where they apply and where they don't.

- **[Sealed Hierarchy]({{ "/en/glossary/sealed-hierarchy/" | relative_url }}) Navigation**: Smart casts shine in [`when` expressions]({{ "/en/glossary/when-expression/" | relative_url }}) over [sealed classes]({{ "/en/01-kotlin-core/sealed-classes-interfaces/" | relative_url }}). After matching [`is UIState.Success`]({{ "/en/glossary/is-operator/" | relative_url }}), the compiler knows the variable is [`Success`]({{ "/en/glossary/success-state/" | relative_url }}) and grants direct access to its properties — no explicit [cast]({{ "/en/glossary/cast/" | relative_url }}) needed. This is the foundation of [type-safe]({{ "/en/glossary/type-safety/" | relative_url }}) state handling in [MVI]({{ "/en/glossary/mvi-pattern/" | relative_url }}).
- **Mutability Limitation**: Smart casts only work on [`val`]({{ "/en/glossary/val/" | relative_url }}) (immutable) local variables and properties. A [`var`]({{ "/en/glossary/var/" | relative_url }}) or a property with a custom [getter]({{ "/en/glossary/getter/" | relative_url }}) can change between the check and the usage, so the compiler refuses to smart cast. This is a deliberate safety guarantee, not a limitation.
- **Contract Functions**: Kotlin's [`contract`]({{ "/en/glossary/contract/" | relative_url }}) mechanism (used by [`require`]({{ "/en/glossary/require/" | relative_url }}), [`check`]({{ "/en/glossary/check/" | relative_url }}), [`checkNotNull`]({{ "/en/glossary/check-not-null/" | relative_url }})) informs the compiler about type guarantees, enabling smart casts after validation calls. The stdlib's [`requireNotNull(value)`]({{ "/en/glossary/require-not-null/" | relative_url }}) makes `value` smart-cast to non-null in subsequent code.
- **Explicit Cast Fallback**: When smart cast is unavailable (mutable properties, cross-module boundaries), use the safe [cast]({{ "/en/glossary/cast/" | relative_url }}) [`as?`]({{ "/en/glossary/as-safe-cast/" | relative_url }}) which returns null on failure, never throws. Reserve the unsafe [cast]({{ "/en/glossary/cast/" | relative_url }}) [`as`]({{ "/en/glossary/as-cast/" | relative_url }}) for situations where failure is genuinely impossible.

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

**Question**: Why does the Kotlin compiler refuse to smart cast a [`var`]({{ "/en/glossary/var/" | relative_url }}) property after an [`is`]({{ "/en/glossary/is-operator/" | relative_url }}) check?

**Senior Answer**: Between the [`is`]({{ "/en/glossary/is-operator/" | relative_url }}) check and the subsequent usage, another [thread]({{ "/en/glossary/thread/" | relative_url }}) — or even the same [thread]({{ "/en/glossary/thread/" | relative_url }}) via a [callback]({{ "/en/glossary/callbacks/" | relative_url }}) — could reassign the [`var`]({{ "/en/glossary/var/" | relative_url }}) to a different type. The compiler cannot guarantee that the checked type still holds at the point of use, so it refuses the smart cast to prevent a [`ClassCastException`]({{ "/en/glossary/class-cast-exception/" | relative_url }}) at [runtime]({{ "/en/glossary/runtime/" | relative_url }}). This is the same principle behind Kotlin's [null safety]({{ "/en/01-kotlin-core/null-safety-elvis-safe-calls/" | relative_url }}) design: the type system only makes promises it can enforce. The workaround is to capture the value in a local [`val`]({{ "/en/glossary/val/" | relative_url }}) first, then the smart cast applies to the immutable local.

---

[Back to Chapters]({{ "/" | relative_url }})
