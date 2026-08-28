---
layout: post
title: "Type Inference"
date: 2026-08-28 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/type-inference/
---

## The Theory (The What)

**Type inference** is the compiler's ability to deduce the type of an expression without an explicit type annotation. At [compile time]({{ "/en/glossary/compile-time/" | relative_url }}), the Kotlin compiler analyzes initializers, return expressions, lambda parameters, and generic arguments to determine types automatically. The result is code that is both concise and fully type-safe — every inferred type is checked as rigorously as an explicit one.

## The Senior Nuance

- Type inference happens entirely at compile time. The [bytecode]({{ "/en/glossary/bytecode/" | relative_url }}) contains concrete types — there is no [runtime]({{ "/en/glossary/runtime/" | relative_url }}) cost or ambiguity. `val x = 42` compiles to the same bytecode as `val x: Int = 42`.
- Kotlin infers local variables, function return types (for single-expression functions), lambda parameter types, and generic type arguments. However, **public API return types should be explicit** — relying on inference for public functions couples the API signature to the implementation.
- Smart casts are a form of type narrowing that the compiler infers after `is` checks or null checks. The compiler tracks the narrowed type through control flow, eliminating the need for manual casts.
- When inference fails or produces an unexpected type (e.g., `val items = emptyList()` infers `List<Nothing>`), the fix is an explicit type argument — `emptyList<String>()` — not a type annotation on the variable.
- [Overload resolution]({{ "/en/glossary/overload-resolution/" | relative_url }}) and type inference interact: the compiler uses expected types from the call context to resolve which overload to invoke, and the chosen overload's return type feeds back into inference.

```kotlin
// From FollowApp Suite — TaskMapper.kt
fun TaskEntity.toDomain(): Task {
    return Task(
        id = this.id,                          // inferred as Long
        title = this.title,                    // inferred as String
        isCompleted = this.isCompleted,        // inferred as Boolean
        status = TaskStatus.valueOf(this.status) // inferred as TaskStatus
    )
}
```

Every argument's type is inferred from the property access, yet the compiler verifies each one matches `Task`'s constructor parameter types at compile time.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
