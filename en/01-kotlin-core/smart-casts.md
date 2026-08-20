---
layout: page
title: Smart Casts
lang: en
permalink: /en/01-kotlin-core/smart-casts/
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
sealed interface NetworkResult {
    data class Success(val data: List<String>) : NetworkResult
    data class Error(val code: Int, val message: String) : NetworkResult
    data object Loading : NetworkResult
}

fun handleResult(result: NetworkResult) {
    when (result) {
        is NetworkResult.Success -> {
            // Smart cast: result is now NetworkResult.Success
            println("Got ${result.data.size} items")
        }
        is NetworkResult.Error -> {
            // Smart cast: result is now NetworkResult.Error
            println("Error ${result.code}: ${result.message}")
        }
        NetworkResult.Loading -> println("Loading...")
    }
}

// Smart cast with null checks
fun processName(name: String?) {
    if (name != null) {
        // Smart cast: name is now String (non-null)
        println(name.uppercase())
    }
}

// Smart cast FAILS on var — intentional safety
class Example {
    var status: NetworkResult = NetworkResult.Loading

    fun check() {
        if (status is NetworkResult.Success) {
            // Compilation error: smart cast impossible because
            // 'status' is a mutable property that could change
            // println(status.data) // Won't compile
        }
    }
}
```

## Interview Prep (The Hot Seat)

**Question**: Why does the Kotlin compiler refuse to smart cast a `var` property after an `is` check?

**Senior Answer**: Between the `is` check and the subsequent usage, another thread — or even the same thread via a callback — could reassign the `var` to a different type. The compiler cannot guarantee that the checked type still holds at the point of use, so it refuses the smart cast to prevent a `ClassCastException` at runtime. This is the same principle behind Kotlin's [null safety]({{ "/en/01-kotlin-core/null-safety-elvis-safe-calls/" | relative_url }}) design: the type system only makes promises it can enforce. The workaround is to capture the value in a local `val` first, then the smart cast applies to the immutable local.

---

[Back to Chapters]({{ "/" | relative_url }})
