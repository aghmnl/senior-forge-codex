---
layout: post
title: "Allocations"
date: 2026-08-30 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/allocations/
---

## The Theory (The What)

An **allocation** is the act of reserving memory on the [heap]({{ "/en/glossary/heap/" | relative_url }}) for a new object instance. Every time you call a [constructor]({{ "/en/glossary/constructor/" | relative_url }}) (`MyClass()`), create a [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) that captures variables, or box a [primitive]({{ "/en/glossary/primitives/" | relative_url }}), the [JVM]({{ "/en/glossary/jvm/" | relative_url }}) allocates memory for that object. The [Garbage Collector]({{ "/en/glossary/garbage-collector/" | relative_url }}) later reclaims that memory when the object is no longer referenced. While individual allocations are fast (a pointer bump on the young generation), high-frequency allocations increase GC pressure, causing pauses that affect UI smoothness — especially on Android, where frame budgets are 16ms.

```kotlin
// From FollowApp Suite — RecurrenceRule.kt
// data object Never: ZERO allocations — it is a singleton
sealed class RecurrenceEnd {
    data object Never : RecurrenceEnd()
    data class AfterOccurrences(val remaining: Int) : RecurrenceEnd()  // one allocation per instance
    data class UntilDate(val date: Long) : RecurrenceEnd()             // one allocation per instance
}

// Emitting Never through StateFlow thousands of times creates no objects.
// Emitting AfterOccurrences(5) creates a new object each time.
```

## The Senior Nuance

- In [sealed hierarchies]({{ "/en/glossary/sealed-hierarchy/" | relative_url }}), use `data object` for stateless variants to avoid per-emission allocations. A `data object Loading` is a [singleton]({{ "/en/glossary/singleton/" | relative_url }}) — referencing it is free. A `data class Loading()` would allocate a new object on every [state emission]({{ "/en/glossary/state-emission-patterns/" | relative_url }}), adding GC pressure for zero benefit.
- [Inline functions]({{ "/en/glossary/inline-functions/" | relative_url }}) eliminate the allocation of lambda wrapper objects. When a [higher-order function]({{ "/en/01-kotlin-core/higher-order-functions-lambdas/" | relative_url }}) is marked `inline`, the lambda body is copied to the call site at [compile time]({{ "/en/glossary/compile-time/" | relative_url }}), avoiding the [heap]({{ "/en/glossary/heap/" | relative_url }}) allocation that a normal lambda would require.
- [Autoboxing]({{ "/en/glossary/autoboxing/" | relative_url }}) is a hidden allocation source: a `List<Int>` stores `Integer` objects (boxed), not `int` [primitives]({{ "/en/glossary/primitives/" | relative_url }}). In tight loops, prefer [`IntArray`]({{ "/en/glossary/intarray/" | relative_url }}) over `List<Int>` to keep values on the stack or in a flat array.
- On Android, allocation-heavy code in `onDraw()`, `onMeasure()`, or recomposition lambdas is the top source of jank. Profile with Android Studio's Memory Profiler to identify allocation hotspots before optimizing — premature optimization without profiling is guesswork.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
