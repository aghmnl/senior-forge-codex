---
layout: post
title: "Primitives"
date: 2026-08-28 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/primitives/
---

## The Theory (The What)

**Primitives** are the basic data types that the [JVM]({{ "/en/glossary/jvm/" | relative_url }}) handles directly at the hardware level: `int`, `long`, `float`, `double`, `boolean`, `char`, `byte`, and `short`. They are stored on the stack (or inlined in objects), not on the heap, and have no object overhead — no headers, no [garbage collection]({{ "/en/glossary/garbage-collector/" | relative_url }}). In Kotlin, you write `Int`, `Long`, `Boolean`, etc., and the compiler decides at [compile time]({{ "/en/glossary/compile-time/" | relative_url }}) whether to use a JVM primitive or its boxed wrapper in the generated [bytecode]({{ "/en/glossary/bytecode/" | relative_url }}).

## The Senior Nuance

- Kotlin's `Int` compiles to the JVM primitive `int` whenever possible. It gets boxed to `java.lang.Integer` only when used as a nullable type (`Int?`), as a generic type argument (`List<Int>` stores `Integer` objects), or when passed to a function expecting `Any`. Understanding this boxing boundary is critical for performance-sensitive code.
- **`const val`** only works with primitives and `String`. These compile-time constants are inlined directly into the bytecode — the value itself is copied at each usage site, eliminating any field access at [runtime]({{ "/en/glossary/runtime/" | relative_url }}).
- Kotlin's `UInt`, `ULong`, etc., are **inline classes** wrapping primitives. At the bytecode level, they are still `int`/`long` — the unsigned semantics are enforced at compile time through [overload resolution]({{ "/en/glossary/overload-resolution/" | relative_url }}) and intrinsic functions.
- In arrays, `IntArray` maps to `int[]` (primitive array, no boxing), while `Array<Int>` maps to `Integer[]` (boxed, heap-allocated). For large arrays, this difference is measurable in both memory and performance.

```kotlin
// From FollowApp Suite — DragToReorder.kt
companion object {
    const val LONG_PRESS_TAP_SLOP_PX = 24f  // Float primitive, inlined at every usage site
}
```

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
