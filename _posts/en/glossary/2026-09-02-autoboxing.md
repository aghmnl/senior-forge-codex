---
layout: post
title: "Autoboxing"
date: 2026-09-02 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/autoboxing/
---

## The Theory (The What)

**Autoboxing** is the automatic conversion between a [primitive]({{ "/en/glossary/primitives/" | relative_url }}) type (`int`, `long`, `boolean`) and its corresponding wrapper class (`Integer`, `Long`, `Boolean`) performed by the [JVM]({{ "/en/glossary/jvm/" | relative_url }}). In Kotlin, this happens transparently when a primitive is used in a generic context — because [type erasure]({{ "/en/glossary/type-erasure/" | relative_url }}) forces all generic parameters to be objects at [Runtime]({{ "/en/glossary/runtime/" | relative_url }}).

```kotlin
// Not found in FAS — standalone example
val primitive: Int = 42           // Kotlin Int → JVM int (no object, no heap)
val boxed: Int? = 42              // nullable forces boxing: JVM Integer on the heap
val list: List<Int> = listOf(1, 2, 3)  // each element boxed to Integer — 3 heap allocations
```

The reverse — **unboxing** — extracts the primitive value from a wrapper object. Both happen implicitly and carry a cost: each boxing [allocates]({{ "/en/glossary/allocations/" | relative_url }}) an object on the [heap]({{ "/en/glossary/heap/" | relative_url }}), and each unboxing dereferences a pointer.

## The Senior Nuance

- In Kotlin, `Int` compiles to JVM `int` when used as a non-nullable local or parameter. The moment it becomes nullable (`Int?`), generic (`List<Int>`), or passed to a function expecting `Any`, the compiler boxes it to `java.lang.Integer`. Understanding these triggers is essential for performance-critical code.
- [`IntArray`]({{ "/en/glossary/intarray/" | relative_url }}), `LongArray`, `FloatArray`, etc., are Kotlin's escape hatch: they compile to JVM primitive arrays (`int[]`, `long[]`, `float[]`) with zero per-element boxing. Use them over `Array<Int>` or `List<Int>` in tight loops or large collections.
- [Inline classes]({{ "/en/01-kotlin-core/value-classes/" | relative_url }}) (`@JvmInline value class`) wrap a primitive without boxing in most cases — the wrapper is erased at [compile time]({{ "/en/glossary/compile-time/" | relative_url }}). They get boxed only when used as a generic type or nullable.
- Autoboxing is why identity comparisons (`===`) on boxed values are dangerous: `val a: Int? = 128; val b: Int? = 128; a === b` is `false` because the JVM's `Integer` cache only covers -128 to 127. Use `==` for value equality.
- In Android UI code, autoboxing inside `onDraw()`, `onMeasure()`, or Compose recomposition lambdas creates GC churn that causes frame drops. The [Garbage Collector]({{ "/en/glossary/garbage-collector/" | relative_url }}) reclaims these short-lived boxes, but the pause cost accumulates.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
