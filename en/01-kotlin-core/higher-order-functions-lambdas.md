---
layout: page
title: Higher-Order Functions & Lambdas
lang: en
permalink: /en/01-kotlin-core/higher-order-functions-lambdas/
---

## The Theory (The What)

Higher-order functions (HOFs) are functions that take other functions as parameters or return them as results. In Kotlin, functions are "first-class citizens," meaning they can be treated like any other value: stored in variables, passed into functions, or returned. Lambdas are "function literals"—blocks of code that are not declared as traditional functions but are passed immediately as expressions.

## The Senior Perspective (The Why)

A Senior Engineer evaluates higher-order functions through the lens of **abstraction versus runtime performance**.

- **Memory Overhead**: Every time a lambda is passed without being inlined, the compiler creates a new instance of a `Function` class (e.g., `Function0`, `Function1`). In high-frequency operations, this leads to increased pressure on the Garbage Collector.
- **The `inline` Power**: Using the `inline` keyword instructs the compiler to replace the function call with the actual code of the lambda. This eliminates object allocation and allows for features like "non-local returns" (using `return` inside a lambda to exit the calling function).
- **Control over Inlining**: `crossinline` is used when a lambda is passed to another execution context (like a local object or a different thread) where non-local returns are prohibited. `noinline` is used if you need to keep a specific lambda as an object to store it or pass it further.
- **Declarative DSLs**: HOFs combined with "Function types with receivers" are the foundation of modern Android development, enabling the declarative syntax seen in Jetpack Compose and Hilt configurations.

## Code in Action

```kotlin
// Senior approach: Using inline to optimize functional error handling
sealed interface RepositoryResult {
    data object Loading : RepositoryResult
    data class Success(val data: String) : RepositoryResult
    data class Error(val code: Int) : RepositoryResult
}

// Inline HOF to process results with zero allocation overhead
inline fun RepositoryResult.onSuccess(action: (String) -> Unit): RepositoryResult {
    if (this is RepositoryResult.Success) {
        action(data)
    }
    return this
}

fun fetchAndDisplay() {
    val result = RepositoryResult.Success("Senior Forge Content")

    // The code inside this lambda is "pasted" here by the compiler
    result.onSuccess { data ->
        println("Displaying: $data")
    }
}
```

## Interview Prep (The Hot Seat)

**Question**: Why would you avoid using the inline keyword for every single higher-order function in a large project?

**Senior Answer**: While inline prevents object allocation, it causes the compiler to copy the function's bytecode into every call site. If the function is large and called in many places, it leads to "code bloat," significantly increasing the final binary size (APK/AAB). Additionally, inline functions cannot access private members of the class they are in, which can limit architectural choices. I only inline functions that take lambdas as parameters and are small enough to justify the trade-off.

---

[Back to Chapters]({{ "/" | relative_url }})
